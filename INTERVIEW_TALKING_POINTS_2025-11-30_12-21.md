# Interview Talking Points - November 30, 2025 12:21 PM

## THE STORY

**What They're Building**: A self-aware dashboard that tracks how much money it costs to run itself - basically an AWS bill burner that helps you waste money in the most spectacular, over-engineered way possible.

**Why It's Hilarious**: It's a tool that literally exists to help you burn through your AWS budget by deploying absurdly over-provisioned infrastructure. Think 50 EKS nodes for a single microservice, or CloudFront for internal-only apps. The app roasts you in real-time with AI-generated burns like "You've burned $5,000 - that's 2,500 burritos you'll never eat."

**The Bold Technical Choice**: They built a full enterprise-grade authentication system with Cognito, custom domain with Route53 and ACM certificates, CloudFront CDN, and GitHub OIDC for CI/CD... for a joke app that literally just counts how much money it's wasting. The infrastructure to track waste is itself wasteful.

## WHAT'S HAPPENING NOW

**Current State**: 
- Frontend is fully built with Vue 3, ECharts visualizations, and a slick neon-themed UI
- Backend has Cognito auth, Lambda functions, API Gateway with authorization
- Full CDK infrastructure with CloudFront, S3, Route53, custom domain (wehavetoomuch.com)
- GitHub Actions CI/CD with OIDC authentication
- Mock data system generating fake "burn plans" with hilarious waste scenarios

**Completion Reality Check**: This is surprisingly complete for a hackathon project. The core functionality works - you can configure a "burn plan" (how much money, timeline, architecture style), and it generates visualizations showing how you'd waste that money. The auth flow is there, the deployment pipeline is set up. They're probably 85% done. The vibe is "we actually shipped something functional."

**The Interesting Problem**: They're solving the meta-problem of cloud cost awareness through satire. By gamifying waste, they're actually teaching people about common AWS cost pitfalls. The technical challenge was making the data visualization compelling enough that people want to play with it.

## TECHNICAL ARCHITECTURE

**AWS Services Used**:
- **Lambda** (serverless functions) - Running a simple "Hello World" API that requires full Cognito authentication to say hello
- **API Gateway** (REST API) - Over-engineered API with CORS and Cognito authorizer for basically one endpoint
- **Cognito** (user authentication) - Full user pool with hosted UI, OAuth flows, password policies... to protect a joke dashboard
- **S3** (object storage) - Hosting static frontend files
- **CloudFront** (CDN) - Global content delivery for a dashboard that tracks its own cost
- **Route53** (DNS) - Custom domain management for "wehavetoomuch.com"
- **ACM** (SSL certificates) - HTTPS certificates because even waste should be secure
- **IAM** (permissions) - Complex role-based access with GitHub OIDC federation
- **CDK** (Infrastructure as Code) - TypeScript-based infrastructure deployment

**Most Over-Engineered Component**: The authentication system. They have:
- Cognito User Pool with email verification
- Hosted UI with OAuth flows
- Password policies requiring uppercase, lowercase, digits, and symbols
- Multi-URL callback handling (localhost, CloudFront, custom domain)
- Account recovery flows
- All of this to protect a dashboard that literally just shows you fake numbers going up

What it does: Lets users log in securely
Why it's unnecessarily complex: The app doesn't store any user data, doesn't have any sensitive information, and could work perfectly fine without any auth at all. They added enterprise-grade security to a meme.

**Data Flow**:
1. User visits wehavetoomuch.com → CloudFront serves the Vue app from S3
2. User configures a "burn plan" (amount, timeline, architecture style, "stupidity level")
3. Frontend generates a mock burn plan with fake AWS services and costs
4. Data flows through ECharts to create animated visualizations
5. "Roasts" appear telling you how dumb your spending is
6. If you try to call the API, you need to authenticate through Cognito first
7. Lambda returns "Hello World" with your email (the most expensive hello ever)

Think of it like a flight simulator, but instead of flying planes, you're crashing AWS budgets.

**Creative Technical Decisions**:
- **Normal**: Use environment variables for config
- **What they did**: Created a centralized config system with validation helpers and "feature flags for quick toggles during hackathon"

- **Normal**: Simple dashboard with basic charts
- **What they did**: Full neon cyberpunk theme with animated ECharts, gradient glows, racing bar charts, and a "stupidity level" slider from "Mildly Dumb" to "Brain Damage"

