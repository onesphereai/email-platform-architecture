# Client Domain Authentication Setup with Amazon SES

## Overview
This document explains how to handle SPF, DKIM, and DMARC authentication when clients bring their own domains to use with our Email Platform. This setup ensures proper email deliverability and authentication while maintaining client domain ownership.

## Architecture Pattern: Client-Owned Domain with SES

### High-Level Flow
```
Client Domain (client.com) 
    ↓ DNS Configuration
Amazon SES (Email Platform)
    ↓ Authenticated Emails
Recipients (Inbox Delivery)
```

### Key Components
1. **Domain Verification**: Client proves domain ownership
2. **DKIM Setup**: SES generates DKIM keys for client domain
3. **Custom MAIL FROM**: Optional subdomain for bounce handling
4. **SPF Configuration**: Authorize SES to send from client domain
5. **DMARC Policy**: Define authentication requirements

## Step-by-Step Setup Process

### Phase 1: Domain Verification in SES

#### 1.1 Client Onboarding API Flow
```javascript
// Email Platform API - Domain Registration
POST /api/v1/domains
{
  "client_id": "client-123",
  "domain": "client.com",
  "contact_email": "admin@client.com",
  "mail_from_subdomain": "mail.client.com" // Optional
}

// Response
{
  "domain_id": "domain-456",
  "verification_token": "abc123def456",
  "dns_records": [
    {
      "type": "TXT",
      "name": "_amazonses.client.com",
      "value": "abc123def456",
      "purpose": "Domain Verification"
    }
  ],
  "status": "pending_verification"
}
```

#### 1.2 SES Domain Identity Creation
```javascript
// Backend Lambda Function
const createDomainIdentity = async (domain, clientId) => {
  // Create domain identity in SES
  const sesResponse = await ses.putIdentityVerificationAttributes({
    Identity: domain
  }).promise();
  
  // Store domain mapping in DynamoDB
  await dynamodb.putItem({
    TableName: 'ClientDomains',
    Item: {
      PK: `CLIENT#${clientId}`,
      SK: `DOMAIN#${domain}`,
      domain: domain,
      ses_identity: domain,
      status: 'pending_verification',
      created_at: new Date().toISOString()
    }
  }).promise();
  
  return sesResponse;
};
```

### Phase 2: DKIM Configuration

#### 2.1 Enable DKIM for Client Domain
```javascript
// Enable DKIM signing for the domain
const enableDKIM = async (domain) => {
  // Enable DKIM
  await ses.putIdentityDkimAttributes({
    Identity: domain,
    DkimEnabled: true
  }).promise();
  
  // Get DKIM tokens for DNS setup
  const dkimTokens = await ses.getIdentityDkimAttributes({
    Identities: [domain]
  }).promise();
  
  return dkimTokens.DkimAttributes[domain].DkimTokens;
};
```

#### 2.2 DKIM DNS Records for Client
```javascript
// Generate DKIM DNS records for client
const generateDKIMRecords = (domain, dkimTokens) => {
  return dkimTokens.map(token => ({
    type: 'CNAME',
    name: `${token}._domainkey.${domain}`,
    value: `${token}.dkim.amazonses.com`,
    purpose: 'DKIM Authentication'
  }));
};
```

### Phase 3: Custom MAIL FROM Domain (Optional but Recommended)

#### 3.1 Configure Custom MAIL FROM
```javascript
// Set up custom MAIL FROM domain
const setupCustomMailFrom = async (domain, mailFromDomain) => {
  await ses.setIdentityMailFromDomain({
    Identity: domain,
    MailFromDomain: mailFromDomain,
    BehaviorOnMXFailure: 'UseDefaultValue' // Fallback to SES default
  }).promise();
  
  // Return required DNS records
  return [
    {
      type: 'MX',
      name: mailFromDomain,
      value: `10 feedback-smtp.${AWS_REGION}.amazonses.com`,
      purpose: 'Bounce/Complaint Handling'
    },
    {
      type: 'TXT',
      name: mailFromDomain,
      value: `v=spf1 include:amazonses.com ~all`,
      purpose: 'SPF Authorization'
    }
  ];
};
```

### Phase 4: Complete DNS Configuration

#### 4.1 Required DNS Records Summary
```yaml
# Domain Verification
_amazonses.client.com TXT "verification-token"

# DKIM Authentication (3 records)
token1._domainkey.client.com CNAME token1.dkim.amazonses.com
token2._domainkey.client.com CNAME token2.dkim.amazonses.com  
token3._domainkey.client.com CNAME token3.dkim.amazonses.com

# Custom MAIL FROM (if used)
mail.client.com MX 10 feedback-smtp.ap-southeast-2.amazonses.com
mail.client.com TXT "v=spf1 include:amazonses.com ~all"

# SPF for main domain (if not using custom MAIL FROM)
client.com TXT "v=spf1 include:amazonses.com ~all"

