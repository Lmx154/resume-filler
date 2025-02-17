from typing import Dict
import re

class ParserService:
    def parse_resume(self, content: str) -> Dict:
        """Parse resume content into a structured format"""
        # Clean the text
        cleaned_content = self._clean_text(content)
        
        # Extract sections
        sections = self._identify_sections(cleaned_content)
        
        # Format for prompt
        structured_data = {
            "parsed_sections": sections,
            "summary": self._create_summary(sections),
            "metadata": self._extract_metadata(cleaned_content)
        }
        
        return structured_data
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Normalize line endings
        text = re.sub(r'[\r\n]+', '\n', text)
        return text.strip()
    
    def _identify_sections(self, text: str) -> Dict:
        """Identify common resume sections"""
        common_headers = [
            "experience", "education", "skills", "projects",
            "summary", "objective", "certifications"
        ]
        
        sections = {}
        current_section = "other"
        current_content = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a header
            line_lower = line.lower()
            found_header = False
            
            for header in common_headers:
                if header in line_lower and len(line) < 50:  # Assume headers are short
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = header
                    current_content = []
                    found_header = True
                    break
            
            if not found_header:
                current_content.append(line)
        
        # Add final section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _create_summary(self, sections: Dict) -> str:
        """Create a brief summary of the resume"""
        summary_parts = []
        
        if "summary" in sections:
            summary_parts.append(sections["summary"])
        
        if "experience" in sections:
            # Get first 2 sentences of experience
            exp_sentences = re.split(r'[.!?]+', sections["experience"])
            summary_parts.append(' '.join(exp_sentences[:2]))
        
        if "skills" in sections:
            summary_parts.append(f"Key skills include: {sections['skills']}")
        
        return ' '.join(summary_parts)
    
    def _extract_metadata(self, text: str) -> Dict:
        """Extract metadata from the resume"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "estimated_read_time": len(words) // 200  # Assuming 200 words per minute
        }

parser_service = ParserService()
