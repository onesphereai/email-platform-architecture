# Email Platform Architecture

Comprehensive architecture documentation and diagrams for the Email Platform - a standalone email marketing solution with Message Centre integration.

## 📋 Executive Documentation

- **[Standalone Architecture Documentation](Email_Platform_Standalone_Architecture.md)** - Complete standalone architecture
- **[API Specification](Email_Platform_API_Specification.md)** - REST API documentation
- **[Documentation Summary](Email_Platform_Documentation_Summary.md)** - Executive summary

## 🏗️ Architecture Views

The architecture is organized into five comprehensive views, each focusing on specific aspects of the system:

### 🔧 [Development View](Architecture/Development-View/)
**Software components, APIs, and development processes**
- API specifications and integration patterns
- Component architecture and dependencies
- Business process workflows and sequences
- CI/CD pipeline and development practices

### 🚀 [Deployment View](Architecture/Deployment-View/)
**Infrastructure, runtime environment, and operations**
- Infrastructure architecture and AWS services
- Deployment strategies and environment management
- Monitoring, observability, and alerting
- Error handling and recovery procedures

### 🔒 [Security View](Architecture/Security-View/)
**Security architecture, authentication, and compliance**
- Multi-layered security architecture
- Authentication and authorization mechanisms
- Data protection and encryption strategies
- Compliance frameworks and governance

### 📊 [Data View](Architecture/Data-View/)
**Data architecture, storage, and analytics**
- Multi-tenant data isolation patterns
- Database design and access patterns
- Analytics and reporting architecture
- Data governance and privacy controls

### 💰 [Cost View](Architecture/Cost-View/)
**Cost analysis, optimization, and financial planning**
- Comprehensive cost breakdown and analysis
- Cost optimization strategies and recommendations
- Pricing models and revenue projections
- Financial planning and ROI analysis

## 🎨 Standalone Architecture Diagrams

### High-Level Architecture
- [Standalone High Level Architecture](generated-diagrams/01_high_level_architecture.png) | [Flow Description](Architecture/Deployment-View/01_high_level_architecture_flow.md)

### Integration & Component Views
- [Integration Flow](generated-diagrams/02_integration_flow.png) | [Flow Description](Architecture/Development-View/02_integration_flow_description.md)
- [Detailed Component Architecture](generated-diagrams/03_detailed_component_architecture.png) | [Flow Description](Architecture/Development-View/03_detailed_component_architecture_flow.md)

### Process Flows
- [Callback Flow](generated-diagrams/04_callback_flow.png) | [Flow Description](Architecture/Development-View/04_callback_flow_description.md)

### Security Architecture
- [Security Architecture](generated-diagrams/05_security_architecture.png) | [Flow Description](Architecture/Security-View/05_security_architecture_flow.md)

### Data Flow Diagrams
- [Transaction Status Flow](generated-diagrams/06_transaction_status_flow.png) | [Flow Description](Architecture/Data-View/06_transaction_status_flow_description.md)
- [Message Status Flow](generated-diagrams/07_message_status_flow.png) | [Flow Description](Architecture/Data-View/07_message_status_flow_description.md)

## 🏗️ Standalone Architecture Highlights

### Key Architectural Decisions
- **Standalone Email Platform**: Independent service with dedicated APIs and storage
- **Message Centre Integration**: Wrapper APIs for seamless integration
- **Presigned URL Strategy**: Secure file uploads directly to S3
- **Hierarchical Data Model**: Transaction → Batch → Message structure
- **Event-Driven Processing**: Step Functions and EventBridge orchestration

### Technology Stack
| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Angular, TypeScript | Message Centre UI |
| API Gateway | AWS API Gateway | Request routing & security |
| Authentication | API Keys, OAuth 2.0, mTLS | Multi-layer security |
| Backend | Node.js, Lambda | Serverless processing |
| Orchestration | Step Functions, EventBridge | Workflow management |
| Database | DynamoDB | Scalable NoSQL storage |
| File Storage | S3 | Templates and CSV files |
| Email Service | Amazon SES | Email delivery |
| Analytics | OpenSearch Serverless | Real-time analytics |
| Monitoring | CloudWatch, X-Ray | Observability |

