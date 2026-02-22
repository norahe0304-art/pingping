#!/usr/bin/env python3
"""
Professional PDF Converter v2 - Fixed
"""

def create_professional_html(md_file):
    with open(md_file, 'r') as f:
        content = f.read()
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI Content Marketplace Report</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 11pt;
            line-height: 1.9;
            color: #1a1a1a;
            padding: 60pt 80pt;
            max-width: 100%;
        }}
        
        h1 {{
            font-size: 22pt;
            font-weight: 700;
            color: #111;
            margin-bottom: 8pt;
            padding-bottom: 10pt;
            border-bottom: 1pt solid #999;
        }}
        
        .meta {{
            font-size: 9pt;
            color: #555;
            margin-bottom: 30pt;
        }}
        
        h2 {{
            font-size: 14pt;
            font-weight: 600;
            color: #222;
            margin-top: 36pt;
            margin-bottom: 14pt;
            padding-bottom: 6pt;
            border-bottom: 1pt solid #ddd;
        }}
        
        h3 {{
            font-size: 11pt;
            font-weight: 600;
            color: #333;
            margin-top: 24pt;
            margin-bottom: 6pt;
        }}
        
        p {{
            margin-bottom: 8pt;
        }}
        
        ul, ol {{
            margin-left: 18pt;
            margin-bottom: 12pt;
        }}
        
        li {{
            margin-bottom: 4pt;
        }}
        
        strong {{
            font-weight: 600;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 14pt 0;
            font-size: 10pt;
        }}
        
        th {{
            background: #1a1a1a;
            color: #fff;
            font-weight: 600;
            padding: 8pt 10pt;
            text-align: left;
            border: none;
        }}
        
        td {{
            padding: 7pt 10pt;
            border: 1pt solid #ddd;
            background: #fff;
        }}
        
        tr:nth-child(even) td {{
            background: #f8f8f8;
        }}
        
        hr {{
            border: none;
            border-top: 1pt solid #ddd;
            margin: 24pt 0;
        }}
        
        .footer {{
            font-size: 9pt;
            color: #777;
            margin-top: 30pt;
            padding-top: 12pt;
            border-top: 1pt solid #ddd;
        }}
        
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        
        .inline-list {{
            margin-left: 0;
            list-style: none;
        }}
        
        .inline-list li {{
            display: inline;
            margin-right: 12pt;
        }}
    </style>
</head>
<body>
{parse_content(content)}
</body>
</html>'''
    
    output = md_file.replace('.md', '_clean.html')
    with open(output, 'w') as f:
        f.write(html)
    return output

def parse_content(content):
    import re
    lines = content.split('\n')
    html = []
    i = 0
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Skip empty lines at section boundaries
        if not line.strip():
            i += 1
            continue
            
        # Title
        if line.startswith('# ') and i < 3:
            # Check if it's the main title (usually first non-empty line)
            html.append(f'<h1>{line[2:]}</h1>')
            # Check for meta info on next line
            if i + 1 < len(lines) and '**' in lines[i+1]:
                meta_line = lines[i+1].replace('**', '')
                html.append(f'<p class="meta">{meta_line}</p>')
                i += 2
                continue
            i += 1
            continue
        
        # Section header
        if line.startswith('## '):
            html.append(f'<h2>{line[3:]}</h2>')
            i += 1
            continue
            
        # Subsection
        if line.startswith('### '):
            html.append(f'<h3>{line[4:]}</h3>')
            i += 1
            continue
            
        # Horizontal rule
        if line.strip() == '---':
            html.append('<hr>')
            i += 1
            continue
            
        # Table detection
        if '|' in line and line.strip().startswith('|'):
            # Collect all table rows
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i].rstrip())
                i += 1
            html.append(parse_table(table_lines))
            continue
        
        # List items
        if line.startswith('- ') or line.startswith('* '):
            html.append('<ul>')
            while i < len(lines) and (lines[i].startswith('- ') or lines[i].startswith('* ')):
                text = process_inline(lines[i][2:])
                html.append(f'<li>{text}</li>')
                i += 1
            html.append('</ul>')
            continue
        
        # Numbered list
        if re.match(r'^\d+\.\s', line):
            html.append('<ol>')
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                text = re.sub(r'^\d+\.\s', '', lines[i])
                html.append(f'<li>{process_inline(text)}</li>')
                i += 1
            html.append('</ol>')
            continue
        
        # Regular paragraph
        html.append(f'<p>{process_inline(line)}</p>')
        i += 1
    
    return '\n'.join(html)

def parse_table(lines):
    if len(lines) < 2:
        return ''
    
    # Parse header
    header_cells = [c.strip() for c in lines[0].split('|')[1:-1]]
    
    # Skip separator line (line 2)
    # Parse data rows
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells and any(c for c in cells):
            rows.append(cells)
    
    html = ['<table>', '<thead>', '<tr>']
    for h in header_cells:
        html.append(f'<th>{h}</th>')
    html.extend(['</tr>', '</thead>', '<tbody>'])
    
    for row in rows:
        html.append('<tr>')
        for cell in row:
            html.append(f'<td>{cell}</td>')
        html.append('</tr>')
    
    html.extend(['</tbody>', '</table>'])
    return '\n'.join(html)

def process_inline(text):
    import re
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic  
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Links
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output = create_professional_html(sys.argv[1])
        print(f'Created: {output}')
