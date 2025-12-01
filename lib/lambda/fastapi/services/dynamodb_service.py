"""DynamoDB service for storing and retrieving burn plans."""

from __future__ import annotations

import os
import time
from typing import List
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

from models import BurnPlan


class DynamoDBService:
    """Service for interacting with DynamoDB burn plans table."""

    def __init__(self):
        """Initialize DynamoDB service."""
        self.table_name = os.environ.get("BURN_PLANS_TABLE_NAME", "burn-plans")
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(self.table_name)

    def store_burn_plan(self, session_id: str, burn_plan: BurnPlan) -> None:
        """Store a burn plan in DynamoDB.

        Args:
            session_id: Unique session identifier
            burn_plan: Burn plan to store
        """
        timestamp = int(time.time() * 1000)  # milliseconds

        # Convert BurnPlan to dict and handle float to Decimal conversion
        item = {
            "id": session_id,
            "timestamp": timestamp,
            "burn_plan": self._convert_floats_to_decimals(burn_plan.model_dump())
        }

        self.table.put_item(Item=item)

    def get_recent_burn_plans(self, limit: int = 5) -> List[dict]:
        """Get the most recent burn plans.

        Args:
            limit: Maximum number of burn plans to retrieve

        Returns:
            List of burn plans with session IDs and timestamps
        """
        # Scan the table and sort by timestamp (not ideal for large tables)
        # For production, consider using a GSI with a constant partition key
        response = self.table.scan(
            Limit=limit * 2  # Get more to ensure we have enough after sorting
        )

        items = response.get("Items", [])

        # Sort by timestamp descending
        items.sort(key=lambda x: x.get("timestamp", 0), reverse=True)

        # Take only the requested limit
        recent_items = items[:limit]

        # Convert Decimals back to floats for JSON serialization
        return [self._convert_decimals_to_floats(item) for item in recent_items]

    @staticmethod
    def _convert_floats_to_decimals(obj):
        """Recursively convert floats to Decimals for DynamoDB."""
        if isinstance(obj, float):
            return Decimal(str(obj))
        elif isinstance(obj, dict):
            return {k: DynamoDBService._convert_floats_to_decimals(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [DynamoDBService._convert_floats_to_decimals(item) for item in obj]
        return obj

    @staticmethod
    def _convert_decimals_to_floats(obj):
        """Recursively convert Decimals to floats for JSON serialization."""
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: DynamoDBService._convert_decimals_to_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [DynamoDBService._convert_decimals_to_floats(item) for item in obj]
        return obj
