"""
Project Management
Handles saving/loading translation projects for resume capability.
"""

import json
from typing import List, Optional, Dict
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime


@dataclass
class ProjectData:
    """Translation project data."""
    version: str = "1.0"
    created: str = ""
    modified: str = ""
    
    # Original file info
    original_file: str = ""
    file_size: int = 0
    
    # Subtitle data (1-indexed)
    times: List[Optional[str]] = None
    subs_original: List[Optional[str]] = None
    subs_translated: List[Optional[str]] = None
    
    # Status tracking
    statuses: List[str] = None  # pending, in-progress, done, failed, unresolved
    
    # Settings used
    model: str = ""
    chunk_size: int = 10
    tone: str = ""
    name_map: Dict[str, str] = None
    
    # Progress
    total_lines: int = 0
    completed_lines: int = 0
    failed_lines: int = 0
    
    def __post_init__(self):
        """Initialize defaults."""
        if self.times is None:
            self.times = []
        if self.subs_original is None:
            self.subs_original = []
        if self.subs_translated is None:
            self.subs_translated = []
        if self.statuses is None:
            self.statuses = []
        if self.name_map is None:
            self.name_map = {}
        if not self.created:
            self.created = datetime.now().isoformat()
        if not self.modified:
            self.modified = self.created


