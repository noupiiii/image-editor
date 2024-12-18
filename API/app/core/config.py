from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = [
        "http://frontend:3000",
        "http://54.36.101.216",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
