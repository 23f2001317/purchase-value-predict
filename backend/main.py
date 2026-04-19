from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Purchase Value Prediction API")

# Define input schema
class PredictionInput(BaseModel):
    age: int
    income: float

class PredictionOutput(BaseModel):
    predicted_purchase_value: float
    message: str

# Load model on startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            logger.info("Model loaded successfully.")
        else:
            logger.warning(f"Model file not found at {MODEL_PATH}. Generating a dummy model...")
            import subprocess
            script_path = os.path.join(BASE_DIR, "..", "scripts", "train_dummy_model.py")
            subprocess.run(["python", script_path])
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            logger.info("Dummy model generated and loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading model: {e}")

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    if model is None:
        logger.error("Model is not loaded.")
        raise HTTPException(status_code=500, detail="Model is not loaded.")
    
    try:
        # Prepare features
        features = np.array([[data.age, data.income]])
        
        # Predict
        prediction = model.predict(features)[0]
        prediction = round(float(prediction), 2)
        
        return PredictionOutput(
            predicted_purchase_value=prediction,
            message="Prediction successful"
        )
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
