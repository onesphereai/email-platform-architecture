# Transaction Status Flow Description

## Overview
This diagram illustrates the high-level status transitions for email campaign transactions, showing how campaigns progress from initial acceptance through completion.

## Transaction Status States

### 1. ACCEPT - Transaction Created
- **Trigger**: Email campaign submitted to Email Platform API
- **Description**: Transaction record created with initial metadata
- **Data Stored**: Transaction ID, template ID, callback URL, total message count
- **Next State**: PROCESSING

### 2. PROCESSING - Loading to DynamoDB
- **Trigger**: File processing Step Functions initiated
- **Description**: CSV file being split and individual messages created
- **Activities**: 
  - CSV file validation and parsing
  - Message record creation in DynamoDB
  - Batch creation for parallel processing
  - Placeholder data validation
- **Next State**: SCHEDULED or READY_TO_SEND

### 3. SCHEDULED - All Messages Scheduled (Conditional)
- **Trigger**: Scheduling enabled and all messages have scheduled times
- **Description**: All messages scheduled for future delivery via EventBridge
- **Activities**:
  - EventBridge scheduler events created
  - Message status set to SCHEDULED
  - Transaction marked as SCHEDULED
- **Next State**: READY_TO_SEND (when schedule triggers)

### 4. READY_TO_SEND - Ready for Delivery
- **Trigger**: Either direct from PROCESSING (no scheduling) or from SCHEDULED (when time arrives)
- **Description**: All messages ready for immediate delivery processing
- **Activities**:
  - Messages marked as READY_TO_SEND
  - DynamoDB stream triggers activated
  - Send pipeline Step Functions initiated
- **Next State**: SENT

### 5. SENT - All Messages Sent
- **Trigger**: All messages successfully submitted to Amazon SES
- **Description**: Email delivery initiated for all messages in transaction
- **Activities**:
  - All messages sent to SES
  - SES message IDs recorded
  - Delivery tracking initiated
  - Initial callback notifications sent
- **Next State**: COMPLETED

### 6. COMPLETED - All Messages Delivered
- **Trigger**: All messages have final delivery status (delivered, bounced, or complained)
- **Description**: Transaction fully processed with final outcomes
- **Activities**:
  - Final delivery statistics calculated
  - Analytics data aggregated
  - Final callback notifications sent
  - Transaction marked as complete

## Status Transition Triggers

