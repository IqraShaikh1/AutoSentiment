"""
Script to generate additional sample reviews for the dataset
This helps expand the CSV with more products
"""
import pandas as pd
import random

def generate_phone_reviews():
    """Generate reviews for additional phones"""
    phones = {
        'Pixel 8 Pro': {
            'Camera': [
                ('Google कैमरा AI शानदार है computational photography लाजवाब', 5, 'hindi'),
                ('Night sight feature अद्भुत है low light में perfect', 5, 'hindi'),
                ('कॅमेरा AI खूप चांगला आहे फोटो quality उत्कृष्ट', 5, 'marathi')
            ],
            'Battery': [
                ('बैटरी decent है लेकिन heavy use में कम पड़ती है', 3, 'hindi'),
                ('चार्जिंग स्पीड slow है 30W only', 3, 'hindi'),
                ('बॅटरी सरासरी आहे पूर्ण दिवस कठीण चालते', 3, 'marathi')
            ],
            'Performance': [
                ('Tensor G3 processor unique है AI tasks में best', 5, 'hindi'),
                ('Gaming performance average है heating issue भी है', 3, 'hindi')
            ],
            'Display': [
                ('120Hz OLED display vibrant है colors accurate', 5, 'hindi'),
                ('Screen brightness outdoor में excellent है', 5, 'hindi')
            ],
            'Value': [
                ('कीमत ₹85000 है premium segment में competitive', 4, 'hindi'),
                ('Features के हिसाब से reasonable price है', 4, 'hindi')
            ],
            'Build Quality': [
                ('बिल्ड quality premium है glass back elegant लगता', 5, 'hindi'),
                ('बांधकाम गुणवत्ता उत्तम आहे premium feel', 5, 'marathi')
            ]
        },
        'Nothing Phone 2': {
            'Camera': [
                ('कैमरा decent है unique features हैं', 4, 'hindi'),
                ('50MP sensor अच्छी quality देता है daylight में', 4, 'hindi'),
                ('कॅमेरा चांगला आहे पण top tier नाही', 4, 'marathi')
            ],
            'Battery': [
                ('बैटरी 4700mAh solid backup देती है', 4, 'hindi'),
                ('45W fast charging बहुत तेज है', 5, 'hindi')
            ],
            'Performance': [
                ('Snapdragon 8+ Gen 1 powerful है smooth performance', 5, 'hindi'),
                ('Gaming में कोई lag नहीं है excellent', 5, 'hindi')
            ],
            'Display': [
                ('OLED display stunning है Glyph interface unique', 5, 'hindi'),
                ('120Hz refresh rate butter smooth है', 5, 'hindi')
            ],
            'Value': [
                ('₹45000 में best value unique design के साथ', 5, 'hindi'),
                ('किंमत खूप चांगली आहे features बघता', 5, 'marathi')
            ],
            'Build Quality': [
                ('Transparent back design unique है premium feel', 5, 'hindi'),
                ('Glyph lights का implementation शानदार है', 5, 'hindi')
            ]
        },
        'Motorola Edge 40': {
            'Camera': [
                ('कैमरा ठीक है mid-range segment में अच्छा', 4, 'hindi'),
                ('50MP main sensor decent photos लेता है', 4, 'hindi')
            ],
            'Battery': [
                ('बैटरी 4400mAh है average backup', 3, 'hindi'),
                ('68W fast charging lightning fast है', 5, 'hindi')
            ],
            'Performance': [
                ('Dimensity 8020 processor smooth है daily use के लिए', 4, 'hindi'),
                ('Gaming decent है heavy games में थोड़ी heating', 3, 'hindi')
            ],
            'Display': [
                ('144Hz pOLED display silky smooth है', 5, 'hindi'),
                ('curved display premium look देता है', 5, 'hindi')
            ],
            'Value': [
                ('₹30000 में excellent value thin design के साथ', 5, 'hindi'),
                ('Budget में best looking phone है', 5, 'hindi')
            ],
            'Build Quality': [
                ('7.5mm thickness super slim है comfortable', 5, 'hindi'),
                ('वजन 167g केवल बहुत हल्का लगता है', 5, 'hindi')
            ]
        }
    }
    
    reviews = []
    for phone, aspects in phones.items():
        for aspect, aspect_reviews in aspects.items():
            for text, rating, language in aspect_reviews:
                reviews.append({
                    'product_name': phone,
                    'category': 'phone',
                    'text': text,
                    'rating': rating,
                    'aspect': aspect,
                    'language': language
                })
    
    return reviews

