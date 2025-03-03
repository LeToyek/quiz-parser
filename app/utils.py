import fitz  # PyMuPDF

def process_pdf(file_path):
    doc = fitz.open(file_path)
    quiz_data = []
    for i,page_num in enumerate(doc):
        page = doc.load_page(i)
        text = page.get_textpage()
        quiz_data.append(text)  
    
    return quiz_data
