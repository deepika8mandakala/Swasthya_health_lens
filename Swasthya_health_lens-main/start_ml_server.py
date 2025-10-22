#!/usr/bin/env python3
"""
Swasthya AI - ML Server Startup Script
This script installs dependencies, trains the model, and starts the Flask server
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print("Error:", e.stderr)
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    # Install packages
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python packages"
    )

def setup_ml_backend():
    """Set up the ML backend directory and files"""
    print("\n🔧 Setting up ML backend...")
    
    # Create backend directory if it doesn't exist
    backend_dir = Path('swasthya_ai_backend')
    backend_dir.mkdir(exist_ok=True)
    
    # Check if required files exist
    required_files = [
        'swasthya_ai_backend/app.py',
        'swasthya_ai_backend/train_model.py',
        'swasthya_ai_backend/food_database.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("✅ ML backend files are ready")
    return True

def train_model():
    """Train the ML model"""
    print("\n🤖 Training ML model...")
    
    # Check if dataset exists
    dataset_path = 'health_dataset_india_2000.csv'
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found: {dataset_path}")
        print("Please ensure the dataset file is in the current directory")
        return False
    
    # Change to backend directory and train model
    original_dir = os.getcwd()
    try:
        os.chdir('swasthya_ai_backend')
        
        # Run training script
        success = run_command(
            f"{sys.executable} train_model.py",
            "Training health risk prediction model"
        )
        
        return success
    finally:
        os.chdir(original_dir)

def start_server():
    """Start the Flask server"""
    print("\n🚀 Starting Flask server...")
    
    # Change to backend directory
    original_dir = os.getcwd()
    try:
        os.chdir('swasthya_ai_backend')
        
        # Start the Flask app
        print("Starting Swasthya AI Health Analysis API...")
        print("Server will be available at: http://localhost:5000")
        print("API documentation: http://localhost:5000/")
        print("Health check: http://localhost:5000/api/health")
        print("\nPress Ctrl+C to stop the server")
        print("="*60)
        
        # Run the Flask app
        subprocess.run([sys.executable, 'app.py'])
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
    finally:
        os.chdir(original_dir)

def main():
    """Main function"""
    print("🏥 Swasthya AI - Health Analysis System")
    print("="*50)
    print("This script will set up and start the ML-powered health analysis API")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies. Please check the error messages above.")
        return
    
    # Setup ML backend
    if not setup_ml_backend():
        print("\n❌ Failed to setup ML backend. Please check the error messages above.")
        return
    
    # Train model
    if not train_model():
        print("\n❌ Failed to train model. Please check the error messages above.")
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()


