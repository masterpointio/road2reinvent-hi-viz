"""Router for roast generation endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends, status

from models import RoastRequest, RoastResponse, BurnPlan
from services.strands_service import StrandsService
from utils.agentcore_client import (
    AgentCoreClient,
    AgentCoreError,
    AgentTimeoutError,
    AgentRateLimitError
)
from routers.burn_plan import get_agentcore_client, get_strands_service

router = APIRouter(prefix="/roast", tags=["roast"])


@router.post("", response_model=RoastResponse)
async def generate_roast(
    request: RoastRequest,
    strands_service: StrandsService = Depends(get_strands_service)
) -> RoastResponse:
    """Generate roast commentary for a burn session.

    Args:
        request: Roast request with session ID
        strands_service: Strands service instance

    Returns:
        Generated roast commentary

    Raises:
        HTTPException: If roast generation fails
    """
    try:
        # TODO: Retrieve burn plan from DynamoDB using session_id
        # For now, return a placeholder error
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Session retrieval not yet implemented. Store burn plan in request for now."
        )

        # burn_plan = session_service.get_session(request.session_id)
        # if not burn_plan:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail=f"Session {request.session_id} not found"
        #     )

        # roast_text = strands_service.generate_roast(burn_plan)

        # return RoastResponse(roast_text=roast_text)

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

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
