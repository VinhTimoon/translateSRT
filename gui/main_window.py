"""
Main Window GUI
PySide6-based desktop application interface.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QTextEdit,
    QTableWidget, QTableWidgetItem, QFileDialog,
    QMessageBox, QComboBox, QSpinBox, QGroupBox,
    QSplitter, QHeaderView, QMenu
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QFont, QColor

from core.config import ConfigManager, TranslationSettings
from core.parser import SRTParser, Chunker, export_srt, read_srt_file, write_srt_file
from core.translator import TranslationDispatcher
from core.project import ProjectManager
from core.validator import TranslationValidator


class TranslationWorker(QThread):
    """Worker thread for async translation."""
    
    progress = Signal(int, int, str)  # current, total, message
    finished = Signal(dict)  # results
    error = Signal(str)  # error message
    
    def __init__(self, config, chunks):
        super().__init__()
        self.config = config
        self.chunks = chunks
        self.dispatcher: Optional[TranslationDispatcher] = None
        self._cancelled = False
    
    def run(self):
        """Run translation in thread."""
        try:
            # Create event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run translation
            results = loop.run_until_complete(self._translate())
            
            loop.close()
            
            if not self._cancelled:
                self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))
    
    async def _translate(self):
        """Async translation."""
        async with TranslationDispatcher(self.config) as dispatcher:
            self.dispatcher = dispatcher
            
            # Set progress callback
            dispatcher.set_progress_callback(self._progress_callback)
            
            # Translate
            results = await dispatcher.translate_chunks(self.chunks)
            
            return results
    
    def _progress_callback(self, current: int, total: int, message: str):
        """Progress callback."""
        if not self._cancelled:
            self.progress.emit(current, total, message)
    
    def cancel(self):
        """Cancel translation."""
        self._cancelled = True
        if self.dispatcher:
            self.dispatcher.cancel()


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        
        self.config = ConfigManager()
        self.project_manager = ProjectManager()
        self.worker: Optional[TranslationWorker] = None
        
        self.times = None
        self.subs_original = None
        self.subs_translated = None
        
        self.init_ui()
        self.check_config()
    
    def init_ui(self):
        """Initialize UI."""
        self.setWindowTitle("SRT Translator - Chinese to Vietnamese")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        layout = QVBoxLayout(central)
        
        # Top toolbar
        toolbar = self._create_toolbar()
        layout.addLayout(toolbar)
        
        # Splitter for main content
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Settings & Logs
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Preview table
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        layout.addWidget(splitter)
        
        # Bottom status
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
    
    def _create_toolbar(self):
        """Create toolbar."""
        layout = QHBoxLayout()
        
        self.btn_open = QPushButton("📁 Open SRT")
        self.btn_open.clicked.connect(self.open_file)
        layout.addWidget(self.btn_open)
        
        self.btn_save_project = QPushButton("💾 Save Project")
        self.btn_save_project.clicked.connect(self.save_project)
        self.btn_save_project.setEnabled(False)
        layout.addWidget(self.btn_save_project)
        
        self.btn_load_project = QPushButton("📂 Load Project")
        self.btn_load_project.clicked.connect(self.load_project)
        layout.addWidget(self.btn_load_project)
        
        layout.addStretch()
        
        self.btn_start = QPushButton("▶ Start Translation")
        self.btn_start.clicked.connect(self.start_translation)
        self.btn_start.setEnabled(False)
        self.btn_start.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        layout.addWidget(self.btn_start)
        
        self.btn_stop = QPushButton("⏹ Stop")
        self.btn_stop.clicked.connect(self.stop_translation)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; padding: 8px;")
        layout.addWidget(self.btn_stop)
        
        self.btn_export = QPushButton("📤 Export SRT")
        self.btn_export.clicked.connect(self.export_srt)
        self.btn_export.setEnabled(False)
        self.btn_export.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        layout.addWidget(self.btn_export)
        
        return layout
    
    def _create_left_panel(self):
        """Create left settings panel."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Settings group
        settings_group = QGroupBox("Translation Settings")
        settings_layout = QVBoxLayout()
        
        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(TranslationSettings.AVAILABLE_MODELS)
        self.model_combo.setCurrentText(self.config.settings.model)
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_layout.addWidget(self.model_combo)
        settings_layout.addLayout(model_layout)
        
        # Chunk size
        chunk_layout = QHBoxLayout()
        chunk_layout.addWidget(QLabel("Chunk Size:"))
        self.chunk_spin = QSpinBox()
        self.chunk_spin.setRange(1, 50)
        self.chunk_spin.setValue(self.config.settings.chunk_size)
        chunk_layout.addWidget(self.chunk_spin)
        settings_layout.addLayout(chunk_layout)
        
        # Threads per API
        threads_layout = QHBoxLayout()
        threads_layout.addWidget(QLabel("Threads/API:"))
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 10)
        self.threads_spin.setValue(self.config.settings.threads_per_api)
        threads_layout.addWidget(self.threads_spin)
        settings_layout.addLayout(threads_layout)
        
        # Tone
        tone_layout = QHBoxLayout()
        tone_layout.addWidget(QLabel("Tone:"))
        self.tone_combo = QComboBox()
        self.tone_combo.addItems(["conversational", "formal", "literal"])
        self.tone_combo.setCurrentText(self.config.settings.tone)
        tone_layout.addWidget(self.tone_combo)
        settings_layout.addLayout(tone_layout)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # File info group
        info_group = QGroupBox("File Information")
        info_layout = QVBoxLayout()
        self.info_label = QLabel("No file loaded")
        self.info_label.setWordWrap(True)
        info_layout.addWidget(self.info_label)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Name mapping button
        self.btn_name_map = QPushButton("Edit Name Mapping")
        self.btn_name_map.clicked.connect(self.edit_name_mapping)
        layout.addWidget(self.btn_name_map)
        
        # Logs
        logs_group = QGroupBox("Logs")
        logs_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(300)
        font = QFont("Consolas", 9)
        self.log_text.setFont(font)
        logs_layout.addWidget(self.log_text)
        logs_group.setLayout(logs_layout)
        layout.addWidget(logs_group)
        
        layout.addStretch()
        
        return widget
    
    def _create_right_panel(self):
        """Create right preview panel."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        layout.addWidget(QLabel("<h3>Preview</h3>"))
        
        # Preview table
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(5)
        self.preview_table.setHorizontalHeaderLabels([
            "Index", "Time", "Original (Chinese)", "Translated (Vietnamese)", "Status"
        ])
        self.preview_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.preview_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.preview_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.preview_table.customContextMenuRequested.connect(self.show_context_menu)
        self.preview_table.itemDoubleClicked.connect(self.edit_translation)
        
        layout.addWidget(self.preview_table)
        
        return widget
    
    def check_config(self):
        """Check configuration validity."""
        errors = self.config.validate_config()
        if errors:
            QMessageBox.warning(
                self,
                "Configuration Error",
                "Configuration issues:\n" + "\n".join(errors) +
                "\n\nPlease check your .env file."
            )
            self.log("⚠️ Configuration errors detected")
        else:
            self.log("✓ Configuration validated")
            self.log(f"✓ {len(self.config.get_primary_apis())} primary APIs configured")
            self.log(f"✓ {len(self.config.get_fallback_apis())} fallback APIs configured")
    
    def log(self, message: str):
        """Add log message."""
        self.log_text.append(message)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def open_file(self):
        """Open SRT file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open SRT File",
            "",
            "SRT Files (*.srt);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            # Read file
            self.log(f"📂 Opening: {file_path}")
            content = read_srt_file(file_path)
            
            # Parse
            self.log("🔍 Parsing SRT...")
            self.times, self.subs_original = SRTParser.parse(content)
            
            if not SRTParser.validate(self.times, self.subs_original):
                raise ValueError("Invalid SRT format")
            
            count = SRTParser.get_count(self.subs_original)
            self.log(f"✓ Parsed {count} subtitle lines")
            
            # Initialize translated array
            self.subs_translated = [None] * len(self.subs_original)
            
            # Create project
            self.project_manager.create_new_project(
                original_file=file_path,
                times=self.times,
                subs_original=self.subs_original,
                model=self.config.settings.model,
                chunk_size=self.config.settings.chunk_size,
                tone=self.config.settings.tone,
                name_map=self.config.name_map
            )
            
            # Update UI
            self.update_file_info()
            self.populate_preview_table()
            
            self.btn_start.setEnabled(True)
            self.btn_save_project.setEnabled(True)
            self.status_label.setText(f"Loaded: {Path(file_path).name} ({count} lines)")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")
            self.log(f"❌ Error: {e}")
    
    def update_file_info(self):
        """Update file information display."""
        if not self.project_manager.current_project:
            return
        
        proj = self.project_manager.current_project
        info = f"""<b>File:</b> {Path(proj.original_file).name}<br>
<b>Total Lines:</b> {proj.total_lines}<br>
<b>Model:</b> {proj.model}<br>
<b>Chunk Size:</b> {proj.chunk_size}<br>
<b>Tone:</b> {proj.tone}"""
        
        self.info_label.setText(info)
    
    def populate_preview_table(self):
        """Populate preview table with data."""
        if not self.subs_original:
            return
        
        count = len(self.subs_original) - 1
        self.preview_table.setRowCount(count)
        
        for i in range(1, len(self.subs_original)):
            row = i - 1
            
            # Index
            self.preview_table.setItem(row, 0, QTableWidgetItem(str(i)))
            
            # Time
            time_item = QTableWidgetItem(self.times[i] or "")
            self.preview_table.setItem(row, 1, time_item)
            
            # Original
            orig_item = QTableWidgetItem(self.subs_original[i] or "")
            self.preview_table.setItem(row, 2, orig_item)
            
            # Translated
            trans_text = self.subs_translated[i] or ""
            trans_item = QTableWidgetItem(trans_text)
            self.preview_table.setItem(row, 3, trans_item)
            
            # Status
            if self.project_manager.current_project:
                status = self.project_manager.current_project.statuses[i]
            else:
                status = "pending"
            
            status_item = QTableWidgetItem(status)
            
            # Color code status
            if status == "done":
                status_item.setBackground(QColor(200, 255, 200))
            elif status == "failed":
                status_item.setBackground(QColor(255, 200, 200))
            elif status == "in-progress":
                status_item.setBackground(QColor(255, 255, 200))
            
            self.preview_table.setItem(row, 4, status_item)
    
    def start_translation(self):
        """Start translation process."""
        if not self.subs_original:
            return
        
        # Update settings
        self.config.update_settings(
            model=self.model_combo.currentText(),
            chunk_size=self.chunk_spin.value(),
            threads_per_api=self.threads_spin.value(),
            tone=self.tone_combo.currentText()
        )
        
        # Create chunks
        self.log("🔄 Creating chunks...")
        chunks = Chunker.chunkify(self.subs_original, self.config.settings.chunk_size)
        self.log(f"✓ Created {len(chunks)} chunks")
        
        # Start worker thread
        self.worker = TranslationWorker(self.config, chunks)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_translation_finished)
        self.worker.error.connect(self.on_translation_error)
        
        self.worker.start()
        
        # Update UI
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.btn_open.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(chunks))
        self.progress_bar.setValue(0)
        self.status_label.setText("Translating...")
        
        self.log("▶️ Translation started")
    
    def stop_translation(self):
        """Stop translation."""
        if self.worker:
            self.log("⏹ Stopping translation...")
            self.worker.cancel()
            self.worker.wait()
            self.log("✓ Translation stopped")
        
        self.reset_ui_after_translation()
    
    def on_progress(self, current: int, total: int, message: str):
        """Handle progress update."""
        self.progress_bar.setValue(current)
        self.status_label.setText(f"Progress: {current}/{total} - {message}")
        self.log(f"[{current}/{total}] {message}")
    
    def on_translation_finished(self, results: dict):
        """Handle translation completion."""
        self.log("✓ Translation completed")
        
        # Merge results
        from core.parser import Chunker
        self.subs_translated = Chunker.merge_results(
            self.subs_translated,
            self.worker.chunks if self.worker else [],
            results
        )
        
        # Update project
        for (start, end), lines in results.items():
            # Check if successful (no Chinese)
            has_chinese = any(
                TranslationValidator.contains_chinese(line)
                for line in lines
            )
            
            self.project_manager.update_chunk_result(
                start, end, lines, not has_chinese
            )
        
        # Update table
        self.populate_preview_table()
        
        # Check export readiness
        ready, msg = self.project_manager.is_export_ready()
        if ready:
            self.btn_export.setEnabled(True)
            self.log(f"✓ {msg}")
            QMessageBox.information(self, "Success", "Translation completed!\nReady for export.")
        else:
            self.log(f"⚠️ {msg}")
            QMessageBox.warning(self, "Warning", f"Translation completed with issues:\n{msg}")
        
        # Show stats
        if self.worker and self.worker.dispatcher:
            stats = self.worker.dispatcher.get_stats()
            self.log(f"\n📊 Statistics:")
            self.log(f"  Success: {stats.success_count}/{stats.total_chunks}")
            self.log(f"  Failed: {stats.failed_count}")
            self.log(f"  Duration: {stats.total_duration:.2f}s")
        
        self.reset_ui_after_translation()
    
    def on_translation_error(self, error: str):
        """Handle translation error."""
        self.log(f"❌ Error: {error}")
        QMessageBox.critical(self, "Translation Error", f"An error occurred:\n{error}")
        self.reset_ui_after_translation()
    
    def reset_ui_after_translation(self):
        """Reset UI after translation finishes."""
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_open.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Ready")
    
    def edit_translation(self, item):
        """Edit translation (double-click)."""
        if item.column() != 3:  # Only translated column
            return
        
        row = item.row()
        idx = row + 1  # Convert to 1-based
        
        # Allow editing
        item.setFlags(item.flags() | Qt.ItemIsEditable)
    
    def show_context_menu(self, position):
        """Show context menu on right-click."""
        item = self.preview_table.itemAt(position)
        if not item:
            return
        
        row = item.row()
        idx = row + 1
        
        menu = QMenu()
        
        edit_action = menu.addAction("✏️ Edit Translation")
        retranslate_action = menu.addAction("🔄 Re-translate This Line")
        
        action = menu.exec_(self.preview_table.viewport().mapToGlobal(position))
        
        if action == retranslate_action:
            # TODO: Implement single-line retranslation
            QMessageBox.information(self, "Info", "Re-translate feature coming soon")
    
    def edit_name_mapping(self):
        """Edit name mapping."""
        # Simple dialog for now
        QMessageBox.information(
            self,
            "Name Mapping",
            f"Current mappings: {len(self.config.name_map)}\n\n" +
            "Edit in config file: ~/.srt_translator/name_map.json"
        )
    
    def save_project(self):
        """Save project."""
        if not self.project_manager.current_project:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            self.project_manager.save_project(file_path)
            self.log(f"💾 Project saved: {file_path}")
            QMessageBox.information(self, "Success", "Project saved successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save project:\n{e}")
    
    def load_project(self):
        """Load project."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Project",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            project = self.project_manager.load_project(file_path)
            
            # Restore data
            self.times = project.times
            self.subs_original = project.subs_original
            self.subs_translated = project.subs_translated
            
            # Update UI
            self.update_file_info()
            self.populate_preview_table()
            
            self.btn_start.setEnabled(True)
            self.btn_save_project.setEnabled(True)
            
            # Check if export ready
            ready, msg = self.project_manager.is_export_ready()
            if ready:
                self.btn_export.setEnabled(True)
            
            self.log(f"📂 Project loaded: {file_path}")
            QMessageBox.information(self, "Success", "Project loaded successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load project:\n{e}")
    
    def export_srt(self):
        """Export translated SRT."""
        if not self.subs_translated:
            return
        
        # Check readiness
        ready, msg = self.project_manager.is_export_ready()
        
        if not ready:
            reply = QMessageBox.question(
                self,
                "Export Warning",
                f"{msg}\n\nDo you want to export anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
        
        # Get save path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export SRT",
            "",
            "SRT Files (*.srt);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            # Export
            content = export_srt(self.times, self.subs_translated)
            write_srt_file(file_path, content)
            
            self.log(f"📤 Exported: {file_path}")
            QMessageBox.information(self, "Success", f"SRT exported successfully:\n{file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export:\n{e}")
    
    def on_model_changed(self, model: str):
        """Handle model change."""
        self.log(f"Model changed to: {model}")
    
    def closeEvent(self, event):
        """Handle window close."""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirm Exit",
                "Translation is in progress. Stop and exit?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.worker.cancel()
                self.worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