### File Processing Triggers
```javascript
// Transaction status update during processing
const updateTransactionStatus = async (transactionId, status, metadata) => {
  await dynamodb.updateItem({
    TableName: 'Transactions',
    Key: { PK: `TRANSACTION#${transactionId}`, SK: 'METADATA' },
    UpdateExpression: 'SET #status = :status, updated_at = :timestamp',
    ExpressionAttributeNames: { '#status': 'status' },
    ExpressionAttributeValues: {
      ':status': status,
      ':timestamp': new Date().toISOString()
    }
  }).promise();
};
```

### Scheduling Logic
```javascript
// Conditional scheduling based on campaign configuration
const processScheduling = async (transaction) => {
  if (transaction.schedule && transaction.schedule.send_at) {
    // Create EventBridge scheduled events
    await createScheduledEvents(transaction);
    await updateTransactionStatus(transaction.id, 'SCHEDULED');
  } else {
    // Direct to ready state
    await updateTransactionStatus(transaction.id, 'READY_TO_SEND');
  }
};
```

### Completion Detection
```javascript
// Monitor message completion to update transaction status
const checkTransactionCompletion = async (transactionId) => {
  const stats = await getMessageStatistics(transactionId);
  
  if (stats.total === stats.completed) {
    await updateTransactionStatus(transactionId, 'COMPLETED', {
      final_stats: stats,
      completed_at: new Date().toISOString()
    });
    
    // Trigger final callback
    await triggerCallback(transactionId, 'COMPLETED', stats);
  }
};
```

## Data Model Integration

### Transaction Record Structure
```json
{
  "PK": "TRANSACTION#uuid",
  "SK": "METADATA",
  "transaction_id": "uuid",
  "status": "PROCESSING",
  "template_id": "uuid",
  "callback_url": "https://...",
  "total_messages": 1000,
  "processed_messages": 250,
  "schedule": {
    "send_at": "2024-01-01T10:00:00Z"
  },
  "created_at": "2024-01-01T09:00:00Z",
  "updated_at": "2024-01-01T09:15:00Z"
}
```

### Status Tracking Metadata
```json
{
  "status_history": [
    {
      "status": "ACCEPT",
      "timestamp": "2024-01-01T09:00:00Z",
      "metadata": { "source": "api_request" }
    },
    {
      "status": "PROCESSING",
      "timestamp": "2024-01-01T09:01:00Z",
      "metadata": { "batch_count": 10 }
    }
  ],
  "current_status": "PROCESSING",
  "progress": {
    "total_messages": 1000,
    "processed_messages": 250,
    "percentage": 25
  }
}
```

## Monitoring & Analytics

### Status Transition Metrics
- **Processing Time**: Time spent in each status
- **Success Rate**: Percentage of transactions reaching COMPLETED
- **Failure Points**: Common failure states and reasons
- **Throughput**: Transactions processed per hour

### Real-time Dashboards
```javascript
// CloudWatch metrics for status transitions
const publishStatusMetric = async (status, transactionId) => {
  await cloudwatch.putMetricData({
    Namespace: 'EmailPlatform/Transactions',
    MetricData: [{
      MetricName: 'StatusTransition',
      Dimensions: [
        { Name: 'Status', Value: status },
        { Name: 'TransactionId', Value: transactionId }
      ],
      Value: 1,
      Unit: 'Count',
      Timestamp: new Date()
    }]
  }).promise();
};
```

### Alerting Rules
- **Stuck Transactions**: Transactions in PROCESSING > 30 minutes
- **High Failure Rate**: >5% transactions failing to reach COMPLETED
- **Slow Processing**: Average processing time > SLA thresholds
- **Scheduling Delays**: Scheduled messages not triggering on time

## Error Handling

### Processing Failures
```json
{
  "error": {
    "code": "CSV_PARSING_ERROR",
    "message": "Invalid email format in row 150",
    "details": {
      "row": 150,
      "email": "invalid-email",
      "expected_format": "user@domain.com"
    },
    "recovery_action": "MANUAL_REVIEW"
  }
}
```

### Retry Mechanisms
- **Transient Failures**: Automatic retry with exponential backoff
- **Permanent Failures**: Manual intervention required
- **Partial Failures**: Continue processing valid messages
- **Rollback Procedures**: Revert to previous stable state

### Dead Letter Queues
- **Failed Transactions**: Transactions that cannot be processed
- **Manual Review**: Administrative interface for failed transactions
- **Recovery Procedures**: Steps to recover failed transactions
- **Audit Trail**: Complete history of failure and recovery attempts

## Performance Optimization

### Parallel Processing
- **Batch Processing**: Split large files into manageable batches
- **Concurrent Execution**: Process multiple batches simultaneously
- **Resource Scaling**: Auto-scale based on processing load
- **Queue Management**: Optimize message queue throughput

### Status Update Efficiency
- **Batch Updates**: Group status updates for efficiency
- **Conditional Updates**: Only update when status actually changes
- **Caching**: Cache frequently accessed status information
- **Indexing**: Optimize database queries for status lookups

## Integration Patterns

### Callback Notifications
```javascript
// Status change callback
const notifyStatusChange = async (transactionId, oldStatus, newStatus) => {
  const callback = {
    transaction_id: transactionId,
    event_type: 'status_change',
    old_status: oldStatus,
    new_status: newStatus,
    timestamp: new Date().toISOString()
  };
  
  await callbackService.notify(callback);
};
```

### Event-Driven Updates
- **DynamoDB Streams**: Trigger downstream processing on status changes
- **EventBridge**: Publish status change events for external systems
- **SNS Notifications**: Fan-out status updates to multiple subscribers
- **SQS Processing**: Queue status-dependent operations

### API Integration
```http
GET /api/v1/transactions/{transaction_id}/status
Response:
{
  "transaction_id": "uuid",
  "status": "PROCESSING",
  "progress": {
    "total_messages": 1000,
    "processed_messages": 250,
    "percentage": 25
  },
  "estimated_completion": "2024-01-01T09:30:00Z"
}
```
