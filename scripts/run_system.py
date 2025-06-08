import subprocess
import sys
import time
import threading
import webbrowser
from pathlib import Path

def run_flask_api():
    """Run the Flask API server"""
    print("🚀 Starting Flask API server...")
    try:
        subprocess.run([sys.executable, "flask_api.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Flask API: {e}")
    except KeyboardInterrupt:
        print("🛑 Flask API server stopped")

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask', 'flask-cors', 'numpy', 'pandas', 
        'scikit-learn', 'joblib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def display_system_info():
    """Display system information and instructions"""
    print("=" * 60)
    print("🏙️  SMART TRAFFIC BENGKULU SYSTEM")
    print("=" * 60)
    print()
    print("📋 System Components:")
    print("   🌐 Frontend: HTML + CSS + JavaScript + Leaflet.js")
    print("   🤖 Backend: Python + Flask + Scikit-learn")
    print("   🗺️  Map: Interactive Bengkulu city map")
    print("   🔮 AI Model: Random Forest for traffic prediction")
    print()
    print("🛣️  Monitored Roads:")
    print("   • Jl. Sudirman")
    print("   • Jl. Ahmad Yani") 
    print("   • Jl. Suprapto")
    print("   • Jl. S. Parman")
    print("   • Jl. Raya UNIB")
    print()
    print("⚡ Features:")
    print("   • Real-time traffic monitoring")
    print("   • AI-powered congestion prediction")
    print("   • Route optimization recommendations")
    print("   • Interactive traffic heatmap")
    print("   • Future traffic forecasting")
    print()

def main():
    """Main function to run the entire system"""
    display_system_info()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("🔧 System Setup:")
    print("   1. Training AI model...")
    
    # Import and train the model
    try:
        from traffic_prediction_model import BengkuluTrafficPredictor
        predictor = BengkuluTrafficPredictor()
        predictor.train_model()
        print("   ✅ AI model trained successfully")
    except Exception as e:
        print(f"   ❌ Error training model: {e}")
        return
    
    print("   2. Starting web server...")
    
    # Start Flask API in a separate thread
    api_thread = threading.Thread(target=run_flask_api, daemon=True)
    api_thread.start()
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    print("   ✅ Web server started")
    print()
    print("🌐 Access the system:")
    print("   Frontend: Open index.html in your browser")
    print("   API: http://localhost:5000")
    print()
    print("📊 API Endpoints:")
    print("   GET  /api/traffic-status     - Current traffic status")
    print("   POST /api/predict            - Predict specific road")
    print("   POST /api/future-predictions - Future traffic forecast")
    print("   POST /api/route-optimization - Route recommendations")
    print()
    print("🎯 Usage Instructions:")
    print("   1. Open index.html in your web browser")
    print("   2. Explore the interactive map of Bengkulu")
    print("   3. Click on roads to see traffic status")
    print("   4. Use prediction panel to forecast traffic")
    print("   5. Get route recommendations between locations")
    print("   6. Toggle heatmap to see congestion patterns")
    print()
    print("⚠️  Note: This is a prototype system using simulated data")
    print("   In production, connect to real traffic sensors and APIs")
    print()
    print("🛑 Press Ctrl+C to stop the system")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 System shutdown initiated...")
        print("✅ Smart Traffic Bengkulu system stopped")

if __name__ == "__main__":
    main()
