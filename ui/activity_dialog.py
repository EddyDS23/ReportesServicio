
from PySide6.QtWidgets import ( QTextEdit, QTimeEdit, QPushButton, QScrollArea, QWidget,
    QGridLayout, QFrame, QMessageBox, QFileDialog, QVBoxLayout,QLabel,QDialog, QLineEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QTime, Signal
from PySide6.QtGui import QPixmap, QIcon 
from models.activity_model import Activity
from ui.styles import AppStyles
from typing import Optional, List

import os
import sys

class ImagePreviewWidget(QWidget):
    """Widget to display image preview with delete button."""
    
    remove_requested = Signal(int)  # Emits index when delete is clicked
    
    def __init__(self, image_path: str, index: int, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.index = index
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the image preview UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # Image container
        image_frame = QFrame()
        image_frame.setProperty("card", True)
        image_frame.setFixedSize(120, 120)
        image_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {AppStyles.COLORS['bg_tertiary']};
                border: 2px solid {AppStyles.COLORS['border']};
                border-radius: {AppStyles.RADIUS['md']};
            }}
        """)
        
        image_layout = QVBoxLayout(image_frame)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        # Image label
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        try:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    116, 116,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                image_label.setPixmap(scaled_pixmap)
            else:
                image_label.setText("Invalid\nImage")
                image_label.setProperty("caption", True)
        except Exception as e:
            image_label.setText("Error\nLoading")
            image_label.setProperty("caption", True)
        
        image_layout.addWidget(image_label)
        layout.addWidget(image_frame)
        
        # Delete button
        delete_btn = QPushButton("✕ Remove")
        delete_btn.setProperty("variant", "danger")
        delete_btn.setFixedHeight(28)
        delete_btn.clicked.connect(lambda: self.remove_requested.emit(self.index))
        layout.addWidget(delete_btn)
        
        # Filename label
        filename = os.path.basename(self.image_path)
        if len(filename) > 15:
            filename = filename[:12] + "..."
        filename_label = QLabel(filename)
        filename_label.setProperty("caption", True)
        filename_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filename_label.setWordWrap(True)
        layout.addWidget(filename_label)


class ActivityDialog(QDialog):
    """
    Dialog for creating or editing an activity.
    Supports both CREATE and EDIT modes.
    """
    
    def __init__(self, parent=None, activity: Optional[Activity] = None, mode: str = "CREATE"):
        """
        Initialize activity dialog.
        
        Args:
            parent: Parent widget
            activity: Activity to edit (None for create mode)
            mode: "CREATE" or "EDIT"
        """
        super().__init__(parent)
        self.activity = activity
        self.mode = mode
        self.image_paths: List[str] = []
        self.image_widgets: List[ImagePreviewWidget] = []
        
        # Load existing images if editing
        if self.activity and self.activity.images:
            self.image_paths = self.activity.images.copy()
        
        self.setup_ui()
        self.apply_styles()
        
        # Load data if editing
        if self.mode == "EDIT" and self.activity:
            self.load_activity_data()
    
    def setup_ui(self):
        """Setup the dialog UI."""
        # Window setup
        title = "Edit Activity" if self.mode == "EDIT" else "New Activity"
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(24, 24, 24, 24)
        
        # Header
        header_label = QLabel(title)
        header_label.setProperty("heading", True)
        main_layout.addWidget(header_label)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        scroll_widget = QWidget()
        form_layout = QVBoxLayout(scroll_widget)
        form_layout.setSpacing(16)
        
        # Title field
        title_label = QLabel("Title *")
        title_label.setProperty("subheading", True)
        form_layout.addWidget(title_label)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g., Python Programming")
        form_layout.addWidget(self.title_input)
        
        # Description field
        desc_label = QLabel("Description *")
        desc_label.setProperty("subheading", True)
        form_layout.addWidget(desc_label)
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Describe the activity in detail...")
        self.description_input.setMaximumHeight(120)
        form_layout.addWidget(self.description_input)
        
        # Time fields
        time_container = QWidget()
        time_layout = QHBoxLayout(time_container)
        time_layout.setContentsMargins(0, 0, 0, 0)
        time_layout.setSpacing(16)
        
        # Start time
        start_container = QWidget()
        start_layout = QVBoxLayout(start_container)
        start_layout.setContentsMargins(0, 0, 0, 0)
        start_layout.setSpacing(8)
        
        start_label = QLabel("Start Time *")
        start_label.setProperty("subheading", True)
        start_layout.addWidget(start_label)
        
        self.start_time_input = QTimeEdit()
        self.start_time_input.setDisplayFormat("HH:mm")
        self.start_time_input.setTime(QTime(9, 0))
        self.start_time_input.timeChanged.connect(self.update_duration)
        start_layout.addWidget(self.start_time_input)
        
        time_layout.addWidget(start_container, 1)
        
        # End time
        end_container = QWidget()
        end_layout = QVBoxLayout(end_container)
        end_layout.setContentsMargins(0, 0, 0, 0)
        end_layout.setSpacing(8)
        
        end_label = QLabel("End Time *")
        end_label.setProperty("subheading", True)
        end_layout.addWidget(end_label)
        
        self.end_time_input = QTimeEdit()
        self.end_time_input.setDisplayFormat("HH:mm")
        self.end_time_input.setTime(QTime(12, 0))
        self.end_time_input.timeChanged.connect(self.update_duration)
        end_layout.addWidget(self.end_time_input)
        
        time_layout.addWidget(end_container, 1)
        
        # Duration display
        duration_container = QWidget()
        duration_layout = QVBoxLayout(duration_container)
        duration_layout.setContentsMargins(0, 0, 0, 0)
        duration_layout.setSpacing(8)
        
        duration_label = QLabel("Duration")
        duration_label.setProperty("subheading", True)
        duration_layout.addWidget(duration_label)
        
        self.duration_display = QLabel("03:00")
        self.duration_display.setStyleSheet(f"""
            QLabel {{
                background-color: {AppStyles.COLORS['bg_tertiary']};
                padding: 10px 12px;
                border-radius: {AppStyles.RADIUS['md']};
                font-size: {AppStyles.FONTS['size_lg']};
                font-weight: 600;
                color: {AppStyles.COLORS['primary']};
            }}
        """)
        duration_layout.addWidget(self.duration_display)
        
        time_layout.addWidget(duration_container, 1)
        
        form_layout.addWidget(time_container)
        
        # Images section
        images_header = QHBoxLayout()
        images_header.setSpacing(12)
        
        images_label = QLabel("Images")
        images_label.setProperty("subheading", True)
        images_header.addWidget(images_label)
        
        self.image_count_label = QLabel(f"0/{Activity.MAX_IMAGES}")
        self.image_count_label.setProperty("caption", True)
        images_header.addWidget(self.image_count_label)
        images_header.addStretch()
        
        add_image_btn = QPushButton("+ Add Images")
        add_image_btn.setProperty("variant", "secondary")
        add_image_btn.clicked.connect(self.add_images)
        images_header.addWidget(add_image_btn)
        
        form_layout.addLayout(images_header)
        
        # Images grid
        self.images_container = QWidget()
        self.images_grid = QGridLayout(self.images_container)
        self.images_grid.setSpacing(12)
        self.images_grid.setContentsMargins(0, 0, 0, 0)
        form_layout.addWidget(self.images_container)
        
        # Spacer
        form_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Separator
        separator = QFrame()
        separator.setProperty("separator", True)
        main_layout.addWidget(separator)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("variant", "secondary")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        buttons_layout.addStretch()
        
        save_text = "Update Activity" if self.mode == "EDIT" else "Create Activity"
        self.save_btn = QPushButton(save_text)
        self.save_btn.setProperty("variant", "success")
        self.save_btn.clicked.connect(self.save_activity)
        buttons_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(buttons_layout)
        
        # Initial duration calculation
        self.update_duration()
        
        # Load existing images if any
        if self.image_paths:
            self.refresh_image_grid()
    
    def apply_styles(self):
        """Apply stylesheet to dialog."""
        self.setStyleSheet(AppStyles.get_main_stylesheet())
    
    def load_activity_data(self):
        """Load existing activity data into form fields."""
        if not self.activity:
            return
        
        self.title_input.setText(self.activity.title)
        self.description_input.setPlainText(self.activity.description)
        
        # Parse and set times
        try:
            start_parts = self.activity.start_time.split(":")
            self.start_time_input.setTime(QTime(int(start_parts[0]), int(start_parts[1])))
            
            end_parts = self.activity.end_time.split(":")
            self.end_time_input.setTime(QTime(int(end_parts[0]), int(end_parts[1])))
        except:
            pass
        
        self.update_duration()
    
    def update_duration(self):
        """Update duration display when times change."""
        start = self.start_time_input.time()
        end = self.end_time_input.time()
        
        # Calculate duration in minutes
        start_minutes = start.hour() * 60 + start.minute()
        end_minutes = end.hour() * 60 + end.minute()
        
        # Handle overnight activities
        if end_minutes <= start_minutes:
            end_minutes += 24 * 60
        
        duration_minutes = end_minutes - start_minutes
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        
        self.duration_display.setText(f"{hours:02d}:{minutes:02d}")
    
    def add_images(self):
        """Open file dialog to add images."""
        if len(self.image_paths) >= Activity.MAX_IMAGES:
            QMessageBox.warning(
                self,
                "Limit Reached",
                f"Maximum of {Activity.MAX_IMAGES} images allowed per activity."
            )
            return
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp *.webp)"
        )
        
        if files:
            for file in files:
                if len(self.image_paths) >= Activity.MAX_IMAGES:
                    QMessageBox.information(
                        self,
                        "Limit Reached",
                        f"Only {Activity.MAX_IMAGES} images can be added. Remaining files were not added."
                    )
                    break
                
                # Check file size
                file_size_mb = os.path.getsize(file) / (1024 * 1024)
                if file_size_mb > Activity.MAX_SIZE_IMAGE_MB:
                    QMessageBox.warning(
                        self,
                        "File Too Large",
                        f"File {os.path.basename(file)} is too large ({file_size_mb:.1f}MB).\nMaximum size is {Activity.MAX_SIZE_IMAGE_MB}MB."
                    )
                    continue
                
                self.image_paths.append(file)
            
            self.refresh_image_grid()
    
    def remove_image(self, index: int):
        """Remove image at index."""
        if 0 <= index < len(self.image_paths):
            self.image_paths.pop(index)
            self.refresh_image_grid()
    
    def refresh_image_grid(self):
        """Refresh the image preview grid."""
        # Clear existing widgets
        for widget in self.image_widgets:
            widget.deleteLater()
        self.image_widgets.clear()
        
        # Add image previews (3 per row)
        row = 0
        col = 0
        for i, image_path in enumerate(self.image_paths):
            widget = ImagePreviewWidget(image_path, i)
            widget.remove_requested.connect(self.remove_image)
            
            self.images_grid.addWidget(widget, row, col)
            self.image_widgets.append(widget)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
        
        # Update count label
        self.image_count_label.setText(f"{len(self.image_paths)}/{Activity.MAX_IMAGES}")
    
    def validate_form(self) -> tuple[bool, str]:
        """Validate form data."""
        title = self.title_input.text().strip()
        if not title:
            return False, "Title is required"
        
        description = self.description_input.toPlainText().strip()
        if not description:
            return False, "Description is required"
        
        return True, "Valid"
    
    def save_activity(self):
        """Save the activity."""
        # Validate
        valid, message = self.validate_form()
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
        
        # Create activity object
        start_time = self.start_time_input.time().toString("HH:mm")
        end_time = self.end_time_input.time().toString("HH:mm")
        
        self.activity = Activity(
            title=self.title_input.text().strip(),
            description=self.description_input.toPlainText().strip(),
            start_time=start_time,
            end_time=end_time,
            images=self.image_paths.copy()
        )
        
        # Validate activity
        valid, message = self.activity.complete_validate()
        if not valid:
            QMessageBox.warning(self, "Activity Error", message)
            return
        
        self.accept()
    
    def get_activity(self) -> Optional[Activity]:
        """Get the created/edited activity."""
        return self.activity


# Test the dialog
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Test CREATE mode
    dialog = ActivityDialog(mode="CREATE")
    if dialog.exec():
        activity = dialog.get_activity()
        if activity:
            print("Activity created:")
            print(activity)
    
    # Test EDIT mode
    test_activity = Activity(
        title="Test Activity",
        description="This is a test",
        start_time="10:00",
        end_time="12:30"
    )
    
    dialog2 = ActivityDialog(activity=test_activity, mode="EDIT")
    if dialog2.exec():
        activity = dialog2.get_activity()
        if activity:
            print("\nActivity edited:")
            print(activity)