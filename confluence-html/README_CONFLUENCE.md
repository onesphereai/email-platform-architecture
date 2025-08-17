# Confluence HTML Files - Email Platform Architecture

This directory contains Confluence-ready HTML versions of all Email Platform architecture documentation. These files are formatted using Confluence Storage Format and can be directly imported into Confluence pages.

## 📋 Generated Files Summary

### Root Level Documentation
- **[Email_Platform_Standalone_Architecture.html](Email_Platform_Standalone_Architecture.html)** - Complete standalone architecture documentation
- **[Email_Platform_Architecture_Documentation.html](Email_Platform_Architecture_Documentation.html)** - Legacy integrated architecture
- **[Email_Platform_API_Specification.html](Email_Platform_API_Specification.html)** - REST API documentation
- **[Email_Platform_Documentation_Summary.html](Email_Platform_Documentation_Summary.html)** - Executive summary
- **[README.html](README.html)** - Main project overview
- **[Context.html](Context.html)** - Project context and background

### Architecture Views

#### 🔧 Development View
- **[Architecture/Development-View/README.html](Architecture/Development-View/README.html)** - Development view overview
- **[Architecture/Development-View/02_integration_flow_description.html](Architecture/Development-View/02_integration_flow_description.html)** - Integration flow details
- **[Architecture/Development-View/03_detailed_component_architecture_flow.html](Architecture/Development-View/03_detailed_component_architecture_flow.html)** - Component architecture
- **[Architecture/Development-View/04_callback_flow_description.html](Architecture/Development-View/04_callback_flow_description.html)** - Callback system flow
- **[Architecture/Development-View/10_campaign_creation_sequence_flow.html](Architecture/Development-View/10_campaign_creation_sequence_flow.html)** - Campaign creation sequence
- **[Architecture/Development-View/11_email_sending_sequence_flow.html](Architecture/Development-View/11_email_sending_sequence_flow.html)** - Email sending sequence
- **[Architecture/Development-View/12_api_integration_sequence_flow.html](Architecture/Development-View/12_api_integration_sequence_flow.html)** - API integration sequence
- **[Architecture/Development-View/Email_Platform_API_Specification.html](Architecture/Development-View/Email_Platform_API_Specification.html)** - API specification

#### 🚀 Deployment View
- **[Architecture/Deployment-View/README.html](Architecture/Deployment-View/README.html)** - Deployment view overview
- **[Architecture/Deployment-View/01_high_level_architecture_flow.html](Architecture/Deployment-View/01_high_level_architecture_flow.html)** - High-level architecture flow
- **[Architecture/Deployment-View/15_error_handling_sequence_flow.html](Architecture/Deployment-View/15_error_handling_sequence_flow.html)** - Error handling sequence
- **[Architecture/Deployment-View/16_clean_high_level_architecture_flow.html](Architecture/Deployment-View/16_clean_high_level_architecture_flow.html)** - Clean architecture flow

#### 🔒 Security View
- **[Architecture/Security-View/README.html](Architecture/Security-View/README.html)** - Security view overview
- **[Architecture/Security-View/05_security_architecture_flow.html](Architecture/Security-View/05_security_architecture_flow.html)** - Security architecture flow
- **[Architecture/Security-View/14_authentication_sequence_flow.html](Architecture/Security-View/14_authentication_sequence_flow.html)** - Authentication sequence
- **[Architecture/Security-View/19_clean_security_architecture_flow.html](Architecture/Security-View/19_clean_security_architecture_flow.html)** - Clean security architecture

#### 📊 Data View
- **[Architecture/Data-View/README.html](Architecture/Data-View/README.html)** - Data view overview
- **[Architecture/Data-View/06_transaction_status_flow_description.html](Architecture/Data-View/06_transaction_status_flow_description.html)** - Transaction status flow
- **[Architecture/Data-View/07_message_status_flow_description.html](Architecture/Data-View/07_message_status_flow_description.html)** - Message status flow
- **[Architecture/Data-View/13_email_delivery_analytics_sequence_flow.html](Architecture/Data-View/13_email_delivery_analytics_sequence_flow.html)** - Email delivery analytics
- **[Architecture/Data-View/18_clean_multitenant_architecture_flow.html](Architecture/Data-View/18_clean_multitenant_architecture_flow.html)** - Multi-tenant architecture

#### 💰 Cost View
- **[Architecture/Cost-View/README.html](Architecture/Cost-View/README.html)** - Cost view overview
- **[Architecture/Cost-View/Email_Platform_Cost_Analysis.html](Architecture/Cost-View/Email_Platform_Cost_Analysis.html)** - Cost analysis

#### Architecture Overview
- **[Architecture/README.html](Architecture/README.html)** - Architecture overview

## 🔧 Confluence Import Instructions

### Method 1: Copy-Paste Content
1. Open any HTML file in a text editor
2. Copy the content between `<!-- Confluence Storage Format -->` and `</body>`
3. In Confluence, create a new page
4. Switch to "Source Editor" mode
5. Paste the copied content
6. Switch back to "Visual Editor" to see the formatted content

### Method 2: Import HTML Files
1. In Confluence, go to Space Settings → Content Tools → Import
2. Select "HTML" as the import format
3. Upload the HTML files
4. Follow the import wizard to complete the process

### Method 3: Use Confluence REST API
```bash
# Example API call to create a page
curl -X POST \
  'https://your-confluence-instance.atlassian.net/wiki/rest/api/content' \
  -H 'Authorization: Basic <your-auth-token>' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "page",
    "title": "Email Platform Architecture",
    "space": {"key": "YOUR_SPACE_KEY"},
    "body": {
      "storage": {
        "value": "<content from HTML file>",
        "representation": "storage"
      }
    }
  }'
```

## 📝 File Format Details

### Confluence Storage Format Features
- **Headers**: Converted to `<h1>`, `<h2>`, etc.
- **Code Blocks**: Converted to Confluence code macros with syntax highlighting
- **Tables**: Converted to HTML tables compatible with Confluence
- **Lists**: Converted to HTML `<ul>` and `<ol>` elements
- **Links**: Converted to HTML `<a>` tags
- **Images**: Converted to Confluence image macros
- **Formatting**: Bold, italic, strikethrough, and inline code preserved

### Special Confluence Macros Used
- **Code Macro**: `<ac:structured-macro ac:name="code">` for code blocks
- **Image Macro**: `<ac:image><ri:url>` for images
- **Plain Text Body**: `<ac:plain-text-body><![CDATA[]]>` for code content

## 🔄 Updating Files

To regenerate the Confluence HTML files after updating the markdown documentation:

```bash
cd /Users/ammarkhalid/Documents/workspace/email-platform-diagrams
python3 md_to_confluence.py
```

This will update all HTML files in the `confluence-html` directory while preserving the directory structure.

## 📞 Support

For questions about importing these files into Confluence:
- **Confluence Documentation**: Refer to Atlassian's import documentation
- **Technical Issues**: Contact the development team
- **Content Questions**: Refer to the original markdown files

---

**Generated**: August 17, 2024  
**Total Files**: 30 HTML files  
**Last Updated**: August 17, 2024  
**Format**: Confluence Storage Format
