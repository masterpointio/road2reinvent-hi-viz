# Requirements Document

## Introduction

The AWS Cost Forensics Agent is a Strands-based system that performs reverse-engineering analysis of AWS spending patterns. Given a spending amount and an efficiency level (stupidity level), the system determines what AWS resources were likely provisioned to result in that cost. The agent provides forensic analysis with realistic but potentially wasteful AWS service combinations, detailed cost breakdowns, and usage pattern explanations.

## Glossary

- **Agent**: The Strands-based AI system that analyzes AWS spending patterns
- **Stupidity Level**: An efficiency indicator ranging from "Mildly dumb" to "Brain damage" that determines the wastefulness of resource provisioning
- **Forensic Analysis**: The reverse-engineering process of determining AWS resources from spending amounts
- **Cost Breakdown**: Detailed per-service cost analysis showing how spending is distributed
- **Usage Pattern**: Description of how AWS resources are likely being utilized

## Requirements

### Requirement 1

**User Story:** As a cloud cost analyst, I want to input a spending amount and efficiency level, so that I can understand what AWS resources were likely provisioned.

#### Acceptance Criteria

1. WHEN a user provides a spending amount in dollars or rupees, THE Agent SHALL parse and normalize the currency value
2. WHEN a user provides a stupidity level (Mildly dumb, Moderately stupid, Very stupid, Brain damage), THE Agent SHALL validate and accept the efficiency indicator
3. WHEN both inputs are provided, THE Agent SHALL initiate forensic analysis
4. WHEN invalid inputs are provided, THE Agent SHALL reject the request and provide clear error messages
5. THE Agent SHALL support spending amounts ranging from $100 to $1,000,000

### Requirement 2

**User Story:** As a cloud cost analyst, I want the agent to identify likely AWS services used, so that I can understand the spending composition.

#### Acceptance Criteria

1. WHEN performing forensic analysis, THE Agent SHALL identify at least 3 AWS services that could account for the spending
2. WHEN the stupidity level is "Mildly dumb", THE Agent SHALL suggest slightly over-provisioned but reasonable service configurations
3. WHEN the stupidity level is "Moderately stupid", THE Agent SHALL suggest clearly wasteful configurations with some redundancy
4. WHEN the stupidity level is "Very stupid", THE Agent SHALL suggest extremely inefficient configurations with significant redundancy
5. WHEN the stupidity level is "Brain damage", THE Agent SHALL suggest maximum absurdity with everything over-provisioned, redundant, and running globally 24/7

### Requirement 3

**User Story:** As a cloud cost analyst, I want detailed resource configurations for each service, so that I can understand the specific provisioning decisions.

#### Acceptance Criteria

1. WHEN identifying EC2 usage, THE Agent SHALL specify instance types, quantities, and running hours
2. WHEN identifying RDS usage, THE Agent SHALL specify database engine, instance class, storage size, and multi-AZ configuration
3. WHEN identifying S3 usage, THE Agent SHALL specify storage amount, storage class, and request quantities
4. WHEN identifying data transfer, THE Agent SHALL specify transfer amounts and directions (inbound/outbound/inter-region)
5. THE Agent SHALL ensure all resource specifications are based on actual AWS pricing models

### Requirement 4

**User Story:** As a cloud cost analyst, I want a cost breakdown per service, so that I can see how spending is distributed across AWS services.

#### Acceptance Criteria

1. WHEN generating forensic analysis, THE Agent SHALL provide individual cost amounts for each identified service
2. WHEN calculating service costs, THE Agent SHALL ensure the sum of all service costs equals the input spending amount within 5% tolerance
3. WHEN presenting cost breakdown, THE Agent SHALL display costs in the same currency as the input amount
4. WHEN multiple services are identified, THE Agent SHALL order them by cost from highest to lowest
5. THE Agent SHALL include percentage of total spending for each service

### Requirement 5

**User Story:** As a cloud cost analyst, I want usage pattern descriptions, so that I can understand how the resources are being utilized.

#### Acceptance Criteria

1. WHEN describing usage patterns, THE Agent SHALL explain the likely operational scenario for the identified resources
2. WHEN the stupidity level indicates waste, THE Agent SHALL highlight specific wasteful practices (e.g., 24/7 operation, unused capacity)
3. WHEN redundancy is present, THE Agent SHALL explain the redundant configurations
4. WHEN global deployments are suggested, THE Agent SHALL specify regions and explain the distribution
5. THE Agent SHALL provide realistic usage scenarios that justify the identified resource configurations

### Requirement 6

**User Story:** As a developer, I want to interact with the agent programmatically, so that I can integrate it into other systems.

#### Acceptance Criteria

1. THE Agent SHALL expose a creation function that returns a configured Strands agent instance
2. WHEN the agent is invoked with a prompt, THE Agent SHALL return structured analysis results
3. THE Agent SHALL support configuration of the underlying LLM model ID
4. WHEN processing requests, THE Agent SHALL use Amazon Bedrock as the LLM provider
5. THE Agent SHALL provide a formatting function that structures the raw analysis into readable output

### Requirement 7

**User Story:** As a user, I want to interact with the agent via command line, so that I can quickly analyze spending scenarios.

#### Acceptance Criteria

1. WHEN the main script is executed with amount and stupidity parameters, THE Agent SHALL perform analysis and display results
2. WHEN the main script is executed in interactive mode, THE Agent SHALL prompt for inputs and display results
3. WHEN displaying results, THE Agent SHALL format output with clear sections for services, costs, and usage patterns
4. WHEN errors occur, THE Agent SHALL display user-friendly error messages
5. THE Agent SHALL support both flag-based and interactive input modes

### Requirement 8

**User Story:** As a developer, I want clear separation between agent logic, formatting utilities, and interface code, so that the system is maintainable and extensible.

#### Acceptance Criteria

1. WHEN the agent module is modified, THE formatting and interface modules SHALL remain unaffected
2. WHEN the formatting logic is updated, THE agent and interface modules SHALL continue functioning unchanged
3. WHEN the interface is modified, THE agent and formatting modules SHALL operate without modification
4. THE Agent SHALL be defined in a separate module from the main entry point
5. THE Agent SHALL use dependency injection for configuration parameters
