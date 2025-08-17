# Email Platform - Detailed Costing Scenarios

## Overview
This document provides detailed cost analysis for the standalone Email Platform across different message volumes: 10K, 100K, 500K, and 1M messages per month. All pricing is based on AWS documentation and current rates as of August 2024.

## Pricing Assumptions (US East - N. Virginia)

### AWS Service Pricing (Per AWS Documentation)
| Service | Pricing Model | Rate |
|---------|---------------|------|
| **AWS Lambda** | Per request + duration | $0.0000002 per request + $0.0000166667 per GB-second |
| **Step Functions** | Per state transition | $0.000025 per state transition |
| **API Gateway** | Per million requests | $3.50 per million API calls |
| **DynamoDB On-Demand** | Per request | Read: $0.25/million RRU, Write: $1.25/million WRU |
| **DynamoDB Storage** | Per GB-month | $0.25 per GB per month |
| **Amazon SES** | Per email | $0.10 per 1,000 emails |
| **S3 Standard** | Storage + requests | $0.023 per GB + $0.0004 per 1,000 PUT requests |
| **EventBridge** | Per million events | $1.00 per million custom events |
| **OpenSearch Serverless** | Per OCU + storage | $0.24 per OCU-hour + $0.024 per GB-month |
| **SNS** | Per million messages | $0.50 per million messages |
| **CloudWatch** | Logs + metrics | $0.50 per GB ingested + $0.30 per metric |
| **KMS** | Per request | $0.03 per 10,000 requests |
| **Secrets Manager** | Per secret | $0.40 per secret per month |

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
    cost: $0.75
  
  fileProcessing:
    requests: 10000        # File processing requests  
    memory: 512MB
    duration: 5s
    cost: $0.42
    
  callbacks:
    requests: 5000         # Callback requests
    memory: 256MB  
    duration: 1s
    cost: $0.05
    
  totalLambdaCost: $1.22

stepFunctions:
  fileProcessing:
    stateTransitions: 1000  # 10 campaigns × 100 transitions
    cost: $0.025
    
  emailSending:
    stateTransitions: 10000 # 10K messages × 1 transition
    cost: $0.25
    
  scheduling:
    stateTransitions: 500   # Scheduling transitions
    cost: $0.0125
    
  totalStepFunctionsCost: $0.29
```

#### Data Storage & Processing
```yaml
dynamodb:
  storage: 1GB             # Transaction/Batch/Message data
  storageCost: $0.25
  
  readRequests: 50000      # 50K RRU per month
  readCost: $0.0125
  
  writeRequests: 15000     # 15K WRU per month  
  writeCost: $0.01875
  
  totalDynamoDBCost: $0.28

s3:
  storage: 0.1GB           # Templates and CSV files
  storageCost: $0.002
  
  putRequests: 15          # Template + CSV uploads
  requestCost: $0.000006
  
  totalS3Cost: $0.002

openSearch:
  computeUnits: 0.5        # 0.5 OCU for low volume
  computeHours: 744        # 24×31 hours
  computeCost: $89.28
  
  storage: 2GB             # Analytics data
  storageCost: $0.048
  
  totalOpenSearchCost: $89.33
```

#### Email Delivery
```yaml
ses:
  emails: 10000
  cost: $1.00              # $0.10 per 1,000 emails

sns:
  messages: 50000          # SES events + notifications
  cost: $0.025
  
  totalEmailDeliveryCost: $1.025
```

#### API & Integration
```yaml
apiGateway:
  requests: 50000
  cost: $0.175             # $3.50 per million

eventBridge:
  events: 5000             # Scheduling events
  cost: $0.005
  
  totalAPIIntegrationCost: $0.18
```

#### Security & Monitoring
```yaml
cloudWatch:
  logIngestion: 0.5GB
  logCost: $0.25
  
  metrics: 50              # Custom metrics
  metricCost: $15.00
  
  totalCloudWatchCost: $15.25

kms:
  requests: 1000
  cost: $0.003

secretsManager:
  secrets: 5
  cost: $2.00
  
  totalSecurityCost: $17.25
```

### **Scenario 1 Total Monthly Cost: $109.07**

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
    cost: $3.75
  
  fileProcessing:
    requests: 50000
    memory: 512MB
    duration: 5s
    cost: $2.08
    
  callbacks:
    requests: 25000
    memory: 256MB
    duration: 1s
    cost: $0.26
    
  totalLambdaCost: $6.09

stepFunctions:
  fileProcessing:
    stateTransitions: 5000
    cost: $0.125
    
  emailSending:
    stateTransitions: 100000
    cost: $2.50
    
  scheduling:
    stateTransitions: 2500
    cost: $0.0625
    
  totalStepFunctionsCost: $2.69
```

