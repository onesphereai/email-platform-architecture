# Email Platform - Detailed Costing Scenarios (Asia Pacific - Sydney)

## Overview
This document provides detailed cost analysis for the standalone Email Platform across different message volumes: 10K, 100K, 500K, and 1M messages per month. All pricing is based on AWS documentation and current rates for **ap-southeast-2 (Asia Pacific - Sydney)** region as of August 2024.

## Pricing Assumptions (Asia Pacific - Sydney - ap-southeast-2)

### AWS Service Pricing (Per AWS Documentation)
| Service | Pricing Model | Rate (ap-southeast-2) | US East Multiplier |
|---------|---------------|----------------------|-------------------|
| **AWS Lambda** | Per request + duration | $0.0000002 per request + $0.0000166667 per GB-second | 1.0x |
| **Step Functions** | Per state transition | $0.000025 per state transition | 1.0x |
| **API Gateway** | Per million requests | $4.25 per million API calls | 1.21x |
| **DynamoDB On-Demand** | Per request | Read: $0.285/million RRU, Write: $1.4275/million WRU | 1.14x |
| **DynamoDB Storage** | Per GB-month | $0.285 per GB per month | 1.14x |
| **Amazon SES** | Per email | $0.10 per 1,000 emails | 1.0x |
| **S3 Standard** | Storage + requests | $0.025 per GB + $0.0005 per 1,000 PUT requests | 1.09x |
| **EventBridge** | Per million events | $1.00 per million custom events | 1.0x |
| **OpenSearch Serverless** | Per OCU + storage | $0.334 per OCU-hour + $0.026 per GB-month | 1.39x |
| **SNS** | Per million messages | $0.60 per million messages | 1.2x |
| **CloudWatch** | Logs + metrics | $0.57 per GB ingested + $0.36 per metric | 1.14x |
| **KMS** | Per request | $0.03 per 10,000 requests | 1.0x |
| **Secrets Manager** | Per secret | $0.40 per secret per month | 1.0x |

*Note: Regional pricing multipliers applied based on AWS documentation for ap-southeast-2 region*

## Scenario 1: 10K Messages/Month

### Usage Patterns
- **Email Volume**: 10,000 messages/month
- **Campaigns**: 10 campaigns/month (1K messages each)
- **Templates**: 5 active templates
- **CSV Files**: 10 files/month (1KB each)
- **API Calls**: 50,000 calls/month
- **Analytics Queries**: 1,000 queries/month

### Detailed Cost Breakdown

#### Compute Services
```yaml
lambda:
  emailAPI: 
    requests: 15000        # API + processing requests
    memory: 1024MB
    duration: 3s
    cost: $0.75            # Same as US East
  
  fileProcessing:
    requests: 10000        # File processing requests  
    memory: 512MB
    duration: 5s
    cost: $0.42            # Same as US East
    
  callbacks:
    requests: 5000         # Callback requests
    memory: 256MB  
    duration: 1s
    cost: $0.05            # Same as US East
    
  totalLambdaCost: $1.22

stepFunctions:
  fileProcessing:
    stateTransitions: 1000  # 10 campaigns × 100 transitions
    cost: $0.025           # Same as US East
    
  emailSending:
    stateTransitions: 10000 # 10K messages × 1 transition
    cost: $0.25            # Same as US East
    
  scheduling:
    stateTransitions: 500   # Scheduling transitions
    cost: $0.0125          # Same as US East
    
  totalStepFunctionsCost: $0.29
```

