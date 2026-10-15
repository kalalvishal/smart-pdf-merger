from pathlib import Path
from io import BytesIO
from pypdf import PdfWriter
from PIL import Image, ImageOps

# Folder containing source documents
folder = Path("/Users/vishalkalal/Documents/pdfmerge/input")

# Select files in your preferred order
selected_files = [
    "Sep15.pdf",
    "Aug30.pdf",
    "Aug15.pdf",
    "July30.pdf",
    "July15.pdf",
    "June30.pdf",
]

# Output file
output = folder / "Paystubs.pdf"

writer = PdfWriter()

for filename in selected_files:
    file_path = folder / filename

    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {filename}")

    extension = file_path.suffix.lower()

    print(f"Adding: {filename}")

    if extension == ".pdf":
        writer.append(
            str(file_path),
            outline_item=file_path.stem
        )

    elif extension in [".jpg", ".jpeg", ".png"]:
        with Image.open(file_path) as original:
            image = ImageOps.exif_transpose(original)

            # Handle transparency with a white background
            image = image.convert("RGBA")
            background = Image.new(
                "RGB", image.size, "white"
            )
            background.paste(image, mask=image.getchannel("A"))

            # Convert image to PDF in memory
            pdf_buffer = BytesIO()
            background.save(pdf_buffer, format="PDF")
            pdf_buffer.seek(0)

            # Add image PDF to merged document
            writer.append(
                pdf_buffer,
                outline_item=file_path.stem
            )

    else:
        raise ValueError(f"Unsupported file: {filename}")

# Save final PDF
with open(output, "wb") as f:
    writer.write(f)

writer.close()

print(f"\nMerged PDF saved to: {output}")