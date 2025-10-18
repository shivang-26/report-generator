from docx2pdf import convert
import os

def convert_docx_to_pdf(docx_path: str, output_path: str = None) -> str:
    """
    Convert a DOCX file to PDF
    
    Args:
        docx_path: Path to the input DOCX file
        output_path: Path to save the output PDF (optional)
        
    Returns:
        str: Path to the generated PDF file
    """
    if not output_path:
        output_path = os.path.splitext(docx_path)[0] + '.pdf'
    
    convert(docx_path, output_path)
    return output_path
