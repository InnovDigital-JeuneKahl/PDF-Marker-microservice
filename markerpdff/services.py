from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.config.parser import ConfigParser
import re
import os
from typing import List, Dict, Optional

def init_marker():
    raw_config = {
        "output_format": "markdown",
    }
    config_parser = ConfigParser(raw_config)
    return PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
    )

converter = init_marker()

def process_pdf(file_path: str):
    rendered = converter(file_path)
    text, _, images = text_from_rendered(rendered)
    
    saved_images = []
    if images:
        os.makedirs('./output', exist_ok=True)
        for path, image in images.items():
            image.save(f'./output/{path}', image.format)
            saved_images.append(path)
    
    return text, saved_images

def find_all_sentence_contexts(
    full_text: str,
    search_terms: List[str],
    language: str = 'fr'
) -> Dict[str, List[Dict[str, Optional[str]]]]:
    sentence_endings = r'(?<!\w\.\w.)(?<![A-ZÀ-Ü][a-zà-ü]\.)(?<=\.|\?|\!|\…|\n)\s+'
    sentences = [s.strip() for s in re.split(sentence_endings, full_text) if s.strip()]
    
    patterns = {
        term: re.compile(rf'(?<!\w){re.escape(term)}(?!\w)', re.IGNORECASE)
        for term in search_terms
    }
    
    results = {term: [] for term in search_terms}
    
    for idx, sentence in enumerate(sentences):
        for term, pattern in patterns.items():
            if pattern.search(sentence):
                context = {
                    'prev': sentences[idx-1] if idx > 0 else None,
                    'match': sentence,
                    'next': sentences[idx+1] if idx < len(sentences)-1 else None
                }
                results[term].append(context)
    
    return results