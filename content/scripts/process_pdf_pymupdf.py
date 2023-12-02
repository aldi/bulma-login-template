import fitz  # PyMuPDF
import re

# Function to extract text, formulas, and images from a PDF page
def extract_content_from_page(doc, page):
    extracted_text = ""

    # Extract text
    text = page.get_text()
    extracted_text += text + "\n"

    # Extract images
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_path = f"extracted_image_{page.number}_{img_index}.{image_ext}"
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        extracted_text += f"[Image: {image_path}]\n"

    # Extract mathematical formulas (basic detection)
    formulas = re.findall(r'\$(.*?)\$', text)
    for formula in formulas:
        extracted_text += f"Formula: {formula}\n"

    return extracted_text

# Main function to process the PDF
def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_extracted_content = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_content = extract_content_from_page(doc, page)
        all_extracted_content += page_content

    return all_extracted_content

# Define the PDF path and output file path
pdf_path = 'content/clean_pdfs/Jurafsky_Martin.pdf'  # Replace with your PDF file path
output_text_path = 'content/processed_pdfs/Jurafsky_Martin/Jurafsky_Martin.pymupdf.txt'

# Process the PDF and save the content
extracted_content = process_pdf(pdf_path)

# Open the file with UTF-8 encoding to handle a wider range of characters
with open(output_text_path, "w", encoding='utf-8') as text_file:
    text_file.write(extracted_content)

print(f"Content extracted and saved to {output_text_path}")