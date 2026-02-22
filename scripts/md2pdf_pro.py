#!/usr/bin/env python3
"""
Professional PDF Converter - Clean & Beautiful
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
            line-height: 1.6;
            color: #1a1a1a;
            padding: 40pt 50pt;
            max-width: 100%;
        }}
        
        h1 {{
            font-size: 24pt;
            font-weight: 700;
            color: #111;
            margin-bottom: 6pt;
            padding-bottom: 12pt;
            border-bottom: 2pt solid #000;
            letter-spacing: -0.5pt;
        }}
        
        .meta {{
            font-size: 9pt;
            color: #666;
            margin-bottom: 30pt;
            padding-bottom: 20pt;
            border-bottom: 1pt solid #e0e0e0;
        }}
        
        h2 {{
            font-size: 14pt;
            font-weight: 600;
            color: #222;
            margin-top: 24pt;
            margin-bottom: 12pt;
            padding-bottom: 6pt;
            border-bottom: 1pt solid #ddd;
        }}
        
        h3 {{
            font-size: 11pt;
            font-weight: 600;
            color: #333;
            margin-top: 16pt;
            margin-bottom: 8pt;
        }}
        
        p {{
            margin-bottom: 8pt;
            text-align: justify;
        }}
        
        ul, ol {{
            margin-left: 16pt;
            margin-bottom: 12pt;
        }}
        
        li {{
            margin-bottom: 4pt;
        }}
        
        strong {{
            font-weight: 600;
        }}
        
        .highlight-box {{
            background: #f8f9fa;
            border-left: 3pt solid #333;
            padding: 12pt 16pt;
            margin: 16pt 0;
        }}
        
        .section {{
            margin-bottom: 20pt;
        }}
        
        .two-col {{
            display: table;
            width: 100%;
            margin: 12pt 0;
        }}
        
        .two-col > div {{
            display: table-cell;
            width: 50%;
            padding: 8pt;
            vertical-align: top;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
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
            padding: 6pt 10pt;
            border: 1pt solid #ddd;
            background: #fff;
        }}
        
        tr:nth-child(even) td {{
            background: #fafafa;
        }}
        
        hr {{
            border: none;
            border-top: 1pt solid #e0e0e0;
            margin: 24pt 0;
        }}
        
        .footer {{
            font-size: 9pt;
            color: #888;
            margin-top: 30pt;
            padding-top: 12pt;
            border-top: 1pt solid #e0e0e0;
        }}
        
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
    </style>
</head>
<body>
{parse_content(content)}
</body>
</html>'''
    
    output = md_file.replace('.md', '_professional.html')
    with open(output, 'w') as f:
        f.write(html)
    return output

def parse_content(content):
    import re
    
    lines = content.split('\n')
    html = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html.append('</ul>')
                in_list = False
            continue
            
        # Title
        if line.startswith('# '):
            html.append(f'<h1>{line[2:]}</h1>')
            
        # Section header
        elif line.startswith('## '):
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append(f'<h2>{line[3:]}</h2>')
            
        # Subsection
        elif line.startswith('### '):
            html.append(f'<h3>{line[4:]}</h3>')
            
        # Horizontal rule
        elif line == '---':
            html.append('<hr>')
            
        # List items
        elif line.startswith('- ') or line.startswith('* '):
            text = process_inline(line[2:])
            if not in_list:
                html.append('<ul>')
                in_list = True
            html.append(f'<li>{text}</li>')
            
        # Numbered list
        elif re.match(r'^\d+\.\s', line):
            match = re.match(r'^(\d+)\.\s(.*)', line)
            if match:
                num, text = match.groups()
                text = process_inline(text)
                if not in_list:
                    html.append('<ol>')
                    in_list = True
                html.append(f'<li>{text}</li>')
            
        # Regular paragraph
        else:
            if in_list:
                html.append('</ul>' if '<ul>' in ''.join(html[-5:]) else '</ol>')
                in_list = False
            html.append(f'<p>{process_inline(line)}</p>')
    
    if in_list:
        html.append('</ul>' if '<ul>' in ''.join(html[-5:]) else '</ol>')
    
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
