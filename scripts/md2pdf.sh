#!/bin/bash
# Convert markdown to PDF using OpenClaw browser

MARKDOWN_FILE=$1
OUTPUT_FILE=${2:-"$(basename $MARKDOWN_FILE .md).pdf"}

# Convert markdown to HTML with styling
python3 << 'EOF'
import sys
import markdown2

with open(sys.argv[1], 'r') as f:
    md_content = f.read()

html = markdown2.markdown(md_content)

css = '''
<style>
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; margin: 40px; line-height: 1.6; color: #333; }
h1 { color: #1a1a1a; border-bottom: 2px solid #333; padding-bottom: 10px; font-size: 28px; }
h2 { color: #333; margin-top: 30px; font-size: 22px; }
h3 { color: #555; font-size: 18px; }
table { border-collapse: collapse; width: 100%; margin: 20px 0; }
th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
th { background-color: #f5f5f5; font-weight: 600; }
ul, ol { padding-left: 25px; }
li { margin: 6px 0; }
blockquote { border-left: 4px solid #ddd; margin: 20px 0; padding-left: 20px; color: #666; font-style: italic; }
code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 14px; }
pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
</style>
'''

full_html = f'<html><head><meta charset="utf-8">{css}</head><body>{html}</body></html>'
with open('/tmp/markdown_convert.html', 'w') as f:
    f.write(full_html)
print('HTML created at /tmp/markdown_convert.html')
EOF

MARKDOWN_FILE

echo "HTML created. Now converting to PDF..."

# The HTML file is ready at /tmp/markdown_convert.html
# User needs to open it in browser and print to PDF
echo "Done! Open /tmp/markdown_convert.html in browser and print to PDF"
