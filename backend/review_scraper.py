"""
review_scraper.py - Scrapes product reviews from various sources
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

class ReviewScraper:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def scrape_amazon_reviews(self, product_url, max_reviews=50):
        """Scrape reviews from Amazon India"""
        reviews = []
        
        try:
            # Navigate to product page
            self.driver.get(product_url)
            time.sleep(2)
            
            # Click on "See all reviews"
            try:
                see_all = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-hook='see-all-reviews-link-foot']"))
                )
                see_all.click()
                time.sleep(2)
            except:
                print("⚠️ Could not find 'See all reviews' button")
            
            # Scrape reviews from multiple pages
            pages = 0
            while len(reviews) < max_reviews and pages < 5:
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Find review containers
                review_divs = soup.find_all('div', {'data-hook': 'review'})
                
                for review_div in review_divs:
                    if len(reviews) >= max_reviews:
                        break
                    
                    try:
                        # Extract review text
                        review_text = review_div.find('span', {'data-hook': 'review-body'})
                        if review_text:
                            text = review_text.get_text(strip=True)
                            
                            # Extract rating
                            rating = review_div.find('i', {'data-hook': 'review-star-rating'})
                            if rating:
                                rating_text = rating.get_text(strip=True)
                                rating_value = float(re.search(r'(\d+\.?\d*)', rating_text).group(1))
                                
                                reviews.append({
                                    'text': text,
                                    'rating': rating_value,
                                    'source': 'amazon'
                                })
                    except Exception as e:
                        print(f"⚠️ Error parsing review: {e}")
                        continue
                
                # Try to go to next page
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "li.a-last a")
                    next_button.click()
                    time.sleep(2)
                    pages += 1
                except:
                    break
            
            print(f"✅ Scraped {len(reviews)} reviews from Amazon")
            
        except Exception as e:
            print(f"❌ Error scraping Amazon: {e}")
        
        return reviews
    
    def scrape_flipkart_reviews(self, product_url, max_reviews=50):
        """Scrape reviews from Flipkart"""
        reviews = []
        
        try:
            self.driver.get(product_url)
            time.sleep(3)
            
            # Scroll to reviews section
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            
            pages = 0
            while len(reviews) < max_reviews and pages < 5:
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Find review containers (Flipkart structure)
                review_divs = soup.find_all('div', class_=re.compile('.*col.*'))
                
                for review_div in review_divs:
                    if len(reviews) >= max_reviews:
                        break
                    
                    try:
                        # Look for review text
                        text_div = review_div.find('div', class_=re.compile('.*t-ZTKy.*'))
                        if not text_div:
                            text_div = review_div.find('div', text=True)
                        
                        if text_div:
                            text = text_div.get_text(strip=True)
                            
                            # Extract rating
                            rating_div = review_div.find('div', class_=re.compile('.*hGSR24.*'))
                            if rating_div:
                                rating_text = rating_div.get_text(strip=True)
                                rating_value = float(re.search(r'(\d+)', rating_text).group(1))
                                
                                if len(text) > 20:  # Valid review
                                    reviews.append({
                                        'text': text,
                                        'rating': rating_value,
                                        'source': 'flipkart'
                                    })
                    except Exception as e:
                        continue
                
                # Try next page
                try:
                    next_button = self.driver.find_element(By.XPATH, "//a[contains(@class, '_9QVEpD')]//span[text()='Next']")
                    next_button.click()
                    time.sleep(2)
                    pages += 1
                except:
                    break
            
            print(f"✅ Scraped {len(reviews)} reviews from Flipkart")
            
        except Exception as e:
            print(f"❌ Error scraping Flipkart: {e}")
        
        return reviews
    
    def close(self):
        self.driver.quit()
    
    def save_reviews(self, reviews, filename):
        """Save reviews to CSV"""
        df = pd.DataFrame(reviews)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"💾 Saved {len(reviews)} reviews to {filename}")