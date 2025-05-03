from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

# Import API routers
from ..api import tournaments, matches, points, analyses, recommendations, agents

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Tennis Tournament Analysis System",
    description="API for the Tennis Tournament Analysis System",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Tennis Tournament Analysis System API",
        "status": "operational",
        "version": "0.1.0"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_version": "0.1.0",
    }

# Include routers from other modules
app.include_router(tournaments.router)
app.include_router(matches.router)
app.include_router(points.router)
app.include_router(analyses.router)
app.include_router(recommendations.router)
app.include_router(agents.router)

if __name__ == "__main__":
    host = os.getenv("API_HOST", "localhost")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run("main:app", host=host, port=port, reload=debug)
