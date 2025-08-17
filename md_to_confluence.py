#!/usr/bin/env python3
import os
import re
from pathlib import Path
import html

def convert_markdown_to_confluence_html(md_content, filename):
    """Convert Markdown content to Confluence-compatible HTML"""
    
    html_lines = []
    lines = md_content.split('\n')
    in_code_block = False
    in_table = False
    in_list = False
    list_stack = []
    
    for i, line in enumerate(lines):
        
        # Code blocks
        if line.strip().startswith('```'):
            if not in_code_block:
                lang = line.strip()[3:].strip() or 'none'
                html_lines.append(f'<ac:structured-macro ac:name="code" ac:schema-version="1">')
                html_lines.append(f'  <ac:parameter ac:name="language">{lang}</ac:parameter>')
                html_lines.append(f'  <ac:plain-text-body><![CDATA[')
                in_code_block = True
            else:
                html_lines.append(']]></ac:plain-text-body>')
                html_lines.append('</ac:structured-macro>')
                in_code_block = False
            continue
            
        if in_code_block:
            html_lines.append(line)
            continue
        
        # Headers
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            if level <= 6:
                text = line[level:].strip()
                html_lines.append(f'<h{level}>{html.escape(text)}</h{level}>')
                continue
        
        # Tables
        if '|' in line and not in_table:
            # Check if this is a table
            if i + 1 < len(lines) and re.match(r'^[\s\|:\-]+$', lines[i + 1]):
                in_table = True
                html_lines.append('<table>')
                html_lines.append('<thead>')
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                html_lines.append('<tr>')
                for cell in cells:
                    html_lines.append(f'<th>{html.escape(cell)}</th>')
                html_lines.append('</tr>')
                html_lines.append('</thead>')
                continue
        elif in_table and '|' in line:
            if re.match(r'^[\s\|:\-]+$', line):
                html_lines.append('<tbody>')
                continue
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            html_lines.append('<tr>')
            for cell in cells:
                html_lines.append(f'<td>{html.escape(cell)}</td>')
            html_lines.append('</tr>')
            continue
        elif in_table and '|' not in line:
            html_lines.append('</tbody>')
            html_lines.append('</table>')
            in_table = False
        
        # Lists
        list_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        ordered_list_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)
        
        if list_match or ordered_list_match:
            if list_match:
                indent = len(list_match.group(1))
                content = list_match.group(2)
                list_type = 'ul'
            else:
                indent = len(ordered_list_match.group(1))
                content = ordered_list_match.group(2)
                list_type = 'ol'
            
            level = indent // 2
            
            # Close deeper levels
            while len(list_stack) > level + 1:
                closed_type = list_stack.pop()
                html_lines.append(f'</{closed_type}>')
            
            # Open new level if needed
            if len(list_stack) <= level:
                html_lines.append(f'<{list_type}>')
                list_stack.append(list_type)
            elif list_stack[level] != list_type:
                # Different list type at same level
                html_lines.append(f'</{list_stack[level]}>')
                list_stack[level] = list_type
                html_lines.append(f'<{list_type}>')
            
            # Process inline formatting
            content = process_inline_formatting(content)
            html_lines.append(f'<li>{content}</li>')
            continue
        else:
            # Close all lists if we're not in a list anymore
            while list_stack:
                closed_type = list_stack.pop()
                html_lines.append(f'</{closed_type}>')
        
        # Horizontal rules
        if re.match(r'^[\-\*_]{3,}$', line.strip()):
            html_lines.append('<hr/>')
            continue
        
        # Blockquotes
        if line.startswith('>'):
            content = line[1:].strip()
            content = process_inline_formatting(content)
            html_lines.append(f'<blockquote>{content}</blockquote>')
            continue
        
        # Regular paragraphs
        if line.strip():
            formatted_line = process_inline_formatting(line)
            html_lines.append(f'<p>{formatted_line}</p>')
        else:
            # Empty line
            if not in_list:
                html_lines.append('<br/>')
    
    # Close any open lists
    while list_stack:
        closed_type = list_stack.pop()
        html_lines.append(f'</{closed_type}>')
    
    # Close table if still open
    if in_table:
        html_lines.append('</tbody>')
        html_lines.append('</table>')
    
    return '\n'.join(html_lines)

def process_inline_formatting(text):
    """Process inline Markdown formatting"""
    
    # Escape HTML entities first
    text = html.escape(text)
    
    # Images: ![alt](url)
    text = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        r'<ac:image><ri:url ri:value="\2" /></ac:image>',
        text
    )
    
    # Links: [text](url)
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        r'<a href="\2">\1</a>',
        text
    )
    
    # Bold: **text** or __text__
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)
    
    # Italic: *text* or _text_
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'_([^_]+)_', r'<em>\1</em>', text)
    
    # Inline code: `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Strikethrough: ~~text~~
    text = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', text)
    
    return text

def convert_file(input_path, output_dir):
    """Convert a single Markdown file to Confluence HTML"""
    
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Get relative path for output structure
    rel_path = os.path.relpath(input_path, '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams')
    output_path = os.path.join(output_dir, rel_path.replace('.md', '.html'))
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convert content
    html_content = convert_markdown_to_confluence_html(md_content, os.path.basename(input_path))
    
    # Add Confluence page wrapper
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <title>{os.path.basename(input_path).replace('.md', '')}</title>
    <meta charset="utf-8">
</head>
<body>
<!-- Confluence Storage Format -->
{html_content}
</body>
</html>'''
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return output_path

def main():
    """Convert all Markdown files to Confluence HTML"""
    
    # Create output directory
    output_dir = '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/confluence-html'
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all markdown files that actually exist
    md_files = [
        # Root level files
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Email_Platform_API_Specification.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Email_Platform_Documentation_Summary.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Email_Platform_Standalone_Architecture.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/README.md',
        
        # Architecture overview
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/README.md',
        
        # Cost View
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Cost-View/README.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Cost-View/Email_Platform_Cost_Analysis.md',
        
        # Data View
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Data-View/README.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Data-View/06_transaction_status_flow_description.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Data-View/07_message_status_flow_description.md',
        
        # Deployment View
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Deployment-View/README.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Deployment-View/01_high_level_architecture_flow.md',
        
        # Development View
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Development-View/README.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Development-View/02_integration_flow_description.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Development-View/03_detailed_component_architecture_flow.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Development-View/04_callback_flow_description.md',
        
        # Security View
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Security-View/README.md',
        '/Users/ammarkhalid/Documents/workspace/email-platform-diagrams/Architecture/Security-View/05_security_architecture_flow.md',
    ]
    
    # Filter to only include files that actually exist
    existing_files = [f for f in md_files if os.path.exists(f)]
    
    print(f"Converting {len(existing_files)} Markdown files to Confluence HTML...")
    print(f"Output directory: {output_dir}\n")
    
    for md_file in existing_files:
        try:
            output_path = convert_file(md_file, output_dir)
            print(f"✓ Converted: {os.path.basename(md_file)} -> {os.path.relpath(output_path, output_dir)}")
        except Exception as e:
            print(f"✗ Error converting {md_file}: {e}")
    
    print(f"\nConversion complete! HTML files saved in: {output_dir}")

if __name__ == "__main__":
    main()