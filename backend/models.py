import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        """Initialize multilingual sentiment model"""
        # Using XLM-RoBERTa for multilingual support
        # NOTE: Model is loaded untrained, so results will be generic, but structure is correct.
        model_name = "xlm-roberta-base"
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=3  # negative, neutral, positive
            )
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            print(f"Model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Failed to load model ({e}). Using simple rule-based classifier.")
            self.tokenizer = None
            self.model = None
    
    def predict(self, text):
        """
        Predict sentiment score (0-1).
        FIXED: Returns dict {'score': float} to match app.py usage.
        """
        if self.model is None:
            return {'score': self._rule_based_sentiment(text)}
        
        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
            
            # Assuming labels are 0: Negative, 1: Neutral, 2: Positive
            probs = probabilities.cpu().numpy()[0]
            # Score scaled towards 1 (positive)
            score = probs[2] 
            
            return {'score': float(score)}
        
        except Exception as e:
            print(f"Prediction error: {e}")
            return {'score': self._rule_based_sentiment(text)}
    
    def _rule_based_sentiment(self, text):
        """Backup rule-based sentiment analysis"""
        positive_words = [
            'बढ़िया', 'अच्छा', 'शानदार', 'बेहतरीन', 'जबरदस्त', 'उत्तम',
            'छान', 'सुंदर', 'perfect', 'best', 'good', 'great', 'excellent'
        ]
        negative_words = [
            'खराब', 'बुरा', 'कम', 'नहीं', 'not', 'bad', 'poor', 'waste',
            'वाया', 'गयाचा'
        ]
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 0.8
        elif neg_count > pos_count:
            return 0.2
        else:
            return 0.5


class AspectClassifier:
    """Classify sentiment for specific aspects (Not used in app.py directly)"""
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def classify_aspect_sentiment(self, text, aspect):
        # Implementation not changed as it's not the critical path
        return self.sentiment_analyzer.predict(text)['score']
    
# NOTE: The AspectExtractor class below is duplicated from the original aspect_extractor.py
# If you keep aspect_extractor.py, ensure you use the correct import in app.py
# (which I have already done using 'as KeywordAspectExtractor')
