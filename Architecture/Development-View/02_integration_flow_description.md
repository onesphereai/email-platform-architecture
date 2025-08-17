# Integration Flow Description

## Overview
This diagram details the step-by-step integration flow between Message Centre and the standalone Email Platform, showing how templates and email campaigns are processed.

## Flow Steps

### Template Upload Process (Steps 1-3)
1. **Get Presigned URL**: Message Centre API requests presigned URL from Email Platform
2. **Receive URL**: Email Platform returns secure presigned URL for S3 upload
3. **Upload Template**: Message Centre uploads template directly to S3 using presigned URL

### Email Campaign Processing (Steps 4-6)
4. **Upload CSV**: User uploads CSV file with recipient data through Message Centre
5. **Trigger Processing**: Message Centre API calls Email Platform to start processing
6. **Process File**: File Processor Step Functions split CSV and create message records

### Message Storage & Scheduling (Steps 7-8)
7. **Store Messages**: Individual message records stored in DynamoDB with status tracking
8. **Schedule (Optional)**: If scheduling enabled, EventBridge creates scheduled events

### Email Delivery Pipeline (Steps 9-10)
9. **Trigger Send**: DynamoDB streams or scheduled events trigger Send Pipeline
10. **Send Emails**: Step Functions orchestrate email sending through Amazon SES

### Analytics & Monitoring (Steps 11-12)
11. **SES Events**: Delivery, bounce, complaint, open, and click events flow to OpenSearch
12. **Analytics Data**: Message status and transaction data replicated to OpenSearch

### Status Tracking (Step 13)
13. **Status Check**: Message Centre can query Email Platform Status API for real-time updates

## API Endpoints

### Template Management
```http
POST /api/v1/templates/presigned-url
GET /api/v1/templates/{template_id}
```

### Email Processing
```http
POST /api/v1/campaigns
GET /api/v1/campaigns/{transaction_id}/status
```

### File Upload
```http
POST /api/v1/files/presigned-url
```

## Data Flow Patterns

### Asynchronous Processing
- File processing happens asynchronously via Step Functions
- Status updates provided through polling or webhooks
- Non-blocking user experience

### Event-Driven Architecture
- DynamoDB streams trigger downstream processing
- EventBridge handles scheduled delivery
- SNS notifications for SES events

### Microservices Integration
- Clear API boundaries between services
- Independent scaling and deployment
- Fault isolation and resilience

## Error Handling

### File Processing Errors
- Invalid CSV format validation
- Duplicate email detection
- Template validation failures

### Delivery Errors
- SES sending failures
- Bounce and complaint handling
- Retry mechanisms with exponential backoff

### Integration Errors
- API timeout handling
- Circuit breaker patterns
- Graceful degradation

## Security Considerations

### Authentication
- API key validation for all requests
- Optional OAuth 2.0 for enhanced security
- Service-to-service authentication via IAM roles

### Data Protection
- Presigned URLs for secure file uploads
- Encryption in transit and at rest
- Access logging and audit trails

### Rate Limiting
- API Gateway throttling
- SES sending rate management
- DynamoDB capacity protection

## Performance Optimization

### Batch Processing
- Efficient CSV file splitting
- Parallel message processing
- Optimized DynamoDB batch operations

### Caching
- Template caching for repeated use
- Configuration caching
- Connection pooling

### Monitoring
- Real-time performance metrics
- Latency tracking
- Error rate monitoring
