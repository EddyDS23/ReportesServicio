"""
PDF Generator for Daily Report System
Generates professional PDF reports with image grid layout
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, Image as RLImage, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from PIL import Image as PILImage
from typing import Tuple, List, Optional
from datetime import datetime
import os
import tempfile
from models.report_model import Report
from models.activity_model import Activity


class CompressionLevel:
    """Compression levels for images in PDF."""
    LOW = "low"      # High quality, larger file
    MEDIUM = "medium"  # Balanced
    HIGH = "high"    # Lower quality, smaller file


class PDFGenerator:
    """
    Generates professional PDF reports from Report objects.
    
    Features:
    - Professional layout with headers and footers
    - Image compression (low, medium, high)
    - 3x3 image grid layout
    - Automatic page breaks
    - Signature fields
    """
    
    # Image settings by compression level
    COMPRESSION_SETTINGS = {
        CompressionLevel.LOW: {
            'max_width': 800,
            'max_height': 600,
            'quality': 95,
            'dpi': 150
        },
        CompressionLevel.MEDIUM: {
            'max_width': 600,
            'max_height': 450,
            'quality': 85,
            'dpi': 100
        },
        CompressionLevel.HIGH: {
            'max_width': 400,
            'max_height': 300,
            'quality': 75,
            'dpi': 72
        }
    }
    
    def __init__(self, report: Report, compression_level: str = CompressionLevel.MEDIUM, include_signatures: bool = False):
        """
        Initialize PDF generator.
        
        Args:
            report: Report object to generate PDF from
            compression_level: "low", "medium", or "high"
            include_signatures: Whether to include signature fields
        """
        self.report = report
        self.compression_level = compression_level
        self.compression_settings = self.COMPRESSION_SETTINGS[compression_level]
        self.include_signatures = include_signatures
        self.temp_images = []  # Track temporary compressed images
        
        # Page setup
        self.pagesize = letter
        self.width, self.height = self.pagesize
        self.margin = 0.75 * inch
        
        # Styles
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2563EB'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Activity title
        self.styles.add(ParagraphStyle(
            name='ActivityTitle',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#111827'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            spaceAfter=8,
            fontName='Helvetica'
        ))
        
        # Caption
        self.styles.add(ParagraphStyle(
            name='Caption',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=4,
            fontName='Helvetica'
        ))
    
    def _add_header_footer(self, canvas_obj, doc):
        """Add header and footer to each page."""
        canvas_obj.saveState()
        
        # Header
        canvas_obj.setFont('Helvetica-Bold', 10)
        canvas_obj.setFillColor(colors.HexColor('#6B7280'))
        canvas_obj.drawString(
            self.margin,
            self.height - 0.5 * inch,
            "Daily Activity Report"
        )
        
        # Page number
        canvas_obj.setFont('Helvetica', 9)
        page_num = f"Page {doc.page}"
        canvas_obj.drawRightString(
            self.width - self.margin,
            self.margin / 2,
            page_num
        )
        
        # Footer line
        canvas_obj.setStrokeColor(colors.HexColor('#E5E7EB'))
        canvas_obj.setLineWidth(0.5)
        canvas_obj.line(
            self.margin,
            self.margin,
            self.width - self.margin,
            self.margin
        )
        
        canvas_obj.restoreState()
    
    def _compress_image(self, image_path: str) -> str:
        """
        Compress and resize image according to compression level.
        
        Args:
            image_path: Path to original image
            
        Returns:
            str: Path to compressed temporary image
        """
        try:
            # Open image
            img = PILImage.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                background = PILImage.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img)
                img = background
            
            # Resize maintaining aspect ratio
            max_w = self.compression_settings['max_width']
            max_h = self.compression_settings['max_height']
            
            img.thumbnail((max_w, max_h), PILImage.Resampling.LANCZOS)
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.jpg'
            )
            
            img.save(
                temp_file.name,
                'JPEG',
                quality=self.compression_settings['quality'],
                optimize=True
            )
            
            temp_file.close()
            self.temp_images.append(temp_file.name)
            
            return temp_file.name
            
        except Exception as e:
            print(f"Error compressing image {image_path}: {e}")
            return image_path  # Return original if compression fails
    
    def _create_image_grid(self, images: List[str], max_width: float) -> List:
        """
        Create a 3-column grid of images.
        
        Args:
            images: List of image paths
            max_width: Maximum width available for the grid
            
        Returns:
            List of Table objects for the image grid
        """
        if not images:
            return []
        
        elements = []
        
        # Compress images
        compressed_images = [self._compress_image(img) for img in images]
        
        # Calculate image size for 3-column grid
        # Account for spacing between images
        spacing = 0.1 * inch
        available_width = max_width - (2 * spacing)  # Space for 2 gaps
        img_width = available_width / 3
        img_height = img_width * 0.75  # 4:3 aspect ratio
        
        # Create rows of 3 images
        rows = []
        for i in range(0, len(compressed_images), 3):
            row_images = compressed_images[i:i+3]
            row = []
            
            for img_path in row_images:
                try:
                    # Create Image object
                    img = RLImage(img_path, width=img_width, height=img_height)
                    row.append(img)
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")
                    # Add placeholder
                    row.append(Paragraph(
                        f"<i>Image error</i>",
                        self.styles['Caption']
                    ))
            
            # Pad row if less than 3 images
            while len(row) < 3:
                row.append("")
            
            rows.append(row)
        
        # Create table
        if rows:
            table = Table(rows, colWidths=[img_width] * 3)
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), spacing / 2),
                ('RIGHTPADDING', (0, 0), (-1, -1), spacing / 2),
                ('TOPPADDING', (0, 0), (-1, -1), spacing / 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), spacing / 2),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_general_info_table(self) -> Table:
        """Create the general information table."""
        data = [
            ['Responsible:', self.report.responsible],
            ['Student:', self.report.student],
            ['Date:', self.report.date.strftime('%B %d, %Y')],
            ['Entry Time:', self.report.entry_time],
            ['Exit Time:', self.report.exit_time],
            ['Instance Hours:', self.report.instance_hours],
        ]
        
        table = Table(data, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#374151')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#111827')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
        ]))
        
        return table
    
    def _create_activity_section(self, activity: Activity, activity_num: int) -> List:
        """
        Create PDF elements for a single activity.
        
        Args:
            activity: Activity object
            activity_num: Activity number (for display)
            
        Returns:
            List of PDF elements
        """
        elements = []
        
        # Activity header box
        activity_title = Paragraph(
            f"<b>Activity {activity_num}: {activity.title}</b>",
            self.styles['ActivityTitle']
        )
        elements.append(activity_title)
        
        # Activity details table
        details_data = [
            ['Time:', f"{activity.start_time} - {activity.end_time}"],
            ['Duration:', activity.duration],
        ]
        
        details_table = Table(details_data, colWidths=[1.2 * inch, 2.5 * inch])
        details_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
            ('PADDING', (0, 0), (-1, -1), 4),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        elements.append(details_table)
        elements.append(Spacer(1, 0.1 * inch))
        
        # Description
        desc_title = Paragraph("<b>Description:</b>", self.styles['CustomBody'])
        elements.append(desc_title)
        
        description = Paragraph(activity.description, self.styles['CustomBody'])
        elements.append(description)
        elements.append(Spacer(1, 0.15 * inch))
        
        # Images (if any)
        if activity.images:
            img_title = Paragraph(
                f"<b>Images ({len(activity.images)}):</b>",
                self.styles['CustomBody']
            )
            elements.append(img_title)
            elements.append(Spacer(1, 0.1 * inch))
            
            # Create image grid
            available_width = self.width - (2 * self.margin)
            image_grid = self._create_image_grid(activity.images, available_width)
            elements.extend(image_grid)
        
        # Separator
        elements.append(Spacer(1, 0.1 * inch))
        
        # Activity box border
        return [KeepTogether(elements)]
    
    def _create_signature_section(self) -> List:
        """Create signature fields."""
        elements = []
        
        elements.append(Spacer(1, 0.5 * inch))
        
        # Signature table
        sig_data = [
            ['_' * 30, '_' * 30],
            ['Responsible Signature', 'Student Signature'],
            ['Date: _______________', 'Date: _______________'],
        ]
        
        sig_table = Table(sig_data, colWidths=[3 * inch, 3 * inch])
        sig_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
            ('TOPPADDING', (0, 0), (-1, 0), 20),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 5),
        ]))
        
        elements.append(sig_table)
        
        return elements
    
    def generate(self, output_path: str) -> Tuple[bool, str]:
        """
        Generate the PDF report.
        
        Args:
            output_path: Path where to save the PDF
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Validate report
            valid, message = self.report.complete_validate()
            if not valid:
                return False, f"Invalid report: {message}"
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=self.pagesize,
                leftMargin=self.margin,
                rightMargin=self.margin,
                topMargin=self.margin + 0.3 * inch,
                bottomMargin=self.margin + 0.3 * inch
            )
            
            # Build content
            story = []
            
            # Title
            title = Paragraph(
                "Daily Activity Report",
                self.styles['CustomTitle']
            )
            story.append(title)
            
            # Subtitle with generation date
            subtitle = Paragraph(
                f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
                self.styles['CustomSubtitle']
            )
            story.append(subtitle)
            story.append(Spacer(1, 0.3 * inch))
            
            # General Information section
            section_header = Paragraph(
                "General Information",
                self.styles['SectionHeader']
            )
            story.append(section_header)
            story.append(self._create_general_info_table())
            story.append(Spacer(1, 0.4 * inch))
            
            # Activities section
            activities_header = Paragraph(
                f"Activities ({self.report.get_activity_count()})",
                self.styles['SectionHeader']
            )
            story.append(activities_header)
            story.append(Spacer(1, 0.2 * inch))
            
            # Add each activity
            for i in range(self.report.get_activity_count()):
                activity = self.report.get_activity(i)
                if activity:
                    activity_elements = self._create_activity_section(activity, i + 1)
                    story.extend(activity_elements)
                    
                    # Add spacer between activities
                    if i < self.report.get_activity_count() - 1:
                        story.append(Spacer(1, 0.3 * inch))
            
            # Summary section
            story.append(Spacer(1, 0.3 * inch))
            summary_header = Paragraph(
                "Summary",
                self.styles['SectionHeader']
            )
            story.append(summary_header)
            
            stats = self.report.get_statistics()
            summary_data = [
                ['Total Activities:', str(stats['total_activities'])],
                ['Total Activity Time:', stats['total_activity_hours']],
                ['Total Images:', str(stats['total_images'])],
            ]
            
            summary_table = Table(summary_data, colWidths=[2 * inch, 2 * inch])
            summary_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))
            story.append(summary_table)
            
            # Signature section (optional)
            if self.include_signatures:
                signature_elements = self._create_signature_section()
                story.extend(signature_elements)
            
            # Build PDF
            doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
            
            # Cleanup temporary images
            self._cleanup_temp_images()
            
            return True, f"PDF generated successfully: {output_path}"
            
        except Exception as e:
            self._cleanup_temp_images()
            return False, f"Error generating PDF: {str(e)}"
    
    def _cleanup_temp_images(self):
        """Clean up temporary compressed images."""
        for temp_file in self.temp_images:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        self.temp_images.clear()


# Convenience function
def generate_pdf(
    report: Report,
    output_path: str,
    compression_level: str = CompressionLevel.MEDIUM,
    include_signatures: bool = False
) -> Tuple[bool, str]:
    """
    Generate a PDF report.
    
    Args:
        report: Report object
        output_path: Where to save the PDF
        compression_level: "low", "medium", or "high"
        include_signatures: Whether to include signature fields
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    generator = PDFGenerator(report, compression_level, include_signatures)
    return generator.generate(output_path)