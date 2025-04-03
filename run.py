#!/usr/bin/env python3
"""
Run script for the LLM Prompt Engineering Framework.
This script provides a unified interface for starting different variants
of the application and performing basic setup tasks.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
import webbrowser
import time
from concurrent.futures import ThreadPoolExecutor


def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import pandas
        import requests
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        return False


def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("Creating .env file from .env.example...")
            with open(".env.example", "r") as example:
                with open(".env", "w") as env:
                    env.write(example.read())
            print("Created .env file. Please edit it with your API keys.")
        else:
            print("Warning: .env.example not found. You may need to create .env manually.")


def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ["templates", "stored_states"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Ensured directory exists: {directory}")


def open_browser(port=8501, delay=2):
    """Open browser after a short delay to allow the server to start"""
    def _open_browser():
        time.sleep(delay)
        webbrowser.open(f"http://localhost:{port}")
    
    with ThreadPoolExecutor() as executor:
        executor.submit(_open_browser)


def run_app(dev_mode=False, port=8501, no_browser=False):
    """Run the Streamlit application"""
    app_script = "dev_app.py" if dev_mode else "app.py"
    
    if not no_browser:
        open_browser(port=port)
    
    cmd = [
        "streamlit", "run", app_script,
        "--server.port", str(port),
    ]
    
    print(f"Starting {'development' if dev_mode else 'production'} server on port {port}...")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped.")


def main():
    """Main function to parse arguments and run the application"""
    parser = argparse.ArgumentParser(description="LLM Prompt Engineering Framework")
    parser.add_argument("--dev", action="store_true", help="Run in development mode with additional debugging tools")
    parser.add_argument("--port", type=int, default=8501, help="Port to run the server on")
    parser.add_argument("--setup-only", action="store_true", help="Only perform setup without running the app")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    
    args = parser.parse_args()
    
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Perform setup steps
    if not check_dependencies():
        print("Please install missing dependencies with: pip install -r requirements.txt")
        return 1
    
    create_env_file()
    create_directories()
    
    if args.setup_only:
        print("Setup completed successfully.")
        return 0
    
    # Run the application
    run_app(dev_mode=args.dev, port=args.port, no_browser=args.no_browser)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