# DMARC Policy
_dmarc.client.com TXT "v=DMARC1; p=quarantine; rua=mailto:dmarc@client.com"
```

#### 4.2 Client DNS Setup Instructions
```javascript
// API Response with DNS Instructions
const getDNSInstructions = (domain, dkimTokens, mailFromDomain) => {
  return {
    domain: domain,
    instructions: "Add the following DNS records to your domain:",
    records: [
      // Domain verification
      {
        type: "TXT",
        name: `_amazonses.${domain}`,
        value: verificationToken,
        ttl: 1800,
        priority: "HIGH",
        description: "Required for domain verification"
      },
      
      // DKIM records
      ...dkimTokens.map(token => ({
        type: "CNAME",
        name: `${token}._domainkey.${domain}`,
        value: `${token}.dkim.amazonses.com`,
        ttl: 1800,
        priority: "HIGH",
        description: "Required for DKIM authentication"
      })),
      
      // Custom MAIL FROM (if configured)
      ...(mailFromDomain ? [
        {
          type: "MX",
          name: mailFromDomain,
          value: `10 feedback-smtp.${region}.amazonses.com`,
          ttl: 1800,
          priority: "MEDIUM",
          description: "For bounce and complaint handling"
        },
        {
          type: "TXT", 
          name: mailFromDomain,
          value: "v=spf1 include:amazonses.com ~all",
          ttl: 1800,
          priority: "HIGH",
          description: "SPF authorization for MAIL FROM domain"
        }
      ] : []),
      
      // Main domain SPF (if not using custom MAIL FROM)
      ...(!mailFromDomain ? [{
        type: "TXT",
        name: domain,
        value: "v=spf1 include:amazonses.com ~all",
        ttl: 1800,
        priority: "HIGH",
        description: "SPF authorization for main domain"
      }] : []),
      
      // DMARC policy (recommended)
      {
        type: "TXT",
        name: `_dmarc.${domain}`,
        value: "v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@client.com",
        ttl: 1800,
        priority: "MEDIUM",
        description: "DMARC policy for email authentication"
      }
    ]
  };
};
```

## Email Sending with Client Domain

### Sending Configuration
```javascript
// Send email using client's verified domain
const sendEmailWithClientDomain = async (clientId, emailData) => {
  // Get client domain configuration
  const clientDomain = await getClientDomain(clientId);
  
  if (clientDomain.status !== 'verified') {
    throw new Error('Client domain not verified');
  }
  
  // Configure email parameters
  const emailParams = {
    Source: `${emailData.fromName} <${emailData.fromEmail}>`, // e.g., "Company <noreply@client.com>"
    Destination: {
      ToAddresses: emailData.recipients
    },
    Message: {
      Subject: {
        Data: emailData.subject,
        Charset: 'UTF-8'
      },
      Body: {
        Html: {
          Data: emailData.htmlBody,
          Charset: 'UTF-8'
        },
        Text: {
          Data: emailData.textBody,
          Charset: 'UTF-8'
        }
      }
    },
    // Use client's configuration set if available
    ConfigurationSetName: clientDomain.configuration_set,
    
    // Tags for tracking
    Tags: [
      {
        Name: 'ClientId',
        Value: clientId
      },
      {
        Name: 'Domain',
        Value: clientDomain.domain
      }
    ]
  };
  
  return await ses.sendEmail(emailParams).promise();
};
```

### Authentication Flow Validation
```javascript
// Validate authentication setup
const validateDomainAuthentication = async (domain) => {
  const results = {
    domain_verified: false,
    dkim_enabled: false,
    dkim_verified: false,
    spf_configured: false,
    dmarc_configured: false,
    mail_from_configured: false
  };
  
  try {
    // Check domain verification
    const verificationAttrs = await ses.getIdentityVerificationAttributes({
      Identities: [domain]
    }).promise();
    
    results.domain_verified = verificationAttrs.VerificationAttributes[domain]?.VerificationStatus === 'Success';
    
    // Check DKIM
    const dkimAttrs = await ses.getIdentityDkimAttributes({
      Identities: [domain]
    }).promise();
    
    const dkimData = dkimAttrs.DkimAttributes[domain];
    results.dkim_enabled = dkimData?.DkimEnabled || false;
    results.dkim_verified = dkimData?.DkimVerificationStatus === 'Success';
    
    // Check MAIL FROM domain
    const mailFromAttrs = await ses.getIdentityMailFromDomainAttributes({
      Identities: [domain]
    }).promise();
    
    const mailFromData = mailFromAttrs.MailFromDomainAttributes[domain];
    results.mail_from_configured = mailFromData?.MailFromDomain ? true : false;
    
    // DNS checks would require additional validation
    // This could be done via DNS lookup APIs
    
  } catch (error) {
    console.error('Error validating domain authentication:', error);
  }
  
  return results;
};
```

## DMARC Compliance Strategies

### Option 1: DKIM Alignment (Recommended)
```yaml
# Client DNS Configuration
# DKIM records point to SES
token1._domainkey.client.com CNAME token1.dkim.amazonses.com
token2._domainkey.client.com CNAME token2.dkim.amazonses.com
token3._domainkey.client.com CNAME token3.dkim.amazonses.com

