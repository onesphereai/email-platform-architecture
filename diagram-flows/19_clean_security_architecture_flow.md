# Security Architecture - Flow Description

**Diagram**: `19_clean_security_architecture.png`

## Overview
This diagram illustrates the comprehensive security architecture of the Email Platform, showing multiple layers of security controls from edge protection to data encryption and monitoring.

## Security Layer Flow Analysis

| Layer | Component | Security Function | Protection Type | Flow Direction |
|-------|-----------|-------------------|-----------------|----------------|
| Edge Security | WAF | Web application firewall | Attack prevention | User → WAF |
| Edge Security | Shield | DDoS protection | Traffic filtering | WAF → Shield |
| Edge Security | CloudFront | SSL termination, geo-blocking | Content delivery security | Shield → CloudFront |
| API Security | API Gateway | Request validation, rate limiting | API protection | CloudFront → API Gateway |
| API Security | Rate Limiting | Throttling and abuse prevention | Traffic control | Within API Gateway |
| Authentication | Cognito | User authentication | Identity verification | API Gateway → Cognito |
| Authentication | SAML IdP | Enterprise identity provider | Federated authentication | Cognito ↔ SAML IdP |
| Authentication | JWT Validator | Token validation | Session security | Cognito → JWT Validator |
| Data Protection | KMS | Key management | Encryption key security | → Encrypted Services |
| Data Protection | Encrypted DynamoDB | Database encryption | Data at rest security | KMS → DynamoDB |
| Data Protection | Encrypted S3 | File storage encryption | File security | KMS → S3 |
| Email Security | SES | Email delivery | Email authentication | JWT Validator → SES |
| Email Security | SPF/DKIM/DMARC | Email authentication | Email integrity | SES → Email Auth |
| Monitoring | CloudTrail | API audit logging | Compliance tracking | All Services → CloudTrail |
| Monitoring | GuardDuty | Threat detection | Security monitoring | Services → GuardDuty |

## Security Control Flow

### Request Security Flow
```
User Request → WAF (Filter) → Shield (DDoS Protection) → CloudFront (SSL/Geo) → 
API Gateway (Validation) → Rate Limiting → Authentication → Authorized Access
```

### Authentication Flow
```
User → API Gateway → Cognito → SAML IdP → Credential Validation → 
JWT Token Generation → Token Validation → Authorized Session
```

### Data Protection Flow
```
Application Request → JWT Validation → KMS Key Retrieval → 
Encrypted Data Access → Decryption → Authorized Data Access
```

### Email Security Flow
```
Email Request → Authentication → SES Processing → SPF/DKIM/DMARC Validation → 
Secure Email Delivery
```

### Monitoring Flow
```
All Security Events → CloudTrail (Audit) → GuardDuty (Analysis) → 
Security Alerts → Incident Response
```

## Security Controls by Layer

### Edge Security Layer

#### AWS WAF Configuration
```json
{
  "webAcl": {
    "name": "EmailPlatformWAF",
    "rules": [
      {
        "name": "SQLInjectionRule",
        "priority": 1,
        "statement": {
          "sqliMatchStatement": {
            "fieldToMatch": {
              "allQueryArguments": {}
            }
          }
        },
        "action": {
          "block": {}
        }
      },
      {
        "name": "XSSRule",
        "priority": 2,
        "statement": {
          "xssMatchStatement": {
            "fieldToMatch": {
              "body": {}
            }
          }
        },
        "action": {
          "block": {}
        }
      },
      {
        "name": "RateLimitRule",
        "priority": 3,
        "statement": {
          "rateBasedStatement": {
            "limit": 2000,
            "aggregateKeyType": "IP"
          }
        },
        "action": {
          "block": {}
        }
      }
    ]
  }
}
```

#### AWS Shield Advanced Features
- **DDoS Protection**: Automatic detection and mitigation
- **Attack Notifications**: Real-time attack alerts
- **Cost Protection**: DDoS-related cost protection
- **24/7 Support**: Access to DDoS Response Team

#### CloudFront Security Features
```json
{
  "distribution": {
    "viewerProtocolPolicy": "redirect-to-https",
    "allowedMethods": ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"],
    "geoRestriction": {
      "restrictionType": "blacklist",
      "locations": ["CN", "RU", "KP"]
    },
    "webAclId": "arn:aws:wafv2:us-east-1:account:global/webacl/EmailPlatformWAF"
  }
}
```

### API Security Layer

#### API Gateway Security Configuration
```json
{
  "apiGateway": {
    "throttle": {
      "rateLimit": 1000,
      "burstLimit": 2000
    },
    "requestValidation": {
      "validateRequestBody": true,
      "validateRequestParameters": true
    },
    "cors": {
      "allowOrigins": ["https://emailplatform.messagecentre.com"],
      "allowMethods": ["GET", "POST", "PUT", "DELETE"],
      "allowHeaders": ["Content-Type", "Authorization", "x-api-key"]
    },
    "authorizers": [
      {
        "name": "CognitoAuthorizer",
        "type": "COGNITO_USER_POOLS",
        "providerARNs": ["arn:aws:cognito-idp:region:account:userpool/pool-id"]
      }
    ]
  }
}
```

