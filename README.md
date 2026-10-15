# 📄 Smart PDF Merger

**A simple, user-friendly PDF and image merging application built with Python and Streamlit.**

Smart PDF Merger allows users to combine multiple PDFs and images into a single PDF document while maintaining complete control over file selection, document order, and output location.

The application provides an intuitive interface, native macOS folder selection, automatic file discovery, and automated setup using Python virtual environments.

## 🖥️ Application Preview

![Smart PDF Merger Application Preview](images/app-preview-01.png)

*Illustrative preview of the Smart PDF Merger interface.*

## ✨ Key Features

- 📂 **Native Folder Selection** — Browse and select source and destination folders using native macOS dialogs.
- 📄 **Multiple File Formats** — Merge PDF, JPG, JPEG, and PNG files into one PDF.
- 🔍 **Automatic File Discovery** — Automatically display supported files after selecting a source folder.
- ☑️ **Flexible File Selection** — Select individual files using checkboxes, or use Select All and Clear All.
- ⬆️ **Custom File Ordering** — Rearrange selected documents with up/down controls.
- 📑 **PDF Bookmarks** — Automatically create bookmarks based on the original filenames.
- 🖼️ **Image Conversion** — Convert JPG, JPEG, and PNG files into PDF pages while handling orientation and transparency.
- 💾 **Custom Output Location** — Choose your destination folder and merged PDF filename.
- 🛡️ **Overwrite Protection** — Prevent accidental overwriting of existing files.
- 🔒 **Local Processing** — Process documents locally without uploading them to a document-conversion service.
- 🚀 **Automated Setup** — Automatically create a virtual environment, install dependencies, and launch the application.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core application |
| Streamlit | Web-based user interface |
| pypdf | PDF merging and bookmarks |
| Pillow | Image processing and PDF conversion |
| AppleScript | Native macOS folder picker |
| Python venv | Virtual environment management |

## 📁 Project Structure

```text
smart-pdf-merger/
├── app.py
├── bootstrap.py
├── requirements.txt
├── README.md
├── .gitignore
├── images/
│   └── app-preview.png
└── Start PDF Merger.command   # Optional
```

The `.venv/` directory is created automatically during installation and should not be committed to Git.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.10 or later
- macOS for native folder-selection pop-ups
- Internet connection for the initial dependency installation

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

1. Checks the Python version.
2. Creates a `.venv` virtual environment if needed.
3. Installs the required libraries.
4. Verifies installed dependencies.
5. Launches the Streamlit application.

Open the application at:

**http://localhost:8501**

You do not need to activate the virtual environment manually.

### Option 2: Manual Setup

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the environment:

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

### Option 3: One-Click macOS Launcher

If the optional launcher is included, make it executable:

```bash
chmod +x "Start PDF Merger.command"
```

Double-click `Start PDF Merger.command` in Finder to run the application.

## 📖 How to Use

### Step 1: Select Source Folder

Click **Browse** to select the folder containing your PDF and image files.

The application automatically detects supported files in the selected folder.

### Step 2: Select Files

All supported files appear automatically with checkboxes.

For example:

```text
☑ Document_01.pdf
☑ Image_01.jpeg
☐ Document_02.pdf
☑ Image_02.png
```

Use **Select All** or **Clear All** to manage multiple files quickly.

### Step 3: Arrange Document Order

After selecting files, use the up/down arrows to specify the order in which they should appear in the merged PDF.

Example:

```text
1. Document_01.pdf
2. Image_01.jpeg
3. Document_02.pdf
4. Image_02.png
```

The first document in the list will appear first in the output PDF.

### Step 4: Select Destination Folder

Click **Browse** to select the folder where the final merged PDF should be saved.

### Step 5: Enter Output Filename

Specify the output filename:

```text
Merged_Documents.pdf
```

If the `.pdf` extension is missing, the application adds it automatically.

### Step 6: Merge Files

Click **Merge Files**.

The application combines the selected documents according to the specified sequence and saves the output to your selected destination folder.

A download option is displayed after successful merging.

## 📑 Automatic PDF Bookmarks

Smart PDF Merger creates a bookmark for each original source file,