- **Normal**: Deploy with simple S3 + CloudFront
- **What they did**: Full CDK stack with custom domain, SSL certs, GitHub OIDC federation, and a pre-deploy hook that builds the frontend

- **Normal**: Mock some data in the component
- **What they did**: Created a complete type system for "BurnPlanResponse" with services, waste factors, deployment scenarios, key mistakes, and recommendations

## CONVERSATION STARTERS

**Most Demo-Worthy Feature**: The burn configuration wizard. It's got personality - asking "How stupid should this be?" with a slider, offering architecture choices like "Kubernetes - EKS, EC2, Load Balancers" vs "Serverless - Lambda, API Gateway, DynamoDB", and burning styles like "Horizontal - Many small services" vs "Vertical - Few expensive services". Then it generates a visualization showing exactly how you'd waste that money over time.

**User Journey**:
1. Land on the dashboard showing a fake cost counter ticking up ($0.01 per second)
2. See cards showing "Cost Per View: $0.08" and "Monthly Projection: $2,592.00"
3. Click "Start New Burn" to configure your waste
4. Choose how much money ($1,500+), timeline (1 hour to 1 month), architecture (serverless/kubernetes/traditional/mixed)
5. Set your "stupidity level" on a slider
6. Get a generated burn plan with specific services like "50x r7g.16xlarge EKS nodes for a single microservice"
7. Watch animated charts showing your money disappearing
8. Get roasted: "That RDS cluster costs more per hour than most people make. But hey, your 3 users will appreciate the redundancy."

**The "Wait, Really?" Moment**: They have a GitHub Actions workflow that uses OIDC to assume an IAM role with PowerUserAccess PLUS custom IAM permissions... to deploy a joke app. The deployment role has more permissions than most production systems. Also, the domain name "wehavetoomuch.com" is perfect.

**The Chaos Factor**: The custom domain setup. They're using Route53 hosted zone lookup, ACM certificate validation, and CloudFront custom domain configuration. If any of these DNS/certificate steps fail, the whole deployment breaks. Also, they're deploying the frontend as part of the CDK stack, so if the Vue build fails, the entire infrastructure deployment fails.

**Abandoned Attempts**: 
- There's a `CallbackView.vue` AND a `LoginCallbackView.vue` - looks like they tried two different OAuth callback approaches
- The router has `requiresAuth: false` on the main app routes, suggesting they initially planned to lock everything behind auth but gave up
- There's an `AboutView.vue` that's never used in the router
- The Lambda function is called "hello-world" but they clearly planned something more ambitious initially
- Mock data instead of a real backend API - they probably ran out of time to build the actual burn plan generator

## DEVELOPMENT INSIGHTS

**Time Pressure Adaptations**:
- Using mock data instead of real API calls - smart move to get the UI working first
- Feature flags in config ("enableToasts", "enableThemeSwitcher") - they knew they might need to disable stuff quickly
- Session storage for burn plans instead of a database - no backend persistence needed
- Pre-built UI components (UiCard, UiButton) - they created a component library early to move fast
- The "predeploy" script that builds frontend before CDK deploy - one command to rule them all

What these mean: They prioritized getting something visual and interactive working over building a complete backend. This is smart hackathon strategy - demo the frontend, fake the backend.

**Technical Learning Moments**:
- **CDK Infrastructure as Code**: This is a masterclass in CDK patterns - showing how to compose multiple AWS services (Cognito, S3, CloudFront, Lambda, API Gateway) into a single deployable stack
- **GitHub OIDC for CI/CD**: They're using the modern approach to AWS authentication from GitHub Actions (no long-lived credentials) - this is actually a best practice
- **Vue 3 Composition API**: Clean use of composables for reusable logic (useAuth, useTheme, useToasts)
- **ECharts Integration**: Shows how to integrate complex charting libraries with reactive Vue data
- **Type-Safe Configuration**: Their config system with validation is actually a good pattern for any app
- **Mock Data Patterns**: The way they structure mock data to match real API responses makes it easy to swap in real APIs later

The meta-lesson: Sometimes the best way to teach people about cloud costs is to make them laugh at their own mistakes. This project is secretly educational while being hilarious.
