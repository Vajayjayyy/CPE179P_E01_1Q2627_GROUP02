from io import BytesIO
import json
import logging
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from excel_export import create_excel_report
from ocr_pipeline import process_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MAX_UPLOAD_BYTES = 15 * 1024 * 1024

app = FastAPI(
    title="Container BIC OCR",
    description="Detect and validate container identification codes using EasyOCR, TrOCR, and ISO 6346 check-digit validation.",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.get("/health")
async def health():
    return {"status": "ok", "service": "container-bic-ocr"}

@app.post("/api/ocr")
async def ocr_image(file: UploadFile = File(...)):
    filename = file.filename or "upload"
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported file type. Upload JPG, JPEG, PNG, BMP, or WEBP.")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Image exceeds the 15 MB upload limit.")
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    try:
        return process_image(content, filename)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("OCR processing failed")
        raise HTTPException(status_code=500, detail="OCR processing failed. Check the server terminal for details.") from exc

@app.post("/api/export")
async def export_excel(payload: dict):
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise HTTPException(status_code=400, detail="'records' must be a list.")
    # Limit export payload size and avoid trying to export arbitrary nested objects.
    records = [record for record in records[:1000] if isinstance(record, dict)]
    try:
        data = create_excel_report(records)
    except Exception as exc:
        logger.exception("Excel export failed")
        raise HTTPException(status_code=500, detail="Could not create Excel report.") from exc
    return StreamingResponse(
        BytesIO(data),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="container_ocr_results.xlsx"'}
    )
