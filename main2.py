import os
import base64
import json
import zlib

# Set the folder path to SVG folder
folder_path = "D:/Code/web-assets/svgs/solid"
# Set the base output filename
file_name = "fa-solid"
# Set Icon width
icon_width = 200
# Set Icon height
icon_height = 200
# Set number item per page
per_page = 300

def load_svgs_html(folder_path, file_name):
    svg_files = [f for f in os.listdir(folder_path) if f.endswith('.svg')]
    total_files = len(svg_files)

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

    # Create the HTML filename
    html_file_name = f"{file_name}.html"
    
    # Update the HTML content to include pagination and search functionality
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{file_name}</title>
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
    h3 {{ text-align: center; font-size: 20px; }}
    input {{ margin-bottom: 20px; padding: 10px; font-size: 16px; width: 300px; }}
    .pagination {{
      position: fixed;
      bottom: 20px;
      right: 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .pagination button {{
      padding: 10px;
      font-size: 24px;
      font-weight: bold;
      border: none;
      border-radius: 5px;
      background-color: #007BFF;
      color: white;
      cursor: pointer;
      transition: background-color 0.3s;
      margin: 5px 0;
      width: 40px; /* Make buttons square */
      height: 40px; /* Make buttons square */
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .pagination button:disabled {{
      background-color: #ccc;
      cursor: not-allowed;
    }}
    .pagination span {{
      font-size: 16px;
      margin: 10px 0;
    }}
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.0.4/pako.min.js"></script>
  <script>
    const compressedSvgData = '{compressed_base64}';
    let svgData = [];
    const itemsPerPage = {per_page};
    let currentPage = 0;
    let filteredData = [];
    let isRendering = false; // Flag to prevent multiple render calls

    function debounce(func, delay) {{
      let timeout;
      return function(...args) {{
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
      }};
    }}

    function searchSVGs() {{
      const input = document.getElementById('searchInput').value.toLowerCase();
      filteredData = svgData.filter(svg => svg.file.toLowerCase().includes(input));
      currentPage = 0; // Reset to first page
      renderPage(currentPage);
    }}

    function loadSVGs() {{
      const compressedData = atob(compressedSvgData);
      const binaryData = new Uint8Array(compressedData.length);
      for (let i = 0; i < compressedData.length; i++) {{
        binaryData[i] = compressedData.charCodeAt(i);
      }}
      const decompressedData = pako.inflate(binaryData, {{ to: 'string' }});
      svgData = JSON.parse(decompressedData);
      filteredData = svgData; // Initialize with all data
      renderPage(currentPage);
    }}

    const renderPage = debounce((page) => {{
      if (isRendering) return; // Prevent multiple render calls
      isRendering = true; // Set rendering flag

      const container = document.querySelector('.container');
      container.innerHTML = '';
      const start = page * itemsPerPage;
      const end = Math.min(start + itemsPerPage, filteredData.length);
      
      for (let i = start; i < end; i++) {{
        const svg = filteredData[i];
        const div = document.createElement('div');
        div.className = 'svg-preview';
        const iframeSrc = 'data:image/svg+xml;base64,' + svg.base64;

        div.innerHTML = `
            <h3>${{svg.file}}</h3>
            <div class="iframe-container">
                <iframe src="${{iframeSrc}}" scrolling="no" frameborder="0"></iframe>
            </div>
            <a class="download-link" href="${{iframeSrc}}" download="${{svg.file}}"></a>
        `;
        container.appendChild(div);
      }}

      updatePagination();
      isRendering = false; // Reset rendering flag
    }}, 100); // Adjust delay as needed

    function updatePagination() {{
      const pagination = document.querySelector('.pagination');
      const totalPages = Math.ceil(filteredData.length / itemsPerPage);
      pagination.innerHTML = `
          <button onclick="changePage(currentPage - 1)" ${{
              currentPage === 0 ? 'disabled' : ''
          }}><</button>
          <span>${{currentPage + 1}} / ${{totalPages}}</span>
          <button onclick="changePage(currentPage + 1)" ${{
              currentPage >= totalPages - 1 ? 'disabled' : ''
          }}>></button>
      `;
    }}

    function changePage(newPage) {{
      const totalPages = Math.ceil(filteredData.length / itemsPerPage);
      if (newPage >= 0 && newPage < totalPages) {{
        currentPage = newPage;
        renderPage(currentPage);
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }}
    }}

    document.addEventListener('DOMContentLoaded', loadSVGs);
  </script>
</head>
<body>
  <h1>{file_name}</h1>
  <input type="text" id="searchInput" placeholder="Search SVG files..." onkeyup="searchSVGs()">
  <div class="container"></div>
  <div class="pagination"></div>
</body>
</html>
    '''
    
    # Save the HTML file
    with open(html_file_name, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f'SVG preview created: {html_file_name}')

# Generate the HTML content
load_svgs_html(folder_path, file_name)