def generate_tv_reviews():
    """Generate reviews for additional TVs"""
    tvs = {
        'TCL C735': {
            'Display': [
                ('QLED panel अच्छा है colors vibrant हैं', 4, 'hindi'),
                ('4K resolution sharp है HDR support भी है', 4, 'hindi'),
                ('डिस्प्ले गुणवत्ता चांगली आहे bright आहे', 4, 'marathi')
            ],
            'Audio': [
                ('Dolby Atmos sound quality बहुत अच्छी है', 5, 'hindi'),
                ('Subwoofer built-in है bass powerful है', 5, 'hindi')
            ],
            'Smart Features': [
                ('Google TV interface user-friendly है', 4, 'hindi'),
                ('Apps की range अच्छी है smooth चलते हैं', 4, 'hindi')
            ],
            'Performance': [
                ('Gaming mode अच्छा है low latency', 4, 'hindi'),
                ('HDMI 2.1 support gaming के लिए बढ़िया', 5, 'hindi')
            ],
            'Value': [
                ('₹55000 में excellent package budget में best', 5, 'hindi'),
                ('किंमत खूप योग्य आहे features बघता', 5, 'marathi')
            ],
            'Build Quality': [
                ('बिल्ड decent है bezels slim हैं', 4, 'hindi'),
                ('Stand stable है premium नहीं लगता', 3, 'hindi')
            ]
        },
        'Hisense U8H': {
            'Display': [
                ('Mini LED backlight शानदार है contrast perfect', 5, 'hindi'),
                ('Brightness level बहुत high है 1500 nits', 5, 'hindi')
            ],
            'Audio': [
                ('साउंड quality अच्छी है लेकिन bass कम है', 3, 'hindi'),
                ('External speakers की recommendation है', 3, 'hindi')
            ],
            'Smart Features': [
                ('VIDAA OS simple है लेकिन apps limited', 3, 'hindi'),
                ('Netflix और Prime preinstalled हैं', 4, 'hindi')
            ],
            'Performance': [
                ('Gaming features excellent हैं VRR support', 5, 'hindi'),
                ('120Hz panel gaming के लिए ideal', 5, 'hindi')
            ],
            'Value': [
                ('₹75000 में Mini LED technology बढ़िया deal', 5, 'hindi'),
                ('Performance to price ratio outstanding', 5, 'hindi')
            ],
            'Build Quality': [
                ('बिल्ड quality solid है premium finish', 4, 'hindi'),
                ('Metal frame sturdy है elegant look', 4, 'hindi')
            ]
        }
    }
    
    reviews = []
    for tv, aspects in tvs.items():
        for aspect, aspect_reviews in aspects.items():
            for text, rating, language in aspect_reviews:
                reviews.append({
                    'product_name': tv,
                    'category': 'tv',
                    'text': text,
                    'rating': rating,
                    'aspect': aspect,
                    'language': language
                })
    
    return reviews

