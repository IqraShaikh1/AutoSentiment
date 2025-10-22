"""
run_comparison.py - Easy-to-use script for comparing products
"""
from product_comparator import ProductComparator
import sys

def main():
    print("=" * 80)
    print("🔍 AI Product Comparison System")
    print("=" * 80)
    print()
    
    # Get user input
    print("Enter product details:")
    print()
    
    product1_name = input("Product 1 Name (e.g., iPhone 15): ").strip() or "iPhone 15"
    product1_url = input("Product 1 URL (Amazon/Flipkart): ").strip()
    
    print()
    
    product2_name = input("Product 2 Name (e.g., Samsung S24): ").strip() or "Samsung S24"
    product2_url = input("Product 2 URL (Amazon/Flipkart): ").strip()
    
    print()
    
    max_reviews_input = input("Max reviews per product (default 30): ").strip()
    max_reviews = int(max_reviews_input) if max_reviews_input else 30
    
    # Validate URLs
    if not product1_url or not product2_url:
        print("❌ Error: Both product URLs are required!")
        sys.exit(1)
    
    if not ('amazon.in' in product1_url or 'flipkart.com' in product1_url):
        print("❌ Error: Product 1 URL must be from Amazon India or Flipkart")
        sys.exit(1)
    
    if not ('amazon.in' in product2_url or 'flipkart.com' in product2_url):
        print("❌ Error: Product 2 URL must be from Amazon India or Flipkart")
        sys.exit(1)
    
    # Run comparison
    print("\n🚀 Starting comparison...\n")
    
    try:
        comparator = ProductComparator()
        comparison = comparator.compare_products(
            product1_url=product1_url,
            product2_url=product2_url,
            product1_name=product1_name,
            product2_name=product2_name,
            max_reviews=max_reviews
        )
        
        if comparison:
            print("\n✅ Comparison completed successfully!")
            print("📁 Results saved to JSON and CSV files")
        else:
            print("\n❌ Comparison failed. Check error messages above.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Comparison cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()