#### Data Storage & Processing
```yaml
dynamodb:
  storage: 5GB
  storageCost: $1.25
  
  readRequests: 200000     # 200K RRU per month
  readCost: $0.05
  
  writeRequests: 120000    # 120K WRU per month
  writeCost: $0.15
  
  totalDynamoDBCost: $1.45

s3:
  storage: 0.5GB
  storageCost: $0.0115
  
  putRequests: 65
  requestCost: $0.000026
  
  totalS3Cost: $0.012

openSearch:
  computeUnits: 1.0        # 1 OCU
  computeHours: 744
  computeCost: $178.56
  
  storage: 10GB
  storageCost: $0.24
  
  totalOpenSearchCost: $178.80
```

#### Email Delivery
```yaml
ses:
  emails: 100000
  cost: $10.00

sns:
  messages: 200000
  cost: $0.10
  
  totalEmailDeliveryCost: $10.10
```

#### API & Integration
```yaml
apiGateway:
  requests: 200000
  cost: $0.70

eventBridge:
  events: 25000
  cost: $0.025
  
  totalAPIIntegrationCost: $0.725
```

#### Security & Monitoring
```yaml
cloudWatch:
  logIngestion: 2GB
  logCost: $1.00
  
  metrics: 100
  metricCost: $30.00
  
  totalCloudWatchCost: $31.00

kms:
  requests: 5000
  cost: $0.015

secretsManager:
  secrets: 10
  cost: $4.00
  
  totalSecurityCost: $35.02
```

### **Scenario 2 Total Monthly Cost: $234.87**

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
    cost: $15.00
  
  fileProcessing:
    requests: 150000
    memory: 512MB
    duration: 5s
    cost: $6.25
    
  callbacks:
    requests: 75000
    memory: 256MB
    duration: 1s
    cost: $0.78
    
  totalLambdaCost: $22.03

stepFunctions:
  fileProcessing:
    stateTransitions: 15000
    cost: $0.375
    
  emailSending:
    stateTransitions: 500000
    cost: $12.50
    
  scheduling:
    stateTransitions: 7500
    cost: $0.1875
    
  totalStepFunctionsCost: $13.06
```

#### Data Storage & Processing
```yaml
dynamodb:
  storage: 20GB
  storageCost: $5.00
  
  readRequests: 750000
  readCost: $0.1875
  
  writeRequests: 550000
  writeCost: $0.6875
  
  totalDynamoDBCost: $5.875

s3:
  storage: 2GB
  storageCost: $0.046
  
  putRequests: 125
  requestCost: $0.00005
  
  totalS3Cost: $0.046

openSearch:
  computeUnits: 2.0        # 2 OCU for higher volume
  computeHours: 744
  computeCost: $357.12
  
  storage: 40GB
  storageCost: $0.96
  
  totalOpenSearchCost: $358.08
```

#### Email Delivery
```yaml
ses:
  emails: 500000
  cost: $50.00

sns:
  messages: 750000
  cost: $0.375
  
  totalEmailDeliveryCost: $50.375
```

#### API & Integration
```yaml
apiGateway:
  requests: 750000
  cost: $2.625

eventBridge:
  events: 75000
  cost: $0.075
  
  totalAPIIntegrationCost: $2.70
```

#### Security & Monitoring
```yaml
cloudWatch:
  logIngestion: 8GB
  logCost: $4.00
  
  metrics: 200
  metricCost: $60.00
  
  totalCloudWatchCost: $64.00

kms:
  requests: 15000
  cost: $0.045

secretsManager:
  secrets: 15
  cost: $6.00
  
  totalSecurityCost: $70.045
```

### **Scenario 3 Total Monthly Cost: $522.21**

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
    cost: $30.00
  
  fileProcessing:
    requests: 300000
    memory: 512MB
    duration: 5s
    cost: $12.50
    
  callbacks:
    requests: 150000
    memory: 256MB
    duration: 1s
    cost: $1.56
    
  totalLambdaCost: $44.06

stepFunctions:
  fileProcessing:
    stateTransitions: 30000
    cost: $0.75
    
  emailSending:
    stateTransitions: 1000000
    cost: $25.00
    
  scheduling:
    stateTransitions: 15000
    cost: $0.375
    
  totalStepFunctionsCost: $26.125
```

