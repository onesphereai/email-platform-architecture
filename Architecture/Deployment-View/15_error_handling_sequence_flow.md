# Error Handling & Recovery - Flow Description

**Diagram**: `15_error_handling_sequence.png`

## Overview
This sequence diagram demonstrates the comprehensive error handling and recovery mechanisms in the Email Platform, including retry logic, dead letter queue processing, alerting, and manual recovery procedures.

## Sequence Flow

| Step | Source | Target | Method/Action | Description | Response/Result |
|------|--------|--------|---------------|-------------|-----------------|
| 1 | Marketing User | Angular UI | sendCampaign() | User initiates campaign sending | Send request initiated |
| 2 | Angular UI | API Gateway | POST /campaigns/send | UI sends campaign send request | Request forwarded |
| 3 | API Gateway | Email Processor | processEmailBatch() | Gateway routes to email processing | Processing started |
| 4 | Email Processor | Amazon SES | sendEmail() | Processor attempts to send email | Send attempt made |
| 5 | Amazon SES | Email Processor | return error (rate exceeded) | SES returns rate limiting error | Error received |
| 6 | Email Processor | CloudWatch Logs | logError() | Processor logs error details | Error logged |
| 7 | Email Processor | Email Processor | retryWithBackoff() | Processor initiates retry with exponential backoff | Retry scheduled |
| 8 | Email Processor | Amazon SES | sendEmail() [retry] | Processor retries email sending | Retry attempt made |
| 9 | Amazon SES | Email Processor | return error (still failing) | SES continues to return error | Retry failed |
| 10 | Email Processor | Dead Letter Queue | maxRetriesExceeded() | Processor sends message to DLQ after max retries | Message queued in DLQ |
| 11 | Email Processor | DynamoDB | updateCampaignStatus(failed) | Processor updates campaign status to failed | Status updated |
| 12 | Email Processor | SNS Alerts | triggerAlert() | Processor triggers alert notification | Alert sent |
| 13 | Dead Letter Queue | Error Handler | processFailedMessage() | DLQ triggers error handler for failed message | Error processing started |
| 14 | Error Handler | Error Handler | analyzeError() | Handler analyzes error type and cause | Error analyzed |
| 15 | Error Handler | CloudWatch Logs | logDetailedError() | Handler logs detailed error information | Detailed log created |
| 16 | Error Handler | DynamoDB | updateErrorMetrics() | Handler updates error metrics and statistics | Metrics updated |
| 17 | SNS Alerts | Support Team | sendAlert() | SNS sends alert to support team | Alert delivered |
| 18 | Support Team | CloudWatch Logs | investigateIssue() | Support team investigates using logs | Investigation started |
| 19 | Error Handler | SNS Alerts | notifyUser() | Handler triggers user notification | User notification sent |
| 20 | SNS Alerts | Angular UI | pushNotification() | SNS pushes notification to UI | Notification received |
| 21 | Angular UI | Marketing User | showErrorMessage() | UI displays error message to user | Error message shown |
| 22 | Support Team | Amazon SES | resolveIssue() | Support team resolves underlying issue | Issue resolved |
| 23 | Support Team | Dead Letter Queue | reprocessFailedMessages() | Support team triggers reprocessing | Reprocessing initiated |
| 24 | Dead Letter Queue | Email Processor | retryProcessing() | DLQ sends messages back for retry | Retry processing started |
| 25 | Email Processor | Amazon SES | sendEmail() [recovered] | Processor attempts sending after issue resolution | Send attempt made |
| 26 | Amazon SES | Email Processor | return success | SES returns successful delivery | Success confirmed |
| 27 | Email Processor | DynamoDB | updateStatus(sent) | Processor updates campaign status to sent | Status updated |
| 28 | Email Processor | SNS Alerts | notifyRecovery() | Processor notifies of successful recovery | Recovery notification sent |
| 29 | SNS Alerts | Angular UI | updateUI() | SNS triggers UI update | UI update initiated |
| 30 | Angular UI | Marketing User | showSuccessMessage() | UI displays success message | Success confirmation shown |

## Error Handling Phases

### Phase 1: Initial Error Detection (Steps 1-6)
- **Purpose**: Detect and log initial errors during email processing
- **Components**: Email Processor, Amazon SES, CloudWatch Logs
- **Error Types**:
  - Rate limiting errors
  - Authentication failures
  - Service unavailable errors
  - Invalid recipient errors
