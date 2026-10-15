# 📄 Smart PDF Merger

**A simple, local PDF and image merging application built with Python and Streamlit.**

Smart PDF Merger allows users to combine multiple PDF documents and images into a single PDF while maintaining complete control over document selection, merge order, and output location.

The application features a user-friendly web interface, native macOS folder selection, automatic file discovery, and one-command environment setup.

## ✨ Features

- **Multiple File Formats:** Supports PDF, JPG, JPEG, and PNG.
- **Native macOS Folder Picker:** Browse source and destination folders through native macOS dialogs.
- **Automatic File Discovery:** Automatically displays supported files after selecting a source folder.
- **Selective Merging:** Use checkboxes to choose exactly which files to include.
- **Custom File Ordering:** Rearrange selected documents using up/down controls before merging.
- **PDF Bookmarks:** Automatically creates bookmarks using the original filenames.
- **Image-to-PDF Conversion:** Converts supported images into PDF pages, handling image orientation and transparency.
- **Custom Output:** Choose the destination folder and output filename.
- **Overwrite Protection:** Prevents accidental replacement of existing output files.
- **Local Processing:** Documents are processed locally without requiring a cloud-based conversion service.
- **Automated Setup:** A bootstrap script creates the Python virtual environment, installs dependencies, and launches the application.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Interactive web interface |
| pypdf | PDF merging and bookmarks |
| Pillow (PIL) | Image processing and PDF conversion |
| AppleScript | Native macOS folder selection |
| venv | Isolated Python environment |

## 📁 Project Structure

```text
smart-pdf-merger/
├── app.py
├── bootstrap.py
├── requirements.txt
├── README.md
├── .gitignore
└── Start PDF Merger.command    # Optional macOS launcher
```

The `.venv/` directory is automatically created during setup and should not be committed to Git.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- macOS for native folder-selection dialogs
- Internet connection for initial dependency installation

The application also supports manually entered folder paths when native macOS dialogs are unavailable.

### Option 1: Automatic Setup (Recommended)

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/smart-pdf-merger.git
cd smart-pdf-merger
```

Run the bootstrap script:

```bash
python3 bootstrap.py
```

The bootstrap script automatically:

1. Verifies the Python version.
2. Creates a virtual environment if one does not exist.
3. Installs dependencies from `requirements.txt`.
4. Verifies the required Python libraries.
5. Launches the Streamlit application.

Open the application in your browser:

**http://localhost:8501**

### Option 2: Manual Installation

Clone the repository and navigate to the project directory.

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch the application:

```bash
streamlit run app.py
```

### Option 3: macOS Launcher (Optional)

If the repository includes `Start PDF Merger.command`, make it executable:

```bash
chmod +x "Start PDF Merger.command"
```

You can then launch the application through Finder by double-clicking the launcher.

## 📖 How to Use

### Step 1: Select Source Folder

Click **Browse** to select the folder containing the documents you want to merge.

The application automatically discovers PDF, JPG, JPEG, and PNG files in that folder.

Only files directly inside the selected folder are listed; subfolders are not scanned.

### Step 2: Select Files

All discovered files appear as individual checkboxes.

- Check the files you want to merge.
- Use **Select All** to select every supported file.
- Use **Clear All** to remove all selections.

### Step 3: Arrange File Order

Selected files appear in the merge-order section.

Use the up/down arrow buttons to rearrange their sequence.

The first item in the list becomes the first document in the merged PDF.

**Example:**

```text
1. Cover_Letter.pdf
2. Passport.jpeg
3. Experience_Letter.pdf
4. Certificate.png
```

### Step 4: Select Destination Folder

Click **Browse** to choose where the final merged PDF should be saved.

### Step 5: Enter Output Filename

Enter a filename, such as:

```text
Final_Documents.pdf
```

The application automatically adds the `.pdf` extension if it is missing.

### Step 6: Merge Documents

Click **Merge Files**.

The application processes the selected documents in the specified order and saves the merged PDF to your selected destination.

A download option is also displayed after successful merging.

## 📑 PDF Bookmark Support

Smart PDF Merger automatically adds bookmarks based on the original source filenames.

For example:

```text
Final_Documents.pdf
├── Cover_Letter
├── Passport
├── Experience_Letter
└── Certificate
```

This makes it easier to navigate large merged documents.

## 🖼️ Supported File Formats

| File Format | Supported | Processing |
|---|---|---|
| PDF | ✅ | Merged directly |
| JPG | ✅ | Converted to PDF |
| JPEG | ✅ | Converted to PDF |
| PNG | ✅ | Converted to PDF |

Images are added as PDF pages, using their image dimensions rather than automatically resizing them to A4 or Letter paper.

## 🔒 Privacy and Security

Smart PDF Merger is designed for local execution.

- Files are read from user-selected local folders.
- PDF merging takes place locally.
- No cloud document-conversion API is required.
- Original source documents are not modified.
- Existing output files are protected from accidental overwriting.

The initial dependency installation requires internet access, and Streamlit may provide its usual optional telemetry functionality.

## ⚙️ Configuration

Dependencies are listed in `requirements.txt`:

```text
streamlit>=1.36
pypdf>=4.0
Pillow>=10.0
```

The bootstrap script installs these dependencies in an isolated `.venv` environment.

## 🧭 Platform Compatibility

| Platform | Application | Native Folder Picker |
|---|---|---|
| macOS | ✅ | ✅ |
| Windows | Python/Streamlit compatible | Manual path entry |
| Linux | Python/Streamlit compatible | Manual path entry |

The native Finder-style folder picker is implemented using AppleScript and is available only when the application runs locally on macOS.

## 🗺️ Future Enhancements

Potential enhancements include:

- [ ] Drag-and-drop file reordering
- [ ] PDF and image previews before merging
- [ ] Individual PDF page selection
- [ ] A4 and Letter page-size options
- [ ] PDF compression
- [ ] Password-protected PDF support
- [ ] Windows and Linux native folder pickers
- [ ] Packaged desktop application

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request explaining your changes.

## 📜 License

Add a license file to the repository if you intend to distribute or accept contributions under an open-source license. The MIT License is one possible choice.

## ⭐ Support

If you find Smart PDF Merger useful, consider starring the GitHub repository.

Feedback and feature suggestions are welcome through GitHub Issues.

---

**Built with Python, Streamlit, pypdf, and Pillow.**
