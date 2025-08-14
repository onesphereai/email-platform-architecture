# API Client Integration - Flow Description

**Diagram**: `12_api_integration_sequence.png`

## Overview
This sequence diagram shows how external API clients integrate with the Email Platform, including authentication, campaign processing, asynchronous email delivery, and webhook notifications.

## Sequence Flow

| Step | Source | Target | Method/Action | Description | Response/Result |
|------|--------|--------|---------------|-------------|-----------------|
| 1 | External API Client | API Gateway | POST /campaigns + x-api-key | Client sends campaign creation request with API key | Request received |
| 2 | API Gateway | Auth Service | validateApiKey() | Gateway validates the provided API key | Key validation initiated |
| 3 | Auth Service | API Gateway | return valid | Auth service confirms API key is valid | Validation confirmed |
| 4 | API Gateway | Email API | routeRequest() | Gateway routes authenticated request to Email API | Request routed |
| 5 | Email API | Email API | validateCampaignData() | API validates campaign data structure and content | Data validated |
| 6 | Email API | Template Service | processTemplate() | API sends template for processing and validation | Template processing started |
| 7 | Template Service | Email API | return templateId | Service returns processed template identifier | Template ID received |
| 8 | Email API | Recipient Service | validateRecipients() | API sends recipient list for validation | Recipient validation started |
| 9 | Recipient Service | Email API | return validatedList | Service returns validated recipient list | Validated list received |
| 10 | Email API | DynamoDB | saveCampaign() | API stores campaign data in database | Campaign data stored |
| 11 | DynamoDB | Email API | return campaignId | Database returns unique campaign identifier | Campaign ID received |
| 12 | Email API | Email Queue | queueEmailJob() | API queues email processing job | Job queued |
| 13 | Email API | API Gateway | return campaign | API returns campaign details | Campaign data returned |
| 14 | API Gateway | External API Client | return 201 Created | Gateway returns success response | Campaign created confirmation |
| 15 | Email Queue | Email Processor | processBatch() | Queue triggers batch processing | Batch processing started |
| 16 | Email Processor | Amazon SES | sendEmails() | Processor sends emails via SES | Emails sent for delivery |
| 17 | Amazon SES | Email Processor | return deliveryStatus | SES returns delivery status | Status received |
| 18 | Email Processor | DynamoDB | updateStatus() | Processor updates campaign status | Status updated |
| 19 | Email Processor | Webhook Service | triggerWebhook() | Processor triggers webhook notification | Webhook triggered |
| 20 | Webhook Service | Client Webhook | POST /webhook {status: delivered} | Service sends delivery notification | Webhook delivered |
| 21 | Client Webhook | Webhook Service | return 200 OK | Client confirms webhook receipt | Confirmation received |
| 22 | External API Client | API Gateway | GET /campaigns/{id} | Client requests campaign status | Status request sent |
| 23 | API Gateway | Email API | getCampaignStatus() | Gateway routes status request | Request routed |
| 24 | Email API | DynamoDB | queryStatus() | API queries campaign status | Status query executed |
| 25 | DynamoDB | Email API | return statistics | Database returns campaign statistics | Statistics received |
| 26 | Email API | API Gateway | return status | API returns status information | Status data returned |
| 27 | API Gateway | External API Client | return 200 OK | Gateway returns status response | Status delivered |

## Integration Phases

### Phase 1: Authentication & Request Validation (Steps 1-4)
- **Purpose**: Secure API access and request routing
- **Authentication Methods**: 
  - x-api-key (required)
  - OAuth2 Bearer token (optional)
  - mTLS client certificate (optional)
- **Validation**: API key validity, rate limiting, request format
- **Outcome**: Authenticated request routed to Email API

### Phase 2: Campaign Processing (Steps 5-14)
- **Purpose**: Process and validate campaign data
- **Components**: Email API, Template Service, Recipient Service
- **Operations**: 
  - Template validation and processing
  - Recipient list validation and deduplication
  - Campaign data storage with tenant isolation
- **Outcome**: Campaign created and queued for processing

### Phase 3: Asynchronous Email Processing (Steps 15-18)
- **Purpose**: Process and deliver emails asynchronously
- **Components**: Email Queue, Email Processor, Amazon SES
- **Operations**:
  - Batch processing of email jobs
  - Template rendering with personalization
  - Email delivery through SES
- **Outcome**: Emails delivered with status tracking

### Phase 4: Webhook Notifications (Steps 19-21)
- **Purpose**: Notify client of delivery events
- **Components**: Webhook Service, Client Webhook Endpoint
- **Events**: Delivery, bounce, complaint, open, click
- **Security**: HMAC signature validation
- **Outcome**: Client receives real-time event notifications

### Phase 5: Status Queries (Steps 22-27)
- **Purpose**: Allow clients to query campaign status
- **Components**: Email API, DynamoDB
- **Data**: Campaign statistics, delivery metrics, error information
- **Outcome**: Client receives current campaign status

## API Request Examples