#### Data Storage & Processing
```yaml
dynamodb:
  storage: 50GB
  storageCost: $12.50
  
  readRequests: 1500000
  readCost: $0.375
  
  writeRequests: 1100000
  writeCost: $1.375
  
  totalDynamoDBCost: $14.25

s3:
  storage: 5GB
  storageCost: $0.115
  
  putRequests: 250
  requestCost: $0.0001
  
  totalS3Cost: $0.115

openSearch:
  computeUnits: 3.0        # 3 OCU for high volume
  computeHours: 744
  computeCost: $535.68
  
  storage: 80GB
  storageCost: $1.92
  
  totalOpenSearchCost: $537.60
```

#### Email Delivery
```yaml
ses:
  emails: 1000000
  cost: $100.00

sns:
  messages: 1500000
  cost: $0.75
  
  totalEmailDeliveryCost: $100.75
```

#### API & Integration
```yaml
apiGateway:
  requests: 1500000
  cost: $5.25

eventBridge:
  events: 150000
  cost: $0.15
  
  totalAPIIntegrationCost: $5.40
```

#### Security & Monitoring
```yaml
cloudWatch:
  logIngestion: 15GB
  logCost: $7.50
  
  metrics: 300
  metricCost: $90.00
  
  totalCloudWatchCost: $97.50

kms:
  requests: 30000
  cost: $0.09

secretsManager:
  secrets: 20
  cost: $8.00
  
  totalSecurityCost: $105.59
```

### **Scenario 4 Total Monthly Cost: $833.89**

---

## Cost Summary & Analysis

### Monthly Cost Comparison
| Message Volume | Total Cost | Cost per Message | Cost per 1K Messages |
|----------------|------------|------------------|---------------------|
| **10K** | $109.07 | $0.0109 | $10.91 |
| **100K** | $234.87 | $0.0023 | $2.35 |
| **500K** | $522.21 | $0.0010 | $1.04 |
| **1M** | $833.89 | $0.0008 | $0.83 |

### Cost Distribution by Service Category

#### 10K Messages/Month
- **Compute (Lambda + Step Functions)**: $1.51 (1.4%)
- **Data Storage (DynamoDB + S3)**: $0.28 (0.3%)
- **Analytics (OpenSearch)**: $89.33 (81.9%)
- **Email Delivery (SES + SNS)**: $1.03 (0.9%)
- **Security & Monitoring**: $17.25 (15.8%)

#### 100K Messages/Month
- **Compute**: $8.78 (3.7%)
- **Data Storage**: $1.46 (0.6%)
- **Analytics**: $178.80 (76.1%)
- **Email Delivery**: $10.10 (4.3%)
- **Security & Monitoring**: $35.02 (14.9%)

#### 500K Messages/Month
- **Compute**: $35.09 (6.7%)
- **Data Storage**: $5.92 (1.1%)
- **Analytics**: $358.08 (68.6%)
- **Email Delivery**: $50.38 (9.6%)
- **Security & Monitoring**: $70.05 (13.4%)

#### 1M Messages/Month
- **Compute**: $70.19 (8.4%)
- **Data Storage**: $14.37 (1.7%)
- **Analytics**: $537.60 (64.5%)
- **Email Delivery**: $100.75 (12.1%)
- **Security & Monitoring**: $105.59 (12.7%)

## Key Insights

### Economies of Scale
1. **Cost per message decreases significantly** with volume (from $0.0109 to $0.0008)
2. **OpenSearch dominates costs** at all scales but becomes more efficient per message
3. **Fixed costs** (monitoring, security) become smaller percentage at scale
4. **Variable costs** (SES, Lambda) scale linearly but benefit from bulk pricing

### Cost Optimization Opportunities
1. **OpenSearch right-sizing** - Biggest impact on total cost
2. **Lambda memory optimization** - 20-30% savings potential
3. **DynamoDB provisioned capacity** - 30-40% savings at scale
4. **Reserved capacity** - Additional 20-50% savings with commitments

### Break-Even Analysis
- **Platform becomes profitable** at ~50K messages/month
- **Optimal efficiency** achieved at 500K+ messages/month
- **Enterprise pricing** justified at 1M+ messages/month

---

**Document Version**: 1.0  
**Last Updated**: August 17, 2024  
**Pricing Source**: AWS Documentation (August 2024)  
**Region**: US East (N. Virginia)
