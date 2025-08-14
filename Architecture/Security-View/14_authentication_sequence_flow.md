# User Authentication & Authorization - Flow Description

**Diagram**: `14_authentication_sequence.png`

## Overview
This sequence diagram illustrates the complete SAML-based authentication flow, from initial platform access through enterprise identity provider integration, JWT token generation, and authorized API access.

## Sequence Flow

| Step | Source | Target | Method/Action | Description | Response/Result |
|------|--------|--------|---------------|-------------|-----------------|
| 1 | End User | Web Browser | accessPlatform() | User navigates to Email Platform URL | Browser request initiated |
| 2 | Web Browser | CloudFront CDN | GET / | Browser requests platform homepage | Request sent to CDN |
| 3 | CloudFront CDN | Angular App | serveAngularApp() | CDN serves Angular application files | App files delivered |
| 4 | Angular App | Web Browser | loadApp() | Angular application loads in browser | App loaded |
| 5 | Web Browser | End User | displayLoginPage() | Browser displays login interface | Login page shown |
| 6 | End User | Angular App | clickLogin() | User clicks login button | Login initiated |
| 7 | Angular App | Cognito User Pool | redirectToSAML() | App redirects to SAML authentication | SAML flow started |
| 8 | Cognito User Pool | Enterprise IdP | SAMLRequest | Cognito sends SAML authentication request | Request sent to IdP |
| 9 | Enterprise IdP | End User | authenticateUser() | IdP presents authentication form | Auth form displayed |
| 10 | End User | Enterprise IdP | provideCredentials() | User enters credentials (username/password/MFA) | Credentials submitted |
| 11 | Enterprise IdP | Cognito User Pool | SAMLResponse | IdP sends SAML response with assertions | Response sent |
| 12 | Cognito User Pool | Cognito User Pool | validateSAMLResponse() | Cognito validates SAML response and assertions | Validation completed |
| 13 | Cognito User Pool | Angular App | generateJWTToken() | Cognito generates JWT token for user | Token generated |
| 14 | Angular App | Web Browser | storeToken() | App stores JWT token in browser storage | Token stored |
| 15 | Angular App | Web Browser | redirectToDashboard() | App redirects to main dashboard | Redirect initiated |
| 16 | Web Browser | API Gateway | GET /dashboard | Browser requests dashboard data | Request sent |
| 17 | API Gateway | Auth Service | validateJWTToken() | Gateway validates JWT token | Token validation started |
| 18 | Auth Service | Cognito User Pool | verifyToken() | Service verifies token with Cognito | Token verified |
| 19 | Cognito User Pool | Auth Service | return userClaims | Cognito returns user claims and attributes | Claims returned |
| 20 | Auth Service | Auth Service | extractTenantId() | Service extracts tenant ID from claims | Tenant ID extracted |
| 21 | Auth Service | API Gateway | return authContext | Service returns authentication context | Context returned |
| 22 | API Gateway | UI Service | getUserData() | Gateway routes request to UI service | Request routed |
| 23 | UI Service | DynamoDB | queryUserProfile() | Service queries user profile data | Query executed |
| 24 | DynamoDB | UI Service | return userProfile | Database returns user profile | Profile returned |
| 25 | UI Service | API Gateway | return dashboardData | Service returns dashboard data | Data returned |
| 26 | API Gateway | Angular App | return 200 OK | Gateway returns successful response | Response received |
| 27 | Angular App | Web Browser | renderDashboard() | App renders dashboard with user data | Dashboard rendered |
| 28 | Web Browser | End User | displayDashboard() | Browser displays personalized dashboard | Dashboard shown |
| 29 | Angular App | Cognito User Pool | refreshToken() | App refreshes JWT token before expiry | Refresh initiated |
| 30 | Cognito User Pool | Angular App | return newToken | Cognito returns new JWT token | New token received |
| 31 | Angular App | Web Browser | updateStoredToken() | App updates stored token | Token updated |

## Authentication Phases

### Phase 1: Initial Platform Access (Steps 1-5)
- **Purpose**: Load Email Platform application
- **Components**: Web Browser, CloudFront CDN, Angular App
- **Process**: 
  - User navigates to platform URL
  - CDN serves static Angular application files
  - App loads and displays login interface
