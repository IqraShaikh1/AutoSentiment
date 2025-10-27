import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class CSVDataLoader:
    def __init__(self, csv_path='reviews_dataset.csv'):
        """Initialize CSV data loader"""
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load reviews from CSV file"""
        try:
            self.df = pd.read_csv(self.csv_path, encoding='utf-8')
            logger.info(f"✅ Loaded {len(self.df)} reviews from {self.csv_path}")
            logger.info(f"📊 Categories: {self.df['category'].unique()}")
            logger.info(f"📱 Products: {self.df['product_name'].unique()}")
        except FileNotFoundError:
            logger.error(f"❌ CSV file not found: {self.csv_path}")
            self.df = pd.DataFrame()
        except Exception as e:
            logger.error(f"❌ Error loading CSV: {e}")
            self.df = pd.DataFrame()
    
    def get_product_reviews(self, product_name: str, language: Optional[str] = None) -> List[Dict]:
        """Get all reviews for a product"""
        if self.df is None or self.df.empty:
            return []
        
        # Normalize product name for matching
        product_lower = product_name.lower().strip()
        
        # Find matching product (case-insensitive, partial match)
        mask = self.df['product_name'].str.lower().str.contains(product_lower, na=False)
        
        if language:
            mask = mask & (self.df['language'] == language)
        
        product_reviews = self.df[mask]
        
        if product_reviews.empty:
            logger.warning(f"⚠️ No reviews found for: {product_name}")
            return []
        
        # Convert to list of dictionaries
        reviews = []
        for _, row in product_reviews.iterrows():
            reviews.append({
                'text': row['text'],
                'rating': int(row['rating']),
                'aspect': row['aspect'],
                'language': row['language']
            })
        
        logger.info(f"📝 Found {len(reviews)} reviews for {product_name}")
        return reviews
    
    def get_aspect_scores(self, product_name: str) -> Dict[str, int]:
        """Calculate aspect scores from reviews"""
        reviews = self.get_product_reviews(product_name)
        
        if not reviews:
            return {}
        
        # Group by aspect and calculate average
        aspect_scores = {}
        
        for review in reviews:
            aspect = review['aspect']
            rating = review['rating']
            
            if aspect not in aspect_scores:
                aspect_scores[aspect] = []
            
            # Convert 1-5 rating to 0-100 score
            aspect_scores[aspect].append(rating * 20)
        
        # Average scores
        for aspect in aspect_scores:
            aspect_scores[aspect] = int(np.mean(aspect_scores[aspect]))
        
        return aspect_scores
    
    def get_product_data(self, product_name: str) -> Optional[Dict]:
        """Get complete product data including reviews and scores"""
        reviews = self.get_product_reviews(product_name)
        
        if not reviews:
            return None
        
        aspect_scores = self.get_aspect_scores(product_name)
        
        # Get product category
        product_lower = product_name.lower().strip()
        mask = self.df['product_name'].str.lower().str.contains(product_lower, na=False)
        category = self.df[mask]['category'].iloc[0] if not self.df[mask].empty else 'unknown'
        
        return {
            'product_name': product_name,
            'category': category,
            'reviews': reviews,
            'aspect_scores': aspect_scores,
            'total_reviews': len(reviews)
        }
    
    def search_products(self, query: str, category: Optional[str] = None) -> List[str]:
        """Search for products by name or category"""
        if self.df is None or self.df.empty:
            return []
        
        query_lower = query.lower().strip()
        
        # Filter by category if specified
        if category:
            df_filtered = self.df[self.df['category'] == category]
        else:
            df_filtered = self.df
        
        # Find matching products
        mask = df_filtered['product_name'].str.lower().str.contains(query_lower, na=False)
        products = df_filtered[mask]['product_name'].unique().tolist()
        
        return products
    
    def get_all_products(self, category: Optional[str] = None) -> List[str]:
        """Get all available products"""
        if self.df is None or self.df.empty:
            return []
        
        if category:
            products = self.df[self.df['category'] == category]['product_name'].unique()
        else:
            products = self.df['product_name'].unique()
        
        return sorted(products.tolist())
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        if self.df is None or self.df.empty:
            return []
        
        return sorted(self.df['category'].unique().tolist())
    
    def get_language_stats(self, product_name: str) -> Dict[str, int]:
        """Get review count by language for a product"""
        reviews = self.get_product_reviews(product_name)
        
        stats = {'hindi': 0, 'marathi': 0}
        
        for review in reviews:
            lang = review.get('language', 'hindi')
            if lang in stats:
                stats[lang] += 1
        
        return stats
    
    def get_overall_score(self, product_name: str) -> float:
        """Calculate overall product score"""
        reviews = self.get_product_reviews(product_name)
        
        if not reviews:
            return 0.0
        
        # Average all ratings
        ratings = [r['rating'] for r in reviews]
        avg_rating = np.mean(ratings)
        
        # Convert to 0-10 scale
        return round(avg_rating * 2, 1)
    
    def compare_products(self, product1: str, product2: str) -> Dict:
        """Compare two products side by side"""
        data1 = self.get_product_data(product1)
        data2 = self.get_product_data(product2)
        
        if not data1 or not data2:
            return {
                'error': f"One or both products not found",
                'product1_found': data1 is not None,
                'product2_found': data2 is not None
            }
        
        # Get all aspects from both products
        all_aspects = set(data1['aspect_scores'].keys()) | set(data2['aspect_scores'].keys())
        
        comparison = {
            'product1': {
                'name': product1,
                'score': self.get_overall_score(product1),
                'aspects': data1['aspect_scores'],
                'review_count': data1['total_reviews']
            },
            'product2': {
                'name': product2,
                'score': self.get_overall_score(product2),
                'aspects': data2['aspect_scores'],
                'review_count': data2['total_reviews']
            },
            'aspects': []
        }
        
        # Build aspect comparison
        for aspect in all_aspects:
            comparison['aspects'].append({
                'aspect': aspect,
                product1: data1['aspect_scores'].get(aspect, 0),
                product2: data2['aspect_scores'].get(aspect, 0)
            })
        
        # Determine winner
        if comparison['product1']['score'] > comparison['product2']['score']:
            comparison['winner'] = product1
        elif comparison['product2']['score'] > comparison['product1']['score']:
            comparison['winner'] = product2
        else:
            comparison['winner'] = 'Tie'
        
        return comparison