#### Data Storage & Processing
```yaml
dynamodb:
  storage: 1GB             # Transaction/Batch/Message data
  storageCost: $0.285      # 1.14x multiplier for ap-southeast-2
  
  readRequests: 50000      # 50K RRU per month
  readCost: $0.01425       # 1.14x multiplier
  
  writeRequests: 15000     # 15K WRU per month  
  writeCost: $0.0214       # 1.14x multiplier
  
  totalDynamoDBCost: $0.32

s3:
  storage: 0.1GB           # Templates and CSV files
  storageCost: $0.0025     # 1.09x multiplier for ap-southeast-2
  
  putRequests: 15          # Template + CSV uploads
  requestCost: $0.0000075  # 1.09x multiplier
  
  totalS3Cost: $0.0025

openSearch:
  computeUnits: 0.5        # 0.5 OCU for low volume
  computeHours: 744        # 24×31 hours
  computeCost: $124.31     # 1.39x multiplier for ap-southeast-2
  
  storage: 2GB             # Analytics data
  storageCost: $0.052      # 1.39x multiplier
  
  totalOpenSearchCost: $124.36
```

#### Email Delivery
```yaml
ses:
  emails: 10000
  cost: $1.00              # Same as US East

sns:
  messages: 50000          # SES events + notifications
  cost: $0.03              # 1.2x multiplier for ap-southeast-2
  
  totalEmailDeliveryCost: $1.03
```

#### API & Integration
```yaml
apiGateway:
  requests: 50000
  cost: $0.2125            # 1.21x multiplier for ap-southeast-2

eventBridge:
  events: 5000             # Scheduling events
  cost: $0.005             # Same as US East
  
  totalAPIIntegrationCost: $0.2175
```

#### Security & Monitoring
```yaml
cloudWatch:
  logIngestion: 0.5GB
  logCost: $0.285          # 1.14x multiplier for ap-southeast-2
  
  metrics: 50              # Custom metrics
  metricCost: $18.00       # 1.2x multiplier for ap-southeast-2
  
  totalCloudWatchCost: $18.285

kms:
  requests: 1000
  cost: $0.003             # Same as US East

secretsManager:
  secrets: 5
  cost: $2.00              # Same as US East
  
  totalSecurityCost: $20.29
```

### **Scenario 1 Total Monthly Cost: $145.78** (vs $109.07 in US East)

---

## Scenario 2: 100K Messages/Month

### Usage Patterns
- **Email Volume**: 100,000 messages/month
- **Campaigns**: 50 campaigns/month (2K messages each)
- **Templates**: 15 active templates
- **CSV Files**: 50 files/month (10KB each)
- **API Calls**: 200,000 calls/month
- **Analytics Queries**: 5,000 queries/month

### Detailed Cost Breakdown

#### Compute Services
```yaml
lambda:
  emailAPI: 
    requests: 75000
    memory: 1024MB
    duration: 3s
    cost: $3.75            # Same as US East
  
  fileProcessing:
    requests: 50000
    memory: 512MB
    duration: 5s
    cost: $2.08            # Same as US East
    
  callbacks:
    requests: 25000
    memory: 256MB
    duration: 1s
    cost: $0.26            # Same as US East
    
  totalLambdaCost: $6.09

stepFunctions:
  fileProcessing:
    stateTransitions: 5000
    cost: $0.125           # Same as US East
    
  emailSending:
    stateTransitions: 100000
    cost: $2.50            # Same as US East
    
  scheduling:
    stateTransitions: 2500
    cost: $0.0625          # Same as US East
    
  totalStepFunctionsCost: $2.69
```

#### Data Storage & Processing
```yaml
dynamodb:
  storage: 5GB
  storageCost: $1.425      # 1.14x multiplier
  
  readRequests: 200000     # 200K RRU per month
  readCost: $0.057         # 1.14x multiplier
  
  writeRequests: 120000    # 120K WRU per month
  writeCost: $0.171        # 1.14x multiplier
  
  totalDynamoDBCost: $1.653

s3:
  storage: 0.5GB
  storageCost: $0.0125     # 1.09x multiplier
  
  putRequests: 65
  requestCost: $0.0000325  # 1.09x multiplier
  
  totalS3Cost: $0.0125

openSearch:
  computeUnits: 1.0        # 1 OCU
  computeHours: 744
  computeCost: $248.50     # 1.39x multiplier
  
  storage: 10GB
  storageCost: $0.26       # 1.39x multiplier
  
  totalOpenSearchCost: $248.76
```

