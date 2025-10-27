"""
Test script to verify CSV data loading works correctly
"""
from csv_data_loader import CSVDataLoader
import json

def test_data_loader():
    print("=" * 80)
    print("🧪 Testing CSV Data Loader")
    print("=" * 80)
    print()
    
    # Initialize loader
    loader = CSVDataLoader('reviews_dataset.csv')
    
    # Test 1: Get all products
    print("✅ Test 1: Get All Products")
    products = loader.get_all_products()
    print(f"Total products: {len(products)}")
    print(f"Products: {products}")
    print()
    
    # Test 2: Get categories
    print("✅ Test 2: Get Categories")
    categories = loader.get_categories()
    print(f"Categories: {categories}")
    print()
    
    # Test 3: Get product data
    print("✅ Test 3: Get Product Data - iPhone 15")
    iphone_data = loader.get_product_data('iPhone 15')
    if iphone_data:
        print(f"Category: {iphone_data['category']}")
        print(f"Total reviews: {iphone_data['total_reviews']}")
        print(f"Aspect scores: {iphone_data['aspect_scores']}")
        print(f"Sample review: {iphone_data['reviews'][0]['text'][:100]}...")
    print()
    
    # Test 4: Get overall score
    print("✅ Test 4: Get Overall Scores")
    test_products = ['iPhone 15', 'Samsung S24', 'OnePlus 12']
    for product in test_products:
        score = loader.get_overall_score(product)
        print(f"{product}: {score}/10")
    print()
    
    # Test 5: Language statistics
    print("✅ Test 5: Language Statistics")
    for product in test_products[:2]:
        stats = loader.get_language_stats(product)
        print(f"{product}: {stats}")
    print()
    
    # Test 6: Compare products
    print("✅ Test 6: Compare Products - iPhone 15 vs Samsung S24")
    comparison = loader.compare_products('iPhone 15', 'Samsung S24')
    if 'error' not in comparison:
        print(f"Winner: {comparison['winner']}")
        print(f"iPhone 15 score: {comparison['product1']['score']}")
        print(f"Samsung S24 score: {comparison['product2']['score']}")
        print(f"Aspects compared: {len(comparison['aspects'])}")
    print()
    
    # Test 7: Search products
    print("✅ Test 7: Search Products")
    results = loader.search_products('samsung')
    print(f"Search 'samsung': {results}")
    print()
    
    # Test 8: Category filtering
    print("✅ Test 8: Get Products by Category")
    for category in categories:
        products = loader.get_all_products(category)
        print(f"{category.upper()}: {len(products)} products - {products}")
    print()
    
    print("=" * 80)
    print("✅ All tests completed!")
    print("=" * 80)

if __name__ == "__main__":
    test_data_loader()