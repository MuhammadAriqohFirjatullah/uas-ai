import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import json
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class BengkuluTrafficPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = [
            'hour', 'day_of_week', 'month', 'is_weekend',
            'is_rush_hour', 'weather_score', 'event_factor',
            'historical_avg_speed', 'volume_last_hour'
        ]
        
    def generate_synthetic_data(self, n_samples=15000):
        """Generate enhanced synthetic traffic data for all Bengkulu roads"""
        print("Generating comprehensive synthetic traffic data for Bengkulu...")
        
        np.random.seed(42)
        data = []
        
        # Enhanced Bengkulu roads with characteristics
        roads_config = {
            'sudirman': {'base_speed': 45, 'congestion_factor': 1.3, 'type': 'arterial'},
            'ahmad-yani': {'base_speed': 50, 'congestion_factor': 1.2, 'type': 'arterial'},
            'suprapto': {'base_speed': 40, 'congestion_factor': 0.9, 'type': 'collector'},
            'parman': {'base_speed': 48, 'congestion_factor': 1.1, 'type': 'arterial'},
            'raya-unib': {'base_speed': 55, 'congestion_factor': 0.8, 'type': 'arterial'},
            'salak-raya': {'base_speed': 42, 'congestion_factor': 1.0, 'type': 'collector'},
            'zainul-arifin': {'base_speed': 38, 'congestion_factor': 1.4, 'type': 'local'},
            'veteran': {'base_speed': 40, 'congestion_factor': 1.2, 'type': 'collector'},
            'pantai-nala': {'base_speed': 50, 'congestion_factor': 0.7, 'type': 'arterial'},
            'hibrida-raya': {'base_speed': 45, 'congestion_factor': 0.9, 'type': 'collector'},
            'basuki-rahmat': {'base_speed': 35, 'congestion_factor': 1.5, 'type': 'local'},
            'khadijah': {'base_speed': 30, 'congestion_factor': 1.3, 'type': 'local'},
            'raya-padang-harapan': {'base_speed': 52, 'congestion_factor': 0.8, 'type': 'arterial'},
            'lintas-sumatera': {'base_speed': 60, 'congestion_factor': 0.6, 'type': 'highway'},
            'raya-kandang': {'base_speed': 48, 'congestion_factor': 0.9, 'type': 'arterial'},
            'mahoni': {'base_speed': 35, 'congestion_factor': 1.1, 'type': 'local'},
            'raya-pagar-dewa': {'base_speed': 50, 'congestion_factor': 0.7, 'type': 'arterial'},
            'bypass': {'base_speed': 65, 'congestion_factor': 0.5, 'type': 'highway'},
            'raya-sawah-lebar': {'base_speed': 45, 'congestion_factor': 0.8, 'type': 'collector'},
            'raya-teluk-segara': {'base_speed': 50, 'congestion_factor': 0.6, 'type': 'arterial'}
        }
        
        for _ in range(n_samples):
            # Select random road
            road_id = np.random.choice(list(roads_config.keys()))
            road_config = roads_config[road_id]
            
            # Time features
            hour = np.random.randint(0, 24)
            day_of_week = np.random.randint(0, 7)
            month = np.random.randint(1, 13)
            is_weekend = 1 if day_of_week >= 5 else 0
            
            # Enhanced rush hour definition
            is_rush_hour = 1 if (7 <= hour <= 9) or (17 <= hour <= 19) else 0
            is_lunch_hour = 1 if (12 <= hour <= 13) else 0
            
            # Weather factor
            weather_score = np.random.beta(2, 1)
            
            # Event factor (holidays, special events)
            event_factor = np.random.choice([0, 0.3, 0.6, 1], p=[0.7, 0.2, 0.08, 0.02])
            
            # Road-specific base speed
            base_speed = road_config['base_speed'] + np.random.normal(0, 3)
            
            # Volume calculation with road-specific factors
            base_volume = 200 if road_config['type'] == 'highway' else \
                         300 if road_config['type'] == 'arterial' else \
                         200 if road_config['type'] == 'collector' else 150
            
            volume_last_hour = np.random.poisson(base_volume * road_config['congestion_factor'])
            
            # Enhanced congestion calculation
            congestion_score = 0
            
            # Time-based congestion
            if is_rush_hour:
                congestion_score += 0.4 * road_config['congestion_factor']
            elif is_lunch_hour:
                congestion_score += 0.2 * road_config['congestion_factor']
            elif 22 <= hour or hour <= 5:
                congestion_score -= 0.3
                
            # Day-based congestion
            if is_weekend:
                if road_config['type'] in ['arterial', 'highway']:
                    congestion_score -= 0.1  # Less congestion on main roads
                else:
                    congestion_score += 0.1  # More congestion on local roads (shopping, recreation)
            else:
                congestion_score += 0.1 * road_config['congestion_factor']
                
            # Weather impact
            congestion_score += (1 - weather_score) * 0.3
            
            # Event impact
            congestion_score += event_factor * 0.4
            
            # Volume impact with road type consideration
            volume_threshold = 400 if road_config['type'] == 'highway' else \
                              500 if road_config['type'] == 'arterial' else \
                              300 if road_config['type'] == 'collector' else 200
            
            if volume_last_hour > volume_threshold:
                congestion_score += 0.3
            elif volume_last_hour < volume_threshold * 0.3:
                congestion_score -= 0.2
                
            # Road type impact
            if road_config['type'] == 'highway':
                congestion_score *= 0.6  # Highways handle traffic better
            elif road_config['type'] == 'local':
                congestion_score *= 1.3  # Local roads get congested easier
                
            # Add randomness
            congestion_score += np.random.normal(0, 0.1)
            
            # Normalize to 0-1 range
            congestion_score = max(0, min(1, congestion_score))
            
            # Calculate actual speed
            speed_reduction = congestion_score * 0.7  # Max 70% speed reduction
            actual_speed = base_speed * (1 - speed_reduction)
            actual_speed = max(5, actual_speed)  # Minimum 5 km/h
            
            data.append([
                hour, day_of_week, month, is_weekend, is_rush_hour,
                weather_score, event_factor, base_speed, volume_last_hour,
                congestion_score, actual_speed
            ])
        
        columns = self.feature_names + ['congestion_level', 'speed']
        df = pd.DataFrame(data, columns=columns)
        
        print(f"Generated {len(df)} synthetic data points for {len(roads_config)} roads")
        print(f"Road type distribution in data:")
        print(f"  Highway roads: {len([r for r in roads_config.values() if r['type'] == 'highway'])}")
        print(f"  Arterial roads: {len([r for r in roads_config.values() if r['type'] == 'arterial'])}")
        print(f"  Collector roads: {len([r for r in roads_config.values() if r['type'] == 'collector'])}")
        print(f"  Local roads: {len([r for r in roads_config.values() if r['type'] == 'local'])}")
        print(f"Congestion level distribution:")
        print(f"  Low (0-0.3): {len(df[df['congestion_level'] < 0.3])} samples")
        print(f"  Medium (0.3-0.7): {len(df[(df['congestion_level'] >= 0.3) & (df['congestion_level'] < 0.7)])} samples")
        print(f"  High (0.7-1.0): {len(df[df['congestion_level'] >= 0.7])} samples")
        
        return df
    
    def train_model(self, data=None):
        """Train the traffic prediction model"""
        if data is None:
            data = self.generate_synthetic_data()
        
        print("Training traffic prediction model...")
        
        # Prepare features and targets
        X = data[self.feature_names]
        y_congestion = data['congestion_level']
        y_speed = data['speed']
        
        # Split data
        X_train, X_test, y_cong_train, y_cong_test, y_speed_train, y_speed_test = train_test_split(
            X, y_congestion, y_speed, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train congestion model
        self.model.fit(X_train_scaled, y_cong_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_cong_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_cong_test, y_pred))
        
        print(f"Model Performance:")
        print(f"  MAE: {mae:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  Feature Importance:")
        
        feature_importance = sorted(
            zip(self.feature_names, self.model.feature_importances_),
            key=lambda x: x[1], reverse=True
        )
        
        for feature, importance in feature_importance:
            print(f"    {feature}: {importance:.4f}")
        
        self.is_trained = True
        return mae, rmse
    
    def predict_congestion(self, road_features):
        """Predict congestion level for given road features"""
        if not self.is_trained:
            print("Model not trained yet. Training now...")
            self.train_model()
        
        # Prepare features
        features = np.array([road_features]).reshape(1, -1)
        features_scaled = self.scaler.transform(features)
        
        # Predict
        congestion_prob = self.model.predict(features_scaled)[0]
        congestion_prob = max(0, min(1, congestion_prob))
        
        # Convert to categorical prediction
        if congestion_prob < 0.3:
            status = "Lancar"
            color = "#4CAF50"
        elif congestion_prob < 0.7:
            status = "Sedang"
            color = "#FF9800"
        else:
            status = "Macet"
            color = "#F44336"
        
        return {
            'congestion_probability': float(congestion_prob),
            'status': status,
            'color': color,
            'confidence': float(min(95, max(60, 100 - abs(congestion_prob - 0.5) * 100)))
        }
    
    def predict_future_traffic(self, current_features, hours_ahead=4):
        """Predict traffic for next few hours"""
        predictions = []
        
        for i in range(1, hours_ahead + 1):
            # Modify features for future time
            future_features = current_features.copy()
            current_hour = current_features[0]
            future_hour = (current_hour + i) % 24
            future_features[0] = future_hour
            
            # Update rush hour flag
            future_features[4] = 1 if (7 <= future_hour <= 9) or (17 <= future_hour <= 19) else 0
            
            # Predict
            prediction = self.predict_congestion(future_features)
            prediction['hour'] = future_hour
            prediction['time'] = f"{future_hour:02d}:00"
            predictions.append(prediction)
        
        return predictions
    
    def get_current_features(self, road_id='sudirman'):
        """Get current features for a road (simulated)"""
        now = datetime.now()
        
        # Base features for current time
        features = [
            now.hour,  # hour
            now.weekday(),  # day_of_week
            now.month,  # month
            1 if now.weekday() >= 5 else 0,  # is_weekend
            1 if (7 <= now.hour <= 9) or (17 <= now.hour <= 19) else 0,  # is_rush_hour
            np.random.beta(2, 1),  # weather_score (simulated)
            0,  # event_factor (no special events)
            45 + np.random.normal(0, 5),  # historical_avg_speed
            np.random.poisson(300)  # volume_last_hour
        ]
        
        return features