- **Actions**: Error logging with context and correlation IDs

### Phase 2: Retry Logic (Steps 7-9)
- **Purpose**: Attempt automatic recovery through retry mechanisms
- **Strategy**: Exponential backoff with jitter
- **Configuration**:
  - Initial delay: 1 second
  - Maximum delay: 300 seconds (5 minutes)
  - Maximum retries: 3 attempts
  - Backoff multiplier: 2.0
- **Outcome**: Either successful retry or escalation to DLQ

### Phase 3: Dead Letter Queue Processing (Steps 10-16)
- **Purpose**: Handle messages that exceed maximum retry attempts
- **Components**: Dead Letter Queue, Error Handler, DynamoDB
- **Processing**:
  - Message analysis and categorization
  - Error metrics collection
  - Detailed logging for troubleshooting
- **Outcome**: Comprehensive error documentation and metrics

### Phase 4: Alerting and Notification (Steps 17-21)
- **Purpose**: Notify relevant parties of system issues
- **Recipients**:
  - Support team for technical issues
  - End users for campaign failures
  - Operations team for system-wide problems
- **Channels**: SNS, email, Slack, PagerDuty
- **Outcome**: Stakeholders informed and investigation initiated

### Phase 5: Manual Recovery (Steps 22-30)
- **Purpose**: Resolve issues and recover failed operations
- **Components**: Support Team, Dead Letter Queue, Email Processor
- **Process**:
  - Issue investigation and resolution
  - Failed message reprocessing
  - Status updates and user notification
- **Outcome**: System recovery and user satisfaction

## Error Categories and Handling

### Transient Errors
| Error Type | Cause | Retry Strategy | Resolution |
|------------|-------|----------------|------------|
| Rate Limiting | SES sending limits exceeded | Exponential backoff | Wait and retry |
| Service Unavailable | Temporary AWS service issues | Linear backoff | Retry with delay |
| Network Timeout | Network connectivity issues | Immediate retry | Retry 2-3 times |
| Database Throttling | DynamoDB capacity exceeded | Exponential backoff | Auto-scaling kicks in |

### Permanent Errors
| Error Type | Cause | Action | Resolution |
|------------|-------|--------|------------|
| Invalid Email | Malformed email address | Skip recipient | Remove from list |
| Authentication Error | Invalid AWS credentials | Alert operations | Update credentials |
| Permission Denied | Insufficient IAM permissions | Alert operations | Update permissions |
| Resource Not Found | Missing template or data | Alert user | Recreate resource |

### System Errors
| Error Type | Cause | Action | Resolution |
|------------|-------|--------|------------|
| Lambda Timeout | Function execution timeout | Increase timeout | Optimize code |
| Memory Exhaustion | Insufficient Lambda memory | Increase memory | Optimize memory usage |
| Concurrent Execution | Lambda concurrency limit | Queue requests | Increase concurrency |
| Dead Letter Queue Full | Too many failed messages | Manual intervention | Process DLQ messages |

## Retry Configuration

### Exponential Backoff Algorithm
```javascript
function calculateBackoffDelay(attempt, baseDelay = 1000, maxDelay = 300000) {
  const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);
  const jitter = Math.random() * 0.1 * delay; // Add 10% jitter
  return delay + jitter;
}

// Example retry delays:
// Attempt 1: ~1 second
// Attempt 2: ~2 seconds  
// Attempt 3: ~4 seconds
// Attempt 4: ~8 seconds (if configured)
```

### Retry Policy Configuration
```json
{
  "retryPolicy": {
    "maxRetries": 3,
    "baseDelayMs": 1000,
    "maxDelayMs": 300000,
    "backoffMultiplier": 2.0,
    "jitterPercent": 10,
    "retryableErrors": [
      "ThrottlingException",
      "ServiceUnavailable",
      "InternalServerError",
      "NetworkTimeout"
    ],
    "nonRetryableErrors": [
      "InvalidParameterValue",
      "AccessDenied",
      "ResourceNotFound",
      "ValidationException"
    ]
  }
}
```

## Dead Letter Queue Management

