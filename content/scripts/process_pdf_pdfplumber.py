import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return ''.join(page.extract_text(layout=True) for page in pdf.pages if page.extract_text(layout=True))

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

pdf_folder = 'content/clean_pdfs'
output_folder = 'content/processed_pdfs'

for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith('.pdf'):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        output_path = os.path.join(output_folder, pdf_file.replace('.pdf', '.layout_preserved.txt'))
        pdf_text = extract_text_from_pdf(pdf_path)
        save_text_to_file(pdf_text, output_path)