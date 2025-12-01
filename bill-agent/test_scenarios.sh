#!/bin/bash
# Money Spender Agent - Test Scenarios

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

LOCAL_FLAG=""
if [ "$1" == "--local" ]; then
    LOCAL_FLAG="--local"
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Money Spender Agent - Test Scenarios${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Test 1: Serverless with horizontal burning
echo -e "${BLUE}Test 1: Serverless Architecture - Horizontal Burning${NC}"
echo -e "${YELLOW}Scenario: $2500 over 30 days, moderately stupid${NC}"
agentcore invoke '{
  "amount": "$2500",
  "timeline": 30,
  "stupidity": "Moderately stupid",
  "architecture": "serverless",
  "burning_style": "horizontal"
}' $LOCAL_FLAG
echo ""
echo -e "${GREEN}✓ Test 1 complete${NC}"
echo ""
sleep 2

# Test 2: Kubernetes with vertical bursts
echo -e "${BLUE}Test 2: Kubernetes Architecture - Vertical Bursts${NC}"
echo -e "${YELLOW}Scenario: $5000 over 45 days, very stupid${NC}"
agentcore invoke '{
  "amount": "$5000",
  "timeline": 45,
  "stupidity": "Very stupid",
  "architecture": "kubernetes",
  "burning_style": "vertical"
}' $LOCAL_FLAG
echo ""
echo -e "${GREEN}✓ Test 2 complete${NC}"
echo ""
sleep 2

# Test 3: Traditional with horizontal
echo -e "${BLUE}Test 3: Traditional Architecture - Horizontal Burning${NC}"
echo -e "${YELLOW}Scenario: $1000 over 14 days, mildly dumb${NC}"
agentcore invoke '{
  "amount": "$1000",
  "timeline": 14,
  "stupidity": "Mildly dumb",
  "architecture": "traditional",
  "burning_style": "horizontal"
}' $LOCAL_FLAG
echo ""
echo -e "${GREEN}✓ Test 3 complete${NC}"
echo ""
sleep 2

# Test 4: Mixed with vertical - Brain damage
echo -e "${BLUE}Test 4: Mixed Architecture - Vertical Bursts (Brain Damage)${NC}"
echo -e "${YELLOW}Scenario: $10000 over 60 days, brain damage${NC}"
agentcore invoke '{
  "amount": "$10000",
  "timeline": 60,
  "stupidity": "Brain damage",
  "architecture": "mixed",
  "burning_style": "vertical"
}' $LOCAL_FLAG
echo ""
echo -e "${GREEN}✓ Test 4 complete${NC}"
echo ""

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}All test scenarios completed!${NC}"
echo -e "${GREEN}========================================${NC}"
