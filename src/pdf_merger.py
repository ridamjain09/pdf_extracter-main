import os
import PyPDF2
from src.logger import logger

def merge_pdfs(input_folder, output_file):
    pdf_writer = PyPDF2.PdfWriter()
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(input_folder, file_name)
            pdf_reader = PyPDF2.PdfReader(file_path)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
    
    with open(output_file, 'wb') as out:
        pdf_writer.write(out)
        logger.info(f"Merged PDF saved as {output_file}")

if __name__ == "__main__":
    merge_pdfs('./data/raw_pdfs', './data/merged_policy.txt')
