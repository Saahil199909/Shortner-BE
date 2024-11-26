from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router



app = FastAPI()


# Include API routers
app.include_router(api_router)

origins = [
    "http://localhost:5173",  # Your React app's URL
    "http://192.168.1.6:5173",
    "http://192.168.1.47:5173",
    "http://192.168.0.106:5173"
    # Add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)