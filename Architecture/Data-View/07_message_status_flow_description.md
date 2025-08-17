# Message Status Flow Description

## Overview
This diagram illustrates the detailed status transitions for individual email messages within the Email Platform, showing the complete lifecycle from creation through final engagement tracking.

## Message Status Categories

### Creation States
Messages begin their lifecycle when created from CSV processing.

### Scheduling States
Messages can be scheduled for future delivery or marked for immediate processing.

### Delivery States
Messages progress through various delivery states as they are processed by Amazon SES.

### Final States
Messages reach terminal states based on delivery outcomes.

### Engagement States
Successfully delivered messages can generate engagement events.

## Detailed Status Transitions

### 1. CREATED - Message Record Created
- **Trigger**: CSV file processing creates individual message records
- **Description**: Message record stored in DynamoDB with recipient data
- **Data Stored**:
  - Message ID, Batch ID, Transaction ID
  - Recipient email address
  - Placeholder data for template substitution
  - Initial timestamp
- **Next States**: SCHEDULED or READY_TO_SEND

### 2. SCHEDULED - Message Scheduled (Conditional Path)
- **Trigger**: Campaign has scheduling configuration
- **Description**: Message scheduled for future delivery via EventBridge
- **Activities**:
  - EventBridge scheduled event created
  - Scheduled time stored with message
  - Message marked as SCHEDULED
- **Next State**: READY_TO_SEND (when schedule triggers)

### 3. READY_TO_SEND - Ready for Processing (Direct or Scheduled Path)
- **Trigger**: Either immediate processing or scheduled time arrival
- **Description**: Message ready for email delivery processing
- **Activities**:
  - Message queued for sending
  - Template and placeholder data prepared
  - SES sending parameters configured
- **Next State**: SENDING

### 4. SENDING - Being Processed by SES
- **Trigger**: Send pipeline Step Functions processing message
- **Description**: Message actively being processed by Amazon SES
- **Activities**:
  - Template rendering with placeholder data
  - Email composition and validation
  - SES API call initiated
- **Next State**: SENT

### 5. SENT - Sent to SES
- **Trigger**: SES accepts message for delivery
- **Description**: Message successfully submitted to SES for delivery
- **Data Stored**:
  - SES Message ID
  - Sent timestamp
  - SES response metadata
- **Next States**: DELIVERED, BOUNCED, or COMPLAINED

### 6. DELIVERED - Successfully Delivered
- **Trigger**: SES delivery notification received
- **Description**: Message successfully delivered to recipient's mailbox
- **Activities**:
  - Delivery timestamp recorded
  - Success metrics updated
  - Analytics data updated
- **Next States**: OPENED (optional)

### 7. BOUNCED - Delivery Failed
- **Trigger**: SES bounce notification received
- **Description**: Message delivery failed (hard or soft bounce)
- **Data Stored**:
  - Bounce type (hard/soft)
  - Bounce reason
  - Bounce timestamp
  - Diagnostic information
- **Terminal State**: No further transitions

### 8. COMPLAINED - Spam Complaint
- **Trigger**: SES complaint notification received
- **Description**: Recipient marked message as spam
- **Activities**:
  - Complaint timestamp recorded
  - Recipient suppression list updated
  - Compliance metrics updated
- **Terminal State**: No further transitions

### 9. OPENED - Email Opened
- **Trigger**: SES open tracking notification
- **Description**: Recipient opened the email
- **Data Stored**:
  - Open timestamp
  - User agent information
  - IP address (if available)
- **Next State**: CLICKED (optional)

### 10. CLICKED - Link Clicked
- **Trigger**: SES click tracking notification
- **Description**: Recipient clicked a link in the email
- **Data Stored**:
  - Click timestamp
  - Clicked URL
  - User agent information
  - IP address (if available)
- **Terminal State**: Final engagement event

## Data Model Structure

### Message Record Schema
```json
{
  "PK": "BATCH#batch_id",
  "SK": "MESSAGE#message_id",
  "message_id": "uuid",
  "batch_id": "uuid",
  "transaction_id": "uuid",
  "recipient_email": "user@example.com",
  "placeholder_data": {
    "first_name": "John",
    "last_name": "Doe",
    "company": "ACME Corp"
  },
  "status": "DELIVERED",
  "ses_message_id": "ses-uuid",
  "scheduled_time": "2024-01-01T10:00:00Z",
  "sent_time": "2024-01-01T10:05:00Z",
  "delivered_time": "2024-01-01T10:06:00Z",
  "created_at": "2024-01-01T09:00:00Z",
  "updated_at": "2024-01-01T10:06:00Z"
}
```

### Status History Tracking
```json
{
  "status_history": [
    {
      "status": "CREATED",
      "timestamp": "2024-01-01T09:00:00Z",
      "metadata": { "source": "csv_processing" }
    },
    {
      "status": "READY_TO_SEND",
      "timestamp": "2024-01-01T10:00:00Z",
      "metadata": { "trigger": "immediate" }
    },
    {
      "status": "SENT",
      "timestamp": "2024-01-01T10:05:00Z",
      "metadata": { "ses_message_id": "ses-uuid" }
    },
    {
      "status": "DELIVERED",
      "timestamp": "2024-01-01T10:06:00Z",
      "metadata": { "delivery_delay_ms": 60000 }
    }
  ]
}
```

## SES Event Integration

