from flask import Flask, request, jsonify
from flask_cors import CORS
from csv_data_loader import CSVDataLoader
from models import SentimentAnalyzer
from aspect_extractor import AspectExtractor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
logger.info("🚀 Initializing components...")
data_loader = CSVDataLoader('reviews_dataset.csv')
sentiment_analyzer = SentimentAnalyzer()
aspect_extractor = AspectExtractor()
logger.info("✅ Components initialized")

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all available products"""
    try:
        category = request.args.get('category')
        products = data_loader.get_all_products(category)
        categories = data_loader.get_categories()
        
        return jsonify({
            'products': products,
            'categories': categories,
            'total': len(products)
        })
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/product/<product_name>', methods=['GET'])
def get_product_details(product_name):
    """Get detailed information about a product"""
    try:
        product_data = data_loader.get_product_data(product_name)
        
        if not product_data:
            return jsonify({'error': 'Product not found'}), 404
        
        # Add overall score
        product_data['overall_score'] = data_loader.get_overall_score(product_name)
        product_data['language_stats'] = data_loader.get_language_stats(product_name)
        
        return jsonify(product_data)
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_products():
    try:
        data = request.get_json()
        products = data.get('products', [])
        
        if len(products) < 2:
            return jsonify({'error': 'At least 2 products required for comparison'}), 400
        
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
                'languageStats': {}
            }
        }
        
        # Collect all aspects across products
        all_aspects = set()
        product_data_cache = {}
        
        # Analyze each product
        for product in products:
            logger.info(f"🔍 Analyzing: {product}")
            
            # Get product data from CSV
            product_data = data_loader.get_product_data(product)
            
            if not product_data:
                logger.warning(f"⚠️ No data found for {product}")
                results['comparison']['reviewsFound'][product] = False
                
                # Add placeholder
                results['comparison']['overall'].append({
                    'name': product,
                    'score': 0,
                    'sentiment': 'unknown'
                })
                
                results['comparison']['reviews'][product] = []
                results['comparison']['strengths'][product] = []
                results['comparison']['weaknesses'][product] = []
                
                continue
            
            # Cache product data
            product_data_cache[product] = product_data
            results['comparison']['reviewsFound'][product] = True
            
            # Get overall score
            overall_score = data_loader.get_overall_score(product)
            
            # Determine sentiment
            if overall_score >= 7:
                sentiment = 'positive'
            elif overall_score >= 5:
                sentiment = 'neutral'
            else:
                sentiment = 'negative'
            
            results['comparison']['overall'].append({
                'name': product,
                'score': overall_score,
                'sentiment': sentiment
            })
            
            # Get sample reviews (mix of languages)
            reviews = product_data['reviews']
            sample_reviews = reviews[:5]  # Top 5 reviews
            results['comparison']['reviews'][product] = sample_reviews
            
            # Get language statistics
            results['comparison']['languageStats'][product] = data_loader.get_language_stats(product)
            
            # Get aspect scores
            aspect_scores = product_data['aspect_scores']
            all_aspects.update(aspect_scores.keys())
            
            # Identify strengths (scores >= 80)
            strengths = [asp for asp, score in aspect_scores.items() if score >= 80]
            strengths = sorted(strengths, key=lambda x: aspect_scores[x], reverse=True)[:3]
            
            # Identify weaknesses (scores < 70)
            weaknesses = [asp for asp, score in aspect_scores.items() if score < 70]
            weaknesses = sorted(weaknesses, key=lambda x: aspect_scores[x])[:3]
            
            results['comparison']['strengths'][product] = strengths
            results['comparison']['weaknesses'][product] = weaknesses
        
        # Build aspect comparison
        all_aspects_list = sorted(list(all_aspects))
        
        for aspect in all_aspects_list:
            row = {'aspect': aspect}
            
            for product in products:
                if product in product_data_cache:
                    aspect_scores = product_data_cache[product]['aspect_scores']
                    row[product] = aspect_scores.get(aspect, 0)
                else:
                    row[product] = 0
            
            results['comparison']['aspects'].append(row)
        
        # Radar data is same as aspects
        results['comparison']['radarData'] = results['comparison']['aspects']
        
        # Determine winner
        valid_products = [p for p in results['comparison']['overall'] if p['score'] > 0]
        
        if valid_products:
            results['comparison']['winner'] = max(
                valid_products,
                key=lambda x: x['score']
            )['name']
        else:
            results['comparison']['winner'] = "No data found"
        
        logger.info(f"✅ Analysis complete. Winner: {results['comparison']['winner']}")
        
        return jsonify(results)
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_products():
    """Search for products"""
    try:
        query = request.args.get('q', '')
        category = request.args.get('category')
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        products = data_loader.search_products(query, category)
        
        return jsonify({
            'query': query,
            'products': products,
            'total': len(products)
        })
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '3.0.0',
        'data_source': 'CSV',
        'total_products': len(data_loader.get_all_products()),
        'categories': data_loader.get_categories()
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        categories = data_loader.get_categories()
        stats = {
            'total_products': len(data_loader.get_all_products()),
            'categories': categories,
            'products_by_category': {}
        }
        
        for category in categories:
            products = data_loader.get_all_products(category)
            stats['products_by_category'][category] = len(products)
        
        return jsonify(stats)
    
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
