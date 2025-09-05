import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from datetime import datetime
import xgboost as xgb

class MLTrainer:
    def __init__(self, dataset):
        self.dataset = dataset
        self.model = None
        self.feature_columns = None
        
    def prepare_features(self, df):
        """Prepare features for training - remove non-numeric columns"""
        # Remove timestamp and target
        feature_df = df.drop(['synthetic_timestamp', 'Response'], axis=1)
        # Keep only numeric columns
        numeric_columns = feature_df.select_dtypes(include=[np.number]).columns
        return feature_df[numeric_columns].fillna(0)
    
    def train(self, train_start, train_end, test_start, test_end):
        """Train model and return evaluation metrics"""
        
        # Filter data by date ranges
        train_start_dt = datetime.fromisoformat(train_start)
        train_end_dt = datetime.fromisoformat(train_end)
        test_start_dt = datetime.fromisoformat(test_start)
        test_end_dt = datetime.fromisoformat(test_end)
        
        train_data = self.dataset[
            (self.dataset['synthetic_timestamp'] >= train_start_dt) & 
            (self.dataset['synthetic_timestamp'] <= train_end_dt)
        ]
        
        test_data = self.dataset[
            (self.dataset['synthetic_timestamp'] >= test_start_dt) & 
            (self.dataset['synthetic_timestamp'] <= test_end_dt)
        ]
        
        # Prepare features
        X_train = self.prepare_features(train_data)
        y_train = train_data['Response']
        X_test = self.prepare_features(test_data)
        y_test = test_data['Response']
        
        # Store feature columns
        self.feature_columns = X_train.columns.tolist()
        
        # Train XGBoost model
        self.model = xgb.XGBClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)

        print("Accuracy:", accuracy)
        print("Precision:", precision)
        print("Recall:", recall)
        print("F1 Score:", f1)
        
        return {
            "accuracy": round(accuracy * 100, 2),
            "precision": round(precision * 100, 2),
            "recall": round(recall * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "confusion_matrix": {
                "true_positive": int(cm[1][1]),
                "true_negative": int(cm[0][0]),
                "false_positive": int(cm[0][1]),
                "false_negative": int(cm[1][0])
            }
        }