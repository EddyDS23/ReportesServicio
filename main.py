#!/usr/bin/env python3
"""
Daily Report System
Main entry point for the application.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow


def main():
    """Main application entry point."""
    # Set Qt platform attributes BEFORE creating QApplication
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Daily Report System")
    app.setOrganizationName("ReportApp")
    
    # Set style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()