# Email Platform REST API Specification

## Overview

The Email Platform REST API provides comprehensive email marketing capabilities through a RESTful interface. The API supports campaign management, template operations, recipient list management, and detailed analytics.

## Base URL

```
Production: https://api.emailplatform.messagecentre.com/v1
Staging: https://staging-api.emailplatform.messagecentre.com/v1
Development: https://dev-api.emailplatform.messagecentre.com/v1
```

## Authentication

The API supports multiple authentication methods:

### 1. API Key Authentication (Required)
All requests must include an API key in the header:
```http
x-api-key: your-api-key-here
```

### 2. OAuth 2.0 (Optional)
For enhanced security, OAuth 2.0 Bearer tokens can be used:
```http
Authorization: Bearer your-oauth-token-here
```

### 3. Mutual TLS (Optional)
For enterprise clients, mTLS authentication is supported through client certificates.

## Request/Response Format

- **Content-Type**: `application/json`
- **Character Encoding**: UTF-8
- **Date Format**: ISO 8601 (e.g., `2024-01-15T10:30:00Z`)

## Rate Limiting

- **Default Limit**: 1000 requests per hour per API key
- **Burst Limit**: 100 requests per minute
- **Headers**: Rate limit information is returned in response headers:
  ```http
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 999
  X-RateLimit-Reset: 1642248600
  ```

## Error Handling

### Standard HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request parameters |
| 401 | Unauthorized - Invalid or missing authentication |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation errors |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |
| 503 | Service Unavailable - Service temporarily unavailable |

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "requestId": "req_123456789"
  }
}
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `INVALID_API_KEY` | API key is invalid or expired |
| `VALIDATION_ERROR` | Request validation failed |
| `RESOURCE_NOT_FOUND` | Requested resource not found |
| `DUPLICATE_RESOURCE` | Resource already exists |
| `QUOTA_EXCEEDED` | Account quota exceeded |
| `RATE_LIMIT_EXCEEDED` | Rate limit exceeded |
| `INSUFFICIENT_PERMISSIONS` | Insufficient permissions for operation |

## API Endpoints

### 1. Campaign Management

#### Create Campaign

**POST** `/campaigns`

Creates a new email campaign.

**Request Body:**
```json
{
  "name": "Summer Sale 2024",
  "description": "Promotional campaign for summer sale",
  "subject": "🌞 Summer Sale - Up to 50% Off!",
  "fromName": "Marketing Team",
  "fromEmail": "marketing@company.com",
  "replyTo": "support@company.com",
  "template": {
    "html": "<html><body><h1>{{firstName}}, don't miss our summer sale!</h1></body></html>",
    "text": "{{firstName}}, don't miss our summer sale!"
  },
  "recipients": [
    {
      "email": "customer@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "customFields": {
        "company": "Acme Corp",
        "segment": "premium"
      }
    }
  ],
  "schedule": {
    "sendAt": "2024-06-15T09:00:00Z",
    "timezone": "Australia/Sydney"
  },
  "settings": {
    "trackOpens": true,
    "trackClicks": true,
    "throttle": {
      "emailsPerHour": 1000,
      "emailsPerMinute": 50
    },
    "deliveryWindow": {
      "start": "09:00",
      "end": "17:00",
      "timezone": "Australia/Sydney"
    }
  },
  "tags": ["summer", "sale", "promotional"]
}
```

**Response (201 Created):**
```json
{
  "id": "camp_123456789",
  "name": "Summer Sale 2024",
  "status": "draft",
  "created": "2024-01-15T10:30:00Z",
  "updated": "2024-01-15T10:30:00Z",
  "recipientCount": 1,
  "estimatedSendTime": "2024-06-15T09:00:00Z",
  "links": {
    "self": "/campaigns/camp_123456789",
    "preview": "/campaigns/camp_123456789/preview",
    "send": "/campaigns/camp_123456789/send"
  }
}
```

#### Get Campaign

**GET** `/campaigns/{campaignId}`

Retrieves campaign details and statistics.

**Response (200 OK):**
```json
{
  "id": "camp_123456789",
  "name": "Summer Sale 2024",
  "description": "Promotional campaign for summer sale",
  "status": "sent",
  "created": "2024-01-15T10:30:00Z",
  "updated": "2024-01-15T11:45:00Z",
  "sent": "2024-06-15T09:00:00Z",
  "subject": "🌞 Summer Sale - Up to 50% Off!",
  "fromName": "Marketing Team",
  "fromEmail": "marketing@company.com",
  "recipientCount": 10000,
  "statistics": {
    "sent": 9950,
    "delivered": 9800,
    "bounced": 150,
    "complained": 5,
    "opened": 4900,
    "clicked": 1470,
    "unsubscribed": 25,
    "deliveryRate": 98.49,
    "openRate": 50.0,
    "clickRate": 15.0,
    "bounceRate": 1.51,
    "complaintRate": 0.05,
    "unsubscribeRate": 0.26
  },
  "tags": ["summer", "sale", "promotional"]
}
```

