# High Level Architecture Flow

## Overview
This diagram illustrates the standalone Email Platform architecture with clear separation between Message Centre and Email Platform services.

## Components

### Message Centre Layer
- **Web UI**: User interface for campaign management
- **Wrapper API**: Orchestrates interactions with Email Platform APIs

### Email Platform (Standalone)
- **Email API**: Core email processing service
- **File Storage**: S3 buckets for templates and CSV files
- **Processing**: Step Functions for file processing and EventBridge for scheduling
- **Data Layer**: DynamoDB for message storage and OpenSearch for analytics
- **Email Delivery**: Amazon SES for email delivery and Step Functions for send pipeline

## Flow Description

### 1. User Interaction
- Users interact with Message Centre Web UI
- Web UI communicates with Message Centre Wrapper API

### 2. Email Platform Integration
- Message Centre API integrates with standalone Email Platform API
- Clear API boundaries between systems

### 3. File Management
- Templates stored in dedicated S3 bucket
- CSV recipient files stored in separate S3 bucket
- Presigned URLs used for secure file uploads

### 4. Processing Pipeline
- File Processing Step Functions handle CSV splitting and message creation
- EventBridge manages scheduled email delivery
- DynamoDB stores all message data and status information

### 5. Email Delivery
- Send Pipeline Step Functions orchestrate email delivery
- Amazon SES handles actual email sending
- Recipients receive emails

### 6. Analytics & Monitoring
- DynamoDB streams data to OpenSearch for analytics
- SES events (opens, clicks, bounces) flow to OpenSearch
- Real-time analytics and reporting available

## Key Benefits

### Separation of Concerns
- Email Platform operates independently
- Message Centre focuses on user experience
- Clear API contracts between systems

### Scalability
- Independent scaling of each component
- Serverless architecture auto-scales with demand
- Efficient resource utilization

### Maintainability
- Modular architecture
- Independent deployment cycles
- Clear service boundaries

### Security
- Isolated data storage
- Secure file upload via presigned URLs
- Comprehensive access controls

## Technology Stack
- **Frontend**: Angular/TypeScript (Message Centre)
- **APIs**: Node.js Lambda functions
- **Storage**: S3, DynamoDB, OpenSearch
- **Processing**: Step Functions, EventBridge
- **Email**: Amazon SES
- **Security**: API Gateway, IAM, KMS
