import io
import os
import subprocess
import urllib.request
# pyrefly: ignore[missing-import]
import html_text
from pdfminer.converter import TextConverter, HTMLConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

def extract_text_from_pdf( pdf_path ):
  text = ""
  resource_manager = PDFResourceManager()
  fake_file_handle = io.BytesIO()
  converter = HTMLConverter(resource_manager, fake_file_handle)
  page_interpreter = PDFPageInterpreter(resource_manager, converter)
  with open(pdf_path, 'rb') as fh:
     for page in PDFPage.get_pages(fh, caching=True, check_extractable=True): page_interpreter.process_page(page)
     text = fake_file_handle.getvalue().decode()
  converter.close()
  fake_file_handle.close()
  text = html_text.extract_text(text)
  file = open(pdf_path.replace('.pdf','.txt'), 'w')
  file.write(text)
  file.close()
        
def download_bte( year , number ):      
  filename = "bte" + repr(number) + "_" + repr(year) + ".pdf"
  download_url = "http://bte.gep.msess.gov.pt/completos/" + repr(year) + "/" + filename
  response = urllib.request.urlopen(download_url)
  file = open("../BTE-data/" + filename, 'wb')
  file.write(response.read())
  file.close()
  return filename

# Downloading data (e.g., from 1977 to 2020)
for year in range(2019, 2020):
  for number in range(1, 49):
    try: download_bte( year , number )
    except: print("Error processing number " + repr(number) + " from year " + repr(year) + "...")

# Converting all PDF data to TXT
for year in range(1977, 2020):
  for number in range(1, 49):
    try:
      filename = "bte" + repr(number) + "_" + repr(year) + ".pdf"
      extract_text_from_pdf( "../BTE-data/" + filename )
    except: print("Error processing number " + repr(number) + " from year " + repr(year) + "...")

# Compressing the PDF files safely
bte_dir = os.path.normpath("../BTE-data")
if os.path.isdir(bte_dir):
    for filename in os.listdir(bte_dir):
        if filename.lower().endswith(".pdf"):
            src_file = os.path.join(bte_dir, filename)
            tmp_file = os.path.join(bte_dir, filename + ".tmp")
            
            try:
                # Arguments are passed directly to the binary without shell evaluation
                subprocess.run([
                    "ps2pdf",
                    "-dUseFlateCompression=true",
                    "-dPDFSETTINGS=/screen",
                    src_file,
                    tmp_file
                ], check=True)
                
                # Replace the original only if compression succeeded
                if os.path.isfile(tmp_file):
                    os.replace(tmp_file, src_file)
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                print(f"Error compressing {filename}: {e}")
                if os.path.isfile(tmp_file):
                    os.remove(tmp_file)