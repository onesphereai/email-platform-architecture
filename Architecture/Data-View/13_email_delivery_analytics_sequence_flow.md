# Email Delivery & Analytics - Flow Description

**Diagram**: `13_email_delivery_analytics_sequence.png`

## Overview
This sequence diagram shows the complete email delivery lifecycle, from initial delivery through recipient engagement tracking, bounce handling, and real-time analytics processing.

## Sequence Flow

| Step | Source | Target | Method/Action | Description | Response/Result |
|------|--------|--------|---------------|-------------|-----------------|
| 1 | Amazon SES | Email Recipient | deliverEmail() | SES delivers email to recipient's inbox | Email delivered |
| 2 | Amazon SES | SNS Events | publishEvent(delivered) | SES publishes delivery event to SNS | Event published |
| 3 | SNS Events | Analytics Service | processDeliveryEvent() | SNS triggers analytics processing | Event processing started |
| 4 | Analytics Service | DynamoDB | updateDeliveryStats() | Service updates delivery statistics | Stats updated |
| 5 | Analytics Service | OpenSearch | indexMetrics() | Service indexes delivery metrics | Metrics indexed |
| 6 | Email Recipient | Amazon SES | openEmail() | Recipient opens email (tracking pixel) | Open event triggered |
| 7 | Amazon SES | SNS Events | publishEvent(opened) | SES publishes open event to SNS | Event published |
| 8 | SNS Events | Analytics Service | processOpenEvent() | SNS triggers open event processing | Processing started |
| 9 | Analytics Service | DynamoDB | updateOpenStats() | Service updates open statistics | Stats updated |
| 10 | Analytics Service | OpenSearch | indexOpenData() | Service indexes open event data | Data indexed |
| 11 | Email Recipient | Amazon SES | clickLink() | Recipient clicks link in email | Click event triggered |
| 12 | Amazon SES | SNS Events | publishEvent(clicked) | SES publishes click event to SNS | Event published |
| 13 | SNS Events | Analytics Service | processClickEvent() | SNS triggers click event processing | Processing started |
| 14 | Analytics Service | DynamoDB | updateClickStats() | Service updates click statistics | Stats updated |
| 15 | Analytics Service | OpenSearch | indexClickData() | Service indexes click event data | Data indexed |
| 16 | Amazon SES | SNS Events | publishEvent(bounced) | SES publishes bounce event to SNS | Event published |
| 17 | SNS Events | Analytics Service | processBounceEvent() | SNS triggers bounce event processing | Processing started |
| 18 | Analytics Service | DynamoDB | updateBounceStats() | Service updates bounce statistics | Stats updated |
| 19 | Analytics Service | DynamoDB | addToSuppressionList() | Service adds bounced email to suppression list | Email suppressed |
| 20 | Analytics Service | Webhook Service | triggerWebhook() | Service triggers webhook notification | Webhook triggered |
| 21 | Webhook Service | Client Webhook | POST /webhook {event: opened} | Service sends event notification | Webhook delivered |
| 22 | Client Webhook | Webhook Service | return 200 OK | Client confirms webhook receipt | Confirmation received |
| 23 | Analytics Service | SNS Events | publishUpdate() | Service publishes real-time update | Update published |
| 24 | SNS Events | Angular UI | notifyUI() | SNS notifies UI of metric updates | UI notification sent |
| 25 | Angular UI | Marketing User | updateDashboard() | UI updates dashboard with new metrics | Dashboard refreshed |
| 26 | Marketing User | Angular UI | viewAnalytics() | User requests detailed analytics | Analytics request sent |
| 27 | Angular UI | Analytics Service | GET /analytics | UI requests analytics data | Request sent |
| 28 | Analytics Service | OpenSearch | queryMetrics() | Service queries aggregated metrics | Query executed |
| 29 | OpenSearch | Analytics Service | return aggregatedData | Search returns aggregated analytics | Data returned |
| 30 | Analytics Service | Angular UI | return analytics | Service returns analytics data | Analytics delivered |
| 31 | Angular UI | Marketing User | displayCharts() | UI displays analytics charts and metrics | Charts displayed |

