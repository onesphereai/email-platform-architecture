# Campaign Creation Sequence - Flow Description

**Diagram**: `10_campaign_creation_sequence.png`

## Overview
This sequence diagram shows the complete flow for a marketing user creating an email campaign, from authentication through template upload and recipient management.

## Sequence Flow

| Step | Source | Target | Method/Action | Description | Response/Result |
|------|--------|--------|---------------|-------------|-----------------|
| 1 | Marketing User | Angular UI | login() | User initiates login process | Login form displayed |
| 2 | Angular UI | API Gateway | authenticate() | UI sends authentication request | Request forwarded |
| 3 | API Gateway | Cognito Auth | validateCredentials() | API Gateway validates user credentials | Credentials verified |
| 4 | Cognito Auth | API Gateway | return JWT token | Authentication service returns JWT token | Token received |
| 5 | API Gateway | Angular UI | return auth success | API Gateway confirms successful authentication | Auth success returned |
| 6 | Angular UI | Marketing User | show dashboard | UI displays the main dashboard | Dashboard visible |
| 7 | Marketing User | Angular UI | createCampaign() | User initiates campaign creation | Campaign form opened |
| 8 | Angular UI | API Gateway | POST /campaigns | UI sends campaign data to API | Request sent |
| 9 | API Gateway | Campaign Service | validateRequest() | API Gateway validates and routes request | Request validated |
| 10 | Campaign Service | DynamoDB | saveCampaign() | Campaign service stores campaign data | Data stored |
| 11 | DynamoDB | Campaign Service | return campaignId | Database returns unique campaign identifier | Campaign ID received |
| 12 | Campaign Service | API Gateway | return campaign | Service returns campaign object | Campaign data returned |
| 13 | API Gateway | Angular UI | return 201 Created | API confirms campaign creation | Success status returned |
| 14 | Angular UI | Marketing User | show success | UI displays success message | Success confirmation |
| 15 | Marketing User | Angular UI | uploadTemplate() | User uploads email template | Template upload initiated |
| 16 | Angular UI | API Gateway | POST /templates | UI sends template data to API | Template data sent |
| 17 | API Gateway | Template Service | processTemplate() | API routes to template processing service | Template processing started |
| 18 | Template Service | S3 Storage | storeTemplate() | Service stores template files in S3 | Template files stored |
| 19 | Template Service | DynamoDB | saveMetadata() | Service saves template metadata | Metadata stored |
| 20 | Template Service | API Gateway | return template | Service returns template information | Template data returned |
| 21 | API Gateway | Angular UI | return success | API confirms template upload success | Success confirmed |
| 22 | Marketing User | Angular UI | uploadRecipients() | User uploads recipient list | Recipient upload initiated |
| 23 | Angular UI | API Gateway | POST /recipients | UI sends recipient data to API | Recipient data sent |
| 24 | API Gateway | Recipient Service | validateEmails() | API routes to recipient validation service | Email validation started |
| 25 | Recipient Service | DynamoDB | storeRecipients() | Service stores validated recipients | Recipients stored |
| 26 | Recipient Service | API Gateway | return validation | Service returns validation results | Validation results returned |
| 27 | API Gateway | Angular UI | return success | API confirms recipient upload success | Success confirmed |
| 28 | Angular UI | Marketing User | show ready to send | UI indicates campaign is ready to send | Ready status displayed |

## Process Phases

### Phase 1: Authentication (Steps 1-6)
- **Purpose**: Secure user authentication using SAML/JWT
- **Components**: Angular UI, API Gateway, Cognito Auth
- **Outcome**: Authenticated user session with dashboard access

### Phase 2: Campaign Creation (Steps 7-14)
- **Purpose**: Create new email campaign with basic information
- **Components**: Campaign Service, DynamoDB
- **Data Stored**: Campaign metadata, settings, tenant information
- **Outcome**: Campaign created with unique identifier

### Phase 3: Template Upload (Steps 15-21)
- **Purpose**: Upload and process email template
- **Components**: Template Service, S3 Storage, DynamoDB
- **Data Stored**: HTML/text templates, assets, template metadata
- **Outcome**: Template ready for campaign use

### Phase 4: Recipient Management (Steps 22-28)
- **Purpose**: Upload and validate recipient email list
- **Components**: Recipient Service, DynamoDB
- **Validation**: Email format, domain validation, duplicate checking
- **Outcome**: Campaign ready for sending

## Data Flow

### Authentication Data
- **Input**: User credentials (SAML assertion)
- **Processing**: Cognito validation, JWT generation
- **Output**: Authenticated session token

### Campaign Data
- **Input**: Campaign name, subject, settings, sender information
- **Processing**: Validation, tenant association, metadata creation
- **Storage**: DynamoDB with tenant-specific partition key
- **Output**: Campaign ID and configuration

### Template Data
- **Input**: HTML template, text version, assets
- **Processing**: Template validation, asset optimization
- **Storage**: S3 for files, DynamoDB for metadata
- **Output**: Template ID and processing status

### Recipient Data
- **Input**: Email list (CSV/JSON), custom fields
- **Processing**: Email validation, deduplication, formatting
- **Storage**: DynamoDB with campaign association
- **Output**: Validated recipient count and status

## Error Handling

### Authentication Errors
- Invalid credentials → Return 401 Unauthorized
- Expired tokens → Redirect to login
- SAML errors → Display error message

### Campaign Creation Errors
- Validation failures → Return 400 Bad Request with details
- Duplicate names → Return 409 Conflict
- Database errors → Return 500 Internal Server Error

### Template Upload Errors
- Invalid template format → Return 422 Unprocessable Entity
- File size limits → Return 413 Payload Too Large
- Storage errors → Return 500 Internal Server Error

### Recipient Upload Errors
- Invalid email formats → Return validation report
- Empty lists → Return 400 Bad Request
- Processing errors → Return 500 Internal Server Error

## Security Measures

### Authentication Security
- JWT tokens with expiration
- SAML assertion validation
- Session management

### Data Security
- Tenant isolation in all operations
- Input validation and sanitization
- Encrypted data storage

### API Security
- Request validation at API Gateway
- Rate limiting and throttling
- Audit logging for all operations

## Performance Considerations

### Asynchronous Processing
- Template processing can be async for large files
- Recipient validation can be batched
- Progress indicators for long operations

### Caching Strategy
- Template metadata caching
- User session caching
- Campaign configuration caching

### Scalability
- Serverless auto-scaling
- Database partition design
- CDN for static assets
