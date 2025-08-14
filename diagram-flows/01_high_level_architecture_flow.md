# High Level Architecture - Flow Description

**Diagram**: `01_high_level_architecture.png`

## Overview
This diagram shows the complete high-level architecture of the Email Platform, including user access, core services, data flow, and external integrations.

## Flow Description

| Step | Source | Target | Action | Description |
|------|--------|--------|--------|-------------|
| 1 | B2B Customers | Internet | Access Platform | Users access the Email Platform through the internet |
| 2 | Internet | CloudFront CDN | Route Traffic | Internet traffic is routed through AWS CloudFront CDN |
| 3 | CloudFront CDN | S3 Static Website | Serve Static Content | CDN serves the Angular application static files from S3 |
| 4 | CloudFront CDN | API Gateway | API Requests | Dynamic API requests are forwarded to API Gateway |
| 5 | API Gateway | AWS Cognito | Authenticate | API Gateway validates user authentication through Cognito |
| 6 | API Gateway | Email Platform UI Backend | UI Requests | Authenticated UI requests are routed to the UI backend service |
| 7 | API Gateway | Email API | API Requests | External API requests are routed to the standalone Email API |
| 8 | Email Platform UI Backend | Campaign Manager | Campaign Operations | UI backend delegates campaign operations to the Campaign Manager |
| 9 | Email API | Email Processor | Email Processing | API requests trigger email processing workflows |
| 10 | Campaign Manager | Email Queue (SQS) | Queue Messages | Campaign operations are queued for asynchronous processing |
| 11 | Email Processor | Email Queue (SQS) | Process Queue | Email processor consumes messages from the queue |
| 12 | Email Queue (SQS) | Amazon SES | Send Emails | Queued email jobs are processed and sent via Amazon SES |
| 13 | Amazon SES | SNS Notification Topic | Delivery Status | SES publishes delivery status events to SNS |
| 14 | Email Platform UI Backend | DynamoDB | Store Data | UI operations store data in the single-table DynamoDB |
| 15 | Email API | DynamoDB | Store Data | API operations store campaign and user data |
| 16 | Campaign Manager | S3 Storage | Store Templates | Email templates and assets are stored in S3 |
| 17 | SNS Notification Topic | Analytics Engine | Analytics Data | Delivery events trigger analytics processing |
| 18 | Analytics Engine | OpenSearch Serverless | Index Data | Analytics data is indexed in OpenSearch for reporting |
| 19 | Email Platform UI Backend | CloudWatch | Logs & Metrics | Application logs and metrics are sent to CloudWatch |
| 20 | Email API | CloudWatch | Logs & Metrics | API logs and performance metrics are monitored |
| 21 | External Systems | Message Centre | Push Data | External systems push data to Message Centre for reporting |
| 22 | Message Centre | Email API | Report Data | Message Centre sends reporting data to the Email Platform |
| 23 | Bitbucket | Jenkins | Code Changes | Code changes trigger Jenkins CI/CD pipeline |
| 24 | Jenkins | Email Platform UI Backend | Deploy | Jenkins deploys updates to the platform services |

## Key Components

### Frontend Layer
- **CloudFront CDN**: Global content delivery network for static assets
- **S3 Static Website**: Hosts the Angular application files

### API Layer
- **API Gateway**: Centralized API management with authentication and rate limiting
- **AWS Cognito**: SAML-based authentication and user management

### Backend Services
- **Email Platform UI Backend**: Handles web application requests
- **Email API**: Standalone API for programmatic access
- **Campaign Manager**: Manages email campaign lifecycle
- **Email Processor**: Processes and sends email batches
- **Analytics Engine**: Processes delivery and engagement metrics

### Data Layer
- **DynamoDB**: Single-table design for all application data
- **S3 Storage**: File storage for templates and assets
- **OpenSearch Serverless**: Analytics and search capabilities

### Email Service
- **Amazon SES**: Email delivery service with reputation management

### Message Processing
- **SQS Email Queue**: Reliable message queuing for email processing
- **SNS Notification Topic**: Event-driven notifications

### Monitoring
- **CloudWatch**: Centralized logging and monitoring

### External Integration
- **Message Centre**: External reporting integration
- **Jenkins CI/CD**: Continuous integration and deployment

## Data Flow Patterns

### User Request Flow
1. User accesses platform → CDN → Static content served
2. API requests → API Gateway → Authentication → Backend services

### Email Processing Flow
1. Campaign creation → Queue → Asynchronous processing → SES delivery
2. Delivery events → SNS → Analytics → OpenSearch indexing

### External Integration Flow
1. External systems → Message Centre → Email Platform API
2. Cross-platform data sharing and reporting

## Security Considerations
- All traffic flows through secure HTTPS connections
- Authentication required at API Gateway level
- Data encryption at rest and in transit
- Audit logging through CloudWatch

## Scalability Features
- CDN for global content delivery
- Serverless architecture with auto-scaling
- Queue-based processing for high throughput
- Managed services for operational efficiency