#### Rate Limiting Strategy
| Client Type | Rate Limit | Burst Limit | Time Window |
|-------------|------------|-------------|-------------|
| Web UI | 100 req/min | 200 req/min | 1 minute |
| API Client | 1000 req/hour | 100 req/min | 1 hour |
| Premium API | 10000 req/hour | 500 req/min | 1 hour |
| Internal Services | No limit | 1000 req/min | 1 minute |

### Authentication Layer

#### Cognito User Pool Configuration
```json
{
  "userPool": {
    "passwordPolicy": {
      "minimumLength": 12,
      "requireUppercase": true,
      "requireLowercase": true,
      "requireNumbers": true,
      "requireSymbols": true
    },
    "mfaConfiguration": "OPTIONAL",
    "accountRecoverySetting": {
      "recoveryMechanisms": [
        {
          "name": "verified_email",
          "priority": 1
        }
      ]
    },
    "deviceConfiguration": {
      "challengeRequiredOnNewDevice": true,
      "deviceOnlyRememberedOnUserPrompt": false
    }
  }
}
```

#### SAML Identity Provider Configuration
```xml
<EntityDescriptor xmlns="urn:oasis:names:tc:SAML:2.0:metadata">
  <IDPSSODescriptor>
    <KeyDescriptor use="signing">
      <KeyInfo>
        <X509Data>
          <X509Certificate>...</X509Certificate>
        </X509Data>
      </KeyInfo>
    </KeyDescriptor>
    <SingleSignOnService 
      Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
      Location="https://idp.company.com/saml/sso"/>
  </IDPSSODescriptor>
</EntityDescriptor>
```

#### JWT Token Validation
```javascript
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');

const client = jwksClient({
  jwksUri: 'https://cognito-idp.region.amazonaws.com/userPoolId/.well-known/jwks.json'
});

function validateJWT(token) {
  return new Promise((resolve, reject) => {
    jwt.verify(token, getKey, {
      audience: 'clientId',
      issuer: 'https://cognito-idp.region.amazonaws.com/userPoolId',
      algorithms: ['RS256']
    }, (err, decoded) => {
      if (err) {
        reject(err);
      } else {
        resolve(decoded);
      }
    });
  });
}

function getKey(header, callback) {
  client.getSigningKey(header.kid, (err, key) => {
    const signingKey = key.publicKey || key.rsaPublicKey;
    callback(null, signingKey);
  });
}
```

### Data Protection Layer

#### AWS KMS Key Management
```json
{
  "keyPolicy": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "Enable IAM User Permissions",
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::account:root"
        },
        "Action": "kms:*",
        "Resource": "*"
      },
      {
        "Sid": "Allow use of the key for Email Platform",
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::account:role/EmailPlatformRole"
        },
        "Action": [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ],
        "Resource": "*"
      }
    ]
  }
}
```

#### DynamoDB Encryption Configuration
```json
{
  "table": {
    "tableName": "EmailPlatform",
    "sseSpecification": {
      "enabled": true,
      "sseType": "KMS",
      "kmsMasterKeyId": "arn:aws:kms:region:account:key/key-id"
    },
    "pointInTimeRecoverySpecification": {
      "pointInTimeRecoveryEnabled": true
    }
  }
}
```

#### S3 Encryption Configuration
```json
{
  "bucket": {
    "bucketName": "email-platform-storage",
    "serverSideEncryptionConfiguration": {
      "rules": [
        {
          "applyServerSideEncryptionByDefault": {
            "sseAlgorithm": "aws:kms",
            "kmsMasterKeyID": "arn:aws:kms:region:account:key/key-id"
          },
          "bucketKeyEnabled": true
        }
      ]
    },
    "publicAccessBlockConfiguration": {
      "blockPublicAcls": true,
      "blockPublicPolicy": true,
      "ignorePublicAcls": true,
      "restrictPublicBuckets": true
    }
  }
}
```

### Email Security Layer

#### Amazon SES Security Configuration
```json
{
  "sesConfiguration": {
    "identityPolicies": {
      "emailIdentity": "company.com",
      "policy": {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Effect": "Allow",
            "Principal": {
              "AWS": "arn:aws:iam::account:role/EmailPlatformRole"
            },
            "Action": [
              "ses:SendEmail",
              "ses:SendRawEmail"
            ],
            "Resource": "arn:aws:ses:region:account:identity/company.com"
          }
        ]
      }
    },
    "configurationSet": {
      "name": "EmailPlatformConfigSet",
      "eventDestinations": [
        {
          "name": "CloudWatchDestination",
          "enabled": true,
          "matchingEventTypes": [
            "send",
            "reject",
            "bounce",
            "complaint",
            "delivery"
          ]
        }
      ]
    }
  }
}
```

