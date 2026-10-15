
import platform
import subprocess
from pathlib import Path
from io import BytesIO

import streamlit as st
from PIL import Image, ImageOps
from pypdf import PdfWriter


# -----------------------------------------
# Application Configuration
# -----------------------------------------

st.set_page_config(
    page_title="PDF Merger",
    page_icon="📄",
    layout="wide"
)

st.title("📄 PDF & Image Merger")
st.caption("Select files, arrange their order, and merge into one PDF.")

SUPPORTED = {".pdf", ".jpg", ".jpeg", ".png"}


# -----------------------------------------
# Session State
# -----------------------------------------

defaults = {
    "source_folder": "",
    "destination_folder": "",
    "source_text": "",
    "destination_text": "",
    "file_order": [],
    "available_files": [],
    "output_filename": "Final_Merged.pdf",
    "merged_path": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------------------
# Native macOS Folder Picker
# -----------------------------------------

def choose_folder(prompt):

    if platform.system() != "Darwin":
        st.warning("Folder picker requires macOS.")
        return None

    script = """
    on run argv
        try
            set chosen to choose folder with prompt (item 1 of argv)
            return POSIX path of chosen
        on error number -128
            return ""
        end try
    end run
    """

    result = subprocess.run(
        ["osascript", "-e", script, prompt],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        st.error(result.stderr.strip() or "Folder picker failed.")
        return None

    return result.stdout.strip() or None


# -----------------------------------------
# Discover Supported Files
# -----------------------------------------

def find_files(folder):

    path = Path(folder).expanduser()

    if not path.is_dir():
        return []

    return sorted(
        [
            file.name
            for file in path.iterdir()
            if file.is_file()
            and file.suffix.lower() in SUPPORTED
        ],
        key=str.lower
    )


# -----------------------------------------
# Refresh Files Automatically
# -----------------------------------------

def refresh_files():

    folder = st.session_state.source_folder
    files = find_files(folder) if folder else []

    # Remove old checkbox keys
    for key in list(st.session_state.keys()):
        if key.startswith("file_checkbox_"):
            del st.session_state[key]

    st.session_state.available_files = files
    st.session_state.file_order = []
    st.session_state.merged_path = None


def browse_source():

    folder = choose_folder("Select Source Folder")

    if folder:
        st.session_state.source_folder = folder
        st.session_state.source_text = folder
        refresh_files()


def source_changed():

    st.session_state.source_folder = (
        st.session_state.source_text.strip()
    )

    refresh_files()


def browse_destination():

    folder = choose_folder("Select Destination Folder")

    if folder:
        st.session_state.destination_folder = folder
        st.session_state.destination_text = folder
        st.session_state.merged_path = None


def destination_changed():

    st.session_state.destination_folder = (
        st.session_state.destination_text.strip()
    )

    st.session_state.merged_path = None


# -----------------------------------------
# Checkbox Selection
# -----------------------------------------

def checkbox_key(filename):
    return f"file_checkbox_{filename}"


def select_all():

    for filename in st.session_state.available_files:
        st.session_state[checkbox_key(filename)] = True


def clear_all():

    for filename in st.session_state.available_files:
        st.session_state[checkbox_key(filename)] = False


# -----------------------------------------
# Rearrange Order
# -----------------------------------------

def move_file(index, direction):

    order = st.session_state.file_order
    new_index = index + direction

    if 0 <= new_index < len(order):
        order[index], order[new_index] = (
            order[new_index],
            order[index]
        )


# -----------------------------------------
# Convert Image to PDF
# -----------------------------------------

def image_to_pdf(path):

    with Image.open(path) as original:

        image = ImageOps.exif_transpose(original)
        image = image.convert("RGBA")

        background = Image.new(
            "RGB",
            image.size,
            "white"
        )

        background.paste(
            image,
            mask=image.getchannel("A")
        )

        buffer = BytesIO()

        background.save(buffer, format="PDF")
        buffer.seek(0)

        return buffer


# -----------------------------------------
# Merge Selected Documents
# -----------------------------------------

def merge_documents(source, files, output):

    writer = PdfWriter()
    buffers = []

    try:

        for filename in files:

            path = source / filename

            if not path.is_file():
                raise FileNotFoundError(filename)

            extension = path.suffix.lower()

            if extension == ".pdf":

                writer.append(
                    str(path),
                    outline_item=path.stem
                )

            elif extension in {".jpg", ".jpeg", ".png"}:

                buffer = image_to_pdf(path)
                buffers.append(buffer)

                writer.append(
                    buffer,
                    outline_item=path.stem
                )

            else:
                raise ValueError(f"Unsupported file: {filename}")

        # Exclusive creation prevents overwriting
        with output.open("xb") as f:
            writer.write(f)

    finally:

        writer.close()

        for buffer in buffers:
            buffer.close()


# =========================================
# 1. SOURCE FOLDER
# =========================================

st.subheader("1. Select Source Folder")

col1, col2 = st.columns(
    [5, 1],
    vertical_alignment="bottom"
)

with col1:

    st.text_input(
        "Source Folder",
        key="source_text",
        on_change=source_changed
    )

with col2:

    st.button(
        "📂 Browse",
        key="browse_source",
        on_click=browse_source,
        use_container_width=True
    )


# =========================================
# 2. AUTOMATIC FILE CHECKBOXES
# =========================================

source = st.session_state.source_folder
available_files = st.session_state.available_files

if source and Path(source).expanduser().is_dir():

    st.markdown("### Files in Selected Folder")

    st.caption(
        f"{len(available_files)} supported files found"
    )

    if available_files:

        col_all, col_clear = st.columns(2)

        with col_all:

            st.button(
                "☑ Select All",
                on_click=select_all,
                use_container_width=True
            )

        with col_clear:

            st.button(
                "☐ Clear All",
                on_click=clear_all,
                use_container_width=True
            )

        # Display checkboxes automatically
        with st.container(border=True):

            for filename in available_files:

                extension = Path(filename).suffix.lower()

                icon = (
                    "📕"
                    if extension == ".pdf"
                    else "🖼️"
                )

                st.checkbox(
                    f"{icon} {filename}",
                    key=checkbox_key(filename)
                )

        # Determine selected files
        selected_files = [
            filename
            for filename in available_files
            if st.session_state.get(
                checkbox_key(filename),
                False
            )
        ]

        # Preserve existing order
        order = [
            filename
            for filename in st.session_state.file_order
            if filename in selected_files
        ]

        # Add newly checked files
        for filename in selected_files:

            if filename not in order:
                order.append(filename)

        st.session_state.file_order = order

        st.write(
            f"**Selected: {len(selected_files)} "
            f"of {len(available_files)} files**"
        )

    else:

        st.warning(
            "No PDF, JPG, JPEG, or PNG files found."
        )

elif source:

    st.error("Source folder does not exist.")

else:

    st.info("Choose a source folder to display files.")


# =========================================
# 3. REARRANGE FILES
# =========================================

if st.session_state.file_order:

    st.divider()

    st.subheader("2. Arrange File Order")

    st.caption(
        "Files will merge in the sequence displayed below."
    )

    for index, filename in enumerate(
        st.session_state.file_order
    ):

        col_num, col_name, col_up, col_down = st.columns(
            [0.6, 7, 1, 1],
            vertical_alignment="center"
        )

        with col_num:
            st.write(f"**{index + 1}.**")

        with col_name:
            st.write(filename)

        with col_up:

            if st.button(
                "⬆️",
                key=f"up_{index}",
                disabled=index == 0
            ):
                move_file(index, -1)
                st.rerun()

        with col_down:

            if st.button(
                "⬇️",
                key=f"down_{index}",
                disabled=(
                    index ==
                    len(st.session_state.file_order) - 1
                )
            ):
                move_file(index, 1)
                st.rerun()


# =========================================
# 4. DESTINATION FOLDER
# =========================================

st.divider()

st.subheader("3. Select Destination Folder")

col1, col2 = st.columns(
    [5, 1],
    vertical_alignment="bottom"
)

with col1:

    st.text_input(
        "Destination Folder",
        key="destination_text",
        on_change=destination_changed
    )

with col2:

    st.button(
        "📂 Browse",
        key="browse_destination",
        on_click=browse_destination,
        use_container_width=True
    )


# =========================================
# 5. OUTPUT FILENAME
# =========================================

st.subheader("4. Output Filename")

st.text_input(
    "Enter Output PDF Filename",
    key="output_filename"
)


# =========================================
# 6. MERGE
# =========================================

st.divider()

if st.button(
    "🚀 Merge Files",
    type="primary",
    use_container_width=True
):

    try:

        source_path = Path(
            st.session_state.source_folder
        ).expanduser()

        destination_text = (
            st.session_state.destination_folder
        )

        destination = Path(
            destination_text
        ).expanduser()

        filename = (
            st.session_state.output_filename.strip()
        )

        order = st.session_state.file_order

        if not source_path.is_dir():
            raise ValueError("Select a valid source folder.")

        if not order:
            raise ValueError("Select at least one file.")

        if not destination_text or not destination.is_dir():
            raise ValueError("Select a valid destination folder.")

        if (
            not filename
            or Path(filename).name != filename
            or filename in {".", ".."}
            or "/" in filename
            or "\\" in filename
        ):
            raise ValueError("Enter a valid output filename.")

        if not filename.lower().endswith(".pdf"):
            filename += ".pdf"

        output = destination / filename

        source_paths = {
            (source_path / name).resolve()
            for name in order
        }

        if output.resolve() in source_paths:
            raise ValueError(
                "Output cannot overwrite a source document."
            )

        if output.exists():
            raise ValueError(
                "Output file already exists. Choose another name."
            )

        with st.spinner("Merging documents..."):

            merge_documents(
                source_path,
                order,
                output
            )

        st.session_state.merged_path = str(output)

        st.success(
            f"PDF created successfully: {output}"
        )

    except Exception as e:

        st.error(str(e))


# =========================================
# DOWNLOAD FINAL PDF
# =========================================

result = st.session_state.merged_path

if result and Path(result).is_file():

    with open(result, "rb") as f:

        st.download_button(
            "⬇️ Download Merged PDF",
            data=f.read(),
            file_name=Path(result).name,
            mime="application/pdf",
            use_container_width=True
        )