def generate_camera_reviews():
    """Generate reviews for additional cameras"""
    cameras = {
        'Nikon Z8': {
            'Image Quality': [
                ('45MP sensor incredible resolution detail amazing', 5, 'hindi'),
                ('Dynamic range बेहतरीन है RAW files flexible', 5, 'hindi'),
                ('इमेज quality उत्कृष्ट आहे colors natural', 5, 'marathi')
            ],
            'Autofocus': [
                ('AF system Z9 जैसा है lightning fast', 5, 'hindi'),
                ('Eye detection animals के लिए भी perfect', 5, 'hindi')
            ],
            'Video': [
                ('8K 60fps recording professional grade है', 5, 'hindi'),
                ('Internal RAW recording filmmaker के लिए ideal', 5, 'hindi')
            ],
            'Battery': [
                ('Battery life excellent है full day shooting', 5, 'hindi'),
                ('EN-EL15c battery proven है reliable', 5, 'hindi')
            ],
            'Value': [
                ('₹280000 में Z9 features affordable price', 5, 'hindi'),
                ('Professional work के लिए worth investment', 5, 'hindi')
            ],
            'Build Quality': [
                ('Weather sealing top-notch है rugged body', 5, 'hindi'),
                ('Build quality निकॉन standard excellent', 5, 'hindi')
            ]
        },
        'Canon R7': {
            'Image Quality': [
                ('32.5MP APS-C sensor sharp images crop factor advantage', 4, 'hindi'),
                ('Wildlife photography के लिए ideal है reach बढ़ती', 5, 'hindi')
            ],
            'Autofocus': [
                ('Dual Pixel AF reliable है tracking अच्छी', 4, 'hindi'),
                ('Animal detection काम करता है पर Sony से slow', 4, 'hindi')
            ],
            'Video': [
                ('4K 60fps oversampled quality excellent है', 5, 'hindi'),
                ('Overheating issue है long recording में problem', 3, 'hindi')
            ],
            'Battery': [
                ('LP-E6NH battery decent है spare चाहिए', 4, 'hindi'),
                ('CIPA rating 660 shots average है', 3, 'hindi')
            ],
            'Value': [
                ('₹135000 में wildlife camera best budget option', 5, 'hindi'),
                ('RF-S lenses affordable हैं ecosystem growing', 4, 'hindi')
            ],
            'Build Quality': [
                ('Magnesium alloy body solid है weather sealed', 5, 'hindi'),
                ('Ergonomics comfortable हैं grip अच्छी', 5, 'hindi')
            ]
        }
    }
    
    reviews = []
    for camera, aspects in cameras.items():
        for aspect, aspect_reviews in aspects.items():
            for text, rating, language in aspect_reviews:
                reviews.append({
                    'product_name': camera,
                    'category': 'camera',
                    'text': text,
                    'rating': rating,
                    'aspect': aspect,
                    'language': language
                })
    
    return reviews

def main():
    """Generate and append new reviews to CSV"""
    print("🚀 Generating additional sample data...")
    
    # Load existing data
    try:
        existing_df = pd.read_csv('reviews_dataset.csv')
        print(f"✅ Loaded existing data: {len(existing_df)} reviews")
    except FileNotFoundError:
        existing_df = pd.DataFrame()
        print("⚠️ No existing file found, creating new dataset")
    
    # Generate new reviews
    new_reviews = []
    new_reviews.extend(generate_phone_reviews())
    new_reviews.extend(generate_tv_reviews())
    new_reviews.extend(generate_camera_reviews())
    
    # Create DataFrame
    new_df = pd.DataFrame(new_reviews)
    
    # Combine with existing
    if not existing_df.empty:
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    
    # Save to CSV
    combined_df.to_csv('reviews_dataset.csv', index=False, encoding='utf-8')
    
    print(f"✅ Added {len(new_reviews)} new reviews")
    print(f"📊 Total reviews: {len(combined_df)}")
    print(f"📱 Total products: {combined_df['product_name'].nunique()}")
    print("\nNew products added:")
    for product in new_df['product_name'].unique():
        count = len(new_df[new_df['product_name'] == product])
        print(f"  - {product}: {count} reviews")
    
    print("\n✅ Dataset updated successfully!")

if __name__ == "__main__":
    main()