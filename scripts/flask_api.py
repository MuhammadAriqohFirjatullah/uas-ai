from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import json
from datetime import datetime
import sys
import os

# Import our traffic prediction model
from traffic_prediction_model import BengkuluTrafficPredictor

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Initialize the predictor
predictor = BengkuluTrafficPredictor()
print("Training traffic prediction model...")
predictor.train_model()
print("Model ready for predictions!")

# Bengkulu roads configuration
BENGKULU_ROADS = {
    'sudirman': {'name': 'Jl. Sudirman', 'base_speed': 45, 'type': 'arterial'},
    'ahmad-yani': {'name': 'Jl. Ahmad Yani', 'base_speed': 50, 'type': 'arterial'},
    'suprapto': {'name': 'Jl. Suprapto', 'base_speed': 40, 'type': 'collector'},
    'parman': {'name': 'Jl. S. Parman', 'base_speed': 48, 'type': 'arterial'},
    'raya-unib': {'name': 'Jl. Raya UNIB', 'base_speed': 55, 'type': 'arterial'},
    'salak-raya': {'name': 'Jl. Salak Raya', 'base_speed': 42, 'type': 'collector'},
    'zainul-arifin': {'name': 'Jl. Zainul Arifin', 'base_speed': 38, 'type': 'local'},
    'veteran': {'name': 'Jl. Veteran', 'base_speed': 40, 'type': 'collector'},
    'pantai-nala': {'name': 'Jl. Pantai Nala', 'base_speed': 50, 'type': 'arterial'},
    'hibrida-raya': {'name': 'Jl. Hibrida Raya', 'base_speed': 45, 'type': 'collector'},
    'basuki-rahmat': {'name': 'Jl. Basuki Rahmat', 'base_speed': 35, 'type': 'local'},
    'khadijah': {'name': 'Jl. Khadijah', 'base_speed': 30, 'type': 'local'},
    'raya-padang-harapan': {'name': 'Jl. Raya Padang Harapan', 'base_speed': 52, 'type': 'arterial'},
    'lintas-sumatera': {'name': 'Jl. Lintas Sumatera', 'base_speed': 60, 'type': 'highway'},
    'raya-kandang': {'name': 'Jl. Raya Kandang', 'base_speed': 48, 'type': 'arterial'},
    'mahoni': {'name': 'Jl. Mahoni', 'base_speed': 35, 'type': 'local'},
    'raya-pagar-dewa': {'name': 'Jl. Raya Pagar Dewa', 'base_speed': 50, 'type': 'arterial'},
    'bypass': {'name': 'Jl. Bypass', 'base_speed': 65, 'type': 'highway'},
    'raya-sawah-lebar': {'name': 'Jl. Raya Sawah Lebar', 'base_speed': 45, 'type': 'collector'},
    'raya-teluk-segara': {'name': 'Jl. Raya Teluk Segara', 'base_speed': 50, 'type': 'arterial'}
}

@app.route('/')
def home():
    return jsonify({
        'message': 'Bengkulu Smart Traffic API',
        'version': '1.0',
        'endpoints': [
            '/api/predict',
            '/api/traffic-status',
            '/api/route-optimization',
            '/api/future-predictions'
        ]
    })

