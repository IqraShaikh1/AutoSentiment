import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

class SentimentAnalyzer:
    def __init__(self):
        """Initialize multilingual sentiment model"""
        # Using XLM-RoBERTa for multilingual support
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
        except:
            print("Using simple rule-based classifier")
            self.tokenizer = None
            self.model = None
    
    def predict(self, text):
        """
        Predict sentiment score
        Returns: float between 0-1 (0=negative, 0.5=neutral, 1=positive)
        """
        if self.model is None:
            # Simple rule-based backup
            return self._rule_based_sentiment(text)
        
        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Predict
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.softmax(outputs.logits, dim=1)
            
            # Convert to score
            probs = probabilities.cpu().numpy()[0]
            score = probs[2]  # positive probability
            
            return float(score)
        
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._rule_based_sentiment(text)
    
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
    """Classify sentiment for specific aspects"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def classify_aspect_sentiment(self, text, aspect):
        """Get sentiment for a specific aspect in text"""
        # Check if aspect is mentioned
        if aspect.lower() not in text.lower():
            return None
        
        # Get sentiment for the whole text
        # In production: extract aspect-specific sentences
        sentiment = self.sentiment_analyzer.predict(text)
        return sentiment