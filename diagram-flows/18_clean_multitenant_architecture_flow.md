# Multi-Tenant Data Architecture - Flow Description

**Diagram**: `18_clean_multitenant_architecture.png`

## Overview
This diagram illustrates the multi-tenant silo model implementation, showing how data is completely isolated between tenants while maintaining operational efficiency through shared infrastructure.

## Component Flow Analysis

| Component | Type | Purpose | Tenant Isolation Method | Data Flow |
|-----------|------|---------|------------------------|-----------|
| Tenant A | External User | First tenant organization | Unique tenant ID | → API Gateway |
| Tenant B | External User | Second tenant organization | Unique tenant ID | → API Gateway |
| Tenant C | External User | Third tenant organization | Unique tenant ID | → API Gateway |
| API Gateway | API Layer | Request routing and validation | Tenant context extraction | → Tenant Resolver |
| Tenant Resolver | Service Layer | Tenant identification and context | Tenant ID validation | → Data Services |
| EmailPlatform Table | Database | Single DynamoDB table | Partition key prefixing | ← Tenant Resolver |
| Partition Keys | Data Pattern | Data organization strategy | TENANT#{id}#{entity}#{id} | Within DynamoDB |
| S3 Bucket | File Storage | Shared storage bucket | Folder-based isolation | ← Tenant Resolver |
| Tenant Folders | Storage Pattern | Folder organization | tenant-{id}/ prefix | Within S3 Bucket |
| OpenSearch | Analytics | Shared search cluster | Index-based isolation | ← Tenant Resolver |
| Tenant Indexes | Index Pattern | Search index organization | email-tenant-{id} | Within OpenSearch |

## Multi-Tenancy Implementation

### Tenant Identification Flow
```
User Request → API Gateway → Extract Tenant Context → Validate Tenant → Route to Services
```

### Data Access Pattern
```
Service Request → Tenant Context → Partition Key Generation → Data Access → Tenant-Filtered Results
```

### Storage Isolation Pattern
```
File Operation → Tenant Context → Path Generation → Tenant-Specific Storage → Isolated Access
```

## Data Isolation Strategies

### DynamoDB Single Table Design

#### Partition Key Patterns
| Entity Type | Partition Key Format | Sort Key Format | Example |
|-------------|---------------------|-----------------|---------|
| Tenant Config | `TENANT#{tenantId}` | `CONFIG` | `TENANT#A#CONFIG` |
| User Profile | `TENANT#{tenantId}` | `USER#{userId}` | `TENANT#A#USER#123` |
| Campaign | `TENANT#{tenantId}` | `CAMPAIGN#{campaignId}` | `TENANT#A#CAMPAIGN#456` |
| Template | `TENANT#{tenantId}` | `TEMPLATE#{templateId}` | `TENANT#A#TEMPLATE#789` |
| Recipient List | `TENANT#{tenantId}` | `LIST#{listId}` | `TENANT#A#LIST#101` |
| Analytics | `TENANT#{tenantId}` | `ANALYTICS#{date}#{metric}` | `TENANT#A#ANALYTICS#2024-01-15#OPENS` |

#### Access Pattern Examples
```javascript
// Get all campaigns for Tenant A
const params = {
  TableName: 'EmailPlatform',
  KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
  ExpressionAttributeValues: {
    ':pk': 'TENANT#A',
    ':sk': 'CAMPAIGN#'
  }
};

// Get specific user for Tenant B
const params = {
  TableName: 'EmailPlatform',
  Key: {
    'PK': 'TENANT#B',
    'SK': 'USER#123'
  }
};
```

### S3 Folder-Based Isolation

#### Folder Structure
```
s3://email-platform-storage/
├── tenant-a/
│   ├── templates/
│   │   ├── html/
│   │   ├── images/
│   │   └── css/
│   ├── exports/
│   └── backups/
├── tenant-b/
│   ├── templates/
│   ├── exports/
│   └── backups/
└── tenant-c/
    ├── templates/
    ├── exports/
    └── backups/
```

#### Access Control Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::account:role/EmailPlatformRole"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::email-platform-storage/tenant-${aws:userid}/*"
    }
  ]
}
```

### OpenSearch Index Isolation

#### Index Naming Convention
| Tenant | Index Name | Purpose | Data Types |
|---------|------------|---------|------------|
| Tenant A | `email-analytics-tenant-a` | Email analytics | Opens, clicks, bounces |
| Tenant B | `email-analytics-tenant-b` | Email analytics | Opens, clicks, bounces |
| Tenant C | `email-analytics-tenant-c` | Email analytics | Opens, clicks, bounces |

#### Index Template
```json
{
  "index_patterns": ["email-analytics-tenant-*"],
  "template": {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 1
    },
    "mappings": {
      "properties": {
        "tenantId": { "type": "keyword" },
        "campaignId": { "type": "keyword" },
        "eventType": { "type": "keyword" },
        "timestamp": { "type": "date" },
        "recipient": { "type": "keyword" },
        "metadata": { "type": "object" }
      }
    }
  }
}
```

## Tenant Context Management

### Tenant Resolution Process
```javascript
class TenantResolver {
  async resolveTenant(request) {
    // Extract tenant from JWT token
    const token = this.extractJWTToken(request);
    const claims = this.validateToken(token);
    const tenantId = claims['custom:tenantId'];
    
    // Validate tenant exists and is active
    const tenant = await this.validateTenant(tenantId);
    
    return {
      tenantId: tenantId,
      tenantName: tenant.name,
      permissions: claims['custom:permissions'],
      partitionPrefix: `TENANT#${tenantId}`,
      s3Prefix: `tenant-${tenantId}`,
      searchIndex: `email-analytics-tenant-${tenantId}`
    };
  }
}
```

### Data Access Layer
```javascript
class TenantAwareDataAccess {
  constructor(tenantContext) {
    this.tenantContext = tenantContext;
  }
  
