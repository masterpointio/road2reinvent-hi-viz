# Requirements Document

## Introduction

AWS Bill Burner is a satirical web application developed by Team Hi-Viz that visualizes "burning" money on AWS resources in real-time. Users configure how much money they want to waste, select burning preferences, and watch animated charts show their money disappearing with AI-generated snarky commentary. The application simulates AWS resource consumption without actually provisioning resources, providing entertainment and education about cloud costs through humor. The visual design follows a neon aesthetic consistent with Team Hi-Viz's brand identity.

## Glossary

- **Bill Burner System**: The complete web application including frontend, backend, and AI services
- **Burn Plan**: An AI-generated JSON structure containing simulated AWS services, costs, and timing for resource consumption
- **Burning Style**: User preference for resource allocation - "Horizontal" (many small resources) or "Vertical" (fewer expensive resources)
- **Stupidity Level**: A user-configurable parameter from "Mildly Dumb" to "Brain Damage" that controls the absurdity of the generated burn plan
- **Roast Commentary**: AI-generated snarky remarks about the user's spending choices
- **Burn Visualization**: Real-time animated charts displaying money consumption and resource allocation
- **User**: An authenticated individual interacting with the Bill Burner System
- **Strands Agent**: AI agent system using agentcore for generating burn plans and commentary
- **Cognito Service**: AWS authentication service managing user identity
- **Team Hi-Viz**: The development team creating the Bill Burner System
- **Neon Aesthetic**: A visual design style featuring bright, glowing colors and high-contrast elements characteristic of neon lighting

## Requirements

### Requirement 1

**User Story:** As a user, I want to authenticate with the application, so that I can access the bill burning features securely.

#### Acceptance Criteria

1. WHEN a user navigates to the application THEN the Bill Burner System SHALL display a login interface
2. WHEN a user provides valid credentials THEN the Cognito Service SHALL authenticate the user and grant access
3. WHEN a user provides invalid credentials THEN the Cognito Service SHALL reject authentication and display an error message
4. WHEN an authenticated user session expires THEN the Bill Burner System SHALL redirect the user to the login interface

### Requirement 2

**User Story:** As a user, I want to configure my burn parameters through an intuitive form, so that I can customize how my virtual money gets wasted.

#### Acceptance Criteria

1. WHEN a user accesses the configuration form THEN the Bill Burner System SHALL display input fields for amount, burning style, stupidity level, and optional time horizon
2. WHEN a user enters a monetary amount THEN the Bill Burner System SHALL validate that the amount is a positive number
3. WHEN a user selects a burning style THEN the Bill Burner System SHALL accept either "Horizontal" or "Vertical" as valid options
4. WHEN a user adjusts the stupidity level slider THEN the Bill Burner System SHALL capture values between minimum ("Mildly Dumb") and maximum ("Brain Damage")
5. WHEN a user submits the configuration form THEN the Bill Burner System SHALL send the parameters to the backend for burn plan generation

### Requirement 3

**User Story:** As a user, I want the AI to generate a creative burn plan based on my configuration, so that I can see a realistic simulation of AWS resource waste.

#### Acceptance Criteria

1. WHEN the backend receives burn configuration parameters THEN the Bill Burner System SHALL invoke the Strands Agent to generate a burn plan
2. WHEN the Strands Agent generates a burn plan THEN the Bill Burner System SHALL return a structured JSON containing AWS service names, individual costs, and timing information
3. WHEN the stupidity level is set to maximum THEN the Strands Agent SHALL generate more absurd and expensive resource combinations
4. WHEN the burning style is "Horizontal" THEN the Strands Agent SHALL generate plans with many small-cost resources
5. WHEN the burning style is "Vertical" THEN the Strands Agent SHALL generate plans with fewer high-cost resources
6. WHEN the total cost in the burn plan is calculated THEN the Bill Burner System SHALL ensure it matches the user-specified amount within acceptable tolerance

### Requirement 4

**User Story:** As a user, I want to see real-time animated visualizations of my money burning, so that I can watch the entertaining simulation unfold.

#### Acceptance Criteria

