#!/bin/bash
# Update AgentCore execution role with S3 full access

set -e

ROLE_NAME="AmazonBedrockAgentCoreSDKRuntime-us-east-1-ba3cea6614"
POLICY_ARN="arn:aws:iam::aws:policy/AmazonS3FullAccess"

echo "🔧 Updating IAM role: $ROLE_NAME"
echo "📦 Attaching policy: $POLICY_ARN"
echo ""

# Attach the S3 full access policy to the role
aws iam attach-role-policy \
    --role-name "$ROLE_NAME" \
    --policy-arn "$POLICY_ARN"

if [ $? -eq 0 ]; then
    echo "✅ Successfully attached S3FullAccess policy to role"
    echo ""
    echo "📋 Current attached policies:"
    aws iam list-attached-role-policies --role-name "$ROLE_NAME"
else
    echo "❌ Failed to attach policy"
    exit 1
fi
