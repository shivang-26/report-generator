from typing import Dict, Any
from docx import Document
import os

class DocumentFormatter:
    """Handles formatting documents according to different style guides"""
    
    @staticmethod
    def format_ieee(doc: Document) -> Document:
        """Format document according to IEEE guidelines"""
        # Set margins to 1 inch (72 points = 1 inch)
        sections = doc.sections
        for section in sections:
            section.top_margin = 914400  # 1 inch in twips (1/1440 of an inch)
            section.bottom_margin = 914400
            section.left_margin = 914400
            section.right_margin = 914400
            
            # Set header/footer distance
            section.header_distance = 457200  # 0.5 inch
            section.footer_distance = 457200
        
        # Set font for the entire document
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Times New Roman'
        font.size = 12
        
        # Set paragraph formatting
        for paragraph in doc.paragraphs:
            paragraph_format = paragraph.paragraph_format
            paragraph_format.line_spacing = 2.0  # Double spacing
            paragraph_format.space_after = 0
            paragraph_format.space_before = 0
        
        return doc
    
    @staticmethod
    def format_springer(doc: Document) -> Document:
        """Format document according to Springer guidelines"""
        # Set margins
        sections = doc.sections
        for section in sections:
            section.top_margin = 1000000    # ~1.4 inches
            section.bottom_margin = 1000000
            section.left_margin = 1000000
            section.right_margin = 1000000
            
            # Set header/footer distance
            section.header_distance = 500000
            section.footer_distance = 500000
        
        # Set font for the entire document
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Arial'
        font.size = 10
        
        # Set paragraph formatting
        for paragraph in doc.paragraphs:
            paragraph_format = paragraph.paragraph_format
            paragraph_format.line_spacing = 1.5
            paragraph_format.space_after = 0
            paragraph_format.space_before = 0
        
        return doc

def apply_formatting(doc: Document, format_style: str = 'ieee') -> Document:
    """
    Apply formatting to a document based on the specified style
    
    Args:
        doc: The document to format
        format_style: The style to apply ('ieee' or 'springer')
        
    Returns:
        The formatted document
    """
    formatter = DocumentFormatter()
    
    if format_style.lower() == 'ieee':
        return formatter.format_ieee(doc)
    elif format_style.lower() == 'springer':
        return formatter.format_springer(doc)
    else:
        # Default to IEEE if unknown format
        return formatter.format_ieee(doc)
