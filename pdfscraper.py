import os
import requests
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def download_pdf(url, dest_folder):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error while downloading {url}: {e}")
        return None

    file_name = url.split('/')[-1]
    file_path = os.path.join(dest_folder, file_name)

    with open(file_path, 'wb') as file:
        file.write(response.content)

    return file_path


def extract_text_from_pdf(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return output_string.getvalue()


pdf_links = [
    'https://kursplaner.gu.se/pdf/kurs/sv/FL2230',
]

destination_folder = "downloaded_pdfs"

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

extracted_texts = []

for link in pdf_links:
    pdf_file_path = download_pdf(link, destination_folder)
    if pdf_file_path:
        text = extract_text_from_pdf(pdf_file_path)
        extracted_texts.append(text)
