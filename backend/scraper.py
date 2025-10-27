import requests
from bs4 import BeautifulSoup
import time
import random

class ReviewScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_flipkart_reviews(self, product_url, max_pages=5):
        """Scrape reviews from Flipkart"""
        all_reviews = []
        
        try:
            for page in range(1, max_pages + 1):
                # Construct page URL
                if page == 1:
                    url = product_url
                else:
                    url = f"{product_url}&page={page}"
                
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    print(f"Failed to fetch page {page}")
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find review containers
                reviews = soup.find_all('div', {'class': '_1AtVbE'})
                
                for review in reviews:
                    try:
                        # Extract rating
                        rating_div = review.find('div', {'class': '_3LWZlK'})
                        rating = int(rating_div.text.strip()) if rating_div else 0
                        
                        # Extract review text
                        text_div = review.find('div', {'class': 't-ZTKy'})
                        if not text_div:
                            text_div = review.find('div', {'class': '_6K-7Co'})
                        
                        review_text = text_div.text.strip() if text_div else ""
                        
                        if review_text:
                            all_reviews.append({
                                'text': review_text,
                                'rating': rating,
                                'source': 'flipkart'
                            })
                    
                    except Exception as e:
                        print(f"Error parsing review: {e}")
                        continue
                
                # Be polite - add delay
                time.sleep(random.uniform(1, 3))
            
            print(f"Scraped {len(all_reviews)} reviews from Flipkart")
            return all_reviews
        
        except Exception as e:
            print(f"Scraping error: {e}")
            return []
    
    def scrape_amazon_reviews(self, product_url, max_pages=5):
        """Scrape reviews from Amazon"""
        all_reviews = []
        
        try:
            for page in range(1, max_pages + 1):
                url = product_url if page == 1 else f"{product_url}?pageNumber={page}"
                
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code != 200:
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find review containers
                reviews = soup.find_all('div', {'data-hook': 'review'})
                
                for review in reviews:
                    try:
                        # Extract rating
                        rating_span = review.find('i', {'data-hook': 'review-star-rating'})
                        rating = 0
                        if rating_span:
                            rating_text = rating_span.find('span').text
                            rating = int(float(rating_text.split()[0]))
                        
                        # Extract review text
                        text_span = review.find('span', {'data-hook': 'review-body'})
                        review_text = text_span.text.strip() if text_span else ""
                        
                        if review_text:
                            all_reviews.append({
                                'text': review_text,
                                'rating': rating,
                                'source': 'amazon'
                            })
                    
                    except Exception as e:
                        continue
                
                time.sleep(random.uniform(1, 3))
            
            print(f"Scraped {len(all_reviews)} reviews from Amazon")
            return all_reviews
        
        except Exception as e:
            print(f"Amazon scraping error: {e}")
            return []
    
    def search_product(self, product_name, platform='flipkart'):
        """Search for product and get review page URL"""
        search_urls = {
            'flipkart': f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}",
            'amazon': f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
        }
        
        try:
            url = search_urls.get(platform)
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find first product link
            if platform == 'flipkart':
                product_link = soup.find('a', {'class': '_1fQZEK'})
            else:
                product_link = soup.find('a', {'class': 'a-link-normal s-no-outline'})
            
            if product_link:
                href = product_link.get('href')
                if platform == 'flipkart':
                    full_url = f"https://www.flipkart.com{href}"
                else:
                    full_url = f"https://www.amazon.in{href}"
                
                return full_url
        
        except Exception as e:
            print(f"Search error: {e}")
        
        return None