class ProjectManager:
    """Manages translation projects."""
    
    STATUS_PENDING = "pending"
    STATUS_IN_PROGRESS = "in-progress"
    STATUS_DONE = "done"
    STATUS_FAILED = "failed"
    STATUS_UNRESOLVED = "unresolved"
    
    def __init__(self):
        """Initialize project manager."""
        self.current_project: Optional[ProjectData] = None
        self.project_file: Optional[Path] = None
    
    def create_new_project(
        self,
        original_file: str,
        times: List[Optional[str]],
        subs_original: List[Optional[str]],
        model: str,
        chunk_size: int,
        tone: str,
        name_map: Dict[str, str]
    ) -> ProjectData:
        """
        Create a new project.
        
        Args:
            original_file: Path to original SRT file
            times: Timecode array (1-indexed)
            subs_original: Original subtitle array (1-indexed)
            model: Model name
            chunk_size: Chunk size
            tone: Translation tone
            name_map: Name mapping dict
            
        Returns:
            New ProjectData
        """
        total_lines = len(subs_original) - 1  # Exclude index 0
        
        # Initialize translated array and statuses
        subs_translated = [None] * len(subs_original)
        statuses = [self.STATUS_PENDING] * len(subs_original)
        statuses[0] = ""  # Index 0 is unused
        
        project = ProjectData(
            created=datetime.now().isoformat(),
            modified=datetime.now().isoformat(),
            original_file=original_file,
            file_size=Path(original_file).stat().st_size if Path(original_file).exists() else 0,
            times=times,
            subs_original=subs_original,
            subs_translated=subs_translated,
            statuses=statuses,
            model=model,
            chunk_size=chunk_size,
            tone=tone,
            name_map=name_map,
            total_lines=total_lines,
            completed_lines=0,
            failed_lines=0
        )
        
        self.current_project = project
        return project
    
    def update_chunk_result(
        self,
        start_idx: int,
        end_idx: int,
        translated_lines: List[str],
        success: bool
    ):
        """
        Update project with chunk result.
        
        Args:
            start_idx: Starting index (1-based)
            end_idx: Ending index (1-based)
            translated_lines: Translated lines
            success: Whether translation succeeded
        """
        if not self.current_project:
            return
        
        for i, line in enumerate(translated_lines):
            idx = start_idx + i
            if idx <= end_idx and idx < len(self.current_project.subs_translated):
                self.current_project.subs_translated[idx] = line
                
                if success:
                    self.current_project.statuses[idx] = self.STATUS_DONE
                    self.current_project.completed_lines += 1
                else:
                    self.current_project.statuses[idx] = self.STATUS_FAILED
                    self.current_project.failed_lines += 1
        
        self.current_project.modified = datetime.now().isoformat()
    
    def mark_line_status(self, idx: int, status: str):
        """
        Mark a specific line's status.
        
        Args:
            idx: Line index (1-based)
            status: New status
        """
        if not self.current_project:
            return
        
        if 1 <= idx < len(self.current_project.statuses):
            self.current_project.statuses[idx] = status
            self.current_project.modified = datetime.now().isoformat()
    
    def update_translation(self, idx: int, translated: str):
        """
        Update a single line's translation (manual edit).
        
        Args:
            idx: Line index (1-based)
            translated: New translation
        """
        if not self.current_project:
            return
        
        if 1 <= idx < len(self.current_project.subs_translated):
            self.current_project.subs_translated[idx] = translated
            self.current_project.statuses[idx] = self.STATUS_DONE
            self.current_project.modified = datetime.now().isoformat()
    
    def get_unresolved_lines(self) -> List[int]:
        """
        Get list of unresolved line indices.
        
        Returns:
            List of 1-based indices
        """
        if not self.current_project:
            return []
        
        unresolved = []
        for i in range(1, len(self.current_project.statuses)):
            status = self.current_project.statuses[i]
            if status in [self.STATUS_PENDING, self.STATUS_FAILED, self.STATUS_UNRESOLVED]:
                unresolved.append(i)
        
        return unresolved
    
    def get_lines_with_chinese(self) -> List[int]:
        """
        Get list of line indices that still contain Chinese.
        
        Returns:
            List of 1-based indices
        """
        if not self.current_project:
            return []
        
        from .validator import TranslationValidator
        
        chinese_lines = []
        for i in range(1, len(self.current_project.subs_translated)):
            line = self.current_project.subs_translated[i]
            if line and TranslationValidator.contains_chinese(line):
                chinese_lines.append(i)
        
        return chinese_lines
    
    def is_export_ready(self) -> Tuple[bool, str]:
        """
        Check if project is ready for export.
        
        Returns:
            Tuple of (ready, message)
        """
        if not self.current_project:
            return False, "No project loaded"
        
        unresolved = self.get_unresolved_lines()
        chinese_lines = self.get_lines_with_chinese()
        
        if unresolved:
            return False, f"{len(unresolved)} lines are unresolved"
        
        if chinese_lines:
            return False, f"{len(chinese_lines)} lines still contain Chinese"
        
        return True, "Ready for export"
    
    def get_progress(self) -> Tuple[int, int, float]:
        """
        Get translation progress.
        
        Returns:
            Tuple of (completed, total, percentage)
        """
        if not self.current_project:
            return 0, 0, 0.0
        
        total = self.current_project.total_lines
        completed = sum(
            1 for i in range(1, len(self.current_project.statuses))
            if self.current_project.statuses[i] == self.STATUS_DONE
        )
        
        percentage = (completed / total * 100) if total > 0 else 0.0
        
        return completed, total, percentage
    
    def save_project(self, file_path: str):
        """
        Save project to JSON file.
        
        Args:
            file_path: Path to save to
        """
        if not self.current_project:
            raise ValueError("No project to save")
        
        self.project_file = Path(file_path)
        self.current_project.modified = datetime.now().isoformat()
        
        # Convert to dict
        data = asdict(self.current_project)
        
        # Save
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_project(self, file_path: str) -> ProjectData:
        """
        Load project from JSON file.
        
        Args:
            file_path: Path to load from
            
        Returns:
            Loaded ProjectData
        """
        self.project_file = Path(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Reconstruct ProjectData
        project = ProjectData(**data)
        self.current_project = project
        
        return project
    
    def auto_save(self):
        """Auto-save if project file is set."""
        if self.project_file and self.current_project:
            self.save_project(str(self.project_file))
    
    def get_project_summary(self) -> str:
        """
        Get project summary.
        
        Returns:
            Summary string
        """
        if not self.current_project:
            return "No project loaded"
        
        completed, total, percentage = self.get_progress()
        unresolved = len(self.get_unresolved_lines())
        chinese = len(self.get_lines_with_chinese())
        
        summary = f"""Project Summary:
- File: {Path(self.current_project.original_file).name}
- Total Lines: {total}
- Completed: {completed} ({percentage:.1f}%)
- Unresolved: {unresolved}
- Still Chinese: {chinese}
- Model: {self.current_project.model}
- Tone: {self.current_project.tone}
- Created: {self.current_project.created}
- Modified: {self.current_project.modified}
"""
        return summary
