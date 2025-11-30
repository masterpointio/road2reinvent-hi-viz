# AWS Services Guide for Money Spender Agent

## Purpose
This guide helps maintain consistency and realism when generating AWS spending scenarios. Use this as a reference when updating prompts or adding new service examples.

## Common AWS Services by Category

### Compute Services
- **EC2 (Elastic Compute Cloud)**
  - Instance families: t3, t4g, m5, m6g, c5, c6g, r5, r6g, r7g
  - Common wasteful patterns: Over-provisioned instances, running 24/7 for dev/test
  - Typical hourly costs: $0.0104 (t3.micro) to $5.472 (r7g.16xlarge)

- **EKS (Elastic Kubernetes Service)**
  - Cluster cost: $0.10/hour
  - Node costs: Based on EC2 instance types
  - Common waste: Too many nodes, over-provisioned node types

- **Lambda**
  - Pricing: Per request + duration
  - Common waste: Over-allocated memory, inefficient code

### Database Services
- **RDS (Relational Database Service)**
  - Instance types: db.t3, db.t4g, db.m5, db.r5, db.r6g
  - Common waste: Running 24/7 for dev, Multi-AZ when not needed
  - Typical costs: $0.017/hour (db.t3.micro) to $4.32/hour (db.r6g.16xlarge)

- **DynamoDB**
  - Pricing: Provisioned capacity or on-demand
  - Common waste: Over-provisioned read/write capacity

- **DocumentDB**
  - MongoDB-compatible service
  - Common waste: Redundant with RDS or DynamoDB

### Storage Services
- **S3 (Simple Storage Service)**
  - Storage classes: Standard, Intelligent-Tiering, Glacier, Glacier Instant Retrieval
  - Pricing: $0.023/GB/month (Standard)
  - Common waste: Wrong storage class, excessive retrievals from Glacier

- **EBS (Elastic Block Store)**
  - Types: gp2, gp3, io1, io2
  - Common waste: Provisioned IOPS when not needed

- **EFS (Elastic File System)**
  - Common waste: Using when S3 would suffice

### Networking Services
- **CloudFront**
  - CDN service
  - Common waste: Using for internal-only applications
  - Data transfer costs: $0.085-0.170/GB

- **NAT Gateway**
  - Cost: $0.045/hour + data processing
  - Common waste: Left running when not needed

- **VPN / Direct Connect / Transit Gateway**
  - Common waste: Over-engineered networking for simple apps

### Machine Learning Services
- **SageMaker**
  - Instance types: ml.t3, ml.m5, ml.p3, ml.p4d
  - Common waste: Large instances running 24/7, notebooks left on
  - Costs: $0.0582/hour (ml.t3.medium) to $32.77/hour (ml.p4d.24xlarge)

- **Amazon Braket**
  - Quantum computing service
  - Extremely expensive, rarely needed

### Analytics Services
- **EMR (Elastic MapReduce)**
  - Hadoop/Spark clusters
  - Common waste: Clusters running 24/7 with no processing

- **AWS Batch**
  - Common waste: Maximum compute for minimal workloads

### Specialized/Obscure Services (for "Brain damage" level)
- **AWS RoboMaker**: Robot simulation
- **AWS Ground Station**: Satellite data
- **AWS Snowmobile**: Exabyte-scale data transfer (truck)
- **AWS Thinkbox Deadline**: Render farm management
- **AWS Wavelength**: 5G edge computing
- **AWS Outposts**: On-premises AWS infrastructure
- **AWS Managed Blockchain**: Blockchain networks
- **AWS Elemental MediaLive**: Live video transcoding
- **Amazon Monitron**: Equipment monitoring
- **AWS Panorama**: Computer vision at edge
- **AWS Private 5G**: Private cellular networks
- **Amazon Nimble Studio**: Creative studio in cloud
- **AWS DeepRacer**: Autonomous racing

## Efficiency Level Guidelines

### Mildly Dumb (10-30% waste)
**Characteristics:**
- Rookie mistakes, lack of optimization
- Resources left running unnecessarily
- Minor over-provisioning

**Typical Services:**
- EC2: t3.2xlarge for static website (should be t3.small)
- RDS: db.t3.large running 24/7 for dev (should be stopped when not in use)
- NAT Gateway: Left running (should be deleted)
- S3: Standard storage for archival data (should be Glacier)

