import os
import base64
import json
import zlib

# Set the folder path to svg folder
folder_path = "D:/Code/web-assets/svgs/solid"
# Set the output filename for the HTML file
file_name = "fa-solid"
# Set Icon width
icon_width = 200
# Set Icon height
icon_height = 200

def load_svgs_html(folder_path):
    svg_files = [f for f in os.listdir(folder_path) if f.endswith('.svg')]
    total_files = len(svg_files)

    # Calculate total pages
    total_pages = (total_files + items_per_page - 1) // items_per_page

    for page in range(total_pages):
        svg_data = []
        current_files = svg_files[page * items_per_page:(page + 1) * items_per_page]

        for svg_file in current_files:
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

        # Create unique HTML filename
        html_file_name = f"{file_name}-{page + 1}.html"

        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SVG Preview</title>
  <style>
    body {{ font-family: Arial, sans-serif; }}
    .container {{ display: flex; flex-wrap: wrap; }}
    .svg-preview {{ width: {icon_width}px; margin: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; position: relative; }}
    iframe {{ width: 100%; height: 100%; border: none; }}
    .iframe-container {{
      width: {icon_width}px;
      height: {icon_height}px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }}
    .iframe-container iframe {{
      object-fit: contain;
      width: 100%;
      height: 100%;
    }}
    .download-link {{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0);
      cursor: pointer;
    }}
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
        var iframeSrc = 'data:image/svg+xml;base64,' + svg.base64;
        
        div.innerHTML = `
          <h3>${{svg.file}}</h3>
          <div class="iframe-container">
            <iframe src="${{iframeSrc}}" scrolling="no" frameborder="0"></iframe>
          </div>
          <a class="download-link" href="${{iframeSrc}}" download="${{svg.file}}"></a>
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

# Create the HTML filename
html_file_name = f"{file_name}.html"

# Save the HTML file directly using the updated content
with open(html_file_name, 'w', encoding='utf-8') as file:
    file.write(html_content)

print(f'HTML preview created: {html_file_name}')
