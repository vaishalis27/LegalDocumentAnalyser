from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from transformers.pipelines import AggregationStrategy
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Load Legal-BERT
    tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
    ner_pipeline = pipeline(
        "ner", 
        model=model, 
        tokenizer=tokenizer, 
        aggregation_strategy=AggregationStrategy.SIMPLE
    )
except Exception as e:
    logger.error(f"Error loading models: {str(e)}")
    raise

def extract_legal_entities(text: str):
    try:
        # Truncate long text for performance
        text = text[:1000]

        results = ner_pipeline(text)
        entities = []

        for r in results:
            entities.append({
                "entity": r['entity_group'],
                "word": r['word'],
                "score": round(r['score'], 2)
            })

        return entities
    except Exception as e:
        logger.error(f"Error extracting entities: {str(e)}")
        return []
