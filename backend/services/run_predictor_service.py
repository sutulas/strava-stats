"""
Run Predictor Service
Predicts running pace based on past runs and planned distance/heart rate
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import logging
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)

class RunPredictorService:
    """Service for predicting running pace based on historical data"""
    
    def __init__(self):
        self.model = None
        self.seq_scaler = None
        self.plan_scaler = None
        self.target_scaler = None
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and scalers"""
        try:
            # Get the path to the model file - try multiple possible locations
            service_file = Path(__file__).resolve()
            backend_dir = service_file.parent.parent
            cwd = Path(os.getcwd())
            
            # List of possible paths to try
            possible_paths = [
                backend_dir / "ml" / "running_pace_model.h5",  # Relative to service file
                cwd / "ml" / "running_pace_model.h5",  # Relative to current working directory
                cwd / "backend" / "ml" / "running_pace_model.h5",  # If running from project root
                Path("ml") / "running_pace_model.h5",  # Relative path
                Path("backend/ml/running_pace_model.h5"),  # From project root
            ]
            
            model_path = None
            for path in possible_paths:
                if path.exists():
                    model_path = path.resolve()
                    logger.info(f"Found model at: {model_path}")
                    break
            
            if model_path is None:
                logger.error(f"Model file not found. Tried the following paths:")
                for path in possible_paths:
                    logger.error(f"  - {path.resolve() if path.is_absolute() or path.exists() else path} (exists: {path.exists()})")
                logger.error(f"Current working directory: {cwd}")
                logger.error(f"Service file location: {service_file}")
                logger.error(f"Backend directory: {backend_dir}")
                return
            
            logger.info(f"Loading model from: {model_path}")
            
            # Load the model
            try:
                self.model = load_model(str(model_path), compile=False)
            except Exception as load_error:
                # Try with compile=True if compile=False fails
                logger.warning(f"Failed to load with compile=False, trying with compile=True: {load_error}")
                self.model = load_model(str(model_path), compile=True)
            
            logger.info(f"Model loaded successfully from {model_path}")
            
            # For now, we'll create new scalers and fit them on-the-fly
            # In production, you'd want to save/load the scalers from training
            self.seq_scaler = StandardScaler()
            self.plan_scaler = StandardScaler()
            self.target_scaler = StandardScaler()
            
            self.model_loaded = True
            logger.info("Run predictor service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.model_loaded = False
    
    def _prepare_sequence_data(self, df: pd.DataFrame) -> Optional[np.ndarray]:
        """
        Prepare sequence data from the last 7 runs
        Returns: numpy array of shape (1, 7, 5) or None if insufficient data
        
        Note: This matches the format expected by run_predict.py:
        - distance: in miles
        - average_speed: in m/s (raw from Strava, not converted to min/mile)
        - total_elevation_gain: in meters
        - days_since_last_run: days between runs
        - rolling_7d_distance: sum of last 7 runs' distances
        """
        try:
            # Ensure data is sorted by date (oldest first, like in training)
            if 'start_date' in df.columns:
                df = df.sort_values('start_date').reset_index(drop=True)
            
            # Need at least 7 runs
            if len(df) < 7:
                logger.warning(f"Insufficient data: {len(df)} runs, need at least 7")
                return None
            
            # Get last 7 runs (most recent)
            recent_runs = df.tail(7).copy()
            
            # Calculate derived features matching run_predict.py exactly
            # Days since last run
            if 'start_date' in recent_runs.columns:
                recent_runs['days_since_last_run'] = recent_runs['start_date'].diff().dt.total_seconds() / (3600 * 24)
                recent_runs['days_since_last_run'] = recent_runs['days_since_last_run'].fillna(1.0)
            else:
                recent_runs['days_since_last_run'] = 1.0
            
            # 7-day rolling total distance - calculate on full dataset, then take last 7
            # This matches the training script which calculates rolling on full df
            df_sorted = df.sort_values('start_date').reset_index(drop=True) if 'start_date' in df.columns else df
            df_sorted['rolling_7d_distance'] = df_sorted['distance'].rolling(window=7, min_periods=1).sum()
            # Get the rolling values for the last 7 runs
            recent_runs['rolling_7d_distance'] = df_sorted.tail(7)['rolling_7d_distance'].values
            
            # Convert average_speed from min/mile back to m/s for model input
            # Our data has average_speed in min/mile (from format_data_service)
            # But the model expects it in m/s (raw Strava format)
            # Formula: m/s = 26.822 / (min/mile)
            if 'average_speed' in recent_runs.columns:
                # Convert from min/mile to m/s
                recent_runs['average_speed_mps'] = 26.822 / recent_runs['average_speed'].replace(0, np.nan)
                recent_runs['average_speed_mps'] = recent_runs['average_speed_mps'].fillna(3.5)  # Default ~7.5 min/mile pace
            else:
                # Calculate from distance and time if not available
                # moving_time is in minutes, distance is in miles
                # speed in m/s = (distance in miles * 1609.34) / (moving_time in minutes * 60)
                if 'moving_time' in recent_runs.columns and 'distance' in recent_runs.columns:
                    recent_runs['average_speed_mps'] = (recent_runs['distance'] * 1609.34) / (recent_runs['moving_time'] * 60)
                    recent_runs['average_speed_mps'] = recent_runs['average_speed_mps'].fillna(3.5)
                else:
                    recent_runs['average_speed_mps'] = 3.5  # Default ~7.5 min/mile pace
            
            # Ensure total_elevation_gain exists (should be in meters from Strava)
            if 'total_elevation_gain' not in recent_runs.columns:
                recent_runs['total_elevation_gain'] = 0.0
            
            # Select features in the exact order expected by the model:
            # distance, average_speed (m/s), total_elevation_gain, days_since_last_run, rolling_7d_distance
            features = ['distance', 'average_speed_mps', 'total_elevation_gain', 'days_since_last_run', 'rolling_7d_distance']
            
            # Extract feature values
            sequence_data = recent_runs[features].values
            
            # Reshape to (1, 7, 5) for model input
            sequence_data = sequence_data.reshape(1, 7, 5)
            
            logger.debug(f"Sequence data shape: {sequence_data.shape}")
            logger.debug(f"Sequence data sample: {sequence_data[0, 0, :]}")
            
            return sequence_data
            
        except Exception as e:
            logger.error(f"Error preparing sequence data: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def _fit_scalers_from_data(self, df: pd.DataFrame):
        """
        Fit scalers using historical data
        This matches the format expected by run_predict.py training script
        """
        try:
            # Prepare all sequences from the dataframe
            if len(df) < 7:
                return
            
            # Calculate derived features for all data (matching run_predict.py)
            df_sorted = df.sort_values('start_date').reset_index(drop=True) if 'start_date' in df.columns else df.copy()
            
            # Days since last run
            df_sorted['days_since_last_run'] = df_sorted['start_date'].diff().dt.total_seconds() / (3600 * 24) if 'start_date' in df_sorted.columns else 1.0
            df_sorted['days_since_last_run'] = df_sorted['days_since_last_run'].fillna(1.0)
            
            # 7-day rolling total distance
            df_sorted['rolling_7d_distance'] = df_sorted['distance'].rolling(window=7, min_periods=1).sum()
            
            # Convert average_speed from min/mile to m/s (matching training data format)
            if 'average_speed' in df_sorted.columns:
                # Convert from min/mile to m/s: m/s = 26.822 / (min/mile)
                df_sorted['average_speed_mps'] = 26.822 / df_sorted['average_speed'].replace(0, np.nan)
                df_sorted['average_speed_mps'] = df_sorted['average_speed_mps'].fillna(3.5)  # Default ~7.5 min/mile
            else:
                # Calculate from distance and time
                if 'moving_time' in df_sorted.columns and 'distance' in df_sorted.columns:
                    # moving_time is in minutes, distance is in miles
                    # speed in m/s = (distance in miles * 1609.34) / (moving_time in minutes * 60)
                    df_sorted['average_speed_mps'] = (df_sorted['distance'] * 1609.34) / (df_sorted['moving_time'] * 60)
                    df_sorted['average_speed_mps'] = df_sorted['average_speed_mps'].fillna(3.5)
                else:
                    df_sorted['average_speed_mps'] = 3.5
            
            # Ensure total_elevation_gain exists
            if 'total_elevation_gain' not in df_sorted.columns:
                df_sorted['total_elevation_gain'] = 0.0
            
            # Prepare sequence features (matching run_predict.py exactly)
            seq_features = ['distance', 'average_speed_mps', 'total_elevation_gain', 'days_since_last_run', 'rolling_7d_distance']
            
            # Fit sequence scaler on all data (flattened)
            seq_data_flat = df_sorted[seq_features].values
            self.seq_scaler.fit(seq_data_flat)
            
            # Fit plan scaler (distance, heart rate)
            if 'average_heartrate' in df_sorted.columns:
                plan_data = df_sorted[['distance', 'average_heartrate']].values
            else:
                plan_data = np.column_stack([df_sorted['distance'].values, np.full(len(df_sorted), 155)])
            self.plan_scaler.fit(plan_data)
            
            # Fit target scaler (pace)
            # In run_predict.py: pace_min_per_mile = moving_time / distance
            # where moving_time is in SECONDS (per comment), distance in miles
            # This gives: seconds/mile, which when divided by 60 = min/mile
            # But the variable name suggests it's already in min/mile
            # Let's match exactly: if training used seconds, we convert our minutes to seconds
            if 'moving_time' in df_sorted.columns and 'distance' in df_sorted.columns:
                # Our moving_time is in minutes, convert to seconds to match training
                moving_time_seconds = df_sorted['moving_time'] * 60
                # Match training formula exactly: pace = moving_time / distance
                pace = moving_time_seconds / df_sorted['distance']  # This gives seconds per mile
                # But the variable name says "min_per_mile", so divide by 60
                pace = pace / 60  # Convert to minutes per mile
                pace = pace.replace([np.inf, -np.inf], np.nan)
                pace = pace.dropna()
                if len(pace) > 0:
                    self.target_scaler.fit(pace.values.reshape(-1, 1))
                    logger.debug(f"Pace range for scaler: {pace.min():.2f} - {pace.max():.2f} min/mile")
                else:
                    # Default pace scaler if no valid pace data
                    self.target_scaler.fit(np.array([[7.0], [8.0], [9.0], [10.0]]))  # Typical pace range
            else:
                # Default pace scaler if no time/distance data
                self.target_scaler.fit(np.array([[7.0], [8.0], [9.0], [10.0]]))  # Typical pace range
            
            logger.info("Scalers fitted from historical data")
            
        except Exception as e:
            logger.error(f"Error fitting scalers: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    def predict_pace(self, df: pd.DataFrame, desired_distance: float, desired_hr: float) -> Optional[Dict[str, Any]]:
        """
        Predict pace for a planned run
        
        Args:
            df: DataFrame with user's running history
            desired_distance: Target distance in miles
            desired_hr: Target heart rate in bpm
            
        Returns:
            Dictionary with prediction results or None if prediction fails
        """
        # Try to reload model if not loaded
        if not self.model_loaded:
            logger.warning("Model not loaded, attempting to reload...")
            self._load_model()
        
        if not self.model_loaded:
            logger.error("Model not loaded, cannot make prediction")
            return {
                "error": "Prediction model is not available. Please check server logs for details."
            }
        
        try:
            # Prepare sequence data
            sequence_data = self._prepare_sequence_data(df)
            if sequence_data is None:
                return {
                    "error": "Insufficient data. Need at least 7 previous runs to make predictions.",
                    "available_runs": len(df)
                }
            
            # Fit scalers from historical data
            self._fit_scalers_from_data(df)
            
            # Scale sequence data
            seq_flat = sequence_data.reshape(-1, sequence_data.shape[2])
            seq_scaled = self.seq_scaler.transform(seq_flat).reshape(sequence_data.shape)
            
            # Prepare planned run data
            planned_data = np.array([[desired_distance, desired_hr]])
            planned_scaled = self.plan_scaler.transform(planned_data)
            
            # Make prediction
            pred_scaled = self.model.predict([seq_scaled, planned_scaled], verbose=0)
            
            # Inverse transform to get actual pace
            pred_pace = self.target_scaler.inverse_transform(pred_scaled)[0][0]
            
            # Calculate predicted time
            predicted_time_minutes = pred_pace * desired_distance
            predicted_time_hours = predicted_time_minutes / 60
            
            return {
                "predicted_pace": round(pred_pace, 2),
                "predicted_time_minutes": round(predicted_time_minutes, 1),
                "predicted_time_hours": round(predicted_time_hours, 2),
                "desired_distance": desired_distance,
                "desired_heart_rate": desired_hr,
                "runs_used": 7
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {
                "error": f"Prediction failed: {str(e)}"
            }

# Global instance - will be initialized on import
run_predictor_service = RunPredictorService()

# Log initialization status
if run_predictor_service.model_loaded:
    logger.info("Run predictor service ready")
else:
    logger.warning("Run predictor service initialized but model not loaded - predictions will fail")

