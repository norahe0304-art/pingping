#!/usr/bin/env python3
"""
Markdown to PDF Converter
Usage: python3 md2pdf.py input.md output.pdf
"""

import sys
import os

def convert_md_to_pdf(md_file, pdf_file=None):
    if pdf_file is None:
        pdf_file = md_file.replace('.md', '.pdf')
    
    # Read markdown
    with open(md_file, 'r') as f:
        md_content = f.read()
    
    # Simple HTML conversion (using basic formatting)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
        }}
        h1 {{
            color: #1a1a1a;
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        h2 {{ color: #333; margin-top: 30px; }}
        h3 {{ color: #555; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}
        th {{ background-color: #f5f5f5; }}
        ul, ol {{ padding-left: 25px; }}
        li {{ margin: 6px 0; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
{simple_markdown_to_html(md_content)}
</body>
</html>"""
    
    html_file = pdf_file.replace('.pdf', '.html')
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"HTML created: {html_file}")
    print(f"To convert to PDF: Open {html_file} in browser and print to PDF")
    return html_file

def simple_markdown_to_html(md):
    """Simple markdown to HTML conversion"""
    import re
    
    lines = md.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    
    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                html_lines.append('<pre><code>')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(line)
            continue
        
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        # Lists
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            # Bold
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            # Italic
            line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)
            # Code
            line = re.sub(r'`(.*?)`', r'<code>\1</code>', line)
            # Links
            line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
            html_lines.append(f'<p>{line}</p>')
    
    return '\n'.join(html_lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 md2pdf.py input.md [output.pdf]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    pdf_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_md_to_pdf(md_file, pdf_file)
