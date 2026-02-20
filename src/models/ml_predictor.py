import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os
import logging

logger = logging.getLogger(__name__)

class MLPredictor:
    def __init__(self, model_path="models/return_predictor.joblib"):
        self.model_path = model_path
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        self.model = self._load_or_create_model()

    def _load_or_create_model(self):
        if os.path.exists(self.model_path):
            try:
                return joblib.load(self.model_path)
            except Exception as e:
                logger.error(f"Error loading model: {e}. Creating new.")
                
        # Create untrained dummy model if file doesn't exist
        return RandomForestRegressor(n_estimators=100, random_state=42)

    def train_synthetic(self):
        """Generates synthetic historical data to train the model as an example."""
        logger.info("Training ML predictor on synthetic data...")
        # Features: [volatility, previous_return, interest_rate_trend]
        X = np.random.rand(1000, 3) 
        # Target: Forward 30-day return
        y = X[:, 1] * 0.5 + X[:, 2] * -0.2 + np.random.normal(0, 0.05, 1000)
        
        self.model.fit(X, y)
        joblib.dump(self.model, self.model_path)
        logger.info("Model trained and saved.")

    def predict_returns(self, current_features: np.ndarray):
        """
        Predict returns with confidence intervals.
        Requires shape [1, 3] features.
        """
        try:
            # Check if fitted, if not, train dummy
            if not hasattr(self.model, "estimators_"):
                self.train_synthetic()
                
            prediction = self.model.predict(current_features)[0]
            
            # Use individual tree predictions to establish confidence intervals
            all_preds = np.array([tree.predict(current_features)[0] for tree in self.model.estimators_])
            std_dev = np.std(all_preds)
            
            return {
                "expected_return": round(prediction, 4),
                "lower_bound_95": round(prediction - (1.96 * std_dev), 4),
                "upper_bound_95": round(prediction + (1.96 * std_dev), 4),
                "confidence_interval_width": round((1.96 * std_dev * 2), 4)
            }
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {"error": "Prediction unavailable"}

    def get_feature_importance(self):
        if hasattr(self.model, "feature_importances_"):
            return {
                "Volatility": round(self.model.feature_importances_[0], 3),
                "Trailing Return": round(self.model.feature_importances_[1], 3),
                "Macro Factor": round(self.model.feature_importances_[2], 3)
            }
        return {}