#### List Campaigns

**GET** `/campaigns`

Retrieves a paginated list of campaigns.

**Query Parameters:**
- `limit` (integer, optional): Number of campaigns to return (default: 20, max: 100)
- `offset` (integer, optional): Number of campaigns to skip (default: 0)
- `status` (string, optional): Filter by status (`draft`, `scheduled`, `sending`, `sent`, `failed`)
- `tag` (string, optional): Filter by tag
- `sort` (string, optional): Sort field (`created`, `updated`, `name`, `sent`)
- `order` (string, optional): Sort order (`asc`, `desc`)

**Response (200 OK):**
```json
{
  "campaigns": [
    {
      "id": "camp_123456789",
      "name": "Summer Sale 2024",
      "status": "sent",
      "created": "2024-01-15T10:30:00Z",
      "recipientCount": 10000,
      "statistics": {
        "deliveryRate": 98.49,
        "openRate": 50.0,
        "clickRate": 15.0
      }
    }
  ],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 150,
    "hasMore": true
  }
}
```

#### Update Campaign

**PUT** `/campaigns/{campaignId}`

Updates an existing campaign (only allowed for draft campaigns).

**Request Body:** Same as Create Campaign

**Response (200 OK):** Same as Get Campaign

#### Delete Campaign

**DELETE** `/campaigns/{campaignId}`

Deletes a campaign (only allowed for draft campaigns).

**Response (204 No Content)**

#### Send Campaign

**POST** `/campaigns/{campaignId}/send`

Sends a campaign immediately or schedules it for later.

**Request Body:**
```json
{
  "sendAt": "2024-06-15T09:00:00Z",
  "timezone": "Australia/Sydney"
}
```

**Response (200 OK):**
```json
{
  "id": "camp_123456789",
  "status": "scheduled",
  "scheduledFor": "2024-06-15T09:00:00Z",
  "estimatedCompletion": "2024-06-15T12:00:00Z"
}
```

#### Cancel Campaign

**POST** `/campaigns/{campaignId}/cancel`

Cancels a scheduled campaign.

**Response (200 OK):**
```json
{
  "id": "camp_123456789",
  "status": "cancelled",
  "cancelledAt": "2024-01-15T10:30:00Z"
}
```

### 2. Template Management

#### Create Template

**POST** `/templates`

Creates a new email template.

**Request Body:**
```json
{
  "name": "Welcome Email Template",
  "description": "Template for welcoming new customers",
  "category": "welcome",
  "html": "<html><body><h1>Welcome {{firstName}}!</h1><p>Thank you for joining us.</p></body></html>",
  "text": "Welcome {{firstName}}! Thank you for joining us.",
  "variables": [
    {
      "name": "firstName",
      "type": "string",
      "required": true,
      "description": "Customer's first name"
    },
    {
      "name": "companyName",
      "type": "string",
      "required": false,
      "description": "Customer's company name"
    }
  ],
  "previewData": {
    "firstName": "John",
    "companyName": "Acme Corp"
  },
  "tags": ["welcome", "onboarding"]
}
```

**Response (201 Created):**
```json
{
  "id": "tmpl_123456789",
  "name": "Welcome Email Template",
  "category": "welcome",
  "created": "2024-01-15T10:30:00Z",
  "updated": "2024-01-15T10:30:00Z",
  "version": 1,
  "status": "active",
  "links": {
    "self": "/templates/tmpl_123456789",
    "preview": "/templates/tmpl_123456789/preview"
  }
}
```

#### Get Template

**GET** `/templates/{templateId}`

Retrieves template details.

**Response (200 OK):**
```json
{
  "id": "tmpl_123456789",
  "name": "Welcome Email Template",
  "description": "Template for welcoming new customers",
  "category": "welcome",
  "html": "<html><body><h1>Welcome {{firstName}}!</h1></body></html>",
  "text": "Welcome {{firstName}}! Thank you for joining us.",
  "variables": [
    {
      "name": "firstName",
      "type": "string",
      "required": true,
      "description": "Customer's first name"
    }
  ],
  "created": "2024-01-15T10:30:00Z",
  "updated": "2024-01-15T10:30:00Z",
  "version": 1,
  "status": "active",
  "usageCount": 25,
  "tags": ["welcome", "onboarding"]
}
```

