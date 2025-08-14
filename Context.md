# Context
- Building a new platform called Email Platform (Self service) to be hosted via Message Centre UI.
- Platform will provide self service capability for user/clients to send bulk emails 
- More list of features are listed in MVP.txt file.

- Platform will be hosted in AWS.
- Platform will be built using Angular for the frontend and TypeScript for the backend.
# Technology Stack
- Frontend: Angular
- Backend: TypeScript
- Hosting: AWS
- Database: DynamoDB (Single Table Design)
- Authentication: AWS Cognito (SAML) Cognito to act as SP.
- Email Service: AWS SES (Simple Email Service)
- Monitoring: AWS CloudWatch
- Logging: AWS CloudWatch Logs
- Jenkins (Onpremise)
- IaC (Serverless Framework)
- OpenSearch Serverless (MC) for analytics
- DKIM, DMARC, SPF validation
- Rest APIs.
- Lambdas 
- SQS , SNS.

Integration with External Reporting (Other platforms like Messaging API, Email2SMS) they push data to Message Centre hosted External Reporting via API call of the external reporting Email platform to do the same.

# Design Considerations
- Multi-Tenancy
- Silo Model.
- Scalability
- Security
- Performance
- Cost Efficiency
- User Experience
- Compliance with email standards and regulations
- Monitoring and Logging
- AWS Services Quota consideration.
# Deployment
- Deployment will be managed using Jenkins for CI/CD.
- Infrastructure as Code (IaC) will be implemented using Serverless Framework.
- AWS CloudFormation will be used for resource provisioning.
- Version control will be managed using Bitbucket
- Code reviews and pull requests will be enforced for quality assurance.
- Automated testing will be integrated into the CI/CD pipeline.
- Rollback strategies will be in place for deployment failures.
- Staging and production environments will be maintained separately.
- Blue/Green deployments will be considered for zero downtime.
- Monitoring and alerting will be set up to track deployment health and performance.
- Backup and disaster recovery plans will be established.
- Documentation will be maintained for deployment processes and configurations.
# Security
- AWS Cognito will be used for user authentication and authorization.
- SAML integration for Single Sign-On (SSO) capabilities.
- Data encryption at rest and in transit using AWS KMS.
- IAM roles and policies will be defined for access control.
- Regular security audits and vulnerability assessments will be conducted.
- Logging and monitoring will be implemented to detect and respond to security incidents.
- Compliance with GDPR, CCPA, and other relevant regulations will be ensured.
- Email security measures such as DKIM, DMARC, and SPF will be implemented
- Regular updates and patches will be applied to all components.


# Performance
- Load testing will be conducted to ensure the platform can handle expected traffic.
- Caching strategies will be implemented to improve response times.
- Database optimization techniques will be applied to enhance performance.
- Asynchronous processing will be utilized for bulk email sending to avoid blocking operations.
- Content Delivery Network (CDN) may be considered for static assets.
- Cloud Observability Platform to be used for monitoring and observablility.
- Performance metrics will be collected and analyzed to identify bottlenecks.

# Segregation
- Email Platform will be divided into two core components
- Email Platform UI / Backend
- Email API to provide standalone capability.
- Email Platform backend will not store core email sending configurations.
- Email API expose APIs protected by x-api-key, oAuth and mTLS.
- x-api-key will be required at all times.
- oAuth will be optional as is the case with mTLS.