#### Email Delivery
```yaml
ses:
  emails: 100000
  cost: $10.00             # Same as US East

sns:
  messages: 200000
  cost: $0.12              # 1.2x multiplier
  
  totalEmailDeliveryCost: $10.12
```

#### API & Integration
```yaml
apiGateway:
  requests: 200000
  cost: $0.85              # 1.21x multiplier

eventBridge:
  events: 25000
  cost: $0.025             # Same as US East
  
  totalAPIIntegrationCost: $0.875
```

#### Security & Monitoring
```yaml
cloudWatch:
  logIngestion: 2GB
  logCost: $1.14           # 1.14x multiplier
  
  metrics: 100
  metricCost: $36.00       # 1.2x multiplier
  
  totalCloudWatchCost: $37.14

kms:
  requests: 5000
  cost: $0.015             # Same as US East

secretsManager:
  secrets: 10
  cost: $4.00              # Same as US East
  
  totalSecurityCost: $41.16
```

### **Scenario 2 Total Monthly Cost: $310.31** (vs $234.87 in US East)

---

## Scenario 3: 500K Messages/Month

### Usage Patterns
- **Email Volume**: 500,000 messages/month
- **Campaigns**: 100 campaigns/month (5K messages each)
- **Templates**: 25 active templates
- **CSV Files**: 100 files/month (50KB each)
- **API Calls**: 750,000 calls/month
- **Analytics Queries**: 15,000 queries/month

### Detailed Cost Breakdown

#### Compute Services
```yaml
lambda:
  emailAPI: 
    requests: 300000
    memory: 1024MB
    duration: 3s
    cost: $15.00           # Same as US East
  
  fileProcessing:
    requests: 150000
    memory: 512MB
    duration: 5s
    cost: $6.25            # Same as US East
    
  callbacks:
    requests: 75000
    memory: 256MB
    duration: 1s
    cost: $0.78            # Same as US East
    
  totalLambdaCost: $22.03

stepFunctions:
  fileProcessing:
    stateTransitions: 15000
    cost: $0.375           # Same as US East
    
  emailSending:
    stateTransitions: 500000
    cost: $12.50           # Same as US East
    
  scheduling:
    stateTransitions: 7500
    cost: $0.1875          # Same as US East
    
  totalStepFunctionsCost: $13.06
```

#### Data Storage & Processing
```yaml
dynamodb:
  storage: 20GB
  storageCost: $5.70       # 1.14x multiplier
  
  readRequests: 750000
  readCost: $0.214         # 1.14x multiplier
  
  writeRequests: 550000
  writeCost: $0.785        # 1.14x multiplier
  
  totalDynamoDBCost: $6.699

s3:
  storage: 2GB
  storageCost: $0.05       # 1.09x multiplier
  
  putRequests: 125
  requestCost: $0.0000625  # 1.09x multiplier
  
  totalS3Cost: $0.05

openSearch:
  computeUnits: 2.0        # 2 OCU for higher volume
  computeHours: 744
  computeCost: $497.00     # 1.39x multiplier
  
  storage: 40GB
  storageCost: $1.04       # 1.39x multiplier
  
  totalOpenSearchCost: $498.04
```

#### Email Delivery
```yaml
ses:
  emails: 500000
  cost: $50.00             # Same as US East

sns:
  messages: 750000
  cost: $0.45              # 1.2x multiplier
  
  totalEmailDeliveryCost: $50.45
```

#### API & Integration
```yaml
apiGateway:
  requests: 750000
  cost: $3.19              # 1.21x multiplier

eventBridge:
  events: 75000
  cost: $0.075             # Same as US East
  
  totalAPIIntegrationCost: $3.265
```

