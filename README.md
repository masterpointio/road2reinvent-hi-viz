# 💸 Bill Burner

A satirical AWS bill generator that shows you the most creative ways to waste money on cloud infrastructure. Tell us your budget and how inefficient you want to be, and we'll generate a hilariously over-engineered AWS architecture to burn through it.

## What is this?

Ever wondered how to spend $10,000 on AWS in the most wasteful way possible? Bill Burner uses AI to generate mock AWS configurations that maximize cloud spending through over-provisioning, redundant services, and questionable architecture decisions.

Pick your "stupidity level" from "Mildly dumb" to "Brain damage" and watch as the app generates increasingly absurd AWS deployments - like using AWS Ground Station to fetch weather data or spinning up 50 EKS nodes for a todo list.

## Quick Start

```bash
# Install dependencies
npm install
cd frontend && npm install && cd ..

# Run the web app locally
cd frontend && npm run dev

# Deploy to AWS
npm run deploy
```

## Usage

### Web App

The easiest way to use Bill Burner is through the web interface:

1. Enter how much money you want to burn
2. Choose your timeline (days)
3. Select your stupidity level
4. Pick an architecture style (serverless, kubernetes, traditional, mixed)
5. Choose burning style (horizontal = steady waste, vertical = explosive bursts)
6. Get roasted with a detailed breakdown of your wasteful infrastructure

### CLI

For command-line enthusiasts:

```bash
cd agent
python main.py --interactive
```

Or directly:

```bash
python main.py \
  --amount "$5000" \
  --timeline 30 \
  --stupidity "Brain damage" \
  --architecture kubernetes \
  --burning-style vertical
```

#### CLI Arguments

- `--amount` - How much to burn (e.g., "$1000" or "₹50000")
- `--timeline` - Days to burn it over (e.g., 30, 14, 60)
- `--stupidity` - Your inefficiency level:
  - `Mildly dumb` - Rookie mistakes (10-30% waste)
  - `Moderately stupid` - Significant waste (30-60% waste)
  - `Very stupid` - Extreme over-engineering (60-85% waste)
  - `Brain damage` - Maximum chaos (85-95% waste)
- `--architecture` - Architecture style:
  - `serverless` - Lambda, API Gateway, DynamoDB
  - `kubernetes` - EKS, containers, orchestration
  - `traditional` - EC2, RDS, classic infrastructure
  - `mixed` - Chaotic combination of everything
- `--burning-style` - How to waste it:
  - `horizontal` - Steady waste over time
  - `vertical` - Explosive one-shot bursts
- `--model` - Bedrock model (optional, default: amazon.nova-lite-v1:0)
- `--interactive` - Interactive mode

## Stupidity Levels

### Mildly Dumb
Rookie mistakes like leaving dev servers running 24/7, over-provisioned instances, forgotten test resources.

### Moderately Stupid
Running r7g.16xlarge instances for cron jobs, multiple redundant databases, CloudFront for internal apps.

### Very Stupid
EKS with 50 nodes for a single microservice, multi-region active-active for a personal blog, managed blockchain for a todo list.

### Brain Damage
AWS Snowmobile to transfer 100GB, quantum computing for 2+2, AWS Ground Station for weather widgets, Private 5G for a single IoT device.

## Commands

```bash
# Deploy everything to AWS
npm run deploy

# Frontend development
cd frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run lint         # Lint code

# Infrastructure
npx cdk synth        # Generate CloudFormation
npx cdk diff         # See what changed
npx cdk destroy      # Tear it all down

# Agent CLI
cd agent
python main.py --interactive
```

## Output

Bill Burner generates detailed JSON reports with:

- Service-by-service cost breakdown
- Specific instance types and quantities
- Timeline showing when services started/stopped
- Deployment scenario narrative
- Key mistakes identified
- "Recommendations" (with a wink)

Example output:

```json
{
  "total_amount": "$5000",
  "timeline_days": 30,
  "efficiency_level": "Brain damage",
  "architecture_type": "kubernetes",
  "burning_style": "vertical",
  "services_deployed": [
    {
      "service_name": "EKS",
      "instance_type": "m5.16xlarge nodes",
      "quantity": 50,
      "total_cost": 4800.00,
      "waste_factor": "50 nodes for a hello world app"
    }
  ],
  "deployment_scenario": "...",
  "key_mistakes": ["..."],
  "recommendations": ["..."]
}
```

## Tech Stack

Vue 3, TypeScript, AWS Bedrock (for AI), AWS CDK, Python, Strands Agents

## Disclaimer

This is satire. Please don't actually deploy these configurations. Your AWS bill will not thank you. This tool is for educational purposes to learn about AWS services, pricing, and common cost optimization mistakes.
