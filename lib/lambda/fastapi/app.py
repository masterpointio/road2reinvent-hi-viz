"""FastAPI application for AWS Bill Burner API."""

from __future__ import annotations

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import burn_plan, roast
from models import HealthResponse

app = FastAPI(
    title="AWS Bill Burner API",
    description="API for generating AWS spending burn plans and roast commentary",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(burn_plan.router)
app.include_router(roast.router)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Health check endpoint."""
    agentcore_configured = bool(os.environ.get("AGENTCORE_AGENT_RUNTIME_ARN"))

    return HealthResponse(status="healthy", agentcore_configured=agentcore_configured)


@app.get("/")
def root():
    """Root endpoint to verify API is working."""
    return {
        "message": "AWS Bill Burner API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "burn_plan": "/burn-plan (POST)",
            "burn_plan_recent": "/burn-plan/recent (GET)",
            "roast": "/roast (POST)"
        }
    }
