"""Router for burn plan generation endpoints."""

from __future__ import annotations

import uuid
from typing import Dict, Any, List

from fastapi import APIRouter, HTTPException, Depends, status

from models import BurnPlanRequest, BurnPlanResponse, BurnPlan
from services.strands_service import StrandsService
from services.dynamodb_service import DynamoDBService
from utils.agentcore_client import (
    AgentCoreClient,
    AgentCoreError,
    AgentTimeoutError,
    AgentRateLimitError
)

router = APIRouter(prefix="/burn-plan", tags=["burn-plan"])


def get_agentcore_client() -> AgentCoreClient:
    """Dependency to get AgentCore client instance."""
    try:
        return AgentCoreClient()
    except AgentCoreError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AgentCore client initialization failed: {str(e)}"
        )


def get_strands_service(
    client: AgentCoreClient = Depends(get_agentcore_client)
) -> StrandsService:
    """Dependency to get Strands service instance."""
    return StrandsService(client)


def get_dynamodb_service() -> DynamoDBService:
    """Dependency to get DynamoDB service instance."""
    return DynamoDBService()


@router.post("", response_model=BurnPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_burn_plan(
    request: BurnPlanRequest,
    strands_service: StrandsService = Depends(get_strands_service),
    dynamodb_service: DynamoDBService = Depends(get_dynamodb_service)
) -> BurnPlanResponse:
    """Generate a new burn plan.

    Args:
        request: Burn plan configuration
        strands_service: Strands service instance
        dynamodb_service: DynamoDB service instance

    Returns:
        Generated burn plan with session ID

    Raises:
        HTTPException: If burn plan generation fails
    """
    try:
        # Generate burn plan via Strands agent
        burn_plan = strands_service.generate_burn_plan(request.config)

        # Generate session ID
        session_id = str(uuid.uuid4())

        # Store burn plan in DynamoDB
        dynamodb_service.store_burn_plan(session_id, burn_plan)

        return BurnPlanResponse(
            session_id=session_id,
            burn_plan=burn_plan
        )

    except AgentTimeoutError as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Agent request timed out: {str(e)}"
        )

    except AgentRateLimitError as e:
        headers = {}
        if e.retry_after:
            headers["Retry-After"] = str(e.retry_after)

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded: {str(e)}",
            headers=headers
        )

    except AgentCoreError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Agent error: {str(e)}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/recent", response_model=List[dict], status_code=status.HTTP_200_OK)
async def get_recent_burn_plans(
    limit: int = 5,
    dynamodb_service: DynamoDBService = Depends(get_dynamodb_service)
) -> List[dict]:
    """Get the most recent burn plans.

    Args:
        limit: Maximum number of burn plans to retrieve (default: 5)
        dynamodb_service: DynamoDB service instance

    Returns:
        List of recent burn plans with session IDs and timestamps

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        if limit < 1 or limit > 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be between 1 and 20"
            )

        burn_plans = dynamodb_service.get_recent_burn_plans(limit)

        return burn_plans

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve burn plans: {str(e)}"
        )
