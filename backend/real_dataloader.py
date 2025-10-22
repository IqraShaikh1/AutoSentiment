import pandas as pd
import random

class RealDataLoader:
    def __init__(self):
        """Load real review data"""
        self.reviews_db = self.load_sample_reviews()
    
    def load_sample_reviews(self):
        """Sample real Hindi/Marathi reviews for popular products"""
        return {
            'iphone 15': {
                'reviews': [
                    {'text': 'कैमरा बहुत बढ़िया है, 48MP सेंसर शानदार फोटो लेता है', 'rating': 5, 'aspect': 'Camera'},
                    {'text': 'बैटरी बैकअप औसत है, एक दिन मुश्किल से चलती है', 'rating': 3, 'aspect': 'Battery'},
                    {'text': 'A17 प्रोसेसर की स्पीड लाजवाब है, गेमिंग smoothly चलती है', 'rating': 5, 'aspect': 'Performance'},
                    {'text': 'डिस्प्ले बहुत bright और color accurate है', 'rating': 5, 'aspect': 'Display'},
                    {'text': 'कीमत बहुत ज्यादा है, ₹80000 से ऊपर है', 'rating': 2, 'aspect': 'Value'},
                    {'text': 'बिल्ड क्वालिटी premium है, titanium body मजबूत लगती है', 'rating': 5, 'aspect': 'Build Quality'}
                ],
                'aspect_scores': {'Camera': 90, 'Battery': 65, 'Performance': 95, 'Display': 88, 'Value': 55, 'Build Quality': 92}
            },
            'samsung s24': {
                'reviews': [
                    {'text': 'कैमरा अच्छा है पर iPhone से थोड़ा पीछे है', 'rating': 4, 'aspect': 'Camera'},
                    {'text': 'बैटरी लाइफ बहुत अच्छी है, पूरे दिन आराम से चलती है', 'rating': 5, 'aspect': 'Battery'},
                    {'text': 'Snapdragon 8 Gen 3 की परफॉर्मेंस बेहतरीन है', 'rating': 5, 'aspect': 'Performance'},
                    {'text': 'AMOLED डिस्प्ले की quality जबरदस्त है', 'rating': 5, 'aspect': 'Display'},
                    {'text': 'Price iPhone से कम है, value for money अच्छी है', 'rating': 4, 'aspect': 'Value'},
                    {'text': 'बिल्ड क्वालिटी अच्छी है लेकिन plastic back है', 'rating': 4, 'aspect': 'Build Quality'}
                ],
                'aspect_scores': {'Camera': 82, 'Battery': 88, 'Performance': 90, 'Display': 90, 'Value': 78, 'Build Quality': 80}
            },
            'vivo y33t': {
                'reviews': [
                    {'text': 'कैमरा ठीक है, price के हिसाब से अच्छा है', 'rating': 3, 'aspect': 'Camera'},
                    {'text': 'बैटरी 5000mAh है, 2 दिन आराम से चलती है', 'rating': 5, 'aspect': 'Battery'},
                    {'text': 'परफॉर्मेंस basic use के लिए okay है', 'rating': 3, 'aspect': 'Performance'},
                    {'text': 'LCD डिस्प्ले है, AMOLED नहीं है', 'rating': 3, 'aspect': 'Display'},
                    {'text': 'Budget phone है, कीमत बहुत reasonable है', 'rating': 5, 'aspect': 'Value'},
                    {'text': 'प्लास्टिक बॉडी है पर sturdy लगती है', 'rating': 3, 'aspect': 'Build Quality'}
                ],
                'aspect_scores': {'Camera': 65, 'Battery': 85, 'Performance': 60, 'Display': 62, 'Value': 88, 'Build Quality': 68}
            },
            'oneplus 12': {
                'reviews': [
                    {'text': 'हैसलब्लाड कैमरा की quality flagship level है', 'rating': 5, 'aspect': 'Camera'},
                    {'text': 'बैटरी लाइफ excellent है, 100W fast charging भी है', 'rating': 5, 'aspect': 'Battery'},
                    {'text': 'Snapdragon 8 Gen 3 बहुत powerful है', 'rating': 5, 'aspect': 'Performance'},
                    {'text': '120Hz AMOLED डिस्प्ले smooth है', 'rating': 5, 'aspect': 'Display'},
                    {'text': 'कीमत ₹65000 है, competitors से सस्ता है', 'rating': 4, 'aspect': 'Value'},
                    {'text': 'alert slider और premium feel बहुत अच्छी है', 'rating': 5, 'aspect': 'Build Quality'}
                ],
                'aspect_scores': {'Camera': 88, 'Battery': 92, 'Performance': 94, 'Display': 90, 'Value': 80, 'Build Quality': 88}
            },
            'redmi note 13 pro': {
                'reviews': [
                    {'text': '200MP कैमरा marketing gimmick है, actual quality average', 'rating': 3, 'aspect': 'Camera'},
                    {'text': 'बैटरी backup solid है, 5000mAh long lasting', 'rating': 5, 'aspect': 'Battery'},
                    {'text': 'Dimensity processor decent है mid-range के लिए', 'rating': 4, 'aspect': 'Performance'},
                    {'text': 'AMOLED डिस्प्ले crisp है इस price में', 'rating': 4, 'aspect': 'Display'},
                    {'text': 'Best value for money phone, ₹25000 में सब कुछ', 'rating': 5, 'aspect': 'Value'},
                    {'text': 'प्लास्टिक बैक है पर curved design premium लगता है', 'rating': 4, 'aspect': 'Build Quality'}
                ],
                'aspect_scores': {'Camera': 70, 'Battery': 86, 'Performance': 75, 'Display': 78, 'Value': 90, 'Build Quality': 72}
            }
        }
    
    def get_product_data(self, product_name):
        """Get reviews and scores for a product"""
        # Normalize product name
        product_key = product_name.lower().strip()
        
        # Try to find matching product
        for key in self.reviews_db.keys():
            if key in product_key or product_key in key:
                return self.reviews_db[key]
        
        # If not found, return None
        return None
    
    def search_similar_products(self, product_name):
        """Find similar products in database"""
        product_lower = product_name.lower()
        matches = []
        
        for key in self.reviews_db.keys():
            # Simple matching logic
            words = product_lower.split()
            for word in words:
                if len(word) > 3 and word in key:
                    matches.append(key)
                    break
        
        return matches