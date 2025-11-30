"""Pydantic models for API request/response validation."""

from __future__ import annotations

from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class BurnConfig(BaseModel):
    """Configuration for burn plan generation."""

    amount: str = Field(description="Spending amount (e.g., '$1000' or '₹50000')")
    timeline: int = Field(description="Timeline in days", gt=0)
    stupidity: Literal["Mildly dumb", "Moderately stupid", "Very stupid", "Brain damage"] = Field(
        description="Efficiency level of resource usage"
    )
    architecture: Literal["serverless", "kubernetes", "traditional", "mixed"] = Field(
        description="Type of architecture to burn money on"
    )
    burning_style: Literal["horizontal", "vertical"] = Field(
        description="Burning style: horizontal (regular) or vertical (bursts)"
    )


class ServiceCost(BaseModel):
    """Cost breakdown for a single AWS service."""

    service_name: str = Field(description="AWS service name (e.g., 'EC2', 'RDS', 'S3')")
    instance_type: Optional[str] = Field(default=None, description="Instance type or resource configuration")
    quantity: int = Field(description="Number of instances or resources", default=1)
    start_day: int = Field(description="Day when service starts (0-based)", default=0)
    end_day: int = Field(description="Day when service ends (-1 for end of timeline)", default=-1)
    duration_used: int = Field(description="Duration in days the service was used", default=0)
    unit_cost: float = Field(description="Cost per unit (hourly or daily rate)")
    total_cost: float = Field(description="Total cost for this service in dollars")
    usage_pattern: Optional[str] = Field(default=None, description="Usage pattern description")
    waste_factor: Optional[str] = Field(default=None, description="Waste factor explanation")


class BurnPlan(BaseModel):
    """Complete burn plan with services and analysis."""

    total_amount: str = Field(description="Total spending amount")
    timeline_days: int = Field(description="Timeline in days")
    efficiency_level: str = Field(description="Efficiency level")
    services_deployed: List[ServiceCost] = Field(description="List of AWS services deployed")
    total_calculated_cost: float = Field(description="Sum of all service costs")
    deployment_scenario: str = Field(description="Narrative description of deployment")
    key_mistakes: List[str] = Field(description="List of key mistakes made")
    recommendations: List[str] = Field(description="List of recommendations")


class BurnPlanRequest(BaseModel):
    """Request model for burn plan generation."""

    config: BurnConfig = Field(description="Burn configuration")


class BurnPlanResponse(BaseModel):
    """Response model for burn plan generation."""

    session_id: str = Field(description="Unique session identifier")
    burn_plan: BurnPlan = Field(description="Generated burn plan")


class RoastRequest(BaseModel):
    """Request model for roast generation."""

    session_id: str = Field(description="Session ID to roast")


class RoastResponse(BaseModel):
    """Response model for roast generation."""

    roast_text: str = Field(description="Generated roast commentary")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(description="Service status")
    agentcore_configured: bool = Field(description="Whether AgentCore is configured")
