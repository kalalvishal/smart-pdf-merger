# Local PDF & Image Merger

Select files from a local folder, rearrange them, and merge them into a PDF with bookmarks.

## macOS setup

```bash
cd PDFMergerApp
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit opens in your browser (usually http://localhost:8501). Enter your source and destination folder paths. Select PDFs, JPGs, JPEGs and PNGs, rearrange using arrow buttons, then merge.

Notes:
- The paths refer to the computer running Streamlit. Run it locally for access to Mac files.
- Source PDFs are included with all pages; each image becomes one page.
- A bookmark is added for each original document.
- The app refuses to overwrite an existing output file.
- Password-protected PDFs are not supported.
