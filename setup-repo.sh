#!/bin/bash

# Email Platform Architecture Repository Setup Script
# Run this script from the email-platform-diagrams directory

echo "Setting up Email Platform Architecture repository..."

# Initialize git repository
git init

# Add remote origin (replace with actual repository URL)
git remote add origin https://github.com/onesphereai/email-platform-architecture.git

# Create .gitignore file
cat > .gitignore << EOF
# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.temp
*~

# Log files
*.log

# Node modules (if any)
node_modules/

# Environment files
.env
.env.local
.env.production
EOF

# Create README.md
cat > README.md << EOF
# Email Platform Architecture

Comprehensive architecture documentation and diagrams for the Email Platform - a self-service email marketing solution for B2B customers.

## 📋 Documentation

- **[Architecture Documentation](Email_Platform_Architecture_Documentation.md)** - Complete technical architecture
- **[API Specification](Email_Platform_API_Specification.md)** - REST API documentation
- **[Documentation Summary](Email_Platform_Documentation_Summary.md)** - Executive summary

## 🎨 Architecture Diagrams

### High-Level Architecture
- [Clean High Level Architecture](generated-diagrams/16_clean_high_level_architecture.png)
- [Original High Level Architecture](generated-diagrams/01_high_level_architecture.png)

### Detailed Component Views
- [Detailed Component Architecture](generated-diagrams/02_detailed_component_architecture.png)
- [Clean Multi-Tenant Architecture](generated-diagrams/18_clean_multitenant_architecture.png)

### Security & Compliance
- [Clean Security Architecture](generated-diagrams/19_clean_security_architecture.png)
- [Original Security Architecture](generated-diagrams/05_security_architecture.png)

### Sequence Diagrams
- [Campaign Creation Sequence](generated-diagrams/10_campaign_creation_sequence.png)
- [Email Sending Process](generated-diagrams/11_email_sending_sequence.png)
- [API Integration Sequence](generated-diagrams/12_api_integration_sequence.png)
- [Email Delivery & Analytics](generated-diagrams/13_email_delivery_analytics_sequence.png)
- [Authentication Sequence](generated-diagrams/14_authentication_sequence.png)
- [Error Handling Sequence](generated-diagrams/15_error_handling_sequence.png)

### Process Flows
- [Clean Campaign Sequence](generated-diagrams/17_clean_campaign_sequence.png)
- [Clean API Integration](generated-diagrams/20_clean_api_integration.png)
- [CI/CD Pipeline](generated-diagrams/06_cicd_pipeline_architecture.png)

### Monitoring & Operations
- [Clean Monitoring & Observability](generated-diagrams/21_clean_monitoring_observability.png)
- [Original Monitoring Architecture](generated-diagrams/08_monitoring_observability.png)

## 🏗️ Architecture Highlights

- **Multi-tenant silo model** with complete data isolation
- **Serverless architecture** using AWS Lambda, API Gateway, DynamoDB
- **Single table design** optimized for DynamoDB access patterns
- **Comprehensive security** with multiple authentication methods
- **Email authentication** with SPF, DKIM, DMARC
- **Real-time analytics** with OpenSearch Serverless
- **Scalable processing** with SQS/SNS message queuing

## 🔧 Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Angular, TypeScript | User interface |
| API Gateway | AWS API Gateway | Request routing |
| Authentication | AWS Cognito | SAML SSO |
| Backend | Node.js, Lambda | Business logic |
| Database | DynamoDB | Data storage |
| File Storage | S3 | Templates and assets |
| Email Service | Amazon SES | Email delivery |
| Message Queue | SQS, SNS | Async processing |
| Analytics | OpenSearch | Search and analytics |
| Monitoring | CloudWatch, X-Ray | Observability |
| CI/CD | Jenkins, Serverless | Deployment |

## 📊 Implementation Phases

### Phase 1: MVP (Q1 2024)
- Basic campaign creation and sending
- Simple drag-and-drop builder
- SAML authentication
- Basic reporting

### Phase 2: Enhanced Features (Q2 2024)
- Advanced template management
- A/B testing capabilities
- Enhanced analytics
- API access

### Phase 3: Enterprise Features (Q3 2024)
- Marketing automation
- Advanced segmentation
- CRM integrations
- Multi-brand support

### Phase 4: AI and Advanced Analytics (Q4 2024)
- AI-powered optimization
- Advanced personalization
- Cross-channel orchestration
- Enterprise governance

## 🔒 Compliance & Security

- **GDPR, CCPA compliance** with data sovereignty
- **Email standards compliance** (CAN-SPAM, Australian Spam Act)
- **Enterprise security** with encryption at rest and in transit
- **Comprehensive monitoring** with audit trails
- **Rate limiting and throttling** for abuse prevention

## 📞 Support

For questions about this architecture:
- **Technical Documentation**: See individual markdown files
- **Architecture Questions**: Contact the development team
- **Implementation Support**: Refer to the API specification

## 📄 License

This documentation is proprietary to OneSphere AI and Message Centre.

---

**Generated**: $(date)
**Version**: 1.0.0
**Last Updated**: $(date)
EOF

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Email Platform Architecture Documentation

- Complete architecture documentation with technical specifications
- Comprehensive REST API documentation with examples
- 21 architecture diagrams covering all system aspects
- Clean and detailed sequence diagrams for major workflows
- Multi-tenant data architecture with security considerations
- CI/CD pipeline and monitoring strategies
- Implementation roadmap and technology stack details"

echo "Repository initialized and files committed locally."
echo ""
echo "Next steps:"
echo "1. Create the repository at: https://github.com/onesphereai/email-platform-architecture"
echo "2. Run: git push -u origin main"
echo ""
echo "Repository contents:"
echo "- Architecture documentation (3 markdown files)"
echo "- 21 architecture diagrams (PNG files)"
echo "- Setup script and README"
EOF

chmod +x setup-repo.sh
