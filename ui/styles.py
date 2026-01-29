"""
Modern stylesheet for Daily Report System.
Professional design with clean aesthetics.
"""


class AppStyles:
    """Centralized styles for the application."""
    
    # Color Palette - Professional Blue/Gray theme (Light Mode)
    COLORS_LIGHT = {
        # Primary colors
        'primary': '#2563EB',           # Modern blue
        'primary_hover': '#1D4ED8',     # Darker blue
        'primary_light': '#3B82F6',     # Light blue
        
        # Accent
        'accent': '#10B981',            # Green for success
        'accent_hover': '#059669',
        'warning': '#F59E0B',           # Amber for warnings
        'danger': '#EF4444',            # Red for delete/errors
        'danger_hover': '#DC2626',
        
        # Backgrounds
        'bg_primary': '#FFFFFF',        # White
        'bg_secondary': '#F9FAFB',      # Light gray
        'bg_tertiary': '#F3F4F6',       # Lighter gray
        'bg_dark': '#1F2937',           # Dark gray
        
        # Text
        'text_primary': '#111827',      # Almost black
        'text_secondary': '#6B7280',    # Medium gray
        'text_tertiary': '#9CA3AF',     # Light gray
        'text_white': '#FFFFFF',
        
        # Borders
        'border': '#E5E7EB',            # Light border
        'border_focus': '#2563EB',      # Blue border on focus
        'border_dark': '#D1D5DB',       # Darker border
        
        # Status colors
        'success': '#10B981',
        'info': '#3B82F6',
        'error': '#EF4444',
    }
    
    # Color Palette - Dark Mode
    COLORS_DARK = {
        # Primary colors
        'primary': '#3B82F6',           # Brighter blue for dark
        'primary_hover': '#2563EB',     
        'primary_light': '#60A5FA',     
        
        # Accent
        'accent': '#10B981',            
        'accent_hover': '#059669',
        'warning': '#F59E0B',           
        'danger': '#EF4444',            
        'danger_hover': '#DC2626',
        
        # Backgrounds
        'bg_primary': '#1F2937',        # Dark gray
        'bg_secondary': '#111827',      # Darker gray
        'bg_tertiary': '#374151',       # Medium dark gray
        'bg_dark': '#030712',           # Almost black
        
        # Text
        'text_primary': '#F9FAFB',      # Almost white
        'text_secondary': '#D1D5DB',    # Light gray
        'text_tertiary': '#9CA3AF',     # Medium gray
        'text_white': '#FFFFFF',
        
        # Borders
        'border': '#374151',            # Dark border
        'border_focus': '#3B82F6',      # Blue border on focus
        'border_dark': '#4B5563',       # Darker border
        
        # Status colors
        'success': '#10B981',
        'info': '#3B82F6',
        'error': '#EF4444',
    }
    
    # Active color palette (defaults to light)
    COLORS = COLORS_LIGHT.copy()
    
    # Track current theme
    CURRENT_THEME = "light"
    
    # Fonts
    FONTS = {
        'family': '"Segoe UI", "SF Pro Display", -apple-system, system-ui, sans-serif',
        'family_mono': '"SF Mono", "Consolas", "Monaco", monospace',
        
        # Sizes
        'size_xs': '11px',
        'size_sm': '13px',
        'size_base': '14px',
        'size_lg': '16px',
        'size_xl': '20px',
        'size_2xl': '24px',
        'size_3xl': '30px',
    }
    
    # Spacing
    SPACING = {
        'xs': '4px',
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
        '2xl': '32px',
        '3xl': '48px',
    }
    
    # Border radius
    RADIUS = {
        'sm': '4px',
        'md': '6px',
        'lg': '8px',
        'xl': '12px',
        'full': '9999px',
    }
    
    # Shadows
    SHADOWS = {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    }
    
    @classmethod
    def set_theme(cls, theme: str):
        """
        Change the application theme.
        
        Args:
            theme: "light" or "dark"
        """
        if theme == "dark":
            cls.COLORS = cls.COLORS_DARK.copy()
            cls.CURRENT_THEME = "dark"
        else:
            cls.COLORS = cls.COLORS_LIGHT.copy()
            cls.CURRENT_THEME = "light"
    
    @classmethod
    def toggle_theme(cls):
        """Toggle between light and dark themes."""
        if cls.CURRENT_THEME == "light":
            cls.set_theme("dark")
        else:
            cls.set_theme("light")
    
    @classmethod
    def get_main_stylesheet(cls) -> str:
        """Returns the main application stylesheet."""
        c = cls.COLORS
        f = cls.FONTS
        r = cls.RADIUS
        
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {c['bg_secondary']};
        }}
        
        /* Central Widget */
        QWidget {{
            font-family: {f['family']};
            font-size: {f['size_base']};
            color: {c['text_primary']};
        }}
        
        QWidget#centralwidget {{
            background-color: {c['bg_secondary']};
        }}
        
        /* Labels */
        QLabel {{
            color: {c['text_primary']};
            font-size: {f['size_base']};
        }}
        
        QLabel[heading="true"] {{
            font-size: {f['size_2xl']};
            font-weight: 600;
            color: {c['text_primary']};
        }}
        
        QLabel[subheading="true"] {{
            font-size: {f['size_lg']};
            font-weight: 500;
            color: {c['text_secondary']};
        }}
        
        QLabel[caption="true"] {{
            font-size: {f['size_sm']};
            color: {c['text_tertiary']};
        }}
        
        /* Line Edits */
        QLineEdit {{
            padding: 10px 12px;
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_primary']};
            font-size: {f['size_base']};
            color: {c['text_primary']};
        }}
        
        QLineEdit:focus {{
            border: 2px solid {c['border_focus']};
            padding: 9px 11px;
        }}
        
        QLineEdit:disabled {{
            background-color: {c['bg_tertiary']};
            color: {c['text_tertiary']};
        }}
        
        /* Text Edits */
        QTextEdit {{
            padding: 10px 12px;
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_primary']};
            font-size: {f['size_base']};
            color: {c['text_primary']};
        }}
        
        QTextEdit:focus {{
            border: 2px solid {c['border_focus']};
        }}
        
        /* Buttons - Primary */
        QPushButton {{
            padding: 10px 20px;
            border: none;
            border-radius: {r['md']};
            background-color: {c['primary']};
            color: {c['text_white']};
            font-size: {f['size_base']};
            font-weight: 500;
            min-height: 20px;
        }}
        
        QPushButton:hover {{
            background-color: {c['primary_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {c['primary_hover']};
            padding-top: 11px;
            padding-bottom: 9px;
        }}
        
        QPushButton:disabled {{
            background-color: {c['bg_tertiary']};
            color: {c['text_tertiary']};
        }}
        
        /* Secondary Buttons */
        QPushButton[variant="secondary"] {{
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
            border: 1px solid {c['border_dark']};
        }}
        
        QPushButton[variant="secondary"]:hover {{
            background-color: {c['bg_tertiary']};
            border-color: {c['text_secondary']};
        }}
        
        /* Success Buttons */
        QPushButton[variant="success"] {{
            background-color: {c['accent']};
        }}
        
        QPushButton[variant="success"]:hover {{
            background-color: {c['accent_hover']};
        }}
        
        /* Danger Buttons */
        QPushButton[variant="danger"] {{
            background-color: {c['danger']};
        }}
        
        QPushButton[variant="danger"]:hover {{
            background-color: {c['danger_hover']};
        }}
        
        /* Warning Buttons */
        QPushButton[variant="warning"] {{
            background-color: {c['warning']};
        }}
        
        /* Icon Buttons */
        QPushButton[icon="true"] {{
            padding: 8px;
            min-width: 36px;
            min-height: 36px;
        }}
        
        /* Combo Box */
        QComboBox {{
            padding: 10px 12px;
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
            font-size: {f['size_base']};
            min-height: 20px;
        }}
        
        QComboBox:focus {{
            border: 2px solid {c['border_focus']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
            background-color: {c['bg_primary']};
        }}
        
        QComboBox::down-arrow {{
            width: 12px;
            height: 12px;
        }}
        
        QComboBox QAbstractItemView {{
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
            selection-background-color: {c['primary_light']};
            selection-color: {c['text_white']};
            padding: 4px;
        }}
        
        /* Check Box */
        QCheckBox {{
            color: {c['text_primary']};
            font-size: {f['size_base']};
            spacing: 8px;
            background-color: transparent;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {c['border_dark']};
            border-radius: {r['sm']};
            background-color: {c['bg_primary']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {c['primary']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {c['primary']};
            border-color: {c['primary']};
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
        }}
        
        QCheckBox::indicator:disabled {{
            background-color: {c['bg_tertiary']};
            border-color: {c['border']};
        }}
        
        /* Date/Time Edit */
        QDateEdit, QTimeEdit {{
            padding: 10px 12px;
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
            font-size: {f['size_base']};
        }}
        
        QDateEdit:focus, QTimeEdit:focus {{
            border: 2px solid {c['border_focus']};
        }}
        
        QDateEdit::drop-down, QTimeEdit::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid {c['border']};
            background-color: {c['bg_primary']};
        }}
        
        QDateEdit::down-arrow, QTimeEdit::down-arrow {{
            width: 12px;
            height: 12px;
        }}
        
        QDateEdit QCalendarWidget, QTimeEdit QCalendarWidget {{
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
        }}
        
        QCalendarWidget QWidget {{
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
        }}
        
        QCalendarWidget QAbstractItemView {{
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
            selection-background-color: {c['primary']};
            selection-color: {c['text_white']};
        }}
        
        QCalendarWidget QToolButton {{
            color: {c['text_primary']};
            background-color: {c['bg_primary']};
        }}
        
        QCalendarWidget QMenu {{
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
        }}
        
        QCalendarWidget QSpinBox {{
            background-color: {c['bg_primary']};
            color: {c['text_primary']};
        }}
        
        /* List Widget */
        QListWidget {{
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_secondary']};
            padding: 8px;
        }}
        
        QListWidget::item {{
            padding: 8px;
            border-radius: {r['sm']};
            margin: 6px 0px;
            background-color: transparent;
        }}
        
        QListWidget::item:selected {{
            background-color: transparent;
        }}
        
        QListWidget::item:hover {{
            background-color: transparent;
        }}
        
        /* Scroll Area */
        QScrollArea {{
            background-color: {c['bg_secondary']};
            border: none;
        }}
        
        QScrollArea > QWidget > QWidget {{
            background-color: {c['bg_secondary']};
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            border: none;
            background-color: {c['bg_tertiary']};
            width: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {c['border_dark']};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {c['text_tertiary']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            border: none;
            background-color: {c['bg_tertiary']};
            height: 10px;
            border-radius: 5px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {c['border_dark']};
            border-radius: 5px;
            min-width: 20px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {c['text_tertiary']};
        }}
        
        /* Group Box */
        QGroupBox {{
            border: 1px solid {c['border']};
            border-radius: {r['lg']};
            margin-top: 12px;
            padding: 16px;
            background-color: {c['bg_primary']};
            font-weight: 500;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 8px;
            color: {c['text_primary']};
            font-size: {f['size_lg']};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_primary']};
            top: -1px;
        }}
        
        QTabBar::tab {{
            padding: 10px 20px;
            margin-right: 4px;
            border-top-left-radius: {r['md']};
            border-top-right-radius: {r['md']};
            background-color: {c['bg_tertiary']};
            color: {c['text_secondary']};
        }}
        
        QTabBar::tab:selected {{
            background-color: {c['bg_primary']};
            color: {c['primary']};
            border-bottom: 2px solid {c['primary']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {c['bg_secondary']};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_tertiary']};
            text-align: center;
            height: 20px;
        }}
        
        QProgressBar::chunk {{
            background-color: {c['primary']};
            border-radius: {r['sm']};
        }}
        
        /* Spin Box */
        QSpinBox, QDoubleSpinBox {{
            padding: 10px 12px;
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            background-color: {c['bg_primary']};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {c['bg_primary']};
            border-bottom: 1px solid {c['border']};
            padding: 4px;
        }}
        
        QMenuBar::item {{
            padding: 8px 12px;
            border-radius: {r['sm']};
        }}
        
        QMenuBar::item:selected {{
            background-color: {c['bg_tertiary']};
        }}
        
        /* Menu */
        QMenu {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
            border-radius: {r['md']};
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 24px;
            border-radius: {r['sm']};
        }}
        
        QMenu::item:selected {{
            background-color: {c['primary_light']};
            color: {c['text_white']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {c['bg_primary']};
            border-top: 1px solid {c['border']};
            padding: 4px;
        }}
        
        /* Tool Tip */
        QToolTip {{
            border: 1px solid {c['border']};
            border-radius: {r['sm']};
            background-color: {c['bg_dark']};
            color: {c['text_white']};
            padding: 6px 8px;
            font-size: {f['size_sm']};
        }}
        
        /* Dialog */
        QDialog {{
            background-color: {c['bg_primary']};
        }}
        
        /* Frames */
        QFrame[card="true"] {{
            background-color: {c['bg_primary']};
            border: 1px solid {c['border']};
            border-radius: {r['lg']};
            padding: 16px;
        }}
        
        QFrame[separator="true"] {{
            background-color: {c['border']};
            max-height: 1px;
            border: none;
        }}
        """
    
    @classmethod
    def get_custom_button_style(cls, variant: str = "primary") -> str:
        """Get custom style for specific button variant."""
        c = cls.COLORS
        r = cls.RADIUS
        
        styles = {
            "primary": f"""
                background-color: {c['primary']};
                color: {c['text_white']};
                border: none;
                padding: 10px 20px;
                border-radius: {r['md']};
                font-weight: 500;
            """,
            "secondary": f"""
                background-color: {c['bg_primary']};
                color: {c['text_primary']};
                border: 1px solid {c['border_dark']};
                padding: 10px 20px;
                border-radius: {r['md']};
                font-weight: 500;
            """,
            "danger": f"""
                background-color: {c['danger']};
                color: {c['text_white']};
                border: none;
                padding: 10px 20px;
                border-radius: {r['md']};
                font-weight: 500;
            """,
            "success": f"""
                background-color: {c['accent']};
                color: {c['text_white']};
                border: none;
                padding: 10px 20px;
                border-radius: {r['md']};
                font-weight: 500;
            """,
        }
        
        return styles.get(variant, styles["primary"])