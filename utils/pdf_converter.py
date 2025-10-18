from docx2pdf import convert
import os

import tempfile

def convert_docx_to_pdf(docx_path: str, output_path: str = None) -> str:
    """
    Convert a DOCX file to PDF
    
    Args:
        docx_path: Path to the input DOCX file
        output_path: Path to save the output PDF (optional). If not provided,
                   a temporary file in the system's temp directory will be used.
        
    Returns:
        str: Path to the generated PDF file
    """
    if not output_path:
        # Generate a temporary file in the system's temp directory
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            output_path = temp_file.name
    
    try:
        convert(docx_path, output_path)
        return output_path
    except Exception as e:
        # Clean up the temporary file if there was an error
        if os.path.exists(output_path):
            try:
                os.unlink(output_path)
            except:
                pass
        raise RuntimeError(f"Failed to convert DOCX to PDF: {str(e)}")
