"""Schema definitions for AWS spending analysis output."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class ServiceCost(BaseModel):
    """Cost breakdown for a single AWS service."""

    service_name: str = Field(description="AWS service name (e.g., 'EC2', 'RDS', 'S3')")
    instance_type: str = Field(description="Instance type or resource configuration (e.g., 'r7g.16xlarge', 'db.r6g.large', 'Standard Storage')")
    quantity: int = Field(description="Number of instances or resources", default=1)
    unit_cost: float = Field(description="Cost per unit (per hour, per GB, etc.)")
    total_cost: float = Field(description="Total cost for this service in dollars")
    start_day: int = Field(description="Day number when the service was started (0 = beginning, 1 = Day 1, etc.)")
    end_day: int = Field(description="Day number when the service was stopped or -1 for end of timeline")
    duration_used: str = Field(description="How long the service was running (e.g., '30 days', '2 weeks', '720 hours', 'entire timeline')")
    usage_pattern: str = Field(description="Usage pattern (e.g., 'Running 24/7', 'Burst usage', 'Idle')")
    waste_factor: str = Field(
        description="Why this is wasteful (e.g., 'Over-provisioned for workload', 'Redundant service', 'Unnecessary for use case')"
    )
    roast: str = Field(
        description="A brutal one or two-liner roast specifically calling out this service's wasteful usage. Be savage and funny."
    )


class SpendingAnalysis(BaseModel):
    """Complete AWS spending forensics analysis."""

    total_amount: str = Field(description="Total amount spent as a string (e.g., '$1000', '$10000')")
    timeline_days: int = Field(description="Timeline period in days (e.g., 30, 14, 60)")
    efficiency_level: str = Field(
        description="Efficiency level: 'Mildly dumb', 'Moderately stupid', 'Very stupid', or 'Brain damage'"
    )
    architecture_type: str = Field(
        description="Architecture type: 'serverless', 'kubernetes', 'traditional', or 'mixed'"
    )
    burning_style: str = Field(
        description="Burning style: 'horizontal' (regular spending over timeline) or 'vertical' (one-shot bursts)"
    )
    services_deployed: List[ServiceCost] = Field(
        description="List of AWS services that were deployed with their configurations and costs"
    )
    total_calculated_cost: float = Field(
        description="Sum of all service costs in dollars (should approximately match total_amount)"
    )
    deployment_scenario: str = Field(
        description="Detailed narrative describing the likely use case, what happened, and why these choices were made"
    )
    key_mistakes: List[str] = Field(
        description="List of 3-5 key mistakes or poor decisions that led to this wasteful spending"
    )
    recommendations: List[str] = Field(
        description="List of 3-5 specific recommendations for what should have been done instead to reduce costs"
    )
    roast: str = Field(
        description="A brutal, savage, and merciless roast of the wasteful spending and terrible decisions. Be creative, funny, and absolutely ruthless in calling out the absurdity of these choices."
    )



