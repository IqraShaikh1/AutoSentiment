import csv
import random

hindi_positive = [
    "कैमरा बहुत बढ़िया है फोटो क्वालिटी शानदार",
    "बैटरी लंबे समय तक चलती है",
    "डिस्प्ले ब्राइट और क्लियर है",
    "परफॉर्मेंस स्मूद और तेज़ है",
    "कीमत सही है और मूल्य अच्छा है"
]

hindi_negative = [
    "बैटरी जल्दी खत्म हो जाती है",
    "डिस्प्ले धुंधला है",
    "परफॉर्मेंस स्लो है",
    "कीमत ज्यादा है",
    "बिल्ड क्वालिटी कमजोर है"
]

marathi_positive = [
    "कॅमेरा खूप छान आहे फोटो क्वालिटी उत्तम",
    "बॅटरी चांगली आहे",
    "डिस्प्ले सुंदर आहे",
    "परफॉर्मन्स उत्कृष्ट आहे",
    "कीमत परवडणारी आहे"
]

marathi_negative = [
    "बॅटरी लवकर संपते",
    "डिस्प्ले अस्पष्ट आहे",
    "परफॉर्मन्स मंद आहे",
    "कीमत जास्त आहे",
    "बिल्ड क्वालिटी कमी आहे"
]

languages = ["hindi", "marathi"]
sentiments = ["positive", "negative"]

rows = []

for _ in range(1000):
    lang = random.choice(languages)
    if lang == "hindi":
        sentiment = random.choice(["positive","negative"])
        text = random.choice(hindi_positive if sentiment=="positive" else hindi_negative)
    else:
        sentiment = random.choice(["positive","negative"])
        text = random.choice(marathi_positive if sentiment=="positive" else marathi_negative)
    rows.append([text, sentiment, lang])

# Write CSV
with open("product_reviews1.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["text","sentiment","language"])
    writer.writerows(rows)

print("✅ product_reviews.csv generated with 1000 rows")
