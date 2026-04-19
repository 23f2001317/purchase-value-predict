import os
import sys
import time
import subprocess
import streamlit as st
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# 1. Start the FastAPI backend in the background using Streamlit's cache
# (This ensures it only starts once per session/deployment)
@st.cache_resource
def start_backend():
    print("Starting FastAPI backend...")
    
    # Check if the dummy model exists, if not, generate it
    model_path = os.path.join(os.path.dirname(__file__), "backend", "model.pkl")
    if not os.path.exists(model_path):
        subprocess.run([sys.executable, "scripts/train_dummy_model.py"])
        
    # Start the Uvicorn server in a separate background process
    if not is_port_in_use(8000):
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(3)  # Give the server a few seconds to boot up
        return process
    return None

# Initialize the backend
backend_process = start_backend()

# 2. Execute the frontend UI
# This reads and runs the frontend script directly so Streamlit renders it here
frontend_file = os.path.join(os.path.dirname(__file__), "frontend", "app.py")

with open(frontend_file, "r") as f:
    # We execute the frontend code in the current Streamlit context
    exec(f.read())
