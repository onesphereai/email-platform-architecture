# Email Platform Architecture Documentation

## Executive Summary

The Email Platform is a self-service email marketing solution designed to provide B2B customers with comprehensive email campaign management capabilities. Built on AWS cloud infrastructure, the platform enables users to create, send, and manage email campaigns through an intuitive web interface while maintaining enterprise-grade security, scalability, and compliance.

## Architecture Overview

### High-Level Architecture Principles

1. **Multi-Tenancy**: Silo model implementation ensuring complete data isolation between tenants
2. **Scalability**: Serverless architecture with auto-scaling capabilities
3. **Security**: End-to-end encryption, SAML authentication, and comprehensive access controls
4. **Performance**: Asynchronous processing with throttling and delivery optimization
5. **Compliance**: GDPR, CCPA compliance with email standards (DKIM, DMARC, SPF)
6. **Cost Efficiency**: Pay-per-use model with optimized resource utilization

### Technology Stack

- **Frontend**: Angular (TypeScript)
- **Backend**: Node.js/TypeScript on AWS Lambda
- **Database**: Amazon DynamoDB (Single Table Design)
- **Authentication**: AWS Cognito with SAML integration
- **Email Service**: Amazon SES
- **Message Queuing**: Amazon SQS/SNS
- **Analytics**: Amazon OpenSearch Serverless
- **Monitoring**: Amazon CloudWatch
- **Infrastructure**: Serverless Framework (IaC)
- **CI/CD**: Jenkins (On-premise)

## System Architecture Components

### Core Components

#### 1. Email Platform UI/Backend
- **Purpose**: Self-service web interface for email campaign management
- **Technology**: Angular frontend with TypeScript Lambda backend
- **Features**:
  - Drag-and-drop email builder
  - Campaign management
  - Recipient list management
  - Real-time analytics dashboard
  - Template library

#### 2. Email API
- **Purpose**: Standalone API for programmatic email sending
- **Security**: x-api-key (required), OAuth2 (optional), mTLS (optional)
- **Features**:
  - RESTful API endpoints
  - Bulk email processing
  - Delivery status tracking
  - Webhook notifications

#### 3. Message Centre Integration
- **Purpose**: Integration with existing Message Centre ecosystem
- **Components**:
  - External Reporting API
  - Contact Management integration
  - Cross-platform analytics

## Detailed Architecture

### Data Architecture

#### DynamoDB Single Table Design

**Table Structure**: `EmailPlatform`

**Access Patterns**:
1. Get tenant configuration: `PK=TENANT#{tenantId}`, `SK=CONFIG`
2. Get user profile: `PK=TENANT#{tenantId}`, `SK=USER#{userId}`
3. Get campaign: `PK=TENANT#{tenantId}`, `SK=CAMPAIGN#{campaignId}`
4. Get campaign templates: `PK=TENANT#{tenantId}`, `SK=TEMPLATE#{templateId}`
5. Get delivery reports: `PK=TENANT#{tenantId}`, `SK=REPORT#{campaignId}#{timestamp}`
6. Get recipient lists: `PK=TENANT#{tenantId}`, `SK=LIST#{listId}`

**Global Secondary Indexes**:
- **GSI1**: Campaign status queries (`GSI1PK=TENANT#{tenantId}#STATUS#{status}`)
- **GSI2**: Time-based queries (`GSI2PK=TENANT#{tenantId}#DATE#{date}`)

### Security Architecture

#### Authentication & Authorization
- **AWS Cognito User Pool**: SAML 2.0 integration with enterprise identity providers
- **JWT Tokens**: Stateless authentication with role-based access control
- **API Gateway**: Request validation and rate limiting
- **IAM Roles**: Fine-grained permissions for AWS services

#### Data Protection
- **Encryption at Rest**: AWS KMS encryption for DynamoDB and S3
- **Encryption in Transit**: TLS 1.2+ for all communications
- **Data Sovereignty**: Australian data residency compliance
- **PII Protection**: Tokenization and masking of sensitive data

### Email Delivery Architecture

#### Amazon SES Configuration
- **Domain Authentication**: SPF, DKIM, DMARC setup
- **Reputation Management**: Dedicated IP pools and monitoring
- **Bounce/Complaint Handling**: Automated suppression list management
- **Delivery Optimization**: Throttling and retry mechanisms

#### Processing Pipeline
1. **Campaign Creation**: Template validation and recipient list processing
2. **Queue Management**: SQS for reliable message delivery
3. **Batch Processing**: Lambda functions for bulk email sending
4. **Status Tracking**: Real-time delivery status updates
5. **Analytics**: OpenSearch for advanced reporting

