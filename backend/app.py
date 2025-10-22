from flask import Flask, request, jsonify
from flask_cors import CORS
from models import SentimentAnalyzer
from aspect_extractor import AspectExtractor
from scraper import ReviewScraper # Assuming scraper.py is now fixed
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
logger.info("🚀 Initializing components...")
# NOTE: AspectExtractor is now defined in models.py and aspect_extractor.py 
# We should import it only from one place (models.py) or rename the class in aspect_extractor.py
# Assuming you will use the updated aspect_extractor.py for AspectExtractor class
from aspect_extractor import AspectExtractor as KeywordAspectExtractor 
sentiment_analyzer = SentimentAnalyzer()
aspect_extractor = KeywordAspectExtractor()
scraper = ReviewScraper()
logger.info("✅ Components initialized")

# Dictionary to store analysis results globally to avoid re-analysis
# In a production environment, this would be managed by a database/cache.
ANALYSIS_CACHE = {} 

@app.route('/api/compare', methods=['POST'])
def compare_products():
    try:
        data = request.get_json()
        products = data.get('products', [])
        logger.info(f"📊 Comparing products: {products}")
        
        results = {
            'products': products,
            'comparison': {
                'overall': [],
                'aspects': [],
                'radarData': [],
                'reviews': {},
                'strengths': {},
                'weaknesses': {},
                'reviewsFound': {},
                'analysisData': {} # Store full analysis data here
            }
        }
        
        # Analyze each product
        all_aspects = set()
        
        for product in products:
            logger.info(f"🔍 Analyzing: {product}")
            
            # Get live reviews
            reviews_data = scraper.get_reviews(product)
            
            if not reviews_data['found']:
                logger.warning(f"⚠️ No reviews found for {product}")
                results['comparison']['reviewsFound'][product] = False
                
                # Add placeholder data
                results['comparison']['overall'].append({
                    'name': product,
                    'score': 0,
                    'sentiment': 'unknown'
                })
                
                results['comparison']['reviews'][product] = []
                results['comparison']['strengths'][product] = []
                results['comparison']['weaknesses'][product] = []
                
                continue
            
            results['comparison']['reviewsFound'][product] = True
            
            # Analyze product with real reviews
            analysis = analyze_product(
                product, 
                reviews_data,
                sentiment_analyzer,
                aspect_extractor
            )
            
            # Store analysis for later use in comparison
            results['comparison']['analysisData'][product] = analysis

            results['comparison']['overall'].append({
                'name': product,
                'score': analysis['overall_score'],
                'sentiment': analysis['overall_sentiment']
            })
            
            results['comparison']['reviews'][product] = analysis['sample_reviews']
            results['comparison']['strengths'][product] = analysis['strengths']
            results['comparison']['weaknesses'][product] = analysis['weaknesses']
            
            # Collect all aspects
            all_aspects.update(analysis['aspect_scores'].keys())
        
        # Build aspect comparison from stored analysis data (FIXED: no re-scraping)
        all_aspects_list = list(all_aspects) if all_aspects else ['Overall']
        
        results['comparison']['aspects'] = build_aspect_comparison(
            products, 
            all_aspects_list,
            results['comparison']['analysisData']
        )
        
        results['comparison']['radarData'] = results['comparison']['aspects']
        
        # Determine winner (only from products with reviews)
        valid_products = [p for p in results['comparison']['overall'] if p['score'] > 0]
        
        if valid_products:
            results['comparison']['winner'] = max(
                valid_products,
                key=lambda x: x['score']
            )['name']
        else:
            results['comparison']['winner'] = "No reviews found"
        
        logger.info(f"✅ Analysis complete. Winner: {results['comparison']['winner']}")
        
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


