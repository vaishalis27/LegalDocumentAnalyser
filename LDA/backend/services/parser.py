import fitz  # PyMuPDF
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        logger.info("Opening PDF document")
        doc = fitz.open(stream=BytesIO(file_bytes), filetype="pdf")
        logger.info(f"PDF opened successfully. Number of pages: {len(doc)}")
        
        text = ""
        for page_num, page in enumerate(doc, 1):
            try:
                logger.info(f"Processing page {page_num}")
                page_text = page.get_text()
                text += page_text
                logger.info(f"Page {page_num} processed. Text length: {len(page_text)}")
            except Exception as e:
                logger.error(f"Error processing page {page_num}: {str(e)}")
                continue
        
        doc.close()
        logger.info(f"Total extracted text length: {len(text)}")
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error in PDF processing: {str(e)}")
        raise Exception(f"Failed to process PDF: {str(e)}")