# Initialize and train the model
def main():
    print("=== Bengkulu Traffic Prediction System ===")
    print("Initializing AI model for traffic prediction...")
    
    predictor = BengkuluTrafficPredictor()
    
    # Train the model
    mae, rmse = predictor.train_model()
    
    # Test predictions for different scenarios
    print("\n=== Testing Predictions ===")
    
    # Test scenarios
    scenarios = [
        {
            'name': 'Rush Hour Morning (8 AM, Weekday)',
            'features': [8, 1, 6, 0, 1, 0.8, 0, 45, 600]
        },
        {
            'name': 'Normal Hour (2 PM, Weekday)',
            'features': [14, 1, 6, 0, 0, 0.9, 0, 50, 200]
        },
        {
            'name': 'Evening Rush (6 PM, Weekday)',
            'features': [18, 1, 6, 0, 1, 0.7, 0, 40, 800]
        },
        {
            'name': 'Weekend Morning (10 AM, Saturday)',
            'features': [10, 5, 6, 1, 0, 0.9, 0, 55, 150]
        },
        {
            'name': 'Rainy Day Rush Hour',
            'features': [8, 1, 6, 0, 1, 0.3, 0, 35, 700]
        }
    ]
    
    for scenario in scenarios:
        print(f"\nScenario: {scenario['name']}")
        prediction = predictor.predict_congestion(scenario['features'])
        print(f"  Status: {prediction['status']}")
        print(f"  Congestion Probability: {prediction['congestion_probability']:.2f}")
        print(f"  Confidence: {prediction['confidence']:.1f}%")
    
    # Test future predictions
    print("\n=== Future Traffic Predictions ===")
    current_features = predictor.get_current_features()
    future_predictions = predictor.predict_future_traffic(current_features, 6)
    
    print("Predictions for next 6 hours:")
    for pred in future_predictions:
        print(f"  {pred['time']}: {pred['status']} (Prob: {pred['congestion_probability']:.2f})")
    
    print("\n=== Model Training Complete ===")
    print("The AI model is ready for traffic prediction in Bengkulu!")
    
    return predictor

# Run the main function
if __name__ == "__main__":
    predictor = main()