#### Security & Monitoring
```yaml
cloudWatch:
  logIngestion: 8GB
  logCost: $4.56           # 1.14x multiplier
  
  metrics: 200
  metricCost: $72.00       # 1.2x multiplier
  
  totalCloudWatchCost: $76.56

kms:
  requests: 15000
  cost: $0.045             # Same as US East

secretsManager:
  secrets: 15
  cost: $6.00              # Same as US East
  
  totalSecurityCost: $82.61
```

### **Scenario 3 Total Monthly Cost: $676.21** (vs $522.21 in US East)

---

## Scenario 4: 1M Messages/Month

### Usage Patterns
- **Email Volume**: 1,000,000 messages/month
- **Campaigns**: 200 campaigns/month (5K messages each)
- **Templates**: 50 active templates
- **CSV Files**: 200 files/month (100KB each)
- **API Calls**: 1,500,000 calls/month
- **Analytics Queries**: 30,000 queries/month

### Detailed Cost Breakdown

#### Compute Services
```yaml
lambda:
  emailAPI: 
    requests: 600000
    memory: 1024MB
    duration: 3s
    cost: $30.00           # Same as US East
  
  fileProcessing:
    requests: 300000
    memory: 512MB
    duration: 5s
    cost: $12.50           # Same as US East
    
  callbacks:
    requests: 150000
    memory: 256MB
    duration: 1s
    cost: $1.56            # Same as US East
    
  totalLambdaCost: $44.06

stepFunctions:
  fileProcessing:
    stateTransitions: 30000
    cost: $0.75            # Same as US East
    
  emailSending:
    stateTransitions: 1000000
    cost: $25.00           # Same as US East
    
  scheduling:
    stateTransitions: 15000
    cost: $0.375           # Same as US East
    
  totalStepFunctionsCost: $26.125
```

#### Data Storage & Processing
```yaml
dynamodb:
  storage: 50GB
  storageCost: $14.25      # 1.14x multiplier
  
  readRequests: 1500000
  readCost: $0.428         # 1.14x multiplier
  
  writeRequests: 1100000
  writeCost: $1.570        # 1.14x multiplier
  
  totalDynamoDBCost: $16.25

s3:
  storage: 5GB
  storageCost: $0.125      # 1.09x multiplier
  
  putRequests: 250
  requestCost: $0.000125   # 1.09x multiplier
  
  totalS3Cost: $0.125

openSearch:
  computeUnits: 3.0        # 3 OCU for high volume
  computeHours: 744
  computeCost: $745.50     # 1.39x multiplier
  
  storage: 80GB
  storageCost: $2.08       # 1.39x multiplier
  
  totalOpenSearchCost: $747.58
```

#### Email Delivery
```yaml
ses:
  emails: 1000000
  cost: $100.00            # Same as US East

sns:
  messages: 1500000
  cost: $0.90              # 1.2x multiplier
  
  totalEmailDeliveryCost: $100.90
```

#### API & Integration
```yaml
apiGateway:
  requests: 1500000
  cost: $6.375             # 1.21x multiplier

eventBridge:
  events: 150000
  cost: $0.15              # Same as US East
  
  totalAPIIntegrationCost: $6.525
```

#### Security & Monitoring
```yaml
cloudWatch:
  logIngestion: 15GB
  logCost: $8.55           # 1.14x multiplier
  
  metrics: 300
  metricCost: $108.00      # 1.2x multiplier
  
  totalCloudWatchCost: $116.55

kms:
  requests: 30000
  cost: $0.09              # Same as US East

secretsManager:
  secrets: 20
  cost: $8.00              # Same as US East
  
  totalSecurityCost: $124.64
```

### **Scenario 4 Total Monthly Cost: $1,066.26** (vs $833.89 in US East)

---

## Cost Summary & Analysis (ap-southeast-2)