### Event Processing Pipeline
```javascript
// SES event handler for status updates
const handleSESEvent = async (event) => {
  const { eventType, mail, delivery, bounce, complaint } = event;
  const messageId = mail.commonHeaders.messageId;
  
  switch (eventType) {
    case 'delivery':
      await updateMessageStatus(messageId, 'DELIVERED', {
        delivered_time: delivery.timestamp,
        processing_time_ms: delivery.processingTimeMillis
      });
      break;
      
    case 'bounce':
      await updateMessageStatus(messageId, 'BOUNCED', {
        bounce_type: bounce.bounceType,
        bounce_subtype: bounce.bounceSubType,
        bounce_reason: bounce.bouncedRecipients[0].diagnosticCode
      });
      break;
      
    case 'complaint':
      await updateMessageStatus(messageId, 'COMPLAINED', {
        complaint_type: complaint.complaintFeedbackType,
        complaint_time: complaint.timestamp
      });
      break;
  }
};
```

### Engagement Tracking
```javascript
// Open and click tracking
const handleEngagementEvent = async (event) => {
  const { eventType, messageId, timestamp, metadata } = event;
  
  if (eventType === 'open') {
    await updateMessageStatus(messageId, 'OPENED', {
      opened_time: timestamp,
      user_agent: metadata.userAgent,
      ip_address: metadata.ipAddress
    });
  } else if (eventType === 'click') {
    await updateMessageStatus(messageId, 'CLICKED', {
      clicked_time: timestamp,
      clicked_url: metadata.url,
      user_agent: metadata.userAgent,
      ip_address: metadata.ipAddress
    });
  }
};
```

## Analytics Integration

### OpenSearch Data Structure
```json
{
  "message_id": "uuid",
  "transaction_id": "uuid",
  "batch_id": "uuid",
  "recipient_email": "user@example.com",
  "status": "DELIVERED",
  "event_type": "delivery",
  "timestamp": "2024-01-01T10:06:00Z",
  "metadata": {
    "processing_time_ms": 60000,
    "delivery_delay_ms": 1000,
    "ses_message_id": "ses-uuid"
  },
  "engagement": {
    "opened": true,
    "opened_time": "2024-01-01T11:00:00Z",
    "clicked": false
  }
}
```

### Real-time Analytics Queries
```javascript
// Message status aggregation
const getMessageStatistics = async (transactionId) => {
  const query = {
    query: {
      term: { transaction_id: transactionId }
    },
    aggs: {
      status_breakdown: {
        terms: { field: 'status' }
      },
      engagement_stats: {
        filters: {
          filters: {
            opened: { term: { 'engagement.opened': true } },
            clicked: { term: { 'engagement.clicked': true } }
          }
        }
      }
    }
  };
  
  return await opensearch.search({ index: 'email-events', body: query });
};
```

## Performance Monitoring

### Status Transition Metrics
```javascript
// CloudWatch metrics for message processing
const publishMessageMetrics = async (status, processingTime) => {
  await cloudwatch.putMetricData({
    Namespace: 'EmailPlatform/Messages',
    MetricData: [
      {
        MetricName: 'MessageStatusTransition',
        Dimensions: [{ Name: 'Status', Value: status }],
        Value: 1,
        Unit: 'Count'
      },
      {
        MetricName: 'ProcessingTime',
        Dimensions: [{ Name: 'Status', Value: status }],
        Value: processingTime,
        Unit: 'Milliseconds'
      }
    ]
  }).promise();
};
```

### Performance Benchmarks
- **Processing Speed**: Messages processed per second
- **Delivery Rate**: Percentage of messages reaching DELIVERED status
- **Engagement Rate**: Percentage of delivered messages opened/clicked
- **Error Rate**: Percentage of messages reaching BOUNCED/COMPLAINED status

## Error Handling & Recovery

### Bounce Handling
```javascript
// Bounce classification and handling
const handleBounce = async (messageId, bounceData) => {
  const { bounceType, bounceSubType } = bounceData;
  
  if (bounceType === 'Permanent') {
    // Add to suppression list
    await addToSuppressionList(bounceData.recipient);
    await updateMessageStatus(messageId, 'BOUNCED', {
      bounce_type: 'hard',
      suppressed: true
    });
  } else {
    // Soft bounce - potential retry
    await updateMessageStatus(messageId, 'BOUNCED', {
      bounce_type: 'soft',
      retry_eligible: true
    });
  }
};
```

### Retry Logic
- **Soft Bounces**: Automatic retry after delay
- **Transient Failures**: Exponential backoff retry
- **Rate Limiting**: Respect SES sending limits
- **Dead Letter Queue**: Failed messages for manual review

## Compliance & Reporting

### Suppression List Management
```javascript
// Automatic suppression list updates
const updateSuppressionList = async (email, reason) => {
  await dynamodb.putItem({
    TableName: 'SuppressionList',
    Item: {
      email: { S: email },
      reason: { S: reason },
      added_date: { S: new Date().toISOString() },
      status: { S: 'active' }
    }
  }).promise();
};
```

### Compliance Reporting
- **Bounce Rate Monitoring**: Track bounce rates by domain
- **Complaint Rate Tracking**: Monitor spam complaint rates
- **Suppression List Maintenance**: Automatic list updates
- **Delivery Quality Metrics**: SES reputation monitoring

## Integration Patterns

### Real-time Status Updates
```javascript
// WebSocket notifications for real-time updates
const notifyStatusChange = async (messageId, status) => {
  const notification = {
    message_id: messageId,
    status: status,
    timestamp: new Date().toISOString()
  };
  
  await websocket.broadcast('message-status-update', notification);
};
```

### Batch Status Processing
- **Bulk Updates**: Efficient batch status updates
- **Stream Processing**: Real-time event stream processing
- **Aggregation**: Roll-up statistics for transaction-level reporting
- **Caching**: Cache frequently accessed status information