## API Specifications

### Email API Endpoints

#### Authentication
All API requests require authentication via one of the following methods:
- **x-api-key**: Required header for all requests
- **OAuth2**: Optional Bearer token authentication
- **mTLS**: Optional mutual TLS authentication

#### Core Endpoints

##### 1. Campaign Management

**POST /api/v1/campaigns**
```json
{
  "name": "string",
  "subject": "string",
  "template": {
    "html": "string",
    "text": "string"
  },
  "recipients": [
    {
      "email": "string",
      "variables": {}
    }
  ],
  "schedule": {
    "sendAt": "ISO8601",
    "timezone": "string"
  },
  "settings": {
    "throttle": "number",
    "deliveryWindow": {
      "start": "HH:MM",
      "end": "HH:MM"
    }
  }
}
```

**GET /api/v1/campaigns/{campaignId}**
```json
{
  "id": "string",
  "name": "string",
  "status": "draft|scheduled|sending|sent|failed",
  "created": "ISO8601",
  "statistics": {
    "sent": "number",
    "delivered": "number",
    "bounced": "number",
    "complained": "number",
    "opened": "number",
    "clicked": "number"
  }
}
```

##### 2. Template Management

**POST /api/v1/templates**
```json
{
  "name": "string",
  "description": "string",
  "html": "string",
  "text": "string",
  "variables": ["string"],
  "category": "string"
}
```

##### 3. Recipient Management

**POST /api/v1/recipients/lists**
```json
{
  "name": "string",
  "description": "string",
  "recipients": [
    {
      "email": "string",
      "firstName": "string",
      "lastName": "string",
      "customFields": {}
    }
  ]
}
```

##### 4. Analytics & Reporting

**GET /api/v1/campaigns/{campaignId}/analytics**
```json
{
  "campaignId": "string",
  "period": {
    "start": "ISO8601",
    "end": "ISO8601"
  },
  "metrics": {
    "deliveryRate": "number",
    "openRate": "number",
    "clickRate": "number",
    "bounceRate": "number",
    "complaintRate": "number"
  },
  "timeline": [
    {
      "timestamp": "ISO8601",
      "sent": "number",
      "delivered": "number",
      "opened": "number",
      "clicked": "number"
    }
  ]
}
```

### Error Handling

#### Standard HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request
- **401**: Unauthorized
- **403**: Forbidden
- **404**: Not Found
- **429**: Too Many Requests
- **500**: Internal Server Error

#### Error Response Format
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {},
    "timestamp": "ISO8601",
    "requestId": "string"
  }
}
```

## Deployment Architecture

### CI/CD Pipeline

#### Jenkins Pipeline Stages
1. **Source Control**: Bitbucket integration with webhook triggers
2. **Build**: TypeScript compilation and Angular build
3. **Test**: Unit tests, integration tests, and security scans
4. **Package**: Serverless Framework packaging
5. **Deploy**: Environment-specific deployments
6. **Verify**: Health checks and smoke tests
7. **Monitor**: CloudWatch alerts and notifications

#### Environment Strategy
- **Development**: Feature development and testing
- **Staging**: Pre-production validation
- **Production**: Live customer environment

#### Deployment Strategy
- **Blue/Green Deployments**: Zero-downtime deployments
- **Rollback Capability**: Automated rollback on failure detection
- **Feature Flags**: Gradual feature rollout

### Infrastructure as Code

#### Serverless Framework Configuration
```yaml
service: email-platform
provider:
  name: aws
  runtime: nodejs18.x
  region: ap-southeast-2
  stage: ${opt:stage, 'dev'}
  
functions:
  api:
    handler: src/handler.api
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
          authorizer:
            name: cognitoAuthorizer
            type: COGNITO_USER_POOLS
            arn: ${self:custom.cognitoUserPoolArn}

resources:
  Resources:
    EmailPlatformTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:service}-${self:provider.stage}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: PK
            AttributeType: S
          - AttributeName: SK
            AttributeType: S
        KeySchema:
          - AttributeName: PK
            KeyType: HASH
          - AttributeName: SK
            KeyType: RANGE