## Event Processing Phases

### Phase 1: Email Delivery (Steps 1-5)
- **Purpose**: Track successful email delivery
- **Trigger**: SES delivery confirmation
- **Data Captured**: Delivery timestamp, recipient, message ID
- **Processing**: Update delivery counters, calculate delivery rate
- **Storage**: DynamoDB for stats, OpenSearch for analytics

### Phase 2: Engagement Tracking (Steps 6-15)
- **Purpose**: Track recipient engagement (opens, clicks)
- **Mechanisms**: 
  - **Opens**: 1x1 pixel tracking image
  - **Clicks**: Link redirection through tracking service
- **Data Captured**: Timestamp, recipient, user agent, IP address, location
- **Processing**: Update engagement metrics, calculate rates
- **Storage**: Real-time indexing in OpenSearch

### Phase 3: Bounce Handling (Steps 16-19)
- **Purpose**: Handle delivery failures and maintain list hygiene
- **Bounce Types**:
  - **Hard Bounce**: Permanent failure (invalid email)
  - **Soft Bounce**: Temporary failure (mailbox full)
- **Processing**: Update bounce statistics, manage suppression list
- **Actions**: Automatic suppression for hard bounces

### Phase 4: Real-time Notifications (Steps 20-25)
- **Purpose**: Provide real-time updates to clients and users
- **Channels**: Webhooks for API clients, UI updates for dashboard users
- **Events**: All delivery and engagement events
- **Processing**: Event formatting, delivery confirmation

### Phase 5: Analytics Queries (Steps 26-31)
- **Purpose**: Provide detailed analytics and reporting
- **Data Sources**: OpenSearch aggregated data
- **Metrics**: Delivery rates, engagement rates, performance trends
- **Visualization**: Charts, graphs, tabular data

## Event Data Structures

### Delivery Event
```json
{
  "eventType": "email.delivered",
  "timestamp": "2024-01-15T10:30:00Z",
  "campaignId": "camp_123456789",
  "messageId": "msg_123456789",
  "recipient": "customer@example.com",
  "deliveryTimestamp": "2024-01-15T10:30:00Z",
  "smtpResponse": "250 2.0.0 OK"
}
```

### Open Event
```json
{
  "eventType": "email.opened",
  "timestamp": "2024-01-15T11:15:00Z",
  "campaignId": "camp_123456789",
  "messageId": "msg_123456789",
  "recipient": "customer@example.com",
  "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
  "ipAddress": "192.168.1.100",
  "location": {
    "country": "Australia",
    "region": "NSW",
    "city": "Sydney"
  }
}
```

### Click Event
```json
{
  "eventType": "email.clicked",
  "timestamp": "2024-01-15T11:20:00Z",
  "campaignId": "camp_123456789",
  "messageId": "msg_123456789",
  "recipient": "customer@example.com",
  "url": "https://example.com/product",
  "linkId": "link_001",
  "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
  "ipAddress": "192.168.1.100"
}
```

### Bounce Event
```json
{
  "eventType": "email.bounced",
  "timestamp": "2024-01-15T10:31:00Z",
  "campaignId": "camp_123456789",
  "messageId": "msg_123456789",
  "recipient": "invalid@example.com",
  "bounceType": "Permanent",
  "bounceSubType": "General",
  "diagnosticCode": "smtp; 550 5.1.1 User unknown",
  "action": "failed"
}
```

## Analytics Metrics

### Delivery Metrics
- **Sent**: Total emails sent
- **Delivered**: Successfully delivered emails
- **Bounced**: Failed delivery emails
- **Delivery Rate**: (Delivered / Sent) × 100

### Engagement Metrics
- **Opens**: Unique email opens
- **Clicks**: Unique link clicks
- **Open Rate**: (Opens / Delivered) × 100
- **Click Rate**: (Clicks / Delivered) × 100
- **Click-to-Open Rate**: (Clicks / Opens) × 100

