#!/usr/bin/env python3
"""
Sports Dashboard Setup Script
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is 3.11 or higher"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            shutil.copy('.env.example', '.env')
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your API keys")
        else:
            print("❌ .env.example file not found")
            return False
    else:
        print("✅ .env file already exists")
    return True

def install_dependencies():
    """Install Python dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['.streamlit', 'pages']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🏈 Sports Dashboard Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: streamlit run main.py")
    print("3. Open your browser to http://localhost:8501")

if __name__ == "__main__":
    main()
