import PyPDF2 as pdf
import ollama
import asyncio
from io import BytesIO
import json
import os
from typing import List

# Get the absolute path to the prompts.json file
PROMPTS_FILE = os.path.join(os.path.dirname(__file__), 'prompts.json')

with open(PROMPTS_FILE, 'r') as f:
    prompts = json.load(f)

summary_prompt_template = prompts['summary']
chat_system_prompt = prompts['chat_system_prompt']


# Asynchronously extract text from multiple PDF files
async def get_text_from_pdfs(files_bytes: List[bytes]) -> str:
    def extract_text():
        text = ""
        for file_bytes in files_bytes:
            try:
                pdf_file = BytesIO(file_bytes)
                reader = pdf.PdfReader(pdf_file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            except Exception as e:
                # Handle potential PyPDF2 errors
                print(f"Error processing PDF: {e}")
        return text

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, extract_text)

# Asynchronously generate a summary from the given text
async def generate_summary(text: str) -> str:
    if not text.strip():
        return "The document is empty or contains no readable text."

    summary_prompt = summary_prompt_template.format(text=text)
    try:
        response = await asyncio.to_thread(
            ollama.generate, model='gemma3', prompt=summary_prompt
        )
        return response.get('response', 'Failed to generate summary.')
    except Exception as e:
        return f"Error during summary generation: {e}"

# Asynchronously get a chat response
async def get_chat_response(document_text: str, messages: list) -> str:
    system_prompt_content = chat_system_prompt.format(document_text=document_text)
    system_prompt = {
        "role": "system",
        "content": system_prompt_content
    }
    messages_for_ollama = [system_prompt] + messages
    
    try:
        response = await asyncio.to_thread(
            ollama.chat, model='gemma3', messages=messages_for_ollama
        )
        return response.get('message', {}).get('content', 'Sorry, I could not process your request.')
    except Exception as e:
        return f"Error during chat generation: {e}"