# DMARC policy allows DKIM alignment
_dmarc.client.com TXT "v=DMARC1; p=quarantine; adkim=r; aspf=r"

# Email headers
From: noreply@client.com
DKIM-Signature: d=client.com; s=token1; ...
```

### Option 2: SPF Alignment with Custom MAIL FROM
```yaml
# Custom MAIL FROM subdomain
mail.client.com MX 10 feedback-smtp.ap-southeast-2.amazonses.com
mail.client.com TXT "v=spf1 include:amazonses.com ~all"

# DMARC policy
_dmarc.client.com TXT "v=DMARC1; p=quarantine; adkim=r; aspf=s"

# Email headers (SPF alignment requires From domain = MAIL FROM domain)
From: noreply@client.com
Return-Path: bounce@mail.client.com  # This won't achieve SPF alignment
```

**Note**: SPF alignment is difficult with third-party senders like SES because the MAIL FROM domain is typically different from the From domain. DKIM alignment is the preferred approach.

## Client Onboarding Workflow

### 1. Domain Registration API
```javascript
POST /api/v1/clients/{clientId}/domains
{
  "domain": "client.com",
  "contact_email": "admin@client.com",
  "use_custom_mail_from": true,
  "mail_from_subdomain": "mail"
}
```

### 2. DNS Instructions Response
```javascript
{
  "domain_id": "domain-123",
  "status": "pending_verification",
  "dns_records": [
    // All required DNS records with instructions
  ],
  "verification_url": "https://platform.com/domains/domain-123/verify",
  "estimated_propagation_time": "24-48 hours"
}
```

### 3. Verification Monitoring
```javascript
// Automated verification checking
const monitorDomainVerification = async (domainId) => {
  const domain = await getDomainById(domainId);
  
  // Check SES verification status
  const verification = await validateDomainAuthentication(domain.domain);
  
  if (verification.domain_verified && verification.dkim_verified) {
    // Update domain status
    await updateDomainStatus(domainId, 'verified');
    
    // Notify client
    await sendVerificationSuccessEmail(domain.client_id, domain.domain);
    
    // Enable email sending for this domain
    await enableDomainForSending(domainId);
  }
};
```

## Security Considerations

### 1. Domain Ownership Validation
```javascript
// Additional domain ownership checks
const validateDomainOwnership = async (domain, clientId) => {
  // Check if domain is already claimed by another client
  const existingDomain = await checkDomainExists(domain);
  if (existingDomain && existingDomain.client_id !== clientId) {
    throw new Error('Domain already claimed by another client');
  }
  
  // Validate domain format and restrictions
  if (isRestrictedDomain(domain)) {
    throw new Error('Domain not allowed for client use');
  }
  
  return true;
};
```

### 2. Rate Limiting and Quotas
```javascript
// Domain verification rate limits
const domainRateLimits = {
  max_domains_per_client: 10,
  max_verification_attempts: 5,
  verification_cooldown: 3600 // 1 hour
};
```

### 3. Monitoring and Alerts
```javascript
// Monitor domain health
const monitorDomainHealth = async (domain) => {
  const health = await validateDomainAuthentication(domain);
  
  if (!health.dkim_verified || !health.domain_verified) {
    // Alert client about authentication issues
    await sendDomainHealthAlert(domain, health);
  }
};
```

## Troubleshooting Common Issues

### 1. DKIM Verification Failures
```yaml
Issue: DKIM tokens not verifying
Solutions:
  - Check CNAME records are correctly configured
  - Verify DNS propagation (can take 24-48 hours)
  - Ensure no conflicting DNS records
  - Check for typos in DNS record values
```

### 2. SPF Authentication Failures
```yaml
Issue: SPF checks failing
Solutions:
  - Verify SPF record includes "include:amazonses.com"
  - Check for multiple SPF records (only one allowed)
  - Ensure proper SPF syntax
  - Consider SPF record length limits
```

### 3. DMARC Alignment Issues
```yaml
Issue: DMARC failing despite SPF/DKIM passing
Solutions:
  - Ensure DKIM signature domain matches From domain
  - Use relaxed alignment (adkim=r, aspf=r)
  - Verify From header domain matches authenticated domain
  - Check DMARC policy syntax
```

## Best Practices

### 1. Client Communication
- Provide clear DNS setup instructions
- Offer DNS validation tools
- Set proper expectations for propagation time
- Provide ongoing monitoring and alerts

### 2. Technical Implementation
- Use DKIM alignment over SPF alignment
- Implement automated verification monitoring
- Provide detailed error messages and troubleshooting
- Support both custom MAIL FROM and default configurations

### 3. Deliverability Optimization
- Monitor reputation metrics per client domain
- Implement proper bounce and complaint handling
- Provide deliverability reporting and insights
- Support suppression list management per domain

---

**Document Version**: 1.0  
**Last Updated**: August 18, 2024  
**Architecture**: Standalone Email Platform with Client Domain Authentication
