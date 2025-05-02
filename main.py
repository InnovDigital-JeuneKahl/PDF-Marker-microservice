from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from markerpdff.schemas import SearchResponse, TextResponse
from markerpdff.services import process_pdf, find_all_sentence_contexts
import tempfile
import os
import uvicorn


app = FastAPI()

@app.post("/search", response_model=SearchResponse)
async def search_pdf(
    file: UploadFile = File(...),
    search_terms: str = Form("")
):
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(await file.read())
            tmp_path = tmp_file.name
        
        # Process PDF
        text, images = process_pdf(tmp_path)
        
        # Search terms
        terms = [t.strip() for t in search_terms.split(",") if t.strip()]
        contexts = find_all_sentence_contexts(text, terms)
        
        # Cleanup
        os.unlink(tmp_path)
        
        return {"results": contexts}
        
    except Exception as e:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-text", response_model=TextResponse)
async def get_pdf_text(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(await file.read())
            tmp_path = tmp_file.name
        
        text, images = process_pdf(tmp_path)
        os.unlink(tmp_path)
        
        return {"text": text, "images": images}
        
    except Exception as e:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)