from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QDateEdit, QTimeEdit, QPushButton, QListWidget,
    QListWidgetItem, QMessageBox, QComboBox, QFrame, QFileDialog,
    QApplication, QScrollArea, QGroupBox
)
from PySide6.QtCore import Qt, QDate, QTime, Signal
from PySide6.QtGui import QIcon
from datetime import date
from models.activity_model import Activity
from models.report_model import Report
from ui.activity_dialog import ActivityDialog
from ui.styles import AppStyles
from typing import Optional
import sys
import os


class ActivityListItem(QWidget):
    """Custom widget for activity list items."""
    
    edit_requested = Signal(int)
    delete_requested = Signal(int)
    
    def __init__(self, activity: Activity, index: int, parent=None):
        super().__init__(parent)
        self.activity = activity
        self.index = index
        self.title_label = None
        self.duration_badge = None
        self.setup_ui()
    
    def update_theme(self):
        """Update widget styles when theme changes."""
        # Update card styling
        self.setStyleSheet(f"""
            ActivityListItem {{
                background-color: {AppStyles.COLORS['bg_primary']};
                border: 1px solid {AppStyles.COLORS['border']};
                border-radius: {AppStyles.RADIUS['lg']};
                padding: 4px;
            }}
            ActivityListItem:hover {{
                border-color: {AppStyles.COLORS['primary_light']};
                background-color: {AppStyles.COLORS['bg_secondary']};
            }}
        """)
        
        if self.title_label:
            self.title_label.setStyleSheet(f"""
                QLabel {{
                    font-weight: 600;
                    font-size: {AppStyles.FONTS['size_xl']};
                    color: {AppStyles.COLORS['text_primary']};
                }}
            """)
        
        if self.duration_badge:
            self.duration_badge.setStyleSheet(f"""
                QLabel {{
                    background-color: {AppStyles.COLORS['primary_light']};
                    color: {AppStyles.COLORS['text_white']};
                    padding: 6px 14px;
                    border-radius: {AppStyles.RADIUS['full']};
                    font-size: {AppStyles.FONTS['size_base']};
                    font-weight: 600;
                }}
            """)
    
    def setup_ui(self):
        """Setup the list item UI."""
        # Add card-like styling with more padding
        self.setStyleSheet(f"""
            ActivityListItem {{
                background-color: {AppStyles.COLORS['bg_primary']};
                border: 1px solid {AppStyles.COLORS['border']};
                border-radius: {AppStyles.RADIUS['lg']};
                padding: 4px;
            }}
            ActivityListItem:hover {{
                border-color: {AppStyles.COLORS['primary_light']};
                background-color: {AppStyles.COLORS['bg_secondary']};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)
        
        # Left side - Activity info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)
        
        # Title and duration row
        title_row = QHBoxLayout()
        title_row.setSpacing(12)
        
        # Title
        self.title_label = QLabel(self.activity.title)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-weight: 600;
                font-size: {AppStyles.FONTS['size_xl']};
                color: {AppStyles.COLORS['text_primary']};
            }}
        """)
        self.title_label.setWordWrap(False)
        title_row.addWidget(self.title_label)
        
        # Spacer to push duration to the right
        title_row.addStretch()
        
        # Duration badge
        self.duration_badge = QLabel(self.activity.duration)
        self.duration_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {AppStyles.COLORS['primary_light']};
                color: {AppStyles.COLORS['text_white']};
                padding: 6px 14px;
                border-radius: {AppStyles.RADIUS['full']};
                font-size: {AppStyles.FONTS['size_base']};
                font-weight: 600;
            }}
        """)
        self.duration_badge.setMinimumWidth(70)
        title_row.addWidget(self.duration_badge)
        
        info_layout.addLayout(title_row)
        
        # Description preview (first 100 chars)
        if self.activity.description:
            desc_preview = self.activity.description[:100]
            if len(self.activity.description) > 100:
                desc_preview += "..."
            desc_label = QLabel(desc_preview)
            desc_label.setStyleSheet(f"""
                QLabel {{
                    color: {AppStyles.COLORS['text_secondary']};
                    font-size: {AppStyles.FONTS['size_base']};
                    line-height: 1.5;
                }}
            """)
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
        
        # Metadata row (time and images)
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(16)
        
        # Time range
        time_label = QLabel(f"⏰ {self.activity.start_time} - {self.activity.end_time}")
        time_label.setStyleSheet(f"""
            QLabel {{
                color: {AppStyles.COLORS['text_tertiary']};
                font-size: {AppStyles.FONTS['size_sm']};
            }}
        """)
        meta_layout.addWidget(time_label)
        
        # Images count if any
        if len(self.activity.images) > 0:
            images_label = QLabel(f"🖼️ {len(self.activity.images)} image(s)")
            images_label.setStyleSheet(f"""
                QLabel {{
                    color: {AppStyles.COLORS['text_tertiary']};
                    font-size: {AppStyles.FONTS['size_sm']};
                }}
            """)
            meta_layout.addWidget(images_label)
        
        meta_layout.addStretch()
        info_layout.addLayout(meta_layout)
        
        layout.addLayout(info_layout, 1)
        
        # Right side - Action buttons (HORIZONTAL)
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        edit_btn = QPushButton("✏️ Edit")
        edit_btn.setProperty("variant", "secondary")
        edit_btn.setMinimumWidth(100)
        edit_btn.setMinimumHeight(40)
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.index))
        actions_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setProperty("variant", "danger")
        delete_btn.setMinimumWidth(100)
        delete_btn.setMinimumHeight(40)
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.index))
        actions_layout.addWidget(delete_btn)
        
        layout.addLayout(actions_layout)


class MainWindow(QMainWindow):
    """Main application window for Daily Report System."""
    
    def __init__(self):
        super().__init__()
        self.report: Optional[Report] = None
        self.current_file: Optional[str] = None
        
        # Force proper rendering
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, False)
        
        # Initialize with new report
        self.new_report()
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        """Setup the main window UI."""
        self.setWindowTitle("Daily Report System")
        self.setMinimumSize(1000, 700)
        
        # Central widget
        central = QWidget()
        central.setObjectName("centralwidget")
        self.setCentralWidget(central)
        
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # Header with title and actions
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📋 Daily Report System")
        title_label.setProperty("heading", True)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        new_btn = QPushButton("🆕 New Report")
        new_btn.setProperty("variant", "secondary")
        new_btn.clicked.connect(self.new_report)
        header_layout.addWidget(new_btn)
        
        load_btn = QPushButton("📂 Load")
        load_btn.setProperty("variant", "secondary")
        load_btn.clicked.connect(self.load_report)
        header_layout.addWidget(load_btn)
        
        save_btn = QPushButton("💾 Save")
        save_btn.setProperty("variant", "secondary")
        save_btn.clicked.connect(self.save_report)
        header_layout.addWidget(save_btn)
        
        save_as_btn = QPushButton("💾 Save As...")
        save_as_btn.setProperty("variant", "secondary")
        save_as_btn.clicked.connect(self.save_report_as)
        header_layout.addWidget(save_as_btn)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_widget = QWidget()
        scroll_widget.setAutoFillBackground(True)
        content_layout = QVBoxLayout(scroll_widget)
        content_layout.setSpacing(20)
        
        # General Information Group
        general_group = QGroupBox("General Information")
        general_layout = QVBoxLayout(general_group)
        general_layout.setSpacing(16)
        
        # Row 1: Responsible and Student
        row1 = QHBoxLayout()
        row1.setSpacing(16)
        
        # Responsible
        responsible_container = QWidget()
        responsible_layout = QVBoxLayout(responsible_container)
        responsible_layout.setContentsMargins(0, 0, 0, 0)
        responsible_layout.setSpacing(8)
        
        responsible_label = QLabel("Responsible *")
        responsible_label.setProperty("subheading", True)
        responsible_layout.addWidget(responsible_label)
        
        self.responsible_input = QLineEdit()
        self.responsible_input.setPlaceholderText("Name of responsible person")
        self.responsible_input.textChanged.connect(self.update_report_data)
        responsible_layout.addWidget(self.responsible_input)
        
        row1.addWidget(responsible_container, 1)
        
        # Student
        student_container = QWidget()
        student_layout = QVBoxLayout(student_container)
        student_layout.setContentsMargins(0, 0, 0, 0)
        student_layout.setSpacing(8)
        
        student_label = QLabel("Student *")
        student_label.setProperty("subheading", True)
        student_layout.addWidget(student_label)
        
        self.student_input = QLineEdit()
        self.student_input.setPlaceholderText("Student name")
        self.student_input.textChanged.connect(self.update_report_data)
        student_layout.addWidget(self.student_input)
        
        row1.addWidget(student_container, 1)
        
        general_layout.addLayout(row1)
        
        # Row 2: Date and Times
        row2 = QHBoxLayout()
        row2.setSpacing(16)
        
        # Date
        date_container = QWidget()
        date_layout = QVBoxLayout(date_container)
        date_layout.setContentsMargins(0, 0, 0, 0)
        date_layout.setSpacing(8)
        
        date_label = QLabel("Date *")
        date_label.setProperty("subheading", True)
        date_layout.addWidget(date_label)
        
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.dateChanged.connect(self.update_report_data)
        date_layout.addWidget(self.date_input)
        
        row2.addWidget(date_container, 1)
        
        # Entry Time
        entry_container = QWidget()
        entry_layout = QVBoxLayout(entry_container)
        entry_layout.setContentsMargins(0, 0, 0, 0)
        entry_layout.setSpacing(8)
        
        entry_label = QLabel("Entry Time *")
        entry_label.setProperty("subheading", True)
        entry_layout.addWidget(entry_label)
        
        self.entry_time_input = QTimeEdit()
        self.entry_time_input.setDisplayFormat("HH:mm")
        self.entry_time_input.setTime(QTime(8, 0))
        self.entry_time_input.timeChanged.connect(self.update_report_data)
        entry_layout.addWidget(self.entry_time_input)
        
        row2.addWidget(entry_container, 1)
        
        # Exit Time
        exit_container = QWidget()
        exit_layout = QVBoxLayout(exit_container)
        exit_layout.setContentsMargins(0, 0, 0, 0)
        exit_layout.setSpacing(8)
        
        exit_label = QLabel("Exit Time *")
        exit_label.setProperty("subheading", True)
        exit_layout.addWidget(exit_label)
        
        self.exit_time_input = QTimeEdit()
        self.exit_time_input.setDisplayFormat("HH:mm")
        self.exit_time_input.setTime(QTime(17, 0))
        self.exit_time_input.timeChanged.connect(self.update_report_data)
        exit_layout.addWidget(self.exit_time_input)
        
        row2.addWidget(exit_container, 1)
        
        # Instance Hours (read-only)
        instance_container = QWidget()
        instance_layout = QVBoxLayout(instance_container)
        instance_layout.setContentsMargins(0, 0, 0, 0)
        instance_layout.setSpacing(8)
        
        instance_label = QLabel("Instance Hours")
        instance_label.setProperty("subheading", True)
        instance_layout.addWidget(instance_label)
        
        self.instance_hours_display = QLabel("09:00")
        self.instance_hours_display.setStyleSheet(f"""
            QLabel {{
                background-color: {AppStyles.COLORS['bg_tertiary']};
                padding: 10px 12px;
                border-radius: {AppStyles.RADIUS['md']};
                font-size: {AppStyles.FONTS['size_lg']};
                font-weight: 600;
                color: {AppStyles.COLORS['primary']};
            }}
        """)
        instance_layout.addWidget(self.instance_hours_display)
        
        row2.addWidget(instance_container, 1)
        
        general_layout.addLayout(row2)
        
        content_layout.addWidget(general_group)
        
        # Activities Section
        activities_group = QGroupBox("Activities")
        activities_layout = QVBoxLayout(activities_group)
        activities_layout.setSpacing(12)
        
        # Activities header
        activities_header = QHBoxLayout()
        
        activities_title = QLabel("Activity List")
        activities_title.setProperty("subheading", True)
        activities_header.addWidget(activities_title)
        
        self.activity_count_label = QLabel("0 activities")
        self.activity_count_label.setProperty("caption", True)
        activities_header.addWidget(self.activity_count_label)
        
        activities_header.addStretch()
        
        add_activity_btn = QPushButton("+ Add Activity")
        add_activity_btn.setProperty("variant", "success")
        add_activity_btn.clicked.connect(self.add_activity)
        activities_header.addWidget(add_activity_btn)
        
        activities_layout.addLayout(activities_header)
        
        # Activities list
        self.activities_list = QListWidget()
        self.activities_list.setMinimumHeight(300)
        activities_layout.addWidget(self.activities_list)
        
        # Activities summary
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(16)
        
        self.total_time_label = QLabel("Total Activity Time: 00:00")
        self.total_time_label.setProperty("caption", True)
        summary_layout.addWidget(self.total_time_label)
        
        self.total_images_label = QLabel("Total Images: 0")
        self.total_images_label.setProperty("caption", True)
        summary_layout.addWidget(self.total_images_label)
        
        summary_layout.addStretch()
        
        activities_layout.addLayout(summary_layout)
        
        content_layout.addWidget(activities_group)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Bottom actions
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(12)
        
        # Compression level
        compression_label = QLabel("PDF Compression:")
        bottom_layout.addWidget(compression_label)
        
        self.compression_combo = QComboBox()
        self.compression_combo.addItems(["Low", "Medium", "High"])
        self.compression_combo.setCurrentIndex(1)
        self.compression_combo.setFixedWidth(150)
        bottom_layout.addWidget(self.compression_combo)
        
        # Signature checkbox
        from PySide6.QtWidgets import QCheckBox
        self.signatures_checkbox = QCheckBox("Include Signatures")
        self.signatures_checkbox.setChecked(False)
        bottom_layout.addWidget(self.signatures_checkbox)
        
        # Theme toggle button
        self.theme_btn = QPushButton("🌙 Dark Mode")
        self.theme_btn.setProperty("variant", "secondary")
        self.theme_btn.clicked.connect(self.toggle_theme)
        bottom_layout.addWidget(self.theme_btn)
        
        bottom_layout.addStretch()
        
        preview_btn = QPushButton("👁️ Preview PDF")
        preview_btn.setProperty("variant", "secondary")
        preview_btn.clicked.connect(self.preview_pdf)
        bottom_layout.addWidget(preview_btn)
        
        generate_btn = QPushButton("📄 Generate PDF")
        generate_btn.clicked.connect(self.generate_pdf)
        bottom_layout.addWidget(generate_btn)
        
        main_layout.addLayout(bottom_layout)
        
        # Initial update (block signals to avoid loops)
        self.responsible_input.blockSignals(True)
        self.student_input.blockSignals(True)
        self.date_input.blockSignals(True)
        self.entry_time_input.blockSignals(True)
        self.exit_time_input.blockSignals(True)
        
        self.update_report_data()
        
        self.responsible_input.blockSignals(False)
        self.student_input.blockSignals(False)
        self.date_input.blockSignals(False)
        self.entry_time_input.blockSignals(False)
        self.exit_time_input.blockSignals(False)
    
    def apply_styles(self):
        """Apply stylesheet to window."""
        self.setStyleSheet(AppStyles.get_main_stylesheet())
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        AppStyles.toggle_theme()
        
        # Update button text
        if AppStyles.CURRENT_THEME == "dark":
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self.theme_btn.setText("🌙 Dark Mode")
        
        # Reapply styles
        self.apply_styles()
        
        # Update all activity list items
        for i in range(self.activities_list.count()):
            item = self.activities_list.item(i)
            widget = self.activities_list.itemWidget(item)
            if isinstance(widget, ActivityListItem):
                widget.update_theme()
    
    def new_report(self):
        """Create a new report."""
        # Ask to save if there are changes
        if self.report and self.report.get_activity_count() > 0:
            reply = QMessageBox.question(
                self,
                "New Report",
                "Current report has activities. Create new report anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
        
        self.report = Report()
        self.current_file = None
        
        # Reset form if UI is ready
        if hasattr(self, 'responsible_input'):
            # Block signals
            self.responsible_input.blockSignals(True)
            self.student_input.blockSignals(True)
            self.date_input.blockSignals(True)
            self.entry_time_input.blockSignals(True)
            self.exit_time_input.blockSignals(True)
            
            self.responsible_input.clear()
            self.student_input.clear()
            self.date_input.setDate(QDate.currentDate())
            self.entry_time_input.setTime(QTime(8, 0))
            self.exit_time_input.setTime(QTime(17, 0))
            
            # Unblock signals
            self.responsible_input.blockSignals(False)
            self.student_input.blockSignals(False)
            self.date_input.blockSignals(False)
            self.entry_time_input.blockSignals(False)
            self.exit_time_input.blockSignals(False)
            
            self.refresh_activities_list()
            self.update_summary()
    
    def load_report(self):
        """Load report from JSON file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Report",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            report, message = Report.from_json(file_path)
            if report:
                self.report = report
                self.current_file = file_path
                self.load_report_data()
                QMessageBox.information(self, "Success", f"Report loaded successfully!\n\n{file_path}")
            else:
                QMessageBox.critical(self, "Error", f"Failed to load report:\n\n{message}")
    
    def save_report(self):
        """Save report to current file or ask for location if new."""
        if not self.report:
            return
        
        # Validate first
        valid, message = self.report.complete_validate()
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        # If no current file, use Save As
        if not self.current_file:
            self.save_report_as()
            return
        
        # Save to current file
        success, message = self.report.to_json(self.current_file)
        if success:
            QMessageBox.information(self, "Success", f"Report saved!\n\n{self.current_file}")
        else:
            QMessageBox.critical(self, "Error", message)
    
    def save_report_as(self):
        """Save report with new filename."""
        if not self.report:
            return
        
        # Validate first
        valid, message = self.report.complete_validate()
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        # Suggest filename based on date and student
        suggested_name = f"report_{self.report.date.strftime('%Y-%m-%d')}_{self.report.student.replace(' ', '_')}.json"
        if not suggested_name.endswith('.json'):
            suggested_name += '.json'
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Report As",
            suggested_name,
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            # Ensure .json extension
            if not file_path.endswith('.json'):
                file_path += '.json'
            
            success, message = self.report.to_json(file_path)
            if success:
                self.current_file = file_path
                QMessageBox.information(self, "Success", f"Report saved successfully!\n\n{file_path}")
            else:
                QMessageBox.critical(self, "Error", message)
    
    def load_report_data(self):
        """Load report data into form."""
        if not self.report:
            return
        
        # Block signals to avoid triggering update loops
        self.responsible_input.blockSignals(True)
        self.student_input.blockSignals(True)
        self.date_input.blockSignals(True)
        self.entry_time_input.blockSignals(True)
        self.exit_time_input.blockSignals(True)
        
        self.responsible_input.setText(self.report.responsible)
        self.student_input.setText(self.report.student)
        
        # Set date
        q_date = QDate(
            self.report.date.year,
            self.report.date.month,
            self.report.date.day
        )
        self.date_input.setDate(q_date)
        
        # Set times
        entry_parts = self.report.entry_time.split(":")
        self.entry_time_input.setTime(QTime(int(entry_parts[0]), int(entry_parts[1])))
        
        exit_parts = self.report.exit_time.split(":")
        self.exit_time_input.setTime(QTime(int(exit_parts[0]), int(exit_parts[1])))
        
        # Unblock signals
        self.responsible_input.blockSignals(False)
        self.student_input.blockSignals(False)
        self.date_input.blockSignals(False)
        self.entry_time_input.blockSignals(False)
        self.exit_time_input.blockSignals(False)
        
        # Refresh activities
        self.refresh_activities_list()
        self.update_summary()
    
    def update_report_data(self):
        """Update report object from form data."""
        if not self.report:
            return
        
        try:
            self.report.responsible = self.responsible_input.text()
            self.report.student = self.student_input.text()
            
            # Update date
            q_date = self.date_input.date()
            self.report.date = date(q_date.year(), q_date.month(), q_date.day())
            
            # Update times
            self.report.entry_time = self.entry_time_input.time().toString("HH:mm")
            self.report.exit_time = self.exit_time_input.time().toString("HH:mm")
            
            # Update instance hours display
            self.report.calculate_instance_hours()
            if hasattr(self, 'instance_hours_display'):
                self.instance_hours_display.setText(self.report.instance_hours)
        except Exception as e:
            # Silently catch errors during initialization
            pass
    
    def add_activity(self):
        """Open dialog to add new activity."""
        dialog = ActivityDialog(self, mode="CREATE")
        if dialog.exec():
            activity = dialog.get_activity()
            if activity:
                success, message = self.report.add_activity(activity)
                if success:
                    self.refresh_activities_list()
                    self.update_summary()
                else:
                    QMessageBox.warning(self, "Error", message)
    
    def edit_activity(self, index: int):
        """Open dialog to edit activity."""
        activity = self.report.get_activity(index)
        if not activity:
            return
        
        dialog = ActivityDialog(self, activity=activity, mode="EDIT")
        if dialog.exec():
            updated_activity = dialog.get_activity()
            if updated_activity:
                success, message = self.report.edit_activity(index, updated_activity)
                if success:
                    self.refresh_activities_list()
                    self.update_summary()
                else:
                    QMessageBox.warning(self, "Error", message)
    
    def delete_activity(self, index: int):
        """Delete activity at index."""
        activity = self.report.get_activity(index)
        if not activity:
            return
        
        reply = QMessageBox.question(
            self,
            "Delete Activity",
            f"Delete activity '{activity.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.report.remove_activity(index)
            if success:
                self.refresh_activities_list()
                self.update_summary()
            else:
                QMessageBox.warning(self, "Error", message)
    
    def refresh_activities_list(self):
        """Refresh the activities list widget."""
        self.activities_list.clear()
        
        if not self.report:
            return
        
        for i in range(self.report.get_activity_count()):
            activity = self.report.get_activity(i)
            if activity:
                item = QListWidgetItem(self.activities_list)
                item_widget = ActivityListItem(activity, i)
                item_widget.edit_requested.connect(self.edit_activity)
                item_widget.delete_requested.connect(self.delete_activity)
                
                item.setSizeHint(item_widget.sizeHint())
                self.activities_list.addItem(item)
                self.activities_list.setItemWidget(item, item_widget)
    
    def update_summary(self):
        """Update activity summary labels."""
        if not self.report:
            return
        
        count = self.report.get_activity_count()
        self.activity_count_label.setText(f"{count} {'activity' if count == 1 else 'activities'}")
        
        total_time = self.report.calculate_total_activity_hours()
        self.total_time_label.setText(f"Total Activity Time: {total_time}")
        
        total_images = self.report.get_total_images_count()
        self.total_images_label.setText(f"Total Images: {total_images}")
    
    def preview_pdf(self):
        """Preview PDF before saving."""
        if not self.report:
            return
        
        # Validate first
        valid, message = self.report.complete_validate()
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        try:
            from services.pdf_generator import generate_pdf, CompressionLevel
            import tempfile
            import subprocess
            import platform
            
            # Map combo text to compression level
            compression_map = {
                "Low": CompressionLevel.LOW,
                "Medium": CompressionLevel.MEDIUM,
                "High": CompressionLevel.HIGH
            }
            compression = compression_map.get(
                self.compression_combo.currentText(),
                CompressionLevel.MEDIUM
            )
            
            # Get signature preference
            include_signatures = self.signatures_checkbox.isChecked()
            
            # Generate preview in temp file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.pdf',
                prefix='preview_'
            )
            temp_file.close()
            
            # Show progress
            QMessageBox.information(
                self,
                "Generating Preview",
                "Generating PDF preview...\nThis may take a moment."
            )
            
            # Generate PDF
            success, msg = generate_pdf(self.report, temp_file.name, compression, include_signatures)
            
            if success:
                # Open with default PDF viewer
                system = platform.system()
                try:
                    if system == 'Darwin':  # macOS
                        subprocess.call(['open', temp_file.name])
                    elif system == 'Windows':
                        os.startfile(temp_file.name)
                    else:  # Linux
                        subprocess.call(['xdg-open', temp_file.name])
                    
                    QMessageBox.information(
                        self,
                        "Preview Ready",
                        "PDF preview opened in your default viewer."
                    )
                except Exception as e:
                    QMessageBox.information(
                        self,
                        "Preview Generated",
                        f"Preview saved to:\n{temp_file.name}\n\nPlease open it manually."
                    )
            else:
                QMessageBox.critical(self, "Error", msg)
                
        except ImportError:
            QMessageBox.critical(
                self,
                "Missing Dependency",
                "ReportLab is required for PDF generation.\n\n"
                "Install it with:\npip install reportlab"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error generating preview:\n{str(e)}"
            )
    
    def generate_pdf(self):
        """Generate and save PDF."""
        if not self.report:
            return
        
        # Validate first
        valid, message = self.report.complete_validate()
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        try:
            from services.pdf_generator import generate_pdf, CompressionLevel
            
            # Get save location
            default_name = f"report_{self.report.date.strftime('%Y-%m-%d')}_{self.report.student.replace(' ', '_')}.pdf"
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF Report",
                default_name,
                "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Map combo text to compression level
            compression_map = {
                "Low": CompressionLevel.LOW,
                "Medium": CompressionLevel.MEDIUM,
                "High": CompressionLevel.HIGH
            }
            compression = compression_map.get(
                self.compression_combo.currentText(),
                CompressionLevel.MEDIUM
            )
            
            # Get signature preference
            include_signatures = self.signatures_checkbox.isChecked()
            
            # Generate PDF
            success, msg = generate_pdf(self.report, file_path, compression, include_signatures)
            
            if success:
                reply = QMessageBox.question(
                    self,
                    "PDF Generated",
                    f"PDF saved successfully!\n\n{file_path}\n\nWould you like to open it?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    import subprocess
                    import platform
                    
                    system = platform.system()
                    try:
                        if system == 'Darwin':  # macOS
                            subprocess.call(['open', file_path])
                        elif system == 'Windows':
                            os.startfile(file_path)
                        else:  # Linux
                            subprocess.call(['xdg-open', file_path])
                    except Exception as e:
                        QMessageBox.information(
                            self,
                            "File Saved",
                            f"PDF saved to:\n{file_path}\n\nPlease open it manually."
                        )
            else:
                QMessageBox.critical(self, "Error", msg)
                
        except ImportError:
            QMessageBox.critical(
                self,
                "Missing Dependency",
                "ReportLab is required for PDF generation.\n\n"
                "Install it with:\npip install reportlab"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error generating PDF:\n{str(e)}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())