"""AgentCore SDK client wrapper for Strands agent integration."""

from __future__ import annotations

import json
import os
import time
import uuid
from typing import Any, Dict, Optional

try:
    import boto3
except ImportError:
    boto3 = None


class AgentCoreError(Exception):
    """Base exception for AgentCore client errors."""
    pass


class AgentTimeoutError(AgentCoreError):
    """Raised when agent invocation times out."""
    pass


class AgentRateLimitError(AgentCoreError):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class AgentConnectionError(AgentCoreError):
    """Raised when connection to AgentCore fails."""
    pass


class AgentCoreClient:
    """Client for interacting with Strands agents via AgentCore SDK."""

    def __init__(
        self,
        agent_runtime_arn: Optional[str] = None,
        region: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 2
    ):
        """Initialize AgentCore client with IAM authentication.

        Args:
            agent_runtime_arn: AgentCore agent runtime ARN (defaults to AGENTCORE_AGENT_RUNTIME_ARN env var)
            region: AWS region (defaults to AWS_REGION env var)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.agent_runtime_arn = agent_runtime_arn or os.environ.get("AGENTCORE_AGENT_RUNTIME_ARN", "")
        self.region = region or os.environ.get("AWS_REGION", "us-east-1")
        self.timeout = timeout
        self.max_retries = max_retries

        if not self.agent_runtime_arn:
            raise AgentCoreError("AGENTCORE_AGENT_RUNTIME_ARN is required")

        if boto3 is None:
            raise AgentCoreError("boto3 package is not installed")

        try:
            # Initialize boto3 bedrock-agentcore client with IAM authentication
            # The Lambda execution role will provide credentials automatically
            self.client = boto3.client(
                'bedrock-agentcore',
                region_name=self.region
            )
        except Exception as e:
            raise AgentConnectionError(f"Failed to initialize AgentCore client: {e}")

    def generate_burn_plan(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AWS spending burn plan using Strands agent.

        Args:
            config: Burn configuration with keys:
                - amount: Spending amount (number)
                - timeline: Timeline in days (int)
                - stupidity: Efficiency level (str)
                - architecture: Architecture type (str)
                - burning_style: Burning style (str)

        Returns:
            Structured burn plan with services and costs

        Raises:
            AgentTimeoutError: If agent invocation times out
            AgentCoreError: If agent returns invalid response
        """
        instructions = self._build_burn_plan_instructions(config)
        parameters = {
            "amount": config.get("amount"),
            "timeline": config.get("timeline"),
            "stupidity_level": config.get("stupidity"),
            "architecture": config.get("architecture"),
            "burning_style": config.get("burning_style")
        }

        return self._invoke_agent(
            task_name="burn-plan-generator",
            instructions=instructions,
            parameters=parameters
        )

    def generate_roast(self, context: Dict[str, Any]) -> str:
        """Generate roast commentary for spending scenario.

        Args:
            context: Roast context with keys:
                - total_amount: Total spending amount
                - services: List of services deployed
                - stupidity_level: Efficiency level

        Returns:
            Roast commentary text

        Raises:
            AgentTimeoutError: If agent invocation times out
            AgentCoreError: If agent returns invalid response
        """
        instructions = self._build_roast_instructions(context)
        parameters = {
            "total_amount": context.get("total_amount"),
            "services": context.get("services", []),
            "stupidity_level": context.get("stupidity_level")
        }

        result = self._invoke_agent(
            task_name="roast-generator",
            instructions=instructions,
            parameters=parameters
        )

        return result.get("roast_text", "")

    def _build_burn_plan_instructions(self, config: Dict[str, Any]) -> str:
        """Build instructions for burn plan generation."""
        amount = config.get("amount", "$0")
        timeline = config.get("timeline", 30)
        stupidity = config.get("stupidity", "Moderately stupid")
        architecture = config.get("architecture", "mixed")
        burning_style = config.get("burning_style", "horizontal")

        return f"""Generate an AWS spending burn plan for {amount} over {timeline} days.

Architecture: {architecture}
Burning Style: {burning_style}
Efficiency Level: {stupidity}

Return a structured JSON with:
- total_amount: spending amount
- timeline_days: timeline in days
- efficiency_level: efficiency level
- services_deployed: array of services with cost breakdowns
- deployment_scenario: narrative description
- key_mistakes: list of mistakes made
- recommendations: list of recommendations

Ensure total costs match {amount} within 10% variance."""

    def _build_roast_instructions(self, context: Dict[str, Any]) -> str:
        """Build instructions for roast generation."""
        total_amount = context.get("total_amount", "$0")
        stupidity = context.get("stupidity_level", "Unknown")

        return f"""Generate a witty roast commentary for someone who spent {total_amount} on AWS.

Efficiency Level: {stupidity}

Be snarky but not mean. Compare costs to relatable items like burritos, coffee, or Netflix.
Focus on the absurdity of the spending choices."""

    def _invoke_agent(
        self,
        task_name: str,
        instructions: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Invoke Strands agent with retry logic.

        Args:
            task_name: Name of the agent task
            instructions: Task instructions
            parameters: Task parameters

        Returns:
            Agent response as dictionary

        Raises:
            AgentTimeoutError: If agent times out
            AgentRateLimitError: If rate limited
            AgentConnectionError: If connection fails
            AgentCoreError: For other errors
        """
        last_error = None

        for attempt in range(self.max_retries + 1):
            try:
                start_time = time.time()

                # Generate unique session ID (must be 33+ characters)
                session_id = str(uuid.uuid4()) + "-" + str(uuid.uuid4())[:5]

                # Build payload with prompt and parameters
                payload = json.dumps({
                    "prompt": instructions,
                    **parameters
                })

                # Invoke agent via boto3 bedrock-agentcore client
                response = self.client.invoke_agent_runtime(
                    agentRuntimeArn=self.agent_runtime_arn,
                    runtimeSessionId=session_id,
                    payload=payload,
                    qualifier="DEFAULT"
                )

                elapsed = time.time() - start_time

                # Log invocation
                print(f"Agent invocation: task={task_name}, elapsed={elapsed:.2f}s, attempt={attempt + 1}, session={session_id}")

                # Parse response
                response_body = response['response'].read()
                response_data = json.loads(response_body)

                # Validate response
                if not response_data or not isinstance(response_data, dict):
                    raise AgentCoreError("Invalid response format from agent")

                return response_data

            except self.client.exceptions.ThrottlingException as e:
                retry_after = self._extract_retry_after(str(e))
                last_error = AgentRateLimitError(
                    f"Rate limit exceeded: {e}",
                    retry_after=retry_after
                )
                raise last_error

            except self.client.exceptions.InternalServerException as e:
                last_error = AgentConnectionError(f"Internal server error: {e}")
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    print(f"Internal server error on attempt {attempt + 1}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise last_error

            except (
                self.client.exceptions.AccessDeniedException,
                self.client.exceptions.UnauthorizedException
            ) as e:
                # Don't retry auth errors
                last_error = AgentCoreError(f"Authentication/Authorization failed: {e}")
                raise last_error

            except (
                self.client.exceptions.ResourceNotFoundException,
                self.client.exceptions.InvalidInputException,
                self.client.exceptions.ValidationException
            ) as e:
                # Don't retry validation errors
                last_error = AgentCoreError(f"Invalid request: {e}")
                raise last_error

            except Exception as e:
                error_msg = str(e).lower()

                # Check for timeout
                if "timeout" in error_msg or "timed out" in error_msg:
                    last_error = AgentTimeoutError(f"Agent invocation timed out: {e}")
                    if attempt < self.max_retries:
                        wait_time = 2 ** attempt
                        print(f"Timeout on attempt {attempt + 1}, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    raise last_error

                # Check for connection errors
                if "connection" in error_msg or "network" in error_msg:
                    last_error = AgentConnectionError(f"Connection failed: {e}")
                    if attempt < self.max_retries:
                        wait_time = 2 ** attempt
                        print(f"Connection error on attempt {attempt + 1}, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    raise last_error

                # Generic error
                last_error = AgentCoreError(f"Agent invocation failed: {e}")
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    print(f"Error on attempt {attempt + 1}, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise last_error

        # Should not reach here, but just in case
        raise last_error or AgentCoreError("Agent invocation failed after all retries")

    def _extract_retry_after(self, error_message: str) -> Optional[int]:
        """Extract retry-after value from error message."""
        import re
        match = re.search(r"retry[- ]after[:\s]+(\d+)", error_message, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
