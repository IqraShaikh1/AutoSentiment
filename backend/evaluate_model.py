import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv('../datasets/product_reviews.csv')

# Convert sentiment to numeric labels
sentiment_map = {'negative': 0, 'neutral': 1, 'positive': 2}
df['label'] = df['sentiment'].map(sentiment_map)

texts = df['text'].tolist()
labels = df['label'].tolist()

# -----------------------------
# Split into train/test for evaluation
# -----------------------------
texts_train, texts_test, labels_train, labels_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

# -----------------------------
# Load trained model
# -----------------------------
model_dir = './trained_model1'
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
model.eval()

# -----------------------------
# Tokenize test set
# -----------------------------
encodings_test = tokenizer(
    texts_test, truncation=True, padding=True, max_length=128, return_tensors='pt'
)

# -----------------------------
# Get predictions
# -----------------------------
with torch.no_grad():
    outputs = model(**encodings_test)
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=1).numpy()

# -----------------------------
# Compute accuracy
# -----------------------------
acc = accuracy_score(labels_test, predictions)
print(f"Accuracy on test set: {acc*100:.2f}%")

# -----------------------------
# Classification report
# -----------------------------
# Handle missing classes safely
unique_labels = sorted(list(set(labels_test)))  # only labels present in test set
label_names = ['negative', 'neutral', 'positive']
target_names = [label_names[i] for i in unique_labels]

print(classification_report(labels_test, predictions, labels=unique_labels, target_names=target_names))