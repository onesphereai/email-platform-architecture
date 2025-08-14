# Email Sending Process - Flow Description

**Diagram**: `11_email_sending_sequence.png`

## Overview
This sequence diagram illustrates the complete email sending process, from user initiation through asynchronous processing, delivery, and real-time analytics updates.

## Sequence Flow

| Step | Source | Target | Method/Action | Description | Response/Result |
|------|--------|--------|---------------|-------------|-----------------|
| 1 | Marketing User | Angular UI | sendCampaign() | User triggers campaign sending | Send request initiated |
| 2 | Angular UI | API Gateway | POST /campaigns/{id}/send | UI sends campaign send request | Request forwarded |
| 3 | API Gateway | Campaign Service | triggerSend() | API Gateway routes send request | Send process triggered |
| 4 | Campaign Service | DynamoDB | updateStatus(sending) | Service updates campaign status | Status updated to "sending" |
| 5 | Campaign Service | Email Queue | queueEmailJobs() | Service queues email processing jobs | Jobs queued for processing |
| 6 | Campaign Service | API Gateway | return accepted | Service confirms send request accepted | Acceptance confirmed |
| 7 | API Gateway | Angular UI | return 202 Accepted | API returns accepted status | Async processing started |
| 8 | Angular UI | Marketing User | show sending status | UI displays sending status | User sees progress |
| 9 | Email Queue | Email Processor | processBatch() | Queue triggers batch processing | Batch processing started |
| 10 | Email Processor | DynamoDB | getCampaignData() | Processor retrieves campaign information | Campaign data retrieved |
| 11 | DynamoDB | Email Processor | return campaign | Database returns campaign details | Campaign data received |
| 12 | Email Processor | S3 Storage | getTemplate() | Processor retrieves email template | Template request sent |
| 13 | S3 Storage | Email Processor | return template | Storage returns template files | Template received |
| 14 | Email Processor | Template Service | renderTemplate() | Processor requests template rendering | Rendering initiated |
| 15 | Template Service | Email Processor | return rendered HTML | Service returns personalized HTML | Rendered content received |
| 16 | Email Processor | Amazon SES | sendEmailBatch() | Processor sends email batch to SES | Batch sent for delivery |
| 17 | Amazon SES | Email Processor | return messageIds | SES returns message identifiers | Message IDs received |
| 18 | Email Processor | DynamoDB | updateDeliveryStatus() | Processor updates delivery status | Status updated |
| 19 | Amazon SES | SNS Notifications | deliveryEvent() | SES publishes delivery events | Events published |
| 20 | SNS Notifications | Analytics Service | processEvent() | SNS triggers analytics processing | Event processing started |
| 21 | Analytics Service | DynamoDB | updateMetrics() | Service updates campaign metrics | Metrics updated |
| 22 | Analytics Service | SNS Notifications | publishUpdate() | Service publishes status update | Update published |
| 23 | SNS Notifications | Angular UI | notifyUI() | SNS notifies UI of status change | UI notification received |
| 24 | Angular UI | Marketing User | show delivery stats | UI displays updated delivery statistics | Real-time stats shown |

## Process Phases

### Phase 1: Send Initiation (Steps 1-8)
- **Purpose**: User initiates campaign sending and receives confirmation
- **Pattern**: Synchronous request with asynchronous processing
- **Components**: Angular UI, API Gateway, Campaign Service
- **Outcome**: Campaign status updated, jobs queued, user notified

### Phase 2: Asynchronous Processing (Steps 9-18)
- **Purpose**: Process queued email jobs and prepare for delivery
- **Pattern**: Queue-based batch processing
- **Components**: Email Queue, Email Processor, Template Service
- **Operations**: Data retrieval, template rendering, personalization
- **Outcome**: Emails ready for delivery with tracking

### Phase 3: Email Delivery (Steps 16-18)
- **Purpose**: Send emails through Amazon SES
- **Pattern**: Batch delivery with message tracking
- **Components**: Email Processor, Amazon SES
- **Features**: Throttling, retry logic, delivery confirmation
- **Outcome**: Emails sent with message IDs for tracking

