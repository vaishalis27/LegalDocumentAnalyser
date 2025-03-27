import os
import requests
from dotenv import load_dotenv
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
HF_API_KEY = os.getenv("HF_API_KEY")

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def summarize_text_with_hf(text: str) -> str:
    try:
        if not HF_API_KEY:
            logger.error("Hugging Face API key not found")
            raise Exception("Hugging Face API key not configured")

        if not text or not text.strip():
            logger.error("Empty text provided for summarization")
            raise Exception("Empty text cannot be summarized")

        # Trim text if too long
        if len(text) > 1000:
            logger.info(f"Trimming text from {len(text)} to 1000 characters")
            text = text[:1000]

        logger.info("Preparing API request")
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": 300,
                "min_length": 50,
                "do_sample": False
            }
        }

        logger.info("Sending request to Hugging Face API")
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            try:
                summary = response.json()[0]['summary_text']
                logger.info(f"Successfully generated summary of length: {len(summary)}")
                return summary
            except (KeyError, IndexError) as e:
                logger.error(f"Error parsing API response: {str(e)}")
                raise Exception("Invalid response format from API")
        else:
            error_msg = f"API request failed with status code {response.status_code}"
            logger.error(error_msg)
            if response.text:
                logger.error(f"API error details: {response.text}")
            raise Exception(error_msg)

    except requests.exceptions.Timeout:
        logger.error("API request timed out")
        raise Exception("Request timed out while generating summary")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise Exception(f"Failed to connect to API: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in summarization: {str(e)}")
        raise Exception(f"Error generating summary: {str(e)}")
