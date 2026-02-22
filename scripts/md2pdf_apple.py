#!/usr/bin/env python3
"""
Apple-style Professional PDF Converter
"""

def create_apple_style_html(md_file):
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Report</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Text:wght@300;400;500;600&family=SF+Pro+Display:wght@400;500;600;700&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'WenQuanYi Micro Hei', -apple-system, sans-serif;
            font-size: 13px;
            line-height: 1.6;
            color: #1d1d1f;
            background: #fff;
            padding: 60px 80px;
            max-width: 900px;
            margin: 0 auto;
        }
        
        h1 {
            font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'WenQuanYi Micro Hei', -apple-system, sans-serif;
            font-size: 48px;
            font-weight: 600;
            color: #000;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }
        
        .subtitle {
            font-size: 21px;
            font-weight: 400;
            color: #86868b;
            margin-bottom: 60px;
            padding-bottom: 40px;
            border-bottom: 1px solid #d2d2d7;
        }
        
        h2 {
            font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'WenQuanYi Micro Hei', -apple-system, sans-serif;
            font-size: 32px;
            font-weight: 600;
            color: #000;
            margin-top: 56px;
            margin-bottom: 24px;
        }
        
        h3 {
            font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'WenQuanYi Micro Hei', -apple-system, sans-serif;
            font-size: 22px;
            font-weight: 600;
            color: #000;
            margin-top: 36px;
            margin-bottom: 16px;
        }
        
        p {
            margin-bottom: 16px;
            color: #1d1d1f;
        }
        
        ul, ol {
            margin-left: 24px;
            margin-bottom: 24px;
        }
        
        li {
            margin-bottom: 8px;
        }
        
        strong {
            font-weight: 600;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 32px 0;
            font-size: 13px;
        }
        
        th {
            border-radius: 10px 10px 0 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff;
            color: #1d1d1f;
            font-weight: 600;
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid #d2d2d7;
        }
        
        th:first-child {
            border-radius: 12px 0 0 0;
        }
        
        th:last-child {
            border-radius: 0 12px 0 0;
        }
        
        td {
            padding: 14px 16px;
            border-bottom: 1px solid #d2d2d7;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        .highlight {
            background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
        }
        
        .box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff;
            border-radius: 20px;
            padding: 32px;
            margin: 32px 0;
        }
        
        .box h3 {
            margin-top: 0;
            margin-bottom: 16px;
        }
        
        hr {
            border: none;
            border-top: 1px solid #d2d2d7;
            margin: 56px 0;
        }
        
        .footer {
            margin-top: 80px;
            padding-top: 24px;
            border-top: 1px solid #d2d2d7;
            font-size: 13px;
            color: #86868b;
        }
        
        a {
            color: #007AFF;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        .tag {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
            color: #1d1d1f;
            margin-right: 8px;
        }
        
        .tag.blue {
            background: #e3f2fd;
            color: #007AFF;
        }
        
        .tag.green {
            background: #e8f5e9;
            color: #34c759;
        }
        
        .tag.orange {
            background: #fff3e0;
            color: #ff9500;
        }
    </style>
</head>
<body>
'''
    
    with open(md_file, 'r') as f:
        content = f.read()
    
    html += parse_content(content)
    html += '</body></html>'
    
    output = md_file.replace('.md', '_apple.html')
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
        
        if not line.strip():
            i += 1
            continue
        
        # Title
        if line.startswith('# '):
            html.append(f'<h1>{line[2:]}</h1>')
            # Check for subtitle
            if i + 1 < len(lines) and '**' in lines[i+1]:
                meta = lines[i+1].replace('**', '').strip()
                html.append(f'<p class="subtitle">{meta}</p>')
                i += 2
                continue
            i += 1
            continue
        
        # Section
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
        
        # Table
        if '|' in line and line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i].rstrip())
                i += 1
            html.append(parse_table(table_lines))
            continue
        
        # List
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
    
    headers = [c.strip() for c in lines[0].split('|')[1:-1]]
    
    html = ['<table>', '<thead>', '<tr>']
    for h in headers:
        html.append(f'<th>{h}</th>')
    html.extend(['</tr>', '</thead>', '<tbody>'])
    
    for line in lines[2:]:
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if cells and any(c for c in cells):
            html.append('<tr>')
            for cell in cells:
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
    
    html.extend(['</tbody>', '</table>'])
    return '\n'.join(html)

def process_inline(text):
    import re
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        output = create_apple_style_html(sys.argv[1])
        print(f'Created: {output}')
