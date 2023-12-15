from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelBinarizer
import os
import pandas as pd

class PoemSentimentDetector:
    def __init__(self, elegy_themes, ode_themes):
        # Initialize Tfidf and SVC
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = SVC(probability=True)

        self.elegy_themes = elegy_themes
        self.ode_themes = ode_themes

    def train(self, poem_data, labels):
        
        X = self.vectorizer.fit_transform(poem_data)

        # Split dataset into training and testing sets 
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42, stratify=labels)

    
        self.model.fit(X_train, y_train)

        # Predict on the test set and evaluate performance
        preds = self.model.predict(X_test)
        lb = LabelBinarizer()
        y_test_bin = lb.fit_transform(y_test)
        pred_bin = lb.transform(preds)

        # Print evaluation metrics
        print('Accuracy: ', accuracy_score(y_test, preds))
        print('F1 Score: ', f1_score(y_test, preds, pos_label="elegy"))
        print('ROC AUC Score: ', roc_auc_score(y_test_bin, pred_bin))

    def predict(self, poem_content):
        # Transform poem into TF-IDF features
        X = self.vectorizer.transform([poem_content])
    

        # Predict Sentiment
        sentiment = self.model.predict(X)[0]
        if sentiment in self.elegy_themes:
            return "Elegy"
        elif sentiment in self.ode_themes:
            return "Ode"
        else:
            return "Neither"

    def load_data(self, folder_path):
        # Load poem data and corresponding labels 
        data = []
        labels = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    data.append(content)
                    labels.append("elegy" if "elegy" in filename.lower() else "ode")
        return data, labels
