import json
import re

class AspectExtractor:
    def __init__(self):
        """Initialize aspect keywords"""
        # Merging and refining keywords for clarity
        self.aspect_keywords = {
            'Camera': [
                'कैमरा', 'camera', 'फोटो', 'picture', 'कॅमेरा', 'चित्र', 'selfie', 'video'
            ],
            'Battery': [
                'बैटरी', 'battery', 'बैकअप', 'charging', 'charge', 'power', 'बॅटरी'
            ],
            'Performance': [
                'परफॉर्मेंस', 'performance', 'स्पीड', 'speed', 'fast',
                'slow', 'lag', 'gaming', 'processor', 'ram', 'परफॉर्मन्स'
            ],
            'Display': [
                'डिस्प्ले', 'display', 'स्क्रीन', 'screen', 'brightness', 'color', 'clarity', 'डिस्पले'
            ],
            'Value': [
                'कीमत', 'price', 'दाम', 'पैसा', 'value', 'money', 'worth',
                'महाग', 'किंमत', 'costly', 'cheap'
            ],
            'Build Quality': [
                'बिल्ड', 'build', 'quality', 'design', 'डिज़ाइन', 'look',
                'body', 'material', 'finish', 'गुणवत्ता', 'क्वालिटी'
            ],
            'Sound': [
                'साउंड', 'audio', 'आवाज', 'स्पीकर', 'speaker', 'sound'
            ]
        }
    
    def extract_aspects(self, text):
        """Extract mentioned aspects from text"""
        text_lower = text.lower()
        found_aspects = []
        
        for aspect, keywords in self.aspect_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    if aspect not in found_aspects:
                        found_aspects.append(aspect)
                    break
        
        # Add 'overall' if no specific aspect is found
        return found_aspects if found_aspects else ["overall"]
    
    def get_aspect_sentences(self, text, aspect):
        """Extract sentences mentioning specific aspect"""
        sentences = re.split(r'[।.!?]', text)
        aspect_sentences = []
        
        keywords = self.aspect_keywords.get(aspect, [])
        
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                aspect_sentences.append(sentence)
        
        return aspect_sentences
