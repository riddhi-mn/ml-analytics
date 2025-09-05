import pandas as pd
import numpy as np
from datetime import datetime

class MLPredictor:
    def __init__(self, trainer):
        self.model = trainer.model
        self.feature_columns = trainer.feature_columns
        
    def predict_single(self, features):
        """Predict single sample"""
        prediction = self.model.predict([features])[0]
        confidence = self.model.predict_proba([features])[0].max()
        return prediction, confidence
    
    def simulate(self, dataset, sim_start, sim_end):
        """Simulate real-time predictions"""
        sim_start_dt = datetime.fromisoformat(sim_start)
        sim_end_dt = datetime.fromisoformat(sim_end)
        
        sim_data = dataset[
            (dataset['synthetic_timestamp'] >= sim_start_dt) & 
            (dataset['synthetic_timestamp'] <= sim_end_dt)
        ]
        
        # Prepare features
        feature_df = sim_data.drop(['synthetic_timestamp', 'Response'], axis=1)
        numeric_columns = feature_df.select_dtypes(include=[np.number]).columns
        X_sim = feature_df[numeric_columns].fillna(0)
        
        # Make predictions
        predictions = self.model.predict(X_sim)
        confidences = self.model.predict_proba(X_sim).max(axis=1)
        
        # Format results
        results = []
        for idx, row in sim_data.iterrows():
            pred_idx = len(results)
            if pred_idx < len(predictions):
                results.append({
                    "timestamp": row['synthetic_timestamp'].isoformat(),
                    "sample_id": f"sample_{idx}",
                    "prediction": "Pass" if predictions[pred_idx] == 1 else "Fail",
                    "confidence": round(confidences[pred_idx] * 100, 2),
                    "temperature": round(np.random.uniform(20, 30), 1),  # Mock sensor data
                    "pressure": round(np.random.uniform(1000, 1020), 1),
                    "humidity": round(np.random.uniform(40, 60), 1)
                })
        
        return {
            "total_predictions": len(results),
            "pass_count": sum(1 for r in results if r["prediction"] == "Pass"),
            "fail_count": sum(1 for r in results if r["prediction"] == "Fail"),
            "average_confidence": round(np.mean([r["confidence"] for r in results]), 2),
            "predictions": results
        }