### Quality Metrics
- **Bounce Rate**: (Bounced / Sent) × 100
- **Complaint Rate**: (Complaints / Delivered) × 100
- **Unsubscribe Rate**: (Unsubscribes / Delivered) × 100

### Performance Metrics
- **Time to Delivery**: Average delivery time
- **Time to Open**: Average time from delivery to open
- **Time to Click**: Average time from delivery to click

## Real-time Dashboard Updates

### WebSocket Connection
```javascript
// Real-time dashboard updates
const ws = new WebSocket('wss://api.emailplatform.com/ws');

ws.onmessage = function(event) {
  const update = JSON.parse(event.data);
  if (update.type === 'campaign.metrics') {
    updateDashboardMetrics(update.data);
  }
};
```

### Update Message Format
```json
{
  "type": "campaign.metrics",
  "campaignId": "camp_123456789",
  "timestamp": "2024-01-15T11:20:00Z",
  "metrics": {
    "sent": 1000,
    "delivered": 980,
    "opened": 490,
    "clicked": 147,
    "bounced": 15,
    "deliveryRate": 98.0,
    "openRate": 50.0,
    "clickRate": 15.0
  }
}
```

## Bounce Management

### Hard Bounce Processing
1. **Immediate Suppression**: Add to suppression list
2. **List Cleanup**: Remove from active recipient lists
3. **Notification**: Alert sender about invalid addresses
4. **Reporting**: Include in bounce reports

### Soft Bounce Processing
1. **Retry Logic**: Attempt redelivery with delays
2. **Escalation**: Convert to hard bounce after multiple failures
3. **Monitoring**: Track soft bounce patterns
4. **Throttling**: Reduce sending rate to problematic domains

### Suppression List Management
```json
{
  "email": "bounced@example.com",
  "reason": "hard_bounce",
  "timestamp": "2024-01-15T10:31:00Z",
  "campaignId": "camp_123456789",
  "diagnosticCode": "550 5.1.1 User unknown",
  "suppressionType": "automatic"
}
```

## Webhook Event Delivery

### Event Types Supported
- `email.delivered` - Successful delivery
- `email.bounced` - Delivery failure
- `email.complained` - Spam complaint
- `email.opened` - Email opened
- `email.clicked` - Link clicked
- `email.unsubscribed` - Recipient unsubscribed

### Delivery Guarantees
- **At-least-once delivery**: Events may be delivered multiple times
- **Retry logic**: Failed webhooks retried with exponential backoff
- **Timeout**: 30-second timeout for webhook responses
- **Dead letter queue**: Failed events stored for manual processing

### Security
- **HMAC Signature**: All webhooks signed with shared secret
- **IP Whitelisting**: Optional IP address restrictions
- **HTTPS Required**: All webhook URLs must use HTTPS
- **Verification**: Signature verification recommended

## Performance Considerations

### Event Processing
- **Batch Processing**: Events processed in batches for efficiency
- **Parallel Processing**: Multiple workers process events concurrently
- **Queue Management**: Separate queues for different event types
- **Backpressure**: Handle high-volume campaigns gracefully

### Analytics Storage
- **Hot Data**: Recent data in DynamoDB for fast access
- **Warm Data**: Aggregated data in OpenSearch for analytics
- **Cold Data**: Historical data archived to S3
- **Retention**: Configurable data retention policies

### Real-time Updates
- **Connection Management**: Efficient WebSocket connection handling
- **Update Batching**: Batch multiple updates to reduce noise
- **Rate Limiting**: Prevent overwhelming client applications
- **Fallback**: HTTP polling fallback for WebSocket failures

## Compliance and Privacy

### Data Protection
- **PII Handling**: Minimal PII storage, encryption at rest
- **Right to Deletion**: Support for GDPR deletion requests
- **Data Retention**: Automatic cleanup of old analytics data
- **Anonymization**: Option to anonymize analytics data

### Email Compliance
- **Unsubscribe Handling**: Automatic processing of unsubscribe requests
- **Suppression Lists**: Maintain global and campaign-specific suppression
- **Complaint Handling**: Process spam complaints automatically
- **Reputation Monitoring**: Track sender reputation metrics