### DLQ Message Structure
```json
{
  "messageId": "msg_123456789",
  "originalTimestamp": "2024-01-15T10:30:00Z",
  "failureTimestamp": "2024-01-15T10:35:00Z",
  "retryCount": 3,
  "lastError": {
    "errorCode": "Throttling",
    "errorMessage": "Rate exceeded",
    "stackTrace": "...",
    "requestId": "req_123456789"
  },
  "originalMessage": {
    "campaignId": "camp_123456789",
    "recipients": ["user@example.com"],
    "templateId": "tmpl_123456789"
  }
}
```

### DLQ Processing Workflow
1. **Message Analysis**: Categorize error type and determine if recoverable
2. **Error Aggregation**: Group similar errors for batch resolution
3. **Root Cause Analysis**: Identify underlying system issues
4. **Recovery Planning**: Determine recovery strategy and timeline
5. **Reprocessing**: Retry messages after issue resolution
6. **Monitoring**: Track recovery success rates

## Alerting Configuration

### Alert Severity Levels
| Level | Criteria | Response Time | Notification Channels |
|-------|----------|---------------|----------------------|
| Critical | System down, data loss | Immediate | PagerDuty, SMS, Phone |
| High | Service degradation | 15 minutes | Email, Slack, PagerDuty |
| Medium | Error rate increase | 1 hour | Email, Slack |
| Low | Performance degradation | 4 hours | Email |

### Alert Rules
```json
{
  "alertRules": [
    {
      "name": "High Error Rate",
      "condition": "error_rate > 5% for 5 minutes",
      "severity": "high",
      "channels": ["email", "slack"]
    },
    {
      "name": "DLQ Backup",
      "condition": "dlq_message_count > 100",
      "severity": "medium",
      "channels": ["email", "slack"]
    },
    {
      "name": "SES Quota Alert",
      "condition": "ses_quota_usage > 80%",
      "severity": "medium",
      "channels": ["email"]
    }
  ]
}
```

## Error Metrics and Monitoring

### Key Metrics
- **Error Rate**: Percentage of failed operations
- **Retry Success Rate**: Percentage of successful retries
- **DLQ Message Count**: Number of messages in dead letter queue
- **Mean Time to Recovery (MTTR)**: Average time to resolve issues
- **Mean Time Between Failures (MTBF)**: Average time between failures

### Monitoring Dashboard
```json
{
  "dashboard": {
    "widgets": [
      {
        "type": "metric",
        "title": "Error Rate",
        "metric": "email.error_rate",
        "threshold": 5.0
      },
      {
        "type": "metric",
        "title": "DLQ Depth",
        "metric": "queue.dlq_message_count",
        "threshold": 100
      },
      {
        "type": "log",
        "title": "Recent Errors",
        "query": "ERROR level:error",
        "timeRange": "1h"
      }
    ]
  }
}
```

## Recovery Procedures

### Automated Recovery
1. **Circuit Breaker**: Stop processing when error rate is high
2. **Health Checks**: Monitor service health and auto-recover
3. **Auto-scaling**: Scale resources based on demand
4. **Failover**: Switch to backup systems when primary fails

### Manual Recovery
1. **Issue Investigation**: Analyze logs and metrics
2. **Root Cause Identification**: Determine underlying cause
3. **Fix Implementation**: Apply necessary fixes
4. **Message Reprocessing**: Retry failed messages
5. **Monitoring**: Verify recovery success

### Recovery Validation
```javascript
// Validate recovery by processing test messages
async function validateRecovery() {
  const testMessage = {
    campaignId: "test_recovery",
    recipients: ["test@example.com"],
    templateId: "test_template"
  };
  
  try {
    const result = await processEmailBatch(testMessage);
    if (result.success) {
      console.log("Recovery validated successfully");
      return true;
    }
  } catch (error) {
    console.error("Recovery validation failed:", error);
    return false;
  }
}
```

## Preventive Measures

### Proactive Monitoring
- **Predictive Alerts**: Alert before issues become critical
- **Trend Analysis**: Monitor trends to predict failures
- **Capacity Planning**: Ensure adequate resources
- **Performance Testing**: Regular load testing

### System Resilience
- **Redundancy**: Multiple availability zones and regions
- **Load Balancing**: Distribute load across resources
- **Rate Limiting**: Prevent system overload
- **Graceful Degradation**: Maintain core functionality during issues

### Operational Excellence
- **Runbooks**: Documented procedures for common issues
- **Training**: Regular training for support team
- **Post-Mortem**: Learn from incidents and improve
- **Automation**: Automate common recovery procedures
