# ML Model Deployment Project

A production-ready full-stack application demonstrating how to serve a Machine Learning model.

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py            # FastAPI application
│   └── model.pkl          # Pickled ML Model (generated via scripts/train_dummy_model.py)
├── frontend/
│   └── app.py             # Streamlit web application
├── scripts/
│   └── train_dummy_model.py # Script to generate a dummy model for initial testing
├── requirements.txt       # Shared dependencies
├── Dockerfile.backend     # Container def for backend
├── Dockerfile.frontend    # Container def for frontend
├── docker-compose.yml     # Orchestration to run both together
└── README.md              # Project documentation
```

## 🚀 Setup Instructions (Local Development)

### 1. Create a Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the Dummy Model
Run this script to generate `model.pkl` in the `backend/` folder:
```bash
python scripts/train_dummy_model.py
```

### 4. Run the Application
**Terminal 1 (Backend):**
```bash
cd backend
uvicorn main:app --reload --port 8000
```
Swagger UI will be available at: http://localhost:8000/docs

**Terminal 2 (Frontend):**
```bash
cd frontend
streamlit run app.py
```
App will be available at: http://localhost:8501

## 🐳 Running with Docker

You can spin up the entire application using Docker Compose:

```bash
# Don't forget to generate the model first!
python scripts/train_dummy_model.py

# Build and start the containers
docker-compose up --build
```

## 🌐 Deployment Pipeline

### Backend (Render / Railway)
1. Push this repository to GitHub.
2. In Render/Railway, create a new "Web Service" from your GitHub repo.
3. Configure the Root Directory to `backend` OR use the `Dockerfile.backend`.
4. Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. The platform will provide a live URL (e.g., `https://my-api.onrender.com`).

### Frontend (Streamlit Community Cloud)
1. Log in to [share.streamlit.io](https://share.streamlit.io/).
2. Create a new app pointing to your repository.
3. Set the Main file path to `frontend/app.py`.
4. In Advanced Settings, add the Environment Variable:
   `API_URL = https://my-api.onrender.com/predict` (replace with your backend's actual deployed URL).
