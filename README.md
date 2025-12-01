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

## Stupidity Levels

- **Mildly dumb** - Rookie mistakes, like leaving dev servers running 24/7
- **Moderately stupid** - Running r7g.16xlarge instances for cron jobs
- **Very stupid** - Multi-region active-active for a personal blog
- **Brain damage** - AWS Snowmobile to transfer 100GB, quantum computing for 2+2

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
```

## Tech Stack

Vue 3, TypeScript, AWS Bedrock (for AI), AWS CDK, Python

## Disclaimer

This is satire. Please don't actually deploy these configurations. Your AWS bill will not thank you.