- **Outcome**: User sees login page

### Phase 2: SAML Authentication Flow (Steps 6-13)
- **Purpose**: Authenticate user through enterprise identity provider
- **Components**: Angular App, Cognito User Pool, Enterprise IdP
- **Process**:
  - User initiates login
  - SAML authentication request sent to enterprise IdP
  - User provides credentials to IdP
  - IdP validates credentials and returns SAML response
  - Cognito validates SAML response and generates JWT token
- **Outcome**: Authenticated user with JWT token

### Phase 3: Token Storage and Redirect (Steps 14-15)
- **Purpose**: Store authentication token and redirect to dashboard
- **Components**: Angular App, Web Browser
- **Process**:
  - JWT token stored in browser (localStorage/sessionStorage)
  - User redirected to main dashboard
- **Outcome**: User ready to access protected resources

### Phase 4: Authorized API Access (Steps 16-28)
- **Purpose**: Access protected resources with authentication
- **Components**: API Gateway, Auth Service, Cognito, UI Service, DynamoDB
- **Process**:
  - Browser requests dashboard data
  - API Gateway validates JWT token
  - Auth service verifies token and extracts user context
  - UI service fetches user-specific data
  - Dashboard rendered with personalized content
- **Outcome**: User sees personalized dashboard

### Phase 5: Token Refresh (Steps 29-31)
- **Purpose**: Maintain authentication without re-login
- **Components**: Angular App, Cognito User Pool
- **Process**:
  - App monitors token expiry
  - Refreshes token before expiration
  - Updates stored token
- **Outcome**: Seamless authentication maintenance

## SAML Integration Details

### SAML Request Example
```xml
<samlp:AuthnRequest 
    xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    ID="_8e8dc5f69a98cc4c1ff3427e5ce34606fd672f91e6"
    Version="2.0"
    IssueInstant="2024-01-15T10:30:00Z"
    Destination="https://idp.company.com/saml/sso"
    AssertionConsumerServiceURL="https://emailplatform.messagecentre.com/saml/acs">
    <saml:Issuer xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
        urn:amazon:cognito:sp:us-east-1_XXXXXXXXX
    </saml:Issuer>
</samlp:AuthnRequest>
```

### SAML Response Example
```xml
<samlp:Response 
    xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"
    ID="_8e8dc5f69a98cc4c1ff3427e5ce34606fd672f91e6"
    Version="2.0"
    IssueInstant="2024-01-15T10:30:30Z">
    <saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
        <saml:Subject>
            <saml:NameID Format="urn:oasis:names:tc:SAML:2.0:nameid-format:persistent">
                john.doe@company.com
            </saml:NameID>
        </saml:Subject>
        <saml:AttributeStatement>
            <saml:Attribute Name="email">
                <saml:AttributeValue>john.doe@company.com</saml:AttributeValue>
            </saml:Attribute>
            <saml:Attribute Name="tenantId">
                <saml:AttributeValue>tenant_123456789</saml:AttributeValue>
            </saml:Attribute>
            <saml:Attribute Name="role">
                <saml:AttributeValue>marketing_manager</saml:AttributeValue>
            </saml:Attribute>
        </saml:AttributeStatement>
    </saml:Assertion>
</samlp:Response>
```

## JWT Token Structure