### Phase 4: Event Processing (Steps 19-24)
- **Purpose**: Process delivery events and update analytics
- **Pattern**: Event-driven real-time updates
- **Components**: SNS, Analytics Service, Angular UI
- **Operations**: Metrics calculation, status updates, UI notifications
- **Outcome**: Real-time delivery statistics and user feedback

## Data Flow Details

### Campaign Send Request
```json
{
  "campaignId": "camp_123456789",
  "sendAt": "immediate",
  "throttle": {
    "emailsPerMinute": 100,
    "emailsPerHour": 1000
  }
}
```

### Email Queue Message
```json
{
  "campaignId": "camp_123456789",
  "batchId": "batch_001",
  "recipients": ["user1@example.com", "user2@example.com"],
  "templateId": "tmpl_123456789",
  "priority": "normal"
}
```

### SES Delivery Response
```json
{
  "messageIds": [
    "0000014a-f896-4c07-b8b0-f6b9dee6d13e-000000",
    "0000014a-f896-4c07-b8b0-f6b9dee6d13f-000000"
  ],
  "batchId": "batch_001"
}
```

### Analytics Event
```json
{
  "eventType": "email.sent",
  "campaignId": "camp_123456789",
  "messageId": "0000014a-f896-4c07-b8b0-f6b9dee6d13e-000000",
  "recipient": "user1@example.com",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Error Handling

### Send Request Errors
- **Campaign not found**: Return 404 Not Found
- **Campaign already sent**: Return 409 Conflict
- **Invalid status**: Return 400 Bad Request
- **Permission denied**: Return 403 Forbidden

### Processing Errors
- **Template not found**: Log error, skip batch
- **Recipient validation failure**: Filter invalid emails
- **SES quota exceeded**: Implement backoff and retry
- **Database connection failure**: Retry with exponential backoff

### Delivery Errors
- **Hard bounces**: Add to suppression list
- **Soft bounces**: Retry with delay
- **Rate limiting**: Implement throttling
- **Service unavailable**: Queue for retry

## Performance Optimizations

### Batch Processing
- **Batch Size**: Configurable batch sizes (default: 50 emails)
- **Parallel Processing**: Multiple concurrent batches
- **Memory Management**: Efficient memory usage for large campaigns

### Template Rendering
- **Caching**: Cache rendered templates for similar recipients
- **Optimization**: Minimize template complexity
- **Compression**: Compress large templates

### Database Operations
- **Connection Pooling**: Reuse database connections
- **Batch Updates**: Update multiple records in single operation
- **Indexing**: Optimize queries with proper indexes

### SES Integration
- **Connection Reuse**: Maintain persistent connections
- **Retry Logic**: Exponential backoff for failures
- **Rate Limiting**: Respect SES sending limits

## Monitoring and Observability

### Metrics Tracked
- **Processing Rate**: Emails processed per minute
- **Delivery Rate**: Successful deliveries percentage
- **Error Rate**: Failed processing percentage
- **Queue Depth**: Number of pending jobs

### Logging
- **Campaign Events**: Send initiation, completion, errors
- **Processing Events**: Batch processing, template rendering
- **Delivery Events**: SES responses, delivery confirmations
- **Error Events**: All error conditions with context

### Alerts
- **High Error Rate**: Alert when error rate exceeds threshold
- **Queue Backup**: Alert when queue depth is high
- **SES Quota**: Alert when approaching sending limits
- **Processing Delays**: Alert when processing is slow

## Security Considerations

### Data Protection
- **Encryption**: All data encrypted in transit and at rest
- **Access Control**: Tenant isolation enforced
- **Audit Logging**: All operations logged for compliance

### Email Security
- **Authentication**: SPF, DKIM, DMARC validation
- **Reputation**: Monitor sender reputation
- **Suppression**: Automatic suppression list management

### API Security
- **Authentication**: JWT token validation
- **Authorization**: Role-based access control
- **Rate Limiting**: Prevent abuse and overuse
