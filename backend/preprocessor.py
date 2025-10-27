import re
import string

class TextPreprocessor:
    def __init__(self):
        self.hindi_stopwords = [
            'का', 'के', 'की', 'है', 'हैं', 'था', 'थी', 'थे', 'हो',
            'और', 'या', 'में', 'से', 'को', 'पर', 'यह', 'वह'
        ]
        
        self.marathi_stopwords = [
            'आहे', 'आहेत', 'होते', 'होता', 'आणि', 'किंवा', 'मध्ये',
            'पासून', 'साठी', 'वर', 'हे', 'ते'
        ]
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove emojis (optional)
        text = re.sub(r'[^\w\s\u0900-\u097F]', '', text)
        
        return text.strip()
    
    def remove_stopwords(self, text, language='hindi'):
        """Remove stopwords"""
        stopwords = self.hindi_stopwords if language == 'hindi' else self.marathi_stopwords
        words = text.split()
        filtered = [word for word in words if word not in stopwords]
        return ' '.join(filtered)
    
    def normalize_text(self, text):
        """Normalize unicode and variations"""
        # Normalize variations of similar characters
        replacements = {
            'क़': 'क', 'ख़': 'ख', 'ग़': 'ग',
            'ज़': 'ज', 'फ़': 'फ'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text