### Processing Pipeline
1. **File Upload**: Templates and CSV files via presigned URLs
2. **File Processing**: Step Functions split CSV into batches and messages
3. **Scheduling**: Optional EventBridge scheduling for future delivery
4. **Email Delivery**: Step Functions orchestrate SES email sending
5. **Status Tracking**: Real-time status updates and callback notifications
6. **Analytics**: OpenSearch for engagement tracking and reporting

### Data Architecture
```
Transaction (Campaign Level)
├── Status: ACCEPT → PROCESSING → SCHEDULED/READY_TO_SEND → SENT → COMPLETED
├── Batch 1 (File Chunk)
│   ├── Message 1 (Individual Email)
│   ├── Message 2 (Individual Email)
│   └── ...
├── Batch 2 (File Chunk)
│   └── ...
└── Analytics Data (OpenSearch)
```

### Security Features
- **Multi-layer Authentication**: API Keys (mandatory), OAuth 2.0 (optional), mTLS (optional)
- **Data Encryption**: At rest and in transit with KMS
- **Access Control**: IAM roles and fine-grained permissions
- **Compliance**: GDPR, CCPA, CAN-SPAM, Australian Spam Act

## 📊 Implementation Phases

### Phase 1: Core Standalone Platform (Q1 2024)
- Standalone Email API development
- File processing pipeline with Step Functions
- Basic template management via presigned URLs
- Transaction and message status tracking

### Phase 2: Enhanced Integration (Q2 2024)
- Message Centre wrapper API integration
- Scheduling capabilities with EventBridge
- Callback system for status notifications
- Enhanced security with multiple auth methods

### Phase 3: Advanced Features (Q3 2024)
- Real-time analytics with OpenSearch
- Advanced error handling and retry logic
- Performance optimization and scaling
- Comprehensive monitoring and alerting

### Phase 4: Enterprise Features (Q4 2024)
- AI-powered optimization and insights
- Advanced personalization capabilities
- Multi-region deployment
- Enterprise governance and compliance

## 🔒 Compliance & Security

### Email Compliance
- **CAN-SPAM Act**: US email marketing regulations
- **GDPR**: European data protection compliance
- **CCPA**: California privacy compliance
- **Australian Spam Act**: Australian email regulations
- **CASL**: Canadian Anti-Spam Legislation

### Security Standards
- **SOC 2 Type II**: Security and availability controls
- **ISO 27001**: Information security management
- **Multi-layer Security**: WAF, API Gateway, IAM, KMS
- **Audit Logging**: Comprehensive access and activity logs

### Data Protection
- **Encryption**: AES-256 encryption at rest and TLS 1.2+ in transit
- **Access Control**: Role-based and scope-based permissions
- **Data Isolation**: Multi-tenant data separation
- **Backup & Recovery**: Automated backup with point-in-time recovery

## 🔧 Development Tools

### Documentation Generation
- **Confluence HTML**: Run `python3 md_to_confluence.py` to generate Confluence-ready HTML files
- **Diagram Generation**: AWS architecture diagrams using Python diagrams package
- **Version Control**: Git-based documentation versioning

### Repository Structure
```
├── Email_Platform_Standalone_Architecture.md    # Main architecture doc
├── Email_Platform_API_Specification.md          # API documentation
├── Email_Platform_Documentation_Summary.md      # Executive summary
├── README.md                                     # This file
├── generated-diagrams/                          # Architecture diagrams (01-07)
├── Architecture/                                # Detailed architecture views
│   ├── Development-View/                       # Development architecture
│   ├── Deployment-View/                        # Infrastructure architecture
│   ├── Security-View/                          # Security architecture
│   ├── Data-View/                              # Data architecture
│   └── Cost-View/                              # Cost analysis
├── confluence-html/                            # Confluence-ready HTML files
└── md_to_confluence.py                         # HTML conversion script
```

## 📞 Support

For questions about this architecture:
- **Technical Documentation**: See individual markdown files in Architecture/ folders
- **Standalone Architecture**: Refer to Email_Platform_Standalone_Architecture.md
- **API Integration**: Contact the development team for integration support
- **Security Questions**: Refer to Security View documentation

## 📄 License

This documentation is proprietary to OneSphere AI and Message Centre.

---

**Generated**: August 17, 2024  
**Version**: 2.0.0 (Standalone Architecture - Cleaned)  
**Last Updated**: August 17, 2024  
**Architecture Type**: Standalone Email Platform with Message Centre Integration
