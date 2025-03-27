from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from services.parser import extract_text_from_pdf
from services.summarizer import summarize_text_with_hf
from services.clause_extractor import extract_legal_entities
import os
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def validate_environment():
    """Validate required environment variables"""
    required_vars = ["HF_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing environment variables: {missing_vars}")
        raise HTTPException(
            status_code=500,
            detail=f"Missing required environment variables: {', '.join(missing_vars)}"
        )

@router.post("/upload-pdf")
async def upload_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    try:
        logger.info(f"Received file upload request: {file.filename}")
        logger.info(f"Content type: {file.content_type}")

        # Validate environment variables
        validate_environment()

        # Validate file type
        if file.content_type != "application/pdf":
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Check file size (max 10MB)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
        contents = await file.read()
        file_size = len(contents)
        logger.info(f"File size: {file_size} bytes")
        
        if file_size > MAX_FILE_SIZE:
            logger.error(f"File too large: {file_size} bytes")
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

        # Extract text from PDF
        try:
            logger.info("Starting PDF text extraction")
            extracted_text = extract_text_from_pdf(contents)
            logger.info(f"Extracted text length: {len(extracted_text)} characters")
            
            if not extracted_text.strip():
                logger.error("PDF appears to be empty or unreadable")
                raise HTTPException(status_code=400, detail="PDF appears to be empty or unreadable")
            
            # Basic text quality check
            word_count = len(extracted_text.split())
            logger.info(f"Word count: {word_count}")
            
            if word_count < 10:  # At least 10 words
                logger.error(f"Insufficient text: {word_count} words")
                raise HTTPException(status_code=400, detail="PDF contains insufficient text for analysis")
                
        except Exception as e:
            logger.error(f"PDF processing error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

        # Generate summary with timeout handling
        try:
            logger.info("Starting summary generation")
            summary = summarize_text_with_hf(extracted_text)
            if not summary or summary.startswith("Error"):
                logger.error("Failed to generate summary")
                raise Exception("Failed to generate summary")
            logger.info("Summary generation completed")
        except Exception as e:
            logger.error(f"Summary generation error: {str(e)}")
            summary = "Error generating summary. Please try again later."

        # Extract entities with timeout handling
        try:
            logger.info("Starting entity extraction")
            entities = extract_legal_entities(extracted_text)
            if not isinstance(entities, list):
                logger.error("Invalid entities format")
                raise Exception("Invalid entities format")
            logger.info(f"Extracted {len(entities)} entities")
        except Exception as e:
            logger.error(f"Entity extraction error: {str(e)}")
            entities = []

        # Clean up resources
        background_tasks.add_task(file.close)

        return {
            "filename": file.filename,
            "summary": summary,
            "entities": entities,
            "raw_text": extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text,
            "text_length": len(extracted_text),
            "word_count": word_count
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    finally:
        # Ensure file is closed even if an error occurs
        try:
            await file.close()
        except:
            pass