#### List Templates

**GET** `/templates`

Retrieves a paginated list of templates.

**Query Parameters:**
- `limit` (integer, optional): Number of templates to return (default: 20, max: 100)
- `offset` (integer, optional): Number of templates to skip (default: 0)
- `category` (string, optional): Filter by category
- `status` (string, optional): Filter by status (`active`, `archived`)
- `tag` (string, optional): Filter by tag

**Response (200 OK):**
```json
{
  "templates": [
    {
      "id": "tmpl_123456789",
      "name": "Welcome Email Template",
      "category": "welcome",
      "created": "2024-01-15T10:30:00Z",
      "version": 1,
      "status": "active",
      "usageCount": 25
    }
  ],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 50,
    "hasMore": true
  }
}
```

#### Preview Template

**POST** `/templates/{templateId}/preview`

Generates a preview of the template with sample data.

**Request Body:**
```json
{
  "data": {
    "firstName": "John",
    "companyName": "Acme Corp"
  },
  "format": "html"
}
```

**Response (200 OK):**
```json
{
  "html": "<html><body><h1>Welcome John!</h1><p>Thank you for joining us at Acme Corp.</p></body></html>",
  "text": "Welcome John! Thank you for joining us at Acme Corp.",
  "subject": "Welcome to Acme Corp, John!"
}
```

### 3. Recipient Management

#### Create Recipient List

**POST** `/recipients/lists`

Creates a new recipient list.

**Request Body:**
```json
{
  "name": "Premium Customers",
  "description": "List of premium tier customers",
  "recipients": [
    {
      "email": "john@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "customFields": {
        "company": "Acme Corp",
        "tier": "premium",
        "signupDate": "2023-01-15"
      }
    }
  ],
  "tags": ["premium", "customers"]
}
```

**Response (201 Created):**
```json
{
  "id": "list_123456789",
  "name": "Premium Customers",
  "created": "2024-01-15T10:30:00Z",
  "recipientCount": 1,
  "validEmails": 1,
  "invalidEmails": 0,
  "duplicates": 0,
  "status": "active"
}
```

#### Get Recipient List

**GET** `/recipients/lists/{listId}`

Retrieves recipient list details.

**Response (200 OK):**
```json
{
  "id": "list_123456789",
  "name": "Premium Customers",
  "description": "List of premium tier customers",
  "created": "2024-01-15T10:30:00Z",
  "updated": "2024-01-15T10:30:00Z",
  "recipientCount": 1000,
  "validEmails": 995,
  "invalidEmails": 5,
  "status": "active",
  "tags": ["premium", "customers"]
}
```

#### Add Recipients to List

**POST** `/recipients/lists/{listId}/recipients`

Adds recipients to an existing list.

**Request Body:**
```json
{
  "recipients": [
    {
      "email": "jane@example.com",
      "firstName": "Jane",
      "lastName": "Smith",
      "customFields": {
        "company": "Tech Corp",
        "tier": "premium"
      }
    }
  ],
  "skipDuplicates": true
}
```

**Response (200 OK):**
```json
{
  "added": 1,
  "skipped": 0,
  "invalid": 0,
  "duplicates": 0,
  "totalRecipients": 1001
}
```

#### Validate Email Addresses

**POST** `/recipients/validate`

Validates a list of email addresses.

**Request Body:**
```json
{
  "emails": [
    "valid@example.com",
    "invalid-email",
    "bounced@example.com"
  ]
}
```

**Response (200 OK):**
```json
{
  "results": [
    {
      "email": "valid@example.com",
      "valid": true,
      "reason": "valid"
    },
    {
      "email": "invalid-email",
      "valid": false,
      "reason": "invalid_format"
    },
    {
      "email": "bounced@example.com",
      "valid": false,
      "reason": "previously_bounced"
    }
  ],
  "summary": {
    "total": 3,
    "valid": 1,
    "invalid": 2
  }
}
```

### 4. Analytics and Reporting

#### Get Campaign Analytics

**GET** `/campaigns/{campaignId}/analytics`

Retrieves detailed analytics for a campaign.

**Query Parameters:**
- `period` (string, optional): Time period (`1h`, `24h`, `7d`, `30d`)
- `granularity` (string, optional): Data granularity (`hour`, `day`)