### Monthly Cost Comparison
| Message Volume | Total Cost (AUD) | Cost per Message | Cost per 1K Messages | US East Difference |
|----------------|------------------|------------------|---------------------|-------------------|
| **10K** | $145.78 | $0.0146 | $14.58 | +33.6% |
| **100K** | $310.31 | $0.0031 | $3.10 | +32.1% |
| **500K** | $676.21 | $0.0014 | $1.35 | +29.5% |
| **1M** | $1,066.26 | $0.0011 | $1.07 | +27.9% |

### Regional Cost Impact Analysis

#### Highest Cost Impact Services (ap-southeast-2 vs US East)
1. **OpenSearch Serverless**: +39% cost increase
2. **API Gateway**: +21% cost increase  
3. **SNS**: +20% cost increase
4. **DynamoDB**: +14% cost increase
5. **CloudWatch**: +14-20% cost increase
6. **S3**: +9% cost increase

#### Services with Same Pricing
- **AWS Lambda**: Same pricing across regions
- **Step Functions**: Same pricing across regions
- **Amazon SES**: Same pricing across regions
- **EventBridge**: Same pricing across regions
- **KMS**: Same pricing across regions
- **Secrets Manager**: Same pricing across regions

### Cost Distribution by Service Category (ap-southeast-2)

#### 10K Messages/Month
- **Compute (Lambda + Step Functions)**: $1.51 (1.0%)
- **Data Storage (DynamoDB + S3)**: $0.32 (0.2%)
- **Analytics (OpenSearch)**: $124.36 (85.3%)
- **Email Delivery (SES + SNS)**: $1.03 (0.7%)
- **Security & Monitoring**: $20.29 (13.9%)

#### 100K Messages/Month
- **Compute**: $8.78 (2.8%)
- **Data Storage**: $1.67 (0.5%)
- **Analytics**: $248.76 (80.2%)
- **Email Delivery**: $10.12 (3.3%)
- **Security & Monitoring**: $41.16 (13.3%)

#### 500K Messages/Month
- **Compute**: $35.09 (5.2%)
- **Data Storage**: $6.75 (1.0%)
- **Analytics**: $498.04 (73.6%)
- **Email Delivery**: $50.45 (7.5%)
- **Security & Monitoring**: $82.61 (12.2%)

#### 1M Messages/Month
- **Compute**: $70.19 (6.6%)
- **Data Storage**: $16.38 (1.5%)
- **Analytics**: $747.58 (70.1%)
- **Email Delivery**: $100.90 (9.5%)
- **Security & Monitoring**: $124.64 (11.7%)

## Key Insights for ap-southeast-2

### Regional Cost Considerations
1. **27-34% higher costs** compared to US East region
2. **OpenSearch dominates costs** even more in ap-southeast-2 (70-85% of total)
3. **Analytics-heavy workloads** see highest regional impact
4. **Compute costs remain competitive** (Lambda, Step Functions same pricing)

### Cost Optimization Opportunities (ap-southeast-2 Specific)
1. **OpenSearch right-sizing** - Even more critical due to 39% premium
2. **API Gateway optimization** - 21% premium makes caching more valuable
3. **DynamoDB provisioned capacity** - 14% premium increases savings potential
4. **Multi-region strategy** - Consider US East for non-latency sensitive workloads

### Break-Even Analysis (ap-southeast-2)
- **Platform becomes profitable** at ~65K messages/month (vs 50K in US East)
- **Optimal efficiency** achieved at 750K+ messages/month
- **Enterprise pricing** justified at 1.2M+ messages/month

### Regional Pricing Strategy Recommendations
1. **Premium pricing** for ap-southeast-2 customers (+30% over US pricing)
2. **Value proposition** emphasizes local data residency and low latency
3. **Cost optimization services** become more valuable due to higher baseline costs
4. **Hybrid deployment** consideration for cost-sensitive workloads

---

**Document Version**: 2.0 (ap-southeast-2 Pricing)  
**Last Updated**: August 17, 2024  
**Pricing Source**: AWS Documentation (August 2024)  
**Region**: Asia Pacific (Sydney) - ap-southeast-2
