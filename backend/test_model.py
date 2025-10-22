from models import SentimentAnalyzer
from preprocessor import TextPreprocessor

# Initialize
analyzer = SentimentAnalyzer()
preprocessor = TextPreprocessor()

# Test reviews
test_reviews = [
    "कैमरा बहुत बढ़िया है फोटो क्वालिटी शानदार",  # Should be positive (>0.7)
    "बैटरी बैकअप बहुत कम है निराशाजनक",  # Should be negative (<0.4)
    "परफॉर्मेंस ठीक है कुछ खास नहीं",  # Should be neutral (~0.5)
    "कीमत बहुत ज्यादा है लेकिन features अच्छे हैं"  # Should be mixed (~0.5-0.6)
]

print("🧪 Testing Your Trained Model...\n")

for review in test_reviews:
    clean = preprocessor.clean_text(review)
    score = analyzer.predict(clean)
    
    if score > 0.6:
        sentiment = "Positive ✅"
    elif score < 0.4:
        sentiment = "Negative ❌"
    else:
        sentiment = "Neutral ⚖️"
    
    print(f"Review: {review}")
    print(f"Score: {score:.2f} → {sentiment}\n")