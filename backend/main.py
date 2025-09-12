from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from backend import services

load_dotenv()

app = FastAPI()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    document_text: str
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    content: str

@app.post("/summarize")
async def summarize_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid file type. Please upload a PDF.")

    file_bytes = await file.read()
    text = await services.get_pdf_text(file_bytes)

    if not text:
        raise HTTPException(404, detail="Could not extract text from the PDF.")

    summary = await services.generate_summary(text)
    return {"summary": summary, "document_text": text}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_doc(request: ChatRequest):
    response_content = await services.get_chat_response(request.document_text, [msg.dict() for msg in request.messages])
    return ChatResponse(content=response_content)

@app.get("/")
async def root():
    return {"message": "Welcome to the Smart Summary API"}