### JWT Header
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "cognito-key-id"
}
```

### JWT Payload
```json
{
  "sub": "user_123456789",
  "email": "john.doe@company.com",
  "email_verified": true,
  "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_XXXXXXXXX",
  "aud": "client_id_123456789",
  "token_use": "id",
  "auth_time": 1642248600,
  "iat": 1642248600,
  "exp": 1642252200,
  "custom:tenantId": "tenant_123456789",
  "custom:role": "marketing_manager",
  "custom:permissions": ["campaigns.read", "campaigns.write", "templates.read"]
}
```

## Authentication Context

### User Claims Extraction
```javascript
// Extract user context from JWT token
const authContext = {
  userId: token.sub,
  email: token.email,
  tenantId: token['custom:tenantId'],
  role: token['custom:role'],
  permissions: token['custom:permissions'],
  sessionId: generateSessionId(),
  loginTime: new Date(token.auth_time * 1000),
  expiryTime: new Date(token.exp * 1000)
};
```

### Tenant Isolation
```javascript
// Ensure tenant isolation in all operations
const tenantContext = {
  tenantId: authContext.tenantId,
  partitionKey: `TENANT#${authContext.tenantId}`,
  resourcePrefix: `tenant-${authContext.tenantId}`,
  permissions: authContext.permissions
};
```

## Security Measures

### Token Security
- **Encryption**: JWT tokens signed with RS256 algorithm
- **Expiration**: Short-lived tokens (1 hour) with refresh capability
- **Storage**: Secure storage in browser (httpOnly cookies preferred)
- **Transmission**: HTTPS only for all token exchanges

### SAML Security
- **Assertion Encryption**: SAML assertions encrypted in transit
- **Signature Validation**: Digital signatures verified
- **Replay Protection**: Timestamp and ID validation
- **Audience Restriction**: Tokens valid only for intended audience

### Session Management
- **Session Timeout**: Configurable session timeout
- **Concurrent Sessions**: Limit concurrent sessions per user
- **Session Invalidation**: Immediate invalidation on logout
- **Activity Tracking**: Monitor user activity for security

## Error Handling

### Authentication Errors
| Error Type | HTTP Status | Description | User Action |
|------------|-------------|-------------|-------------|
| Invalid Credentials | 401 | Username/password incorrect | Re-enter credentials |
| Account Locked | 423 | Too many failed attempts | Contact administrator |
| SAML Error | 400 | SAML response invalid | Contact IT support |
| Token Expired | 401 | JWT token expired | Automatic refresh or re-login |

### Authorization Errors
| Error Type | HTTP Status | Description | User Action |
|------------|-------------|-------------|-------------|
| Insufficient Permissions | 403 | User lacks required permissions | Contact administrator |
| Tenant Mismatch | 403 | User not authorized for tenant | Verify account access |
| Resource Not Found | 404 | Requested resource not accessible | Check resource permissions |

### System Errors
| Error Type | HTTP Status | Description | System Action |
|------------|-------------|-------------|---------------|
| IdP Unavailable | 503 | Identity provider not responding | Retry with backoff |
| Cognito Error | 500 | AWS Cognito service error | Log error, alert operations |
| Database Error | 500 | User profile query failed | Retry operation |

## Token Refresh Flow

### Automatic Refresh
```javascript
// Monitor token expiry and refresh automatically
setInterval(() => {
  const token = getStoredToken();
  const expiryTime = new Date(token.exp * 1000);
  const currentTime = new Date();
  const timeUntilExpiry = expiryTime - currentTime;
  
  // Refresh token 5 minutes before expiry
  if (timeUntilExpiry < 5 * 60 * 1000) {
    refreshToken();
  }
}, 60000); // Check every minute
```

### Refresh Request
```javascript
// Refresh JWT token
async function refreshToken() {
  try {
    const response = await fetch('/auth/refresh', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${getCurrentToken()}`,
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      const { token } = await response.json();
      storeToken(token);
    } else {
      // Refresh failed, redirect to login
      redirectToLogin();
    }
  } catch (error) {
    console.error('Token refresh failed:', error);
    redirectToLogin();
  }
}
```

## Multi-Factor Authentication

### MFA Flow Integration
1. **Primary Authentication**: Username/password at IdP
2. **MFA Challenge**: IdP presents MFA challenge (SMS, TOTP, etc.)
3. **MFA Response**: User provides MFA code
4. **Validation**: IdP validates MFA response
5. **SAML Response**: IdP sends SAML response with MFA claim

### MFA Claims in JWT
```json
{
  "custom:mfa_verified": true,
  "custom:mfa_method": "totp",
  "custom:mfa_timestamp": 1642248600
}
```

## Single Sign-On (SSO)

### SSO Benefits
- **User Experience**: Single login for multiple applications
- **Security**: Centralized authentication and authorization
- **Administration**: Centralized user management
- **Compliance**: Consistent security policies

### SSO Session Management
- **Global Session**: Maintained at IdP level
- **Application Sessions**: Individual sessions per application
- **Session Synchronization**: Coordinate session timeouts
- **Single Logout**: Logout from all applications simultaneously