**Cost Pattern:**
- Mostly common services
- Reasonable instance types but wrong sizing
- Forgot to clean up test resources

### Moderately Stupid (30-60% waste)
**Characteristics:**
- Significant over-provisioning
- Redundant services
- Poor architecture choices

**Typical Services:**
- EC2: r7g.16xlarge for cron job (massive overkill)
- RDS: Multiple redundant databases (RDS + DynamoDB + DocumentDB)
- SageMaker: ml.p3.2xlarge running 24/7 for simple tasks
- CloudFront: For internal-only applications
- S3 Glacier Instant Retrieval: With constant retrievals

**Cost Pattern:**
- Mix of expensive instance types
- Multiple redundant services
- Premium features without need

### Very Stupid (60-85% waste)
**Characteristics:**
- Extreme over-engineering
- Multi-region for simple apps
- Massive over-provisioning

**Typical Services:**
- EKS: 50 nodes for single microservice
- Multi-region active-active: For personal blog
- AWS Outposts: For cloud-native app
- Managed Blockchain: For todo list
- EMR: Clusters running 24/7 with no data
- AWS Wavelength: For internal admin panel
- Multiple VPN + Direct Connect + Transit Gateway: For simple app

**Cost Pattern:**
- Architectural disasters
- Services that make no sense for use case
- Maximum over-provisioning

### Brain Damage (85-95% waste)
**Characteristics:**
- Using the most obscure/expensive services
- Maximum chaos and waste
- Services that have no business being used

**Typical Services:**
- AWS RoboMaker: Running 24/7 for no reason
- AWS Ground Station: For basic weather data
- AWS Snowmobile: To transfer 100GB
- AWS Thinkbox Deadline: For PowerPoint slides
- Amazon Braket: To calculate 2+2
- AWS Elemental MediaLive: Transcoding static images
- Amazon Monitron: Monitoring single laptop
- AWS Panorama: For basic webcam
- Amazon Nimble Studio: For MS Paint
- AWS Private 5G: For single IoT device
- All storage classes simultaneously

**Cost Pattern:**
- Maximum use of obscure services
- Completely nonsensical choices
- Every premium feature enabled

## Pricing Reference (Approximate)

### Compute (per hour)
- t3.micro: $0.0104
- t3.medium: $0.0416
- t3.2xlarge: $0.3328
- m5.xlarge: $0.192
- r7g.16xlarge: $3.2256
- c6g.16xlarge: $2.1760

### Database (per hour)
- db.t3.micro: $0.017
- db.t3.large: $0.136
- db.r6g.large: $0.192
- db.r6g.16xlarge: $4.32

### ML (per hour)
- ml.t3.medium: $0.0582
- ml.m5.xlarge: $0.269
- ml.p3.2xlarge: $3.825
- ml.p4d.24xlarge: $32.77

### Storage (per GB/month)
- S3 Standard: $0.023
- S3 Intelligent-Tiering: $0.023 + monitoring
- S3 Glacier Instant Retrieval: $0.004
- EBS gp3: $0.08

### Networking
- NAT Gateway: $0.045/hour + $0.045/GB processed
- CloudFront: $0.085/GB (first 10TB)
- Data Transfer Out: $0.09/GB (first 10TB)

## When Adding New Services

1. **Research realistic pricing** from AWS pricing calculator
2. **Identify common waste patterns** for that service
3. **Map to appropriate efficiency levels**
4. **Add to system prompt** with specific examples
5. **Test with various amounts** to ensure realistic scenarios

## Maintaining Realism

### Do:
- Use actual AWS service names
- Reference real instance types
- Apply realistic pricing
- Describe plausible (if wasteful) scenarios

### Don't:
- Invent fake AWS services
- Use unrealistic pricing
- Create impossible configurations
- Ignore AWS service constraints

## Cost Calculation Tips

- **Hourly services**: cost = hourly_rate × hours × quantity
- **Monthly services**: cost = monthly_rate × (days/30) × quantity
- **Data transfer**: cost = rate_per_GB × GB_transferred
- **Storage**: cost = rate_per_GB_month × GB × (days/30)

Example:
```
EC2 r7g.16xlarge running 30 days:
$3.2256/hour × 24 hours × 30 days × 1 instance = $2,322.43
```