```

## Monitoring and Observability

### CloudWatch Metrics
- **Application Metrics**: Request latency, error rates, throughput
- **Business Metrics**: Campaign success rates, delivery statistics
- **Infrastructure Metrics**: Lambda duration, DynamoDB throttling
- **Cost Metrics**: Service usage and billing alerts

### Logging Strategy
- **Structured Logging**: JSON format with correlation IDs
- **Log Levels**: ERROR, WARN, INFO, DEBUG
- **Retention**: 30 days for application logs, 1 year for audit logs
- **Centralized Logging**: CloudWatch Logs with log groups per service

### Alerting
- **Critical Alerts**: Service outages, high error rates
- **Warning Alerts**: Performance degradation, quota limits
- **Business Alerts**: Campaign failures, delivery issues

## Security Considerations

### Data Privacy
- **GDPR Compliance**: Right to be forgotten, data portability
- **Data Minimization**: Collect only necessary data
- **Consent Management**: Explicit opt-in mechanisms
- **Data Retention**: Automated data lifecycle management

### Email Security
- **SPF Records**: Sender Policy Framework validation
- **DKIM Signing**: DomainKeys Identified Mail authentication
- **DMARC Policy**: Domain-based Message Authentication
- **Reputation Monitoring**: Blacklist and reputation tracking

### Access Control
- **Principle of Least Privilege**: Minimal required permissions
- **Role-Based Access Control**: Granular permission management
- **Multi-Factor Authentication**: Enhanced security for admin access
- **Session Management**: Secure token handling and expiration

## Performance Optimization

### Caching Strategy
- **API Gateway Caching**: Response caching for static data
- **Application Caching**: In-memory caching for frequently accessed data
- **CDN**: CloudFront for static assets and UI resources

### Database Optimization
- **Single Table Design**: Optimized for DynamoDB access patterns
- **Hot Partition Avoidance**: Distributed partition key design
- **Read/Write Capacity**: Auto-scaling based on demand
- **Global Secondary Indexes**: Optimized for query patterns

### Email Delivery Optimization
- **Throttling**: Configurable sending rates per tenant
- **Delivery Windows**: Time-based sending restrictions
- **Retry Logic**: Exponential backoff for failed deliveries
- **Batch Processing**: Optimized batch sizes for SES

## Compliance and Governance

### Regulatory Compliance
- **CAN-SPAM Act**: US anti-spam legislation compliance
- **Australian Spam Act**: Local anti-spam requirements
- **GDPR**: European data protection regulation
- **CCPA**: California Consumer Privacy Act

### Audit and Compliance
- **Audit Logging**: Comprehensive activity tracking
- **Data Lineage**: Track data flow and transformations
- **Compliance Reporting**: Automated compliance reports
- **Regular Audits**: Security and compliance assessments

## Disaster Recovery

### Backup Strategy
- **Database Backups**: Point-in-time recovery for DynamoDB
- **Code Backups**: Version control and artifact storage
- **Configuration Backups**: Infrastructure state management

### Recovery Procedures
- **RTO**: Recovery Time Objective of 4 hours
- **RPO**: Recovery Point Objective of 1 hour
- **Multi-AZ Deployment**: High availability across availability zones
- **Cross-Region Replication**: Disaster recovery in alternate region

## Cost Optimization

### Cost Management
- **Pay-per-Use**: Serverless architecture minimizes idle costs
- **Resource Tagging**: Comprehensive cost allocation
- **Budget Alerts**: Proactive cost monitoring
- **Reserved Capacity**: Cost optimization for predictable workloads

### Performance vs Cost Trade-offs
- **Lambda Memory**: Optimized for performance and cost
- **DynamoDB Capacity**: On-demand vs provisioned capacity
- **SES Pricing**: Dedicated IP vs shared IP pools
- **Storage Optimization**: S3 storage classes for different data types

## Future Roadmap

### Phase 1 (MVP) - Q1 2024
- Basic email campaign creation and sending
- Simple drag-and-drop builder
- Basic reporting and analytics
- SAML authentication integration

### Phase 2 - Q2 2024
- Advanced template management
- A/B testing capabilities
- Enhanced analytics and reporting
- API access for external integrations

### Phase 3 - Q3 2024
- Marketing automation workflows
- Advanced segmentation
- CRM integrations
- Multi-brand support

### Phase 4 - Q4 2024
- AI-powered content optimization
- Advanced personalization
- Cross-channel campaign orchestration
- Enterprise-grade governance features

## Conclusion

The Email Platform architecture provides a robust, scalable, and secure foundation for enterprise email marketing capabilities. The serverless design ensures cost-effectiveness while maintaining high performance and availability. The multi-tenant architecture supports business growth while ensuring data isolation and security compliance.

The platform's modular design allows for incremental feature development and deployment, supporting the MVP-first approach while maintaining architectural flexibility for future enhancements.
