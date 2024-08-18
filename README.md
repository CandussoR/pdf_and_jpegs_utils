# Setup

* `git clone https://github.com/CandussoR/pdf_and_jpegs_utils.git`
* `python -m venv pdf_jpg_utils`
* `pdf_jpeg_utils/Scripts/Activate.ps1` if on Windows
    * `source pdf_jpg_utils/bin/activate` on linux
* `pip install Pillow`
* `pip install pypdf`

# Use Case
* `python image_maker.py path/to/file.jpg another/path/tofile.jpg --out path/to/out_file.jpg`
* `python pdf_maker.py path/to/folder/or/files --out some/pdf/path.pdf`
    * created for binding jpegs into a pdf, I don't if it would work for other formats.
* `python pdf_leaflet_maker.py path/to/files.jpg --out path/to/out_file.jpg [--delete]`