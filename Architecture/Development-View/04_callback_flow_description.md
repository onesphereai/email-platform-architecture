# Callback Flow Description

## Overview
This diagram illustrates the callback mechanism that enables the Email Platform to notify external systems (like Message Centre) about email campaign status changes and delivery events.

## Callback Flow Components

### Message Centre Integration
- **Message Centre API**: Initiates email campaigns with callback URLs
- **Customer Webhook**: Receives status updates and delivery notifications

### Email Platform Services
- **Email API**: Accepts campaign requests with callback configuration
- **Callback Service**: Manages webhook notifications and retry logic
- **Message Status Storage**: DynamoDB stores callback URLs and delivery status

### Processing Pipeline
- **Email Sender Step Functions**: Orchestrates email delivery and status updates
- **Amazon SES**: Handles email delivery and generates delivery events

## Detailed Flow Steps

### 1. Campaign Submission with Callback
```http
POST /api/v1/campaigns
{
  "template_id": "uuid",
  "csv_file_url": "s3://bucket/recipients.csv",
  "callback_url": "https://messagecentre.com/webhooks/email-status",
  "callback_events": ["status_change", "delivery_events"]
}
```

### 2. Callback URL Storage
- Email API stores callback URL with transaction metadata
- Callback configuration includes event types and authentication details
- Validation ensures callback URL is accessible and secure

### 3. Email Processing & Status Updates
- Step Functions process email campaign
- Each status change triggers callback service
- Status transitions: ACCEPT → PROCESSING → SENT → COMPLETED

### 4. Callback Execution
```http
POST https://messagecentre.com/webhooks/email-status
Content-Type: application/json
X-Signature: HMAC-SHA256-signature
X-Event-Type: status_change

{
  "transaction_id": "uuid",
  "event_type": "status_change",
  "status": "PROCESSING",
  "timestamp": "2024-01-01T10:00:00Z",
  "message_count": 1000,
  "processed_count": 250
}
```

### 5. SES Delivery Events
- Amazon SES generates delivery, bounce, complaint, open, and click events
- Events flow directly to Callback Service via SNS
- Individual message events trigger specific callbacks

### 6. Event-Specific Callbacks
```http
POST https://messagecentre.com/webhooks/email-status
Content-Type: application/json
X-Signature: HMAC-SHA256-signature
X-Event-Type: delivery_event

{
  "transaction_id": "uuid",
  "message_id": "uuid",
  "event_type": "delivered",
  "recipient": "user@example.com",
  "timestamp": "2024-01-01T10:05:00Z",
  "ses_message_id": "ses-uuid"
}
```

### 7. Final Status Update
- When all messages are processed, final callback sent
- Includes comprehensive campaign summary
- Updates transaction status to COMPLETED

## Callback Event Types

### Status Change Events
- **ACCEPT**: Campaign accepted for processing
- **PROCESSING**: Messages being loaded into system
- **SCHEDULED**: All messages scheduled (if applicable)
- **SENT**: All messages sent to SES
- **COMPLETED**: All messages processed (delivered/bounced)

### Delivery Events
- **SENT**: Message sent to SES
- **DELIVERED**: Message successfully delivered
- **BOUNCED**: Message bounced (hard/soft bounce)
- **COMPLAINED**: Spam complaint received
- **OPENED**: Email opened by recipient
- **CLICKED**: Link clicked in email

## Callback Security

### Authentication
- **HMAC Signatures**: Verify callback authenticity
- **API Keys**: Optional additional authentication
- **IP Whitelisting**: Restrict callback sources

### Payload Security
```javascript
// Signature verification
const signature = crypto
  .createHmac('sha256', secret)
  .update(JSON.stringify(payload))
  .digest('hex');

const expectedSignature = `sha256=${signature}`;
const receivedSignature = request.headers['x-signature'];

if (expectedSignature !== receivedSignature) {
  throw new Error('Invalid signature');
}
```

### Retry Logic
- **Exponential Backoff**: 1s, 2s, 4s, 8s, 16s intervals
- **Maximum Retries**: 5 attempts per callback
- **Dead Letter Queue**: Failed callbacks for manual review
- **Timeout Handling**: 30-second timeout per attempt

## Error Handling

### Callback Failures
```json
{
  "error": {
    "code": "CALLBACK_FAILED",
    "message": "Webhook endpoint returned 500",
    "retry_count": 3,
    "next_retry": "2024-01-01T10:05:00Z",
    "max_retries": 5
  }
}
```

### Endpoint Validation
- **URL Validation**: Ensure HTTPS endpoints
- **Response Validation**: Expect 2xx status codes
- **Timeout Handling**: 30-second maximum response time
- **Rate Limiting**: Respect endpoint rate limits

### Fallback Mechanisms
- **Email Notifications**: Alert on callback failures
- **Dashboard Alerts**: Real-time failure monitoring
- **Manual Retry**: Administrative retry capabilities
- **Alternative Endpoints**: Backup callback URLs

## Monitoring & Analytics

### Callback Metrics
- **Success Rate**: Percentage of successful callbacks
- **Response Time**: Average callback response latency
- **Retry Rate**: Frequency of callback retries
- **Failure Rate**: Percentage of failed callbacks

### Dashboard Views
- Real-time callback status
- Historical callback performance
- Endpoint health monitoring
- Error pattern analysis

### Alerting
- **High Failure Rate**: Alert when >5% callbacks fail
- **Slow Response**: Alert when response time >10s
- **Endpoint Down**: Alert when endpoint unreachable
- **Retry Exhaustion**: Alert when max retries reached

## Integration Patterns

### Webhook Standards
- **RESTful Design**: Standard HTTP methods and status codes
- **JSON Payloads**: Structured, consistent data format
- **Idempotency**: Safe to retry identical requests
- **Versioning**: API version headers for compatibility

### Event Ordering
- **Sequence Numbers**: Ensure event ordering
- **Timestamps**: UTC timestamps for all events
- **Deduplication**: Prevent duplicate event processing
- **State Reconciliation**: Handle out-of-order events

### Scalability Considerations
- **Async Processing**: Non-blocking callback execution
- **Batch Callbacks**: Group related events when possible
- **Rate Limiting**: Respect downstream system limits
- **Circuit Breaker**: Prevent cascade failures

## Best Practices

### Callback URL Design
```
https://api.customer.com/webhooks/email-platform
├── /status-changes    # Campaign status updates
├── /delivery-events   # Individual message events
└── /health           # Health check endpoint
```

### Payload Design
- **Consistent Schema**: Standardized event structure
- **Minimal Data**: Include only necessary information
- **Reference IDs**: Use UUIDs for correlation
- **Metadata**: Include context for debugging

### Error Recovery
- **Graceful Degradation**: Continue processing on callback failures
- **Manual Intervention**: Admin tools for failed callbacks
- **Data Consistency**: Ensure system state remains consistent
- **Audit Logging**: Comprehensive callback attempt logging
