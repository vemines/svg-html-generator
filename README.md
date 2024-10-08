# svg-html-preview

A Python-based tool that generates HTML pages for previewing, searching by name, and downloading SVG files. This tool allows users to quickly browse and download SVGs, offering a clean and intuitive interface.

# SVG - HTML PREVIEW GENERATOR

This Python tool generates HTML pages that allow you to:

- Preview SVG files
- Search SVGs by name
- Download SVG files directly from the preview page

## Features

- **SVG Previews**: Automatically renders previews of all SVG files within a specified directory.
- **Search by Name**: Quickly search for SVG files using a built-in search bar.
- **Download SVGs**: Users can download any SVG file by clicking on the preview.

## Requirements

To run this project, you need to have Python installed.
If you don’t have Python installed, download it from the official Python website:  
[Download Python](https://www.python.org/downloads/)

## Usage

1. Clone this repository to your local machine:

```bash
git clone https://github.com/vemines/svg-html-preview.git
```

Before running the script, you need to modify the following lines in [`main.py`](./main.py):

2. **Set the folder path** (Line 7): Update the [`folder_path`](./main.py#L7) variable to point to the directory where your SVG files are stored.

```python
# Set the folder path to svg folder
folder_path = "D:/svg-file-path"
```

3. **Set the output file name** (Line 9): Modify the [`file_name`](./main.py#L9) variable to define the name of the output HTML file.

```python
# Set the output filename for the HTML file
file_name = "fileName.html"
```

4. Execute the Python script to generate the HTML preview:

```bash
py main.py
```

## Note

If main.py output can't render all svg. Use main2.py, it have pagination
