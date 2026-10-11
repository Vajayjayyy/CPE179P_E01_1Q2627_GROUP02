import os
import cv2
import numpy as np
import uvicorn
from fastapi import FastAPI, File, UploadFile
from sprint1_pipeline import extract_container_code

app = FastAPI(title="Edge-Optimized Container Identification API")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Read the incoming image bytes
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Save to a temporary file for the extraction pipeline
    temp_path = "temp_inference.jpg"
    cv2.imwrite(temp_path, img)

    # Use the full image dimensions as the default detection box
    bbox = [0, 0, img.shape[1], img.shape[0]]

    # Run the OCR extraction function from Sprint 1
    bic_code = extract_container_code(temp_path, bbox)

    # Clean up temporary artifact
    if os.path.exists(temp_path):
        os.remove(temp_path)

    return {"filename": file.filename, "container_code": bic_code}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)