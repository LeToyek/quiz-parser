import fitz  # PyMuPDF

def process_pdf(file_path):
    doc = fitz.open(file_path)
    quiz_data = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()
        quiz_data.append(text)
    
    return quiz_data
