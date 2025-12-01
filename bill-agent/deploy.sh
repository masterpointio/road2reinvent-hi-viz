#!/bin/bash
# Money Spender Agent - AgentCore Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
AGENT_NAME="money-spender-agent"
ENTRYPOINT="agentcore_handler.py"
RUNTIME="PYTHON_3_12"
REGION="${AWS_REGION:-us-west-2}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Money Spender Agent - AgentCore Deploy${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if AgentCore CLI is installed
if ! command -v agentcore &> /dev/null; then
    echo -e "${RED}Error: AgentCore CLI not found${NC}"
    echo "Install it with: pip install bedrock-agentcore-starter-toolkit"
    exit 1
fi

# Check if we're in the agent directory
if [ ! -f "$ENTRYPOINT" ]; then
    echo -e "${RED}Error: $ENTRYPOINT not found${NC}"
    echo "Please run this script from the agent/ directory"
    exit 1
fi

# Parse command line arguments
ACTION="${1:-deploy}"
LOCAL_FLAG=""
VERBOSE_FLAG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --local)
            LOCAL_FLAG="--local"
            shift
            ;;
        --verbose)
            VERBOSE_FLAG="--verbose"
            shift
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        configure|deploy|test|status|destroy)
            ACTION="$1"
            shift
            ;;
        *)
            shift
            ;;
    esac
done

case $ACTION in
    configure)
        echo -e "${YELLOW}Configuring agent...${NC}"
        agentcore configure \
            --entrypoint "$ENTRYPOINT" \
            --name "$AGENT_NAME" \
            --runtime "$RUNTIME" \
            --requirements-file requirements.txt \
            --region "$REGION" \
            --non-interactive \
            $VERBOSE_FLAG
        echo -e "${GREEN}✓ Configuration complete${NC}"
        ;;

    deploy)
        echo -e "${YELLOW}Deploying agent to AgentCore Runtime...${NC}"
        
        # Configure if not already configured
        if [ ! -f ".bedrock_agentcore.yaml" ]; then
            echo -e "${YELLOW}No configuration found. Running configure first...${NC}"
            agentcore configure \
                --entrypoint "$ENTRYPOINT" \
                --name "$AGENT_NAME" \
                --runtime "$RUNTIME" \
                --requirements-file requirements.txt \
                --region "$REGION" \
                --non-interactive
        fi
        
        # Launch the agent
        agentcore launch $LOCAL_FLAG $VERBOSE_FLAG
        
        if [ -z "$LOCAL_FLAG" ]; then
            echo ""
            echo -e "${GREEN}✓ Deployment complete!${NC}"
            echo ""
            echo -e "${YELLOW}Test your agent with:${NC}"
            echo "  ./deploy.sh test"
            echo ""
            echo -e "${YELLOW}Check status with:${NC}"
            echo "  ./deploy.sh status"
        else
            echo ""
            echo -e "${GREEN}✓ Local agent running!${NC}"
            echo ""
            echo -e "${YELLOW}Test locally with:${NC}"
            echo "  ./deploy.sh test --local"
        fi
        ;;

    test)
        echo -e "${YELLOW}Testing agent...${NC}"
        echo ""
        
        # Test payload
        TEST_PAYLOAD='{
  "amount": "$2500",
  "timeline": 30,
  "stupidity": "Moderately stupid",
  "architecture": "serverless",
  "burning_style": "horizontal"
}'
        
        echo -e "${YELLOW}Sending test request:${NC}"
        echo "$TEST_PAYLOAD"
        echo ""
        
        agentcore invoke "$TEST_PAYLOAD" $LOCAL_FLAG
        
        echo ""
        echo -e "${GREEN}✓ Test complete${NC}"
        ;;

    status)
        echo -e "${YELLOW}Checking agent status...${NC}"
        echo ""
        agentcore status --verbose
        ;;

    destroy)
        echo -e "${RED}WARNING: This will destroy the deployed agent and all resources${NC}"
        read -p "Are you sure? (yes/no): " -r
        echo
        if [[ $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
            echo -e "${YELLOW}Destroying agent...${NC}"
            agentcore destroy --force
            echo -e "${GREEN}✓ Agent destroyed${NC}"
        else
            echo "Cancelled"
        fi
        ;;

    *)
        echo "Usage: ./deploy.sh [ACTION] [OPTIONS]"
        echo ""
        echo "Actions:"
        echo "  configure  - Configure the agent for deployment"
        echo "  deploy     - Deploy the agent to AgentCore Runtime (default)"
        echo "  test       - Test the deployed agent"
        echo "  status     - Check agent status"
        echo "  destroy    - Remove the deployed agent"
        echo ""
        echo "Options:"
        echo "  --local    - Run locally instead of deploying to AWS"
        echo "  --verbose  - Enable verbose output"
        echo "  --region   - AWS region (default: us-west-2)"
        echo ""
        echo "Examples:"
        echo "  ./deploy.sh deploy              # Deploy to AWS"
        echo "  ./deploy.sh deploy --local      # Run locally"
        echo "  ./deploy.sh test                # Test deployed agent"
        echo "  ./deploy.sh test --local        # Test local agent"
        echo "  ./deploy.sh status              # Check status"
        echo "  ./deploy.sh destroy             # Remove deployment"
        exit 1
        ;;
esac
