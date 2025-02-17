import re
from typing import Dict
from datetime import datetime
import logging

# Initialize with empty dict and make it a proper module-level variable
last_extraction: Dict = {}

class ApplicationService:
    def process_extracted_text(self, text: str) -> Dict:
        try:
            global last_extraction
            logging.info(f"Starting extraction with text length: {len(text)}")
            
            result = {
                "status": "success",
                "display_text": text,  # Simplified: just use the raw text for now
                "metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "length": len(text)
                }
            }
            
            # Update global state and verify
            last_extraction.clear()  # Clear existing data
            last_extraction.update(result)  # Update with new data
            
            logging.info(f"Updated last_extraction. Content: {last_extraction}")
            return result
            
        except Exception as e:
            logging.error(f"Error in process_extracted_text: {str(e)}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize the text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Normalize line endings
        text = re.sub(r'[\r\n]+', '\n', text)
        # Remove special characters
        text = re.sub(r'[^\w\s\n.,!?-]', '', text)
        return text.strip()
    
    def _split_into_sections(self, text: str) -> list:
        """Split text into logical sections"""
        # Split on common section indicators
        potential_sections = re.split(r'\n(?=[A-Z][^a-z]*:|\d+\.)', text)
        return [s.strip() for s in potential_sections if s.strip()]
    
    def _format_for_display(self, sections: list) -> str:
        """Format the text in a more readable way"""
        formatted_sections = []
        
        for i, section in enumerate(sections, 1):
            # Try to identify section headers
            if ':' in section.split('\n')[0]:
                header, content = section.split(':', 1)
                formatted_sections.append(f"§{i}. {header.strip()}\n{content.strip()}\n")
            else:
                formatted_sections.append(f"§{i}. Section\n{section}\n")
        
        return "\n".join(formatted_sections)
    
    def _calculate_metrics(self, text: str) -> Dict:
        """Calculate various text metrics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
            "longest_word": max(words, key=len) if words else "",
            "estimated_read_time": len(words) // 200  # Assuming 200 words per minute
        }

application_service = ApplicationService()
