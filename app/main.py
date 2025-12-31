from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routers import expenses

# Initialize FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="API for tracking expenses with full CRUD operations",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(expenses.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    init_db()


@app.get("/", tags=["health"])
def root():
    """Root endpoint for health check."""
    return {
        "message": "Expenses Tracker API",
        "version": settings.api_version,
        "docs": "/docs"
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

