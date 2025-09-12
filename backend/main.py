from fastapi import FastAPI, File, UploadFile, HTTPException, status
from backend.models.model import ChatMessage,ChatRequest,ChatResponse
from typing import List
from dotenv import load_dotenv
import uvicorn
from backend import services
import backend.config

load_dotenv()

app = FastAPI()


@app.post("/summarize", status_code=status.HTTP_200_OK)
async def summarize_pdf(files: List[UploadFile] = File(...)):
    files_bytes = []
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid file type: {file.filename}. Please upload PDFs only.")
        files_bytes.append(await file.read())

    try:
        text = await services.get_text_from_pdfs(files_bytes)
        if not text:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not extract text from the PDFs.")

        summary = await services.generate_summary(text)
        return {"summary": summary, "document_text": text}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred during summarization: {e}")

@app.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_doc(request: ChatRequest):
    try:
        response_content = await services.get_chat_response(request.document_text, [msg.dict() for msg in request.messages])
        return ChatResponse(content=response_content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred during chat: {e}")

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {"message": "Welcome to the Smart Summary API"}

@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok"}



if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)