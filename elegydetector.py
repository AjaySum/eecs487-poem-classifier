from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.preprocessing import LabelBinarizer
import os
import pandas as pd

class ElegyDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = SVC(probability=True)  

    def train(self, elegy_data, other_poem_data):
            all_data = pd.concat([pd.Series(elegy_data), pd.Series(other_poem_data)])
            labels = ['elegy' for _ in range(len(elegy_data))] + ['other' for _ in range(len(other_poem_data))]

            X = self.vectorizer.fit_transform(all_data)
            y = labels

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

            self.model.fit(X_train, y_train)

            preds = self.model.predict(X_test)
            lb = LabelBinarizer()
            y_test_bin = lb.fit_transform(y_test)
            pred_bin = lb.transform(preds)

            print('Accuracy: ', accuracy_score(y_test, preds))
            print('F1 Score: ', f1_score(y_test, preds, pos_label="elegy"))
            print('ROC AUC Score: ', roc_auc_score(y_test_bin, pred_bin))
        
    def predict(self, poem_content):
        X = self.vectorizer.transform([poem_content])
        return self.model.predict(X)

    def load_data(self, folder_path):
        data = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
                    content = file.read()
                    data.append(content)
        return data