def analyze_product(product_name, reviews_data, sentiment_analyzer, aspect_extractor):
    """Analyze all reviews for a product with real sentiment analysis"""
    
    all_reviews = reviews_data['hindi'] + reviews_data['marathi']
    
    if not all_reviews:
        return {
            'overall_score': 0,
            'overall_sentiment': 'unknown',
            'aspect_scores': {},
            'sample_reviews': [],
            'strengths': [],
            'weaknesses': []
        }
    
    # Sentiment analysis
    sentiments = []
    aspect_sentiments = {}
    
    for review in all_reviews:
        review_text = review['text']
        
        # Get sentiment using trained model
        # FIXED: Accessing 'score' from the dict returned by predict
        sentiment_result = sentiment_analyzer.predict(review_text)
        sentiment_score = sentiment_result['score'] 
        sentiments.append(sentiment_score)
        
        # Extract aspects
        aspects = aspect_extractor.extract_aspects(review_text)
        
        for aspect in aspects:
            if aspect not in aspect_sentiments:
                aspect_sentiments[aspect] = []
            aspect_sentiments[aspect].append(sentiment_score)
    
    # Calculate overall score
    overall_score = (sum(sentiments) / len(sentiments)) * 10
    
    # Calculate aspect scores
    aspect_scores = {}
    for aspect, scores in aspect_sentiments.items():
        if scores:
            # Scale score (0-1) to percentage (0-100)
            avg_score = sum(scores) / len(scores)
            aspect_scores[aspect] = int(avg_score * 100) 
        else:
            aspect_scores[aspect] = 50 
    
    # Identify strengths and weaknesses
    # Remove 'overall' from aspect analysis for strengths/weaknesses
    aspects_to_rank = {k: v for k, v in aspect_scores.items() if k != 'overall'}
    sorted_aspects = sorted(aspects_to_rank.items(), key=lambda x: x[1], reverse=True)
    
    strengths = [asp[0] for asp in sorted_aspects[:3] if asp[1] > 65]
    weaknesses = [asp[0] for asp in sorted_aspects[-3:] if asp[1] < 55]
    
    # Prepare sample reviews (top 5 reviews with different aspects)
    sample_reviews = []
    seen_aspects = set()
    
    # Logic to select diverse sample reviews (kept mostly as original logic)
    for review in all_reviews[:15]: 
        aspects = aspect_extractor.extract_aspects(review['text'])
        
        for aspect in aspects:
            if aspect not in seen_aspects and len(sample_reviews) < 5:
                sample_reviews.append({
                    'text': review['text'],
                    'rating': review['rating'],
                    'aspect': aspect,
                    'language': review.get('language', 'regional') # Use .get for robustness
                })
                seen_aspects.add(aspect)
                break
        
        if len(sample_reviews) >= 5:
            break
    
    # Fill remaining samples with general reviews if needed
    if len(sample_reviews) < 5:
        for review in all_reviews[:5]:
            if len(sample_reviews) >= 5: break
            if not any(sr['text'] == review['text'] for sr in sample_reviews):
                aspects = aspect_extractor.extract_aspects(review['text'])
                sample_reviews.append({
                    'text': review['text'],
                    'rating': review['rating'],
                    'aspect': aspects[0] if aspects else 'overall',
                    'language': review.get('language', 'regional')
                })
    
    return {
        'overall_score': round(overall_score, 1),
        'overall_sentiment': 'positive' if overall_score > 6 else 'neutral' if overall_score > 4 else 'negative',
        'aspect_scores': aspect_scores,
        'sample_reviews': sample_reviews,
        'strengths': strengths if strengths else ['Overall Performance'],
        'weaknesses': weaknesses if weaknesses else ['No major weaknesses'],
        'total_reviews': len(all_reviews)
    }


def build_aspect_comparison(products, aspects, analysis_data):
    """Build comparison data for charts using pre-calculated analysis data (FIXED)"""
    comparison = []
    
    for aspect in aspects:
        row = {'aspect': aspect}
        
        for product in products:
            analysis = analysis_data.get(product)
            
            if analysis:
                score = analysis['aspect_scores'].get(aspect)
                
                # If aspect score exists, use it. If not, default to the overall score for 'Overall' or 50 for others.
                if score is not None:
                    row[product] = score
                elif aspect.lower() == 'overall':
                    # Use overall score scaled to 0-100 for the radar chart if available
                    row[product] = int(analysis['overall_score'] * 10) 
                else:
                    # Default neutral for aspects not explicitly found
                    row[product] = 50 
            else:
                row[product] = 0 # No reviews found for this product
        
        comparison.append(row)
    
    return comparison


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'version': '2.0.0', 'scraping': 'enabled'})


@app.route('/api/test-scraper', methods=['POST'])
def test_scraper():
    """Test endpoint to check if scraper is working"""
    try:
        data = request.get_json()
        # Use a demo product name for guaranteed results
        product_name = data.get('product', 'iPhone 15') 
        
        reviews_data = scraper.get_reviews(product_name)
        
        return jsonify({
            'product': product_name,
            'found': reviews_data['found'],
            'total_reviews': reviews_data['total'],
            'hindi_reviews': len(reviews_data['hindi']),
            'marathi_reviews': len(reviews_data['marathi']),
            'sample_reviews': {
                'hindi': reviews_data['hindi'][:2] if reviews_data['hindi'] else [],
                'marathi': reviews_data['marathi'][:2] if reviews_data['marathi'] else []
            }
        })
    
    except Exception as e:
        logger.error(f"Test scraper error: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