  async getCampaigns() {
    const params = {
      TableName: 'EmailPlatform',
      KeyConditionExpression: 'PK = :pk AND begins_with(SK, :sk)',
      ExpressionAttributeValues: {
        ':pk': this.tenantContext.partitionPrefix,
        ':sk': 'CAMPAIGN#'
      }
    };
    
    return await this.dynamodb.query(params).promise();
  }
  
  async storeTemplate(templateData) {
    const s3Key = `${this.tenantContext.s3Prefix}/templates/${templateData.id}.html`;
    
    return await this.s3.putObject({
      Bucket: 'email-platform-storage',
      Key: s3Key,
      Body: templateData.content
    }).promise();
  }
}
```

## Security and Compliance

### Data Isolation Guarantees
- **Physical Separation**: No shared data structures between tenants
- **Logical Separation**: Partition keys prevent cross-tenant access
- **Access Control**: IAM policies enforce tenant boundaries
- **Audit Trail**: All access logged with tenant context

### Compliance Features
- **GDPR Compliance**: Tenant-specific data deletion
- **Data Residency**: Geographic data placement per tenant
- **Audit Logging**: Comprehensive access logging
- **Encryption**: Tenant-specific encryption keys (optional)

### Security Measures
```javascript
// Tenant boundary validation
function validateTenantAccess(requestTenant, resourceTenant) {
  if (requestTenant !== resourceTenant) {
    throw new Error('Cross-tenant access denied');
  }
}

// Automatic tenant context injection
function injectTenantContext(query, tenantId) {
  if (!query.KeyConditionExpression.includes('TENANT#')) {
    throw new Error('Query must include tenant context');
  }
}
```

## Performance Considerations

### DynamoDB Optimization
- **Hot Partition Avoidance**: Distributed partition keys
- **GSI Design**: Tenant-aware global secondary indexes
- **Batch Operations**: Tenant-scoped batch operations
- **Connection Pooling**: Shared connections across tenants

### S3 Optimization
- **Prefix Distribution**: Avoid hot-spotting with random prefixes
- **Multipart Upload**: Efficient large file uploads
- **Lifecycle Policies**: Tenant-specific data lifecycle
- **Transfer Acceleration**: Global upload optimization

### OpenSearch Optimization
- **Index Sharding**: Appropriate shard count per tenant
- **Replica Strategy**: Balanced replica distribution
- **Query Optimization**: Tenant-scoped queries
- **Aggregation Caching**: Tenant-specific caching

## Operational Management

### Tenant Onboarding
```javascript
async function onboardTenant(tenantData) {
  // Create tenant record
  await createTenantRecord(tenantData);
  
  // Initialize S3 folder structure
  await initializeTenantStorage(tenantData.id);
  
  // Create OpenSearch index
  await createTenantIndex(tenantData.id);
  
  // Set up monitoring
  await setupTenantMonitoring(tenantData.id);
}
```

### Tenant Offboarding
```javascript
async function offboardTenant(tenantId) {
  // Delete all tenant data
  await deleteTenantData(tenantId);
  
  // Remove S3 objects
  await deleteTenantStorage(tenantId);
  
  // Delete OpenSearch index
  await deleteTenantIndex(tenantId);
  
  // Clean up monitoring
  await cleanupTenantMonitoring(tenantId);
}
```

### Monitoring and Metrics
- **Per-Tenant Metrics**: Usage, performance, errors
- **Cross-Tenant Analytics**: Platform-wide insights
- **Cost Allocation**: Tenant-specific cost tracking
- **Capacity Planning**: Per-tenant growth projections

## Scalability Patterns

### Horizontal Scaling
- **Tenant Sharding**: Distribute tenants across regions
- **Index Scaling**: Scale OpenSearch clusters per tenant tier
- **Storage Scaling**: Automatic S3 scaling
- **Compute Scaling**: Lambda auto-scaling per tenant load

### Vertical Scaling
- **Resource Allocation**: Tenant-specific resource limits
- **Performance Tiers**: Different service levels per tenant
- **Capacity Reservations**: Guaranteed capacity for premium tenants
- **Priority Queuing**: Tenant-based processing priorities

## Cost Optimization

### Resource Sharing
- **Infrastructure Sharing**: Shared AWS services
- **Operational Efficiency**: Single operational model
- **Bulk Purchasing**: Shared reserved capacity
- **Automation**: Shared automation and tooling

### Cost Allocation
```javascript
// Cost allocation by tenant
const costAllocation = {
  tenantA: {
    dynamodbCost: calculateDynamoDBCost('TENANT#A'),
    s3Cost: calculateS3Cost('tenant-a/'),
    lambdaCost: calculateLambdaCost('tenant-a'),
    sesCost: calculateSESCost('tenant-a')
  }
};
```

### Usage-Based Pricing
- **Metered Billing**: Pay-per-use model
- **Tier-Based Pricing**: Different pricing tiers
- **Resource Limits**: Tenant-specific quotas
- **Overage Charges**: Usage beyond limits
