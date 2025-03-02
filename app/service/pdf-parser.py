import requests
import json
import fitz  # PyMuPDF for PDF parsing
import re
import logging
import time
import os
from dotenv import load_dotenv
load_dotenv()

# logging_path = ../../app.log

groq_api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": "Bearer " + groq_api_key,
    "Content-Type": "application/json",
}
def extract_text_from_pdf(pdf_path):
    try:
        document = fitz.open(pdf_path)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise

def create_prompt_content(pdf_text):
    try:
        return """
            Anda adalah asisten AI yang membantu dalam konversi soal dan jawaban ke dalam format json berikut
            "quiz": [
                    {
                        "question": "some question",
                        "answers": [
                            "answer1",
                            "answer2",
                            "answer3"
                        ],
                        "correct_answer": "answer1"
                    },
                    {
                        "question": "some question",
                        "answers": [
                            "answer1",
                            "answer2",
                            "answer3"
                        ],
                        "correct_answer": "answer1"
                    }
                ]
        dan berikut adalah soal dan jawaban dari PDF yang diberikan:
    """ + pdf_text
    except Exception as e:
        logging.error(f"Error creating prompt content: {e}")
        raise
    
def save_to_json(content, file_path="output.json"):
    try:
        '''
        the content must be the result from the llm. 
        So you have to make sure that the content is in the right format.
        It usualy start with JSON:\n\n``` and end with \n\n```
        '''
        # select the content from the response
        content = content.split("```")[1].split("```")[0].strip()
        # remove any anomaly text like 'json' at the start
        if content.startswith("json"):
            content = content[4:].strip()
        # save the content to json file
        # make sure the first and the last character is { and }
        if content[0] != "{":
            content = "{" + content
        if content[-1] != "}":
            content = content + "}"
        print("-"*50)
        print(content)
        print("-"*50)
        
        with open(file_path, "w") as f:
            f.write(content)
    except Exception as e:
        logging.error(f"Error saving to json: {e}")
        raise


data = {
    "messages": [
        {
            "role": "user", 
            "content": """
                Konversi soal dan jawaban ke dalam format json berikut
            {
                "quiz": [
                    {
                        "question": "some question",
                        "answers": [
                            "answer1",
                            "answer2",
                            "answer3"
                        ],
                        "correct_answer": "answer1"
                    },
                    {
                        "question": "some question",
                        "answers": [
                            "answer1",
                            "answer2",
                            "answer3"
                        ],
                        "correct_answer": "answer1"
                    }
                ]
                    
            }
            """,
        }
    ],
    "model": "llama-3.3-70b-versatile",
}


# if __name__ == "__main__":
#     pdf_path = "sampel-soal.pdf"
#     text = extract_text_from_pdf(pdf_path)
#     prompt_content = create_prompt_content(text)
#     data["messages"][0]["content"] = prompt_content
#     print("="*50)
#     print(prompt_content)
#     print("="*50)
    
#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     response_data = response.json()
#     res_content = response_data["choices"][0]["message"]["content"]
#     print("="*50)
#     print(res_content)
#     print("="*50)
#     now_millis = int(round(time.time() * 1000))
#     output_file = f"public/output_{now_millis}.json"
    
#     save_to_json(res_content, output_file)
    
    
    