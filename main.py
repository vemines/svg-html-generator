import os
import base64
import json
import zlib

# Set the folder path to svg folder
folder_path = "D:/Image/undraw/"
# Set the output filename for the HTML file
file_name = "fileName.html"

def load_svgs_html(folder_path):
    svg_files = [f for f in os.listdir(folder_path) if f.endswith('.svg')]
    svg_data = []

    for svg_file in svg_files:
        svg_path = os.path.join(folder_path, svg_file)
        with open(svg_path, 'r', encoding='utf-8') as file:
            svg_content = file.read()
            svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
            svg_data.append({
                'file': svg_file,
                'content': svg_content,
                'base64': svg_base64
            })

    compressed_data = zlib.compress(json.dumps(svg_data).encode('utf-8'))
    compressed_base64 = base64.b64encode(compressed_data).decode('utf-8')

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SVG Preview</title>
  <style>
    body {{ font-family: Arial, sans-serif; }}
    .container {{ display: flex; flex-wrap: wrap; }}
    .svg-preview {{ margin: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }}
    svg {{ width: 200px; height: 200px; }}
    h3 {{ text-align: center; }}
    input {{ margin-bottom: 20px; padding: 10px; font-size: 16px; width: 300px; }}
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.0.4/pako.min.js"></script>
  <script>
    const compressedSvgData = '{compressed_base64}';

    function searchSVGs() {{
      var input = document.getElementById('searchInput').value.toLowerCase();
      var previews = document.getElementsByClassName('svg-preview');
      for (var i = 0; i < previews.length; i++) {{
        var fileName = previews[i].getElementsByTagName('h3')[0].innerText.toLowerCase();
        previews[i].style.display = fileName.includes(input) ? 'block' : 'none';
      }}
    }}

    function loadSVGs() {{
      var compressedData = atob(compressedSvgData);
      var binaryData = new Uint8Array(compressedData.length);
      for (var i = 0; i < compressedData.length; i++) {{
        binaryData[i] = compressedData.charCodeAt(i);
      }}
      var decompressedData = pako.inflate(binaryData, {{ to: 'string' }});
      var svgData = JSON.parse(decompressedData);
      
      var container = document.querySelector('.container');
      svgData.forEach(function(svg) {{
        var div = document.createElement('div');
        div.className = 'svg-preview';
        div.innerHTML = `
          <h3>${{svg.file}}</h3>
          <a href="data:image/svg+xml;base64,${{svg.base64}}" download="${{svg.file}}">
            ${{svg.content}}
          </a>
        `;
        container.appendChild(div);
      }});
    }}

    document.addEventListener('DOMContentLoaded', loadSVGs);
  </script>
</head>
<body>
  <h1>SVG Preview</h1>
  <input type="text" id="searchInput" placeholder="Search SVG files..." onkeyup="searchSVGs()">
  <div class="container"></div>
</body>
</html>
    '''
    return html_content

# Generate the HTML content
html_content = load_svgs_html(folder_path)

# Save the HTML file directly using the updated content
with open(file_name, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f'HTML preview created: {file_name}')