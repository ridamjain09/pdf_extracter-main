import os
import pdfminer.high_level
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from src.logger import logger

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as f:
        text = pdfminer.high_level.extract_text(f)
    logger.info("Extracted text from PDF.")
    return text.split("\n\n")  # Split text by paragraphs or sections

def clean_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    cleaned_text = " ".join([word for word in words if word.isalnum() and word not in stop_words])
    logger.info("Cleaned text data.")
    return cleaned_text

def save_cleaned_text(cleaned_text, output_file):
    with open(output_file, 'w') as f:
        f.write(cleaned_text)
        logger.info(f"Cleaned text saved to {output_file}")

if __name__ == "__main__":
    text = extract_text_from_pdf('./data/merged_policy.txt')
    cleaned_text = clean_text(text)
    save_cleaned_text(cleaned_text, './data/cleaned_policy.txt')