#### Email Authentication Records
```dns
; SPF Record
company.com. IN TXT "v=spf1 include:amazonses.com ~all"

; DKIM Records (generated by SES)
selector1._domainkey.company.com. IN CNAME selector1.dkim.amazonses.com
selector2._domainkey.company.com. IN CNAME selector2.dkim.amazonses.com

; DMARC Record
_dmarc.company.com. IN TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@company.com; ruf=mailto:dmarc@company.com; sp=quarantine; adkim=r; aspf=r;"
```

### Monitoring Layer

#### CloudTrail Configuration
```json
{
  "trail": {
    "name": "EmailPlatformAuditTrail",
    "s3BucketName": "email-platform-audit-logs",
    "includeGlobalServiceEvents": true,
    "isMultiRegionTrail": true,
    "enableLogFileValidation": true,
    "eventSelectors": [
      {
        "readWriteType": "All",
        "includeManagementEvents": true,
        "dataResources": [
          {
            "type": "AWS::DynamoDB::Table",
            "values": ["arn:aws:dynamodb:*:*:table/EmailPlatform"]
          },
          {
            "type": "AWS::S3::Object",
            "values": ["arn:aws:s3:::email-platform-storage/*"]
          }
        ]
      }
    ]
  }
}
```

#### GuardDuty Configuration
```json
{
  "detector": {
    "enable": true,
    "findingPublishingFrequency": "FIFTEEN_MINUTES",
    "dataSources": {
      "s3Logs": {
        "enable": true
      },
      "kubernetesAuditLogs": {
        "enable": false
      },
      "malwareProtection": {
        "scanEc2InstanceWithFindings": {
          "ebsVolumes": true
        }
      }
    }
  }
}
```

## Security Incident Response

### Incident Classification
| Severity | Description | Response Time | Escalation |
|----------|-------------|---------------|------------|
| Critical | Data breach, system compromise | Immediate | CISO, Legal |
| High | Service disruption, security vulnerability | 1 hour | Security Team |
| Medium | Policy violation, suspicious activity | 4 hours | Operations Team |
| Low | Minor security event | 24 hours | Monitoring Team |

### Automated Response Actions
```javascript
// Automated security response
const securityResponse = {
  suspiciousActivity: {
    action: 'blockIP',
    duration: '1hour',
    notification: ['security-team@company.com']
  },
  
  dataExfiltration: {
    action: 'isolateAccount',
    duration: 'indefinite',
    notification: ['ciso@company.com', 'legal@company.com']
  },
  
  bruteForceAttack: {
    action: 'rateLimitIP',
    duration: '24hours',
    notification: ['ops-team@company.com']
  }
};
```

### Security Metrics and KPIs
- **Mean Time to Detection (MTTD)**: Average time to detect security incidents
- **Mean Time to Response (MTTR)**: Average time to respond to incidents
- **False Positive Rate**: Percentage of false security alerts
- **Security Coverage**: Percentage of assets with security monitoring
- **Compliance Score**: Adherence to security policies and standards

## Compliance and Governance

### Regulatory Compliance
- **GDPR**: Data protection and privacy rights
- **CCPA**: California Consumer Privacy Act compliance
- **SOC 2**: Security and availability controls
- **ISO 27001**: Information security management

### Security Policies
```json
{
  "securityPolicies": {
    "passwordPolicy": {
      "minLength": 12,
      "complexity": "high",
      "rotation": "90days",
      "history": 12
    },
    "accessPolicy": {
      "principleOfLeastPrivilege": true,
      "regularAccessReview": "quarterly",
      "privilegedAccessMonitoring": true
    },
    "dataClassification": {
      "public": "no_encryption",
      "internal": "encryption_at_rest",
      "confidential": "encryption_at_rest_and_transit",
      "restricted": "encryption_plus_access_controls"
    }
  }
}
```

### Audit and Compliance Reporting
```javascript
// Generate compliance report
async function generateComplianceReport(period) {
  const report = {
    period: period,
    securityEvents: await getSecurityEvents(period),
    accessReviews: await getAccessReviews(period),
    vulnerabilityScans: await getVulnerabilityScans(period),
    complianceScore: await calculateComplianceScore(period),
    recommendations: await getSecurityRecommendations()
  };
  
  return report;
}
```

## Security Best Practices

### Defense in Depth
- **Multiple Security Layers**: Overlapping security controls
- **Fail-Safe Defaults**: Secure by default configuration
- **Principle of Least Privilege**: Minimal required access
- **Zero Trust Architecture**: Never trust, always verify

### Continuous Security
- **Security Automation**: Automated security testing and response
- **Continuous Monitoring**: Real-time security monitoring
- **Regular Assessments**: Periodic security assessments
- **Security Training**: Regular security awareness training

### Incident Prevention
- **Threat Modeling**: Identify and mitigate threats
- **Vulnerability Management**: Regular vulnerability scanning
- **Penetration Testing**: Regular security testing
- **Security Code Review**: Secure coding practices