**Response (200 OK):**
```json
{
  "campaignId": "camp_123456789",
  "period": {
    "start": "2024-06-15T09:00:00Z",
    "end": "2024-06-16T09:00:00Z"
  },
  "summary": {
    "sent": 10000,
    "delivered": 9800,
    "bounced": 150,
    "complained": 5,
    "opened": 4900,
    "clicked": 1470,
    "unsubscribed": 25,
    "deliveryRate": 98.0,
    "openRate": 50.0,
    "clickRate": 15.0,
    "bounceRate": 1.5,
    "complaintRate": 0.05,
    "unsubscribeRate": 0.26
  },
  "timeline": [
    {
      "timestamp": "2024-06-15T09:00:00Z",
      "sent": 1000,
      "delivered": 980,
      "opened": 490,
      "clicked": 147
    }
  ],
  "topLinks": [
    {
      "url": "https://example.com/product1",
      "clicks": 500,
      "uniqueClicks": 450
    }
  ],
  "bounceReasons": [
    {
      "reason": "mailbox_full",
      "count": 75
    },
    {
      "reason": "invalid_address",
      "count": 50
    }
  ],
  "deviceStats": {
    "desktop": 60,
    "mobile": 35,
    "tablet": 5
  },
  "locationStats": [
    {
      "country": "Australia",
      "opens": 2450,
      "clicks": 735
    }
  ]
}
```

#### Get Account Analytics

**GET** `/analytics/account`

Retrieves account-level analytics.

**Query Parameters:**
- `period` (string, optional): Time period (`7d`, `30d`, `90d`, `1y`)
- `granularity` (string, optional): Data granularity (`day`, `week`, `month`)

**Response (200 OK):**
```json
{
  "period": {
    "start": "2024-01-01T00:00:00Z",
    "end": "2024-01-31T23:59:59Z"
  },
  "summary": {
    "campaignsSent": 25,
    "emailsSent": 250000,
    "deliveryRate": 98.5,
    "averageOpenRate": 22.5,
    "averageClickRate": 3.2,
    "bounceRate": 1.5,
    "complaintRate": 0.02
  },
  "timeline": [
    {
      "date": "2024-01-01",
      "campaignsSent": 2,
      "emailsSent": 15000,
      "delivered": 14775,
      "opened": 3325,
      "clicked": 480
    }
  ],
  "topCampaigns": [
    {
      "id": "camp_123456789",
      "name": "Summer Sale 2024",
      "openRate": 50.0,
      "clickRate": 15.0
    }
  ]
}
```

### 5. Webhook Management

#### Create Webhook

**POST** `/webhooks`

Creates a new webhook endpoint.

**Request Body:**
```json
{
  "url": "https://your-app.com/webhooks/email-events",
  "events": [
    "email.delivered",
    "email.bounced",
    "email.complained",
    "email.opened",
    "email.clicked",
    "email.unsubscribed"
  ],
  "secret": "your-webhook-secret",
  "active": true
}
```

**Response (201 Created):**
```json
{
  "id": "webhook_123456789",
  "url": "https://your-app.com/webhooks/email-events",
  "events": [
    "email.delivered",
    "email.bounced",
    "email.complained",
    "email.opened",
    "email.clicked",
    "email.unsubscribed"
  ],
  "active": true,
  "created": "2024-01-15T10:30:00Z"
}
```

#### Webhook Event Format

Webhook events are sent as POST requests with the following format:

```json
{
  "id": "event_123456789",
  "type": "email.opened",
  "timestamp": "2024-06-15T10:30:00Z",
  "data": {
    "campaignId": "camp_123456789",
    "recipientEmail": "customer@example.com",
    "messageId": "msg_123456789",
    "userAgent": "Mozilla/5.0...",
    "ipAddress": "192.168.1.1",
    "location": {
      "country": "Australia",
      "region": "NSW",
      "city": "Sydney"
    }
  }
}
```

### 6. Account Management

#### Get Account Information

**GET** `/account`

Retrieves account information and quotas.

**Response (200 OK):**
```json
{
  "id": "acc_123456789",
  "name": "Acme Corporation",
  "plan": "enterprise",
  "status": "active",
  "created": "2023-01-15T10:30:00Z",
  "quotas": {
    "emailsPerMonth": 1000000,
    "emailsUsedThisMonth": 250000,
    "campaignsPerMonth": 100,
    "campaignsUsedThisMonth": 25,
    "recipientListsMax": 50,
    "recipientListsUsed": 12,
    "templatesMax": 100,
    "templatesUsed": 25
  },
  "settings": {
    "timezone": "Australia/Sydney",
    "defaultFromEmail": "noreply@acme.com",
    "defaultFromName": "Acme Corporation",
    "trackingEnabled": true,
    "suppressionListEnabled": true
  }
}
```

## Webhook Events

### Event Types

| Event Type | Description |
|------------|-------------|
| `email.sent` | Email was successfully sent to SES |
| `email.delivered` | Email was delivered to recipient's inbox |
| `email.bounced` | Email bounced (hard or soft bounce) |
| `email.complained` | Recipient marked email as spam |
| `email.opened` | Recipient opened the email |
| `email.clicked` | Recipient clicked a link in the email |
| `email.unsubscribed` | Recipient unsubscribed |
| `campaign.started` | Campaign sending started |
| `campaign.completed` | Campaign sending completed |
| `campaign.failed` | Campaign sending failed |

### Webhook Security

Webhooks are secured using HMAC-SHA256 signatures:

1. The webhook payload is signed using your webhook secret
2. The signature is included in the `X-Signature-SHA256` header
3. Verify the signature to ensure the webhook is from our service

**Example verification (Node.js):**
```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');
  
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignature)
  );
}
```

## SDK Examples

### JavaScript/Node.js

```javascript
const EmailPlatformAPI = require('@messagecentre/email-platform-sdk');

const client = new EmailPlatformAPI({
  apiKey: 'your-api-key',
  baseURL: 'https://api.emailplatform.messagecentre.com/v1'
});

// Create a campaign
const campaign = await client.campaigns.create({
  name: 'Welcome Campaign',
  subject: 'Welcome to our platform!',
  template: {
    html: '<h1>Welcome {{firstName}}!</h1>',
    text: 'Welcome {{firstName}}!'
  },
  recipients: [
    {
      email: 'customer@example.com',
      firstName: 'John'
    }
  ]
});

// Send the campaign
await client.campaigns.send(campaign.id);
```

### Python

```python
from email_platform_sdk import EmailPlatformClient

client = EmailPlatformClient(
    api_key='your-api-key',
    base_url='https://api.emailplatform.messagecentre.com/v1'
)

# Create a campaign
campaign = client.campaigns.create({
    'name': 'Welcome Campaign',
    'subject': 'Welcome to our platform!',
    'template': {
        'html': '<h1>Welcome {{firstName}}!</h1>',
        'text': 'Welcome {{firstName}}!'
    },
    'recipients': [
        {
            'email': 'customer@example.com',
            'firstName': 'John'
        }
    ]
})

# Send the campaign
client.campaigns.send(campaign['id'])
```

### cURL Examples

#### Create Campaign
```bash
curl -X POST https://api.emailplatform.messagecentre.com/v1/campaigns \
  -H "x-api-key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Welcome Campaign",
    "subject": "Welcome!",
    "template": {
      "html": "<h1>Welcome!</h1>",
      "text": "Welcome!"
    },
    "recipients": [
      {
        "email": "test@example.com",
        "firstName": "Test"
      }
    ]
  }'
```

#### Get Campaign Analytics
```bash
curl -X GET https://api.emailplatform.messagecentre.com/v1/campaigns/camp_123456789/analytics \
  -H "x-api-key: your-api-key"
```

## Testing

### Sandbox Environment

Use the sandbox environment for testing:
```
Sandbox URL: https://sandbox-api.emailplatform.messagecentre.com/v1
```

In sandbox mode:
- No actual emails are sent
- All API responses are simulated
- Rate limits are relaxed for testing
- Test data is automatically cleaned up after 24 hours

### Test API Keys

Test API keys are prefixed with `test_` and only work in sandbox mode:
```
Test API Key: test_sk_1234567890abcdef
```

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial API release
- Campaign management endpoints
- Template management endpoints
- Recipient management endpoints
- Analytics and reporting endpoints
- Webhook support

### Version 1.1.0 (Planned - 2024-03-01)
- A/B testing support
- Advanced segmentation
- Automation workflows
- Enhanced analytics

## Support

For API support and questions:
- **Documentation**: https://docs.emailplatform.messagecentre.com
- **Support Email**: api-support@messagecentre.com
- **Status Page**: https://status.emailplatform.messagecentre.com
- **Community Forum**: https://community.messagecentre.com

## Terms of Service

By using this API, you agree to our Terms of Service and Privacy Policy:
- **Terms of Service**: https://messagecentre.com/terms
- **Privacy Policy**: https://messagecentre.com/privacy
- **Acceptable Use Policy**: https://messagecentre.com/acceptable-use
