"""
SRT Translator - Chinese to Vietnamese
Main entry point for the desktop application.
"""

import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """Main entry point."""
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("SRT Translator")
    app.setOrganizationName("SRT Translator")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
