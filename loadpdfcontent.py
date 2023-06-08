import os
import PyPDF2
from langchain.text_splitter import CharacterTextSplitter

UPLOAD_FOLDER = 'uploads'
#FILE_NAME='javascript1.pdf'

def get_pdf_content(file_name:str):
    filepath = os.path.join(os.path.sep,os.getcwd(),UPLOAD_FOLDER, file_name)
    fhandle = open(r''+filepath+'', 'rb')
    pdfReader = PyPDF2.PdfReader(fhandle)
    pdf_content = ''
    lenofpdf=len(pdfReader.pages)
    print('--pdf has no of pages:--',lenofpdf)
    if(lenofpdf >1):
            for i in range(lenofpdf):
                #if(i >5):
                #        break
                current_page = pdfReader.pages[i]
                if(len(current_page.extract_text()) < 1):
                        continue
                pdf_content+=current_page.extract_text()
                
    else:
            pdf_content = pdfReader.pages[0].extract_text()

    return pdf_content



def split_and_chunk(pdf_content):
        text_splitter = CharacterTextSplitter(
              separator="\n",
              chunk_size=1024, 
              chunk_overlap=0,
              length_function=len
              )
        pdf_content = text_splitter.split_text(pdf_content)
        return pdf_content