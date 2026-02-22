#!/usr/bin/env python3
"""
Better Markdown to PDF Converter with proper styling
"""

import re

def convert_md_to_html(md_file):
    with open(md_file, 'r') as f:
        md_content = f.read()
    
    html = md_to_html(md_content)
    
    styled_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI Content Marketplace Report</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            margin: 50px 60px;
            line-height: 1.7;
            color: #1a1a1a;
            font-size: 14px;
        }}
        
        h1 {{
            font-size: 28px;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 8px;
            padding-bottom: 15px;
            border-bottom: 3px solid #4F46E5;
        }}
        
        .meta {{
            color: #6b7280;
            font-size: 12px;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        h2 {{
            font-size: 20px;
            font-weight: 600;
            color: #1f2937;
            margin-top: 35px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e5e7eb;
        }}
        
        h3 {{
            font-size: 16px;
            font-weight: 600;
            color: #374151;
            margin-top: 25px;
            margin-bottom: 10px;
        }}
        
        p {{
            margin-bottom: 12px;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-left: 25px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 6px;
        }}
        
        strong {{
            font-weight: 600;
            color: #1f2937;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 13px;
        }}
        
        th {{
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
            font-weight: 600;
            padding: 12px 15px;
            text-align: left;
            border: none;
        }}
        
        td {{
            padding: 10px 15px;
            border: 1px solid #e5e7eb;
            background: #fafafa;
        }}
        
        tr:nth-child(even) td {{
            background: #f3f4f6;
        }}
        
        tr:hover td {{
            background: #eef2ff;
        }}
        
        code {{
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 12px;
            color: #c026d3;
        }}
        
        pre {{
            background: #1f2937;
            color: #e5e7eb;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        
        pre code {{
            background: none;
            color: #e5e7eb;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 4px solid #4F46E5;
            margin: 20px 0;
            padding: 15px 20px;
            background: #f9fafb;
            font-style: italic;
            color: #4b5563;
        }}
        
        hr {{
            border: none;
            border-top: 1px solid #e5e7eb;
            margin: 30px 0;
        }}
        
        .check {{ color: #10b981; }}
        .fire {{ color: #f59e0b; }}
        .rocket {{ color: #4F46E5; }}
        
        a {{
            color: #4F46E5;
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
    
    output_file = md_file.replace('.md', '_styled.html')
    with open(output_file, 'w') as f:
        f.write(styled_html)
    
    return output_file

def md_to_html(md):
    lines = md.split('\n')
    html_lines = []
    in_code_block = False
    in_table = False
    table_rows = []
    
    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                lang = line[3:].strip()
                html_lines.append(f'<pre><code class="language-{lang}">')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(line)
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            html_lines.append('<hr>')
            continue
        
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{process_inline(line[2:])}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{process_inline(line[3:])}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{process_inline(line[4:])}</h3>')
        # Table
        elif '|' in line and line.strip().startswith('|'):
            table_rows.append(line)
            continue
        # Empty line - process table if we have one
        elif not line.strip() and table_rows:
            if table_rows:
                html_lines.append(process_table(table_rows))
                table_rows = []
            continue
        # List items
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            content = process_inline(line[2:])
            if not any('<ul>' in l for l in html_lines[-3:]):
                html_lines.append('<ul>')
            html_lines.append(f'<li>{content}</li>')
        elif line.strip().startswith('1. ') or line.strip().startswith('2. ') or line.strip().startswith('3. '):
            content = process_inline(line[3:])
            html_lines.append(f'<li>{content}</li>')
        # Paragraph
        elif line.strip():
            if table_rows:
                html_lines.append(process_table(table_rows))
                table_rows = []
            html_lines.append(f'<p>{process_inline(line)}</p>')
    
    # Close any remaining table
    if table_rows:
        html_lines.append(process_table(table_rows))
    
    # Close any open ul
    if '<ul>' in ''.join(html_lines):
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)

def process_table(rows):
    if len(rows) < 2:
        return ''
    
    html = ['<table>', '<thead>', '<tr>']
    
    # Header row
    headers = [cell.strip() for cell in rows[0].split('|')[1:-1]]
    for h in headers:
        html.append(f'<th>{h}</th>')
    html.extend(['</tr>', '</thead>', '<tbody>'])
    
    # Data rows (skip separator line)
    for row in rows[2:]:
        if not row.strip() or not row.replace('|', '').replace('-', '').replace(':', '').strip():
            continue
        cells = [cell.strip() for cell in row.split('|')[1:-1]]
        html.append('<tr>')
        for cell in cells:
            html.append(f'<td>{cell}</td>')
        html.append('</tr>')
    
    html.extend(['</tbody>', '</table>'])
    return '\n'.join(html)

def process_inline(text):
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    # Emoji to span
    text = re.sub(r'✅', '<span class="check">✓</span>', text)
    text = re.sub(r'🔜', '<span class="fire">🔜</span>', text)
    text = re.sub(r'🎯', '<span class="rocket">🎯</span>', text)
    
    return text

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 md2pdf_v2.py input.md")
        sys.exit(1)
    
    output = convert_md_to_html(sys.argv[1])
    print(f"Styled HTML created: {output}")
    print(f"Open in browser and print to PDF")
