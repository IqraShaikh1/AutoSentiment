import re
import string

class TextPreprocessor:
    def __init__(self):
        self.hindi_punctuation = '।॥॰'
        self.english_punctuation = string.punctuation
        
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Remove excessive punctuation (3 or more consecutive)
        text = re.sub(r'([!?।॥.]){3,}', r'\1\1', text)
        
        return text
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for better matching"""
        # Convert to lowercase (only for English characters)
        # Keep Hindi/Marathi as is
        text = text.lower()
        
        # Normalize common variations
        text = text.replace('।', '.')
        text = text.replace('॥', '.')
        
        return text
    
    def remove_emojis(self, text: str) -> str:
        """Remove emojis from text"""
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)
    
    def extract_sentences(self, text: str) -> list:
        """Split text into sentences"""
        # Split on common sentence delimiters
        sentences = re.split(r'[।॥.!?]+', text)
        
        # Clean and filter sentences
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences


if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    
    test_text = "कैमरा बहुत बढ़िया है!!! फोटो क्वालिटी शानदार। बैटरी बैकअप थोड़ा कम है।।।"
    
    print("Original:", test_text)
    print("Cleaned:", preprocessor.clean_text(test_text))
    print("Sentences:", preprocessor.extract_sentences(test_text))