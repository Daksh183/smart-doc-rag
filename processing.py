import fitz
import os

def extract_text_from_pdf(pdf_path):
    #Extracts readable text from a PDF file.
    #Each page is processed sequentially and combined into a single string.

    #Catching exception if PDF not found
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at path: {pdf_path}")
    text=""
    doc=fitz.open(pdf_path)

    #Iterate through all pages in the PDF
    for i in range(doc.page_count):
        page=doc.load_page(i)
        page_text=page.get_text()
        #Append text only if the page contains readable content
        if page_text:
            text+=page_text + "\n"
    doc.close()
    return text.strip()

#Used only for local debugging
if __name__=="__main__":
    pdf_path="rag_test_document.pdf"
    extracted_text=extract_text_from_pdf(pdf_path)
    print(extracted_text)