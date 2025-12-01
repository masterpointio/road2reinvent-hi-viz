"""Service layer for Strands agent integration via AgentCore SDK."""

from __future__ import annotations

import json
from typing import Dict, Any

from utils.agentcore_client import AgentCoreClient, AgentCoreError
from models import BurnConfig, BurnPlan


class StrandsService:
    """Service for interacting with Strands agents."""

    def __init__(self, agentcore_client: AgentCoreClient):
        """Initialize Strands service.

        Args:
            agentcore_client: Configured AgentCore client instance
        """
        self.client = agentcore_client

    def generate_burn_plan(self, config: BurnConfig) -> BurnPlan:
        """Generate burn plan using Strands agent.

        Args:
            config: Burn configuration

        Returns:
            Generated burn plan

        Raises:
            AgentCoreError: If agent invocation fails
        """
        # Convert config to dict for agent
        config_dict = {
            "amount": config.amount,
            "timeline": config.timeline,
            "stupidity": config.stupidity,
            "architecture": config.architecture,
            "burning_style": config.burning_style
        }

        # Invoke agent
        response = self.client.generate_burn_plan(config_dict)

        # Parse and validate response
        try:
            # Check if response is wrapped in 'analysis' key
            if isinstance(response, dict) and 'analysis' in response:
                burn_plan_data = response['analysis']
            else:
                burn_plan_data = response
            
            burn_plan = BurnPlan(**burn_plan_data)
        except Exception as e:
            raise AgentCoreError(f"Failed to parse burn plan response: {e}")

        # Validate cost matches requested amount (within 10%)
        self._validate_cost_match(config.amount, burn_plan.total_calculated_cost)

        return burn_plan

    def generate_roast(self, burn_plan: BurnPlan) -> str:
        """Generate roast commentary for burn plan.

        Args:
            burn_plan: Burn plan to roast

        Returns:
            Roast commentary text

        Raises:
            AgentCoreError: If agent invocation fails
        """
        # Build context for roast
        context = {
            "total_amount": burn_plan.total_amount,
            "services": [
                {
                    "service_name": svc.service_name,
                    "total_cost": svc.total_cost,
                    "waste_factor": svc.waste_factor
                }
                for svc in burn_plan.services_deployed
            ],
            "stupidity_level": burn_plan.efficiency_level
        }

        # Invoke agent
        roast_text = self.client.generate_roast(context)

        if not roast_text:
            raise AgentCoreError("Agent returned empty roast text")

        return roast_text

    def _validate_cost_match(self, requested_amount: str, calculated_cost: float) -> None:
        """Validate that calculated cost matches requested amount.

        Args:
            requested_amount: Requested amount string (e.g., "$1000")
            calculated_cost: Calculated total cost

        Raises:
            AgentCoreError: If costs don't match within tolerance
        """
        # Extract numeric value from amount string
        import re
        match = re.search(r"[\d,]+\.?\d*", requested_amount)
        if not match:
            return  # Can't validate, skip

        requested_value = float(match.group().replace(",", ""))

        # Check within 10% tolerance
        tolerance = 0.10
        lower_bound = requested_value * (1 - tolerance)
        upper_bound = requested_value * (1 + tolerance)

        if not (lower_bound <= calculated_cost <= upper_bound):
            raise AgentCoreError(
                f"Cost mismatch: requested {requested_amount} ({requested_value}), "
                f"but calculated {calculated_cost:.2f} (outside 10% tolerance)"
            )