### Campaign Creation Request
```json
POST /api/v1/campaigns
Headers:
  x-api-key: sk_live_1234567890abcdef
  Content-Type: application/json

{
  "name": "Product Launch Campaign",
  "subject": "Introducing Our New Product",
  "fromEmail": "marketing@company.com",
  "fromName": "Marketing Team",
  "template": {
    "html": "<h1>Hello {{firstName}}</h1><p>Check out our new product!</p>",
    "text": "Hello {{firstName}}, Check out our new product!"
  },
  "recipients": [
    {
      "email": "customer@example.com",
      "firstName": "John",
      "lastName": "Doe"
    }
  ],
  "settings": {
    "trackOpens": true,
    "trackClicks": true,
    "throttle": {
      "emailsPerHour": 1000
    }
  }
}
```

### Campaign Creation Response
```json
HTTP/1.1 201 Created
{
  "id": "camp_1234567890abcdef",
  "name": "Product Launch Campaign",
  "status": "queued",
  "created": "2024-01-15T10:30:00Z",
  "recipientCount": 1,
  "estimatedSendTime": "2024-01-15T10:35:00Z"
}
```

### Status Query Response
```json
HTTP/1.1 200 OK
{
  "id": "camp_1234567890abcdef",
  "name": "Product Launch Campaign",
  "status": "sent",
  "created": "2024-01-15T10:30:00Z",
  "sent": "2024-01-15T10:35:00Z",
  "statistics": {
    "sent": 1000,
    "delivered": 980,
    "bounced": 15,
    "complained": 2,
    "opened": 490,
    "clicked": 147,
    "deliveryRate": 98.0,
    "openRate": 50.0,
    "clickRate": 15.0
  }
}
```

### Webhook Event Example
```json
POST /your-webhook-endpoint
Headers:
  X-Signature-SHA256: sha256=1234567890abcdef...
  Content-Type: application/json

{
  "id": "evt_1234567890abcdef",
  "type": "email.delivered",
  "timestamp": "2024-01-15T10:35:00Z",
  "data": {
    "campaignId": "camp_1234567890abcdef",
    "messageId": "msg_1234567890abcdef",
    "recipientEmail": "customer@example.com",
    "deliveryTimestamp": "2024-01-15T10:35:00Z"
  }
}
```

## Authentication Methods

### API Key Authentication
- **Header**: `x-api-key: sk_live_1234567890abcdef`
- **Required**: Yes, for all requests
- **Validation**: Key validity, rate limits, permissions
- **Scope**: Full API access based on account permissions

### OAuth2 Authentication (Optional)
- **Header**: `Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`
- **Flow**: Client credentials or authorization code
- **Scope**: Granular permissions (campaigns.read, campaigns.write)
- **Expiration**: Configurable token lifetime

### Mutual TLS (Optional)
- **Method**: Client certificate authentication
- **Use Case**: High-security enterprise integrations
- **Validation**: Certificate chain validation
- **Benefits**: Non-repudiation, strong authentication

## Error Handling

### Authentication Errors
| Error Code | HTTP Status | Description | Resolution |
|------------|-------------|-------------|------------|
| INVALID_API_KEY | 401 | API key is invalid or expired | Check API key validity |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests | Implement backoff strategy |
| INSUFFICIENT_PERMISSIONS | 403 | API key lacks required permissions | Check account permissions |

### Validation Errors
| Error Code | HTTP Status | Description | Resolution |
|------------|-------------|-------------|------------|
| VALIDATION_ERROR | 400 | Request data validation failed | Fix request format |
| INVALID_EMAIL | 422 | Email addresses are invalid | Validate email format |
| TEMPLATE_ERROR | 422 | Template processing failed | Check template syntax |

### Processing Errors
| Error Code | HTTP Status | Description | Resolution |
|------------|-------------|-------------|------------|
| QUOTA_EXCEEDED | 429 | Account quota exceeded | Upgrade plan or wait |
| SERVICE_UNAVAILABLE | 503 | Temporary service issue | Retry with backoff |
| INTERNAL_ERROR | 500 | Unexpected server error | Contact support |

## Webhook Configuration

### Supported Events
- `email.sent` - Email successfully sent to SES
- `email.delivered` - Email delivered to recipient
- `email.bounced` - Email bounced (hard or soft)
- `email.complained` - Recipient marked as spam
- `email.opened` - Recipient opened email
- `email.clicked` - Recipient clicked link
- `email.unsubscribed` - Recipient unsubscribed

### Security
- **HMAC Signature**: All webhooks signed with shared secret
- **Retry Logic**: Failed webhooks retried with exponential backoff
- **Timeout**: 30-second timeout for webhook responses
- **Verification**: Signature verification required

### Configuration
```json
POST /api/v1/webhooks
{
  "url": "https://your-app.com/webhooks/email-events",
  "events": ["email.delivered", "email.bounced", "email.opened"],
  "secret": "your-webhook-secret-key",
  "active": true
}
```

## Rate Limiting

### Default Limits
- **Requests per hour**: 1000
- **Requests per minute**: 100
- **Burst limit**: 10 requests per second
- **Email sending**: Based on account tier

### Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642248600
```

### Handling Rate Limits
- **Exponential Backoff**: Increase delay between retries
- **Jitter**: Add randomness to prevent thundering herd
- **Circuit Breaker**: Stop requests when consistently failing
- **Queue Management**: Queue requests during rate limit periods
