from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from models.trainer import MLTrainer
from models.predictor import MLPredictor
import asyncio

app = FastAPI(title="IntelliInspect ML Service")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global storage
dataset_store = {}
model_store = {}

@app.post("/upload-dataset")
async def upload_dataset(file: UploadFile = File(...)):
    """Process uploaded CSV and add synthetic timestamps"""
    try:
        # Read CSV
        df = pd.read_csv(file.file)
        
        # Add synthetic timestamp (1 second intervals starting from 2021-01-01)
        start_time = datetime(2021, 1, 1, 0, 0, 0)
        df['synthetic_timestamp'] = [start_time + timedelta(seconds=i) for i in range(len(df))]
        
        # Store dataset
        dataset_store['data'] = df
        
        # Calculate metadata
        total_records = len(df)
        total_columns = len(df.columns)
        pass_rate = (df['Response'].sum() / len(df)) * 100 if 'Response' in df.columns else 0
        earliest_time = df['synthetic_timestamp'].min()
        latest_time = df['synthetic_timestamp'].max()
        
        return {
            "status": "success",
            "metadata": {
                "total_records": total_records,
                "total_columns": total_columns,
                "pass_rate": round(pass_rate, 2),
                "earliest_timestamp": earliest_time.isoformat(),
                "latest_timestamp": latest_time.isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/validate-ranges")
async def validate_ranges(ranges: dict):
    """Validate date ranges and return record counts"""
    try:
        df = dataset_store['data']
        
        train_start = datetime.fromisoformat(ranges['train_start'])
        train_end = datetime.fromisoformat(ranges['train_end'])
        test_start = datetime.fromisoformat(ranges['test_start'])
        test_end = datetime.fromisoformat(ranges['test_end'])
        sim_start = datetime.fromisoformat(ranges['sim_start'])
        sim_end = datetime.fromisoformat(ranges['sim_end'])
        
        # Count records in each range
        train_count = len(df[(df['synthetic_timestamp'] >= train_start) & (df['synthetic_timestamp'] <= train_end)])
        test_count = len(df[(df['synthetic_timestamp'] >= test_start) & (df['synthetic_timestamp'] <= test_end)])
        sim_count = len(df[(df['synthetic_timestamp'] >= sim_start) & (df['synthetic_timestamp'] <= sim_end)])
        
        return {
            "status": "valid",
            "counts": {
                "training": train_count,
                "testing": test_count,
                "simulation": sim_count
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/train-model")
async def train_model(params: dict):
    """Train ML model and return evaluation metrics"""
    try:
        trainer = MLTrainer(dataset_store['data'])
        metrics = trainer.train(
            train_start=params['train_start'],
            train_end=params['train_end'],
            test_start=params['test_start'],
            test_end=params['test_end']
        )
        
        # Store trained model
        model_store['trainer'] = trainer
        
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start-simulation")
async def start_simulation(params: dict):
    """Start real-time prediction simulation"""
    try:
        predictor = MLPredictor(model_store['trainer'])
        results = predictor.simulate(
            dataset_store['data'],
            sim_start=params['sim_start'],
            sim_end=params['sim_end']
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)