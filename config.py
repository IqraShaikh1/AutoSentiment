"""
config.py - Configuration settings for the product comparison system
"""

# Model Configuration
MODEL_PATH = './trained_model'
MODEL_NAME = 'xlm-roberta-base'  # Used for initial training

# Scraping Configuration
MAX_REVIEWS_DEFAULT = 30
SCRAPER_HEADLESS = True
SCRAPER_TIMEOUT = 10  # seconds
SCRAPER_PAGE_LOAD_DELAY = 2  # seconds

# Supported websites
SUPPORTED_SITES = {
    'amazon': ['amazon.in', 'amazon.com'],
    'flipkart': ['flipkart.com']
}

# Sentiment Configuration
SENTIMENT_LABELS = {
    0: 'negative',
    1: 'neutral',
    2: 'positive'
}

SENTIMENT_WEIGHTS = {
    'positive': 1,
    'neutral': 0,
    'negative': -1
}

# API Configuration
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
FLASK_DEBUG = True

# CORS Configuration
CORS_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

# Output Configuration
SAVE_REVIEWS_TO_CSV = True
SAVE_COMPARISON_TO_JSON = True
OUTPUT_ENCODING = 'utf-8'

# UI Configuration
PRODUCT_CARD_COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#22c55e',
    'danger': '#ef4444',
    'warning': '#fbbf24'
}

# Review Analysis Configuration
MIN_REVIEW_LENGTH = 20  # characters
MAX_REVIEW_LENGTH = 500  # characters for display
CONFIDENCE_THRESHOLD = 0.5  # minimum confidence for predictions

# Chrome Driver Configuration
CHROME_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-blink-features=AutomationControlled',
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
]

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Rate Limiting (to avoid being blocked)
REQUESTS_PER_MINUTE = 10
DELAY_BETWEEN_REQUESTS = 6  # seconds (60 / REQUESTS_PER_MINUTE)

# Feature Flags
ENABLE_CACHING = False
ENABLE_PARALLEL_SCRAPING = False  # Experimental
ENABLE_AUTO_TRANSLATE = False  # Future feature

# Language Support
SUPPORTED_LANGUAGES = ['hi', 'mr', 'en']  # Hindi, Marathi, English

# Comparison Metrics
COMPARISON_METRICS = [
    'sentiment_score',
    'average_rating',
    'positive_percentage',
    'total_reviews'
]

# Sample Review Display
SAMPLE_REVIEWS_COUNT = 5
SHOW_CONFIDENCE_SCORES = True
SHOW_REVIEW_SOURCES = True