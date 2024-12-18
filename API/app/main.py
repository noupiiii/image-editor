from fastapi import FastAPI
from app.core.config import setup_cors
from app.api.endpoints import router as api_router

app = FastAPI(title="Color Palette API", version="1.0.0")

# Configure middlewares (e.g., CORS)
setup_cors(app)

# Include API routes
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Color Palette API!"}