@app.route('/api/predict', methods=['POST'])
def predict_traffic():
    """Predict traffic congestion for a specific road"""
    try:
        data = request.get_json()
        road_id = data.get('road_id', 'sudirman')
        
        # Get current features for the road
        current_features = get_road_features(road_id)
        
        # Make prediction
        prediction = predictor.predict_congestion(current_features)
        
        # Add road information
        prediction['road_id'] = road_id
        prediction['road_name'] = BENGKULU_ROADS[road_id]['name']
        prediction['timestamp'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/traffic-status', methods=['GET'])
def get_traffic_status():
    """Get current traffic status for all roads"""
    try:
        traffic_status = {}
        
        for road_id in BENGKULU_ROADS.keys():
            features = get_road_features(road_id)
            prediction = predictor.predict_congestion(features)
            
            traffic_status[road_id] = {
                'name': BENGKULU_ROADS[road_id]['name'],
                'status': prediction['status'],
                'congestion_probability': prediction['congestion_probability'],
                'color': prediction['color'],
                'confidence': prediction['confidence'],
                'estimated_speed': calculate_speed_from_congestion(
                    BENGKULU_ROADS[road_id]['base_speed'],
                    prediction['congestion_probability']
                )
            }
        
        return jsonify({
            'success': True,
            'traffic_status': traffic_status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/future-predictions', methods=['POST'])
def get_future_predictions():
    """Get future traffic predictions for a road"""
    try:
        data = request.get_json()
        road_id = data.get('road_id', 'sudirman')
        hours_ahead = data.get('hours_ahead', 4)
        
        # Get current features
        current_features = get_road_features(road_id)
        
        # Get future predictions
        predictions = predictor.predict_future_traffic(current_features, hours_ahead)
        
        # Add road information to each prediction
        for pred in predictions:
            pred['road_id'] = road_id
            pred['road_name'] = BENGKULU_ROADS[road_id]['name']
            pred['estimated_speed'] = calculate_speed_from_congestion(
                BENGKULU_ROADS[road_id]['base_speed'],
                pred['congestion_probability']
            )
        
        return jsonify({
            'success': True,
            'road_id': road_id,
            'road_name': BENGKULU_ROADS[road_id]['name'],
            'predictions': predictions,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/route-optimization', methods=['POST'])
def optimize_route():
    """Find optimal route between two points"""
    try:
        data = request.get_json()
        start_point = data.get('start_point', '')
        end_point = data.get('end_point', '')
        
        if not start_point or not end_point:
            return jsonify({
                'success': False,
                'error': 'Start point and end point are required'
            }), 400
        
        # Get current traffic status for all roads
        traffic_status = {}
        for road_id in BENGKULU_ROADS.keys():
            features = get_road_features(road_id)
            prediction = predictor.predict_congestion(features)
            traffic_status[road_id] = prediction
        
        # Generate route recommendations
        routes = generate_route_recommendations(start_point, end_point, traffic_status)
        
        return jsonify({
            'success': True,
            'start_point': start_point,
            'end_point': end_point,
            'routes': routes,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_road_features(road_id):
    """Get current features for a specific road with enhanced road-specific factors"""
    now = datetime.now()
    
    # Enhanced road-specific variations based on road type and location
    road_factors = {
        'sudirman': {'traffic_multiplier': 1.3, 'base_volume': 450, 'congestion_prone': True},
        'ahmad-yani': {'traffic_multiplier': 1.2, 'base_volume': 400, 'congestion_prone': True},
        'suprapto': {'traffic_multiplier': 0.9, 'base_volume': 280, 'congestion_prone': False},
        'parman': {'traffic_multiplier': 1.1, 'base_volume': 350, 'congestion_prone': True},
        'raya-unib': {'traffic_multiplier': 0.8, 'base_volume': 220, 'congestion_prone': False},
        'salak-raya': {'traffic_multiplier': 1.0, 'base_volume': 300, 'congestion_prone': False},
        'zainul-arifin': {'traffic_multiplier': 1.4, 'base_volume': 380, 'congestion_prone': True},
        'veteran': {'traffic_multiplier': 1.2, 'base_volume': 320, 'congestion_prone': True},
        'pantai-nala': {'traffic_multiplier': 0.7, 'base_volume': 180, 'congestion_prone': False},
        'hibrida-raya': {'traffic_multiplier': 0.9, 'base_volume': 250, 'congestion_prone': False},
        'basuki-rahmat': {'traffic_multiplier': 1.5, 'base_volume': 420, 'congestion_prone': True},
        'khadijah': {'traffic_multiplier': 1.3, 'base_volume': 360, 'congestion_prone': True},
        'raya-padang-harapan': {'traffic_multiplier': 0.8, 'base_volume': 200, 'congestion_prone': False},
        'lintas-sumatera': {'traffic_multiplier': 0.6, 'base_volume': 150, 'congestion_prone': False},
        'raya-kandang': {'traffic_multiplier': 0.9, 'base_volume': 240, 'congestion_prone': False},
        'mahoni': {'traffic_multiplier': 1.1, 'base_volume': 290, 'congestion_prone': False},
        'raya-pagar-dewa': {'traffic_multiplier': 0.7, 'base_volume': 190, 'congestion_prone': False},
        'bypass': {'traffic_multiplier': 0.5, 'base_volume': 120, 'congestion_prone': False},
        'raya-sawah-lebar': {'traffic_multiplier': 0.8, 'base_volume': 210, 'congestion_prone': False},
        'raya-teluk-segara': {'traffic_multiplier': 0.6, 'base_volume': 160, 'congestion_prone': False}
    }
    
    factor = road_factors.get(road_id, road_factors['sudirman'])
    road_info = BENGKULU_ROADS.get(road_id, BENGKULU_ROADS['sudirman'])
    
    # Add rush hour multiplier for congestion-prone roads
    rush_hour_multiplier = 1.0
    if factor['congestion_prone'] and ((7 <= now.hour <= 9) or (17 <= now.hour <= 19)):
        rush_hour_multiplier = 1.5
    elif factor['congestion_prone'] and (12 <= now.hour <= 13):
        rush_hour_multiplier = 1.2
    
    # Calculate volume with time-based variations
    base_volume = factor['base_volume'] * factor['traffic_multiplier'] * rush_hour_multiplier
    volume_variation = np.random.normal(0, 0.3)  # 30% variation
    final_volume = int(base_volume * (1 + volume_variation))
    final_volume = max(50, final_volume)  # Minimum 50 vehicles/hour
    
    features = [
        now.hour,  # hour
        now.weekday(),  # day_of_week
        now.month,  # month
        1 if now.weekday() >= 5 else 0,  # is_weekend
        1 if (7 <= now.hour <= 9) or (17 <= now.hour <= 19) else 0,  # is_rush_hour
        np.random.beta(2, 1),  # weather_score
        0,  # event_factor
        road_info['base_speed'],  # historical_avg_speed
        final_volume  # volume_last_hour
    ]
    
    return features

def calculate_speed_from_congestion(base_speed, congestion_prob):
    """Calculate estimated speed based on congestion probability"""
    speed_reduction = congestion_prob * 0.6  # Max 60% speed reduction
    estimated_speed = base_speed * (1 - speed_reduction)
    return max(5, int(estimated_speed))  # Minimum 5 km/h

def generate_route_recommendations(start, end, traffic_status):
    """Generate enhanced route recommendations with more road combinations"""
    # Enhanced route generation with more realistic combinations
    routes = [
        {
            'name': 'Rute Utama (Pusat Kota)',
            'roads': ['sudirman', 'ahmad-yani', 'veteran'],
            'distance_km': 5.8,
            'estimated_duration_minutes': 18,
            'traffic_score': (traffic_status['sudirman']['congestion_probability'] + 
                            traffic_status['ahmad-yani']['congestion_probability'] +
                            traffic_status['veteran']['congestion_probability']) / 3,
            'road_types': ['arterial', 'arterial', 'collector']
        },
        {
            'name': 'Rute Bypass (Cepat)',
            'roads': ['bypass', 'lintas-sumatera'],
            'distance_km': 8.2,
            'estimated_duration_minutes': 12,
            'traffic_score': (traffic_status['bypass']['congestion_probability'] + 
                            traffic_status['lintas-sumatera']['congestion_probability']) / 2,
            'road_types': ['highway', 'highway']
        },
        {
            'name': 'Rute Pantai (Scenic)',
            'roads': ['pantai-nala', 'raya-teluk-segara', 'raya-kandang'],
            'distance_km': 7.5,
            'estimated_duration_minutes': 16,
            'traffic_score': (traffic_status['pantai-nala']['congestion_probability'] + 
                            traffic_status['raya-teluk-segara']['congestion_probability'] +
                            traffic_status['raya-kandang']['congestion_probability']) / 3,
            'road_types': ['arterial', 'arterial', 'arterial']
        },
        {
            'name': 'Rute Universitas',
            'roads': ['raya-unib', 'hibrida-raya', 'salak-raya'],
            'distance_km': 6.9,
            'estimated_duration_minutes': 15,
            'traffic_score': (traffic_status['raya-unib']['congestion_probability'] + 
                            traffic_status['hibrida-raya']['congestion_probability'] +
                            traffic_status['salak-raya']['congestion_probability']) / 3,
            'road_types': ['arterial', 'collector', 'collector']
        },
        {
            'name': 'Rute Dalam Kota (Pendek)',
            'roads': ['zainul-arifin', 'basuki-rahmat', 'khadijah'],
            'distance_km': 4.2,
            'estimated_duration_minutes': 22,
            'traffic_score': (traffic_status['zainul-arifin']['congestion_probability'] + 
                            traffic_status['basuki-rahmat']['congestion_probability'] +
                            traffic_status['khadijah']['congestion_probability']) / 3,
            'road_types': ['local', 'local', 'local']
        },
        {
            'name': 'Rute Alternatif Utara',
            'roads': ['raya-pagar-dewa', 'raya-padang-harapan', 'mahoni'],
            'distance_km': 8.8,
            'estimated_duration_minutes': 14,
            'traffic_score': (traffic_status['raya-pagar-dewa']['congestion_probability'] + 
                            traffic_status['raya-padang-harapan']['congestion_probability'] +
                            traffic_status['mahoni']['congestion_probability']) / 3,
            'road_types': ['arterial', 'arterial', 'local']
        },
        {
            'name': 'Rute Selatan (Sawah Lebar)',
            'roads': ['raya-sawah-lebar', 'suprapto', 'parman'],
            'distance_km': 7.1,
            'estimated_duration_minutes': 17,
            'traffic_score': (traffic_status['raya-sawah-lebar']['congestion_probability'] + 
                            traffic_status['suprapto']['congestion_probability'] +
                            traffic_status['parman']['congestion_probability']) / 3,
            'road_types': ['collector', 'collector', 'arterial']
        }
    ]
    
    # Sort routes by combined score (traffic + distance efficiency)
    for route in routes:
        # Calculate efficiency score (lower is better)
        time_penalty = route['estimated_duration_minutes'] / 60  # Convert to hours
        distance_penalty = route['distance_km'] / 10  # Normalize distance
        traffic_penalty = route['traffic_score'] * 2  # Weight traffic heavily
        
        route['efficiency_score'] = time_penalty + distance_penalty + traffic_penalty
    
    routes.sort(key=lambda x: x['efficiency_score'])
    
    # Add recommendation flag and enhanced traffic status
    for i, route in enumerate(routes):
        route['recommended'] = i == 0
        route['traffic_level'] = 'Lancar' if route['traffic_score'] < 0.3 else \
                                'Sedang' if route['traffic_score'] < 0.7 else 'Macet'
        
        # Adjust duration based on traffic with road type consideration
        base_duration = route['estimated_duration_minutes']
        traffic_delay = route['traffic_score'] * 15  # Max 15 minutes delay
        
        # Highway and arterial roads handle traffic better
        if 'highway' in route['road_types']:
            traffic_delay *= 0.5
        elif 'arterial' in route['road_types'] and 'local' not in route['road_types']:
            traffic_delay *= 0.7
        
        route['estimated_duration_minutes'] = int(base_duration + traffic_delay)
        
        # Add route characteristics
        if 'highway' in route['road_types']:
            route['characteristics'] = '🛣️ Jalan Tol/Bypass'
        elif route['traffic_score'] < 0.3:
            route['characteristics'] = '✅ Lancar'
        elif len([r for r in route['road_types'] if r == 'local']) > 1:
            route['characteristics'] = '🏘️ Jalan Lokal'
        else:
            route['characteristics'] = '🚗 Jalan Utama'
    
    return routes[:5]  # Return top 5 routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_trained': predictor.is_trained,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Bengkulu Smart Traffic API...")
    print("API will be available at: http://localhost:5000")
    print("Available endpoints:")
    print("  GET  /                     - API information")
    print("  POST /api/predict          - Predict traffic for specific road")
    print("  GET  /api/traffic-status   - Get current traffic status")
    print("  POST /api/future-predictions - Get future traffic predictions")
    print("  POST /api/route-optimization - Get optimal route recommendations")
    print("  GET  /api/health           - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