1. WHEN a burn plan is generated THEN the Bill Burner System SHALL display the burn visualization page with animated charts
2. WHEN the burn simulation runs THEN the Bill Burner System SHALL update the money remaining chart in real-time showing decreasing values
3. WHEN resources are being consumed THEN the Bill Burner System SHALL display resource allocation using line or stacked area charts
4. WHEN the simulation progresses THEN the Bill Burner System SHALL animate chart transitions smoothly without jarring updates
5. WHEN the burn simulation completes THEN the Bill Burner System SHALL display a final state showing zero money remaining

### Requirement 5

**User Story:** As a user, I want to receive AI-generated snarky commentary during the burn, so that I can be entertained by witty remarks about my wasteful choices.

#### Acceptance Criteria

1. WHEN the burn simulation reaches spending milestones THEN the Bill Burner System SHALL invoke the Strands Agent to generate roast commentary
2. WHEN roast commentary is generated THEN the Strands Agent SHALL return snarky remarks comparing costs to relatable items
3. WHEN roast commentary is received THEN the Bill Burner System SHALL display the commentary on the visualization page
4. WHEN multiple roasts are generated THEN the Bill Burner System SHALL display them in chronological order without overlap
5. WHEN the stupidity level is higher THEN the Strands Agent SHALL generate more savage roast commentary

### Requirement 6

**User Story:** As a user, I want the application to simulate burns without actually provisioning AWS resources, so that I can enjoy the experience without incurring real costs.

#### Acceptance Criteria

1. WHEN the Bill Burner System generates a burn plan THEN the Bill Burner System SHALL NOT provision actual AWS resources
2. WHEN the burn simulation runs THEN the Bill Burner System SHALL calculate resource consumption based on the generated plan data
3. WHEN displaying costs THEN the Bill Burner System SHALL use realistic AWS pricing for accuracy
4. WHEN the simulation completes THEN the Bill Burner System SHALL have incurred zero actual AWS resource costs beyond the application infrastructure

### Requirement 7

**User Story:** As a user, I want the backend to provide APIs for burn plan generation and status retrieval, so that the frontend can orchestrate the burning experience.

#### Acceptance Criteria

1. WHEN the frontend sends a POST request to /burn-plan with configuration parameters THEN the Bill Burner System SHALL return a structured burn plan JSON
2. WHEN the frontend sends a GET request to /burn-status THEN the Bill Burner System SHALL return the current simulation state
3. WHEN the frontend sends a POST request to /roast with current spending data THEN the Bill Burner System SHALL return AI-generated commentary
4. WHEN API requests fail THEN the Bill Burner System SHALL return appropriate HTTP error codes and error messages
5. WHEN API responses are sent THEN the Bill Burner System SHALL include proper CORS headers for frontend access

### Requirement 8

**User Story:** As a user, I want the application interface to have a humorous and self-aware tone, so that the satirical nature of the app is clear and entertaining.

#### Acceptance Criteria

1. WHEN form inputs are displayed THEN the Bill Burner System SHALL include funny flavor text and labels
2. WHEN error messages are shown THEN the Bill Burner System SHALL maintain the snarky tone while remaining informative
3. WHEN the visualization page loads THEN the Bill Burner System SHALL display humorous titles and descriptions
4. WHEN user interactions occur THEN the Bill Burner System SHALL provide witty feedback messages

### Requirement 9

**User Story:** As a member of Team Hi-Viz, I want the application to feature a neon visual aesthetic, so that the brand identity is consistent and visually striking.

#### Acceptance Criteria

1. WHEN any page of the Bill Burner System is displayed THEN the Bill Burner System SHALL use a color palette featuring bright neon colors
2. WHEN charts are rendered THEN the Bill Burner System SHALL apply neon-style glowing effects to chart elements
3. WHEN interactive elements are displayed THEN the Bill Burner System SHALL use high-contrast neon styling for buttons and inputs
4. WHEN text is displayed THEN the Bill Burner System SHALL use colors and effects that complement the neon aesthetic
5. WHEN animations occur THEN the Bill Burner System SHALL incorporate glowing transitions consistent with neon lighting effects
