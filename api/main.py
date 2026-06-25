from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import router
from api.recommendations import (
    router as recommendations_router
)


app = FastAPI(
    title="Letterboxd Recommender",
    description=(
        "Upload a Letterboxd export ZIP "
        "and receive personalized movie recommendations."
    ),
    version="1.0.0"
)

# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --------------------------------------------------
# API Routes
# --------------------------------------------------

app.include_router(
    router,
    prefix="/api",
    tags=["Letterboxd Recommender"]
)
app.include_router(
    recommendations_router,
    prefix="/api",
    tags=["Recommendations"]
)

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():

    return {

        "application":
            "Letterboxd Recommender",

        "version":
            "1.0.0",

        "status":
            "running",

        "docs":
            "/docs"
    }

# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {

        "status":
            "healthy"
    }