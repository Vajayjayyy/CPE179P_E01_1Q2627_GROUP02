# Container BIC OCR

A web-based OCR application for reading container identification codes from images. The application uses OCR to extract text, validates container identification numbers against ISO 6346 rules, displays the results, and supports exporting results to Excel.


## Contents

- [Requirements](#requirements)
- [Project structure](#project-structure)
- [Run with Docker (recommended)](#run-with-docker-recommended)
- [Run locally with Python](#run-locally-with-python)
- [Using the application](#using-the-application)
- [Dataset](#dataset)
- [Troubleshooting](#troubleshooting)

## Requirements

### Docker

- Windows with Docker Desktop installed and running
- Docker Desktop's Linux container engine running
- The project files, including `Dockerfile` and `requirements.txt`

### Local Python run

- Python compatible with the packages in `requirements.txt` (Python 3.11 is a reasonable starting point)
- `pip`
- The dependencies listed in `requirements.txt`

## Project structure

```text
Project/
├── Dockerfile
├── .dockerignore
├── README.md
├── requirements.txt
├── main.py
├── ocr_pipeline.py
├── excel_export.py
├── validation.py
├── data/
├── static/
└── templates/
```

- `main.py` — FastAPI application and web routes.
- `ocr_pipeline.py` — OCR processing pipeline.
- `validation.py` — container identification number validation.
- `excel_export.py` — Excel export functionality.
- `templates/` — HTML templates.
- `static/` — static assets such as CSS or JavaScript.
- `data/` — project dataset or supporting data, if used by the application.
- `requirements.txt` — Python dependencies.
- `Dockerfile` — instructions for building the Docker image.
- `.dockerignore` — files excluded from Docker's build context.

## Run with Docker (recommended)

The commands below use **Windows PowerShell** and the project location used during development. Change the path if your project is stored elsewhere.

### 1. Start Docker Desktop

Open Docker Desktop and wait until its engine is running. In PowerShell, verify it works:

```powershell
docker --version
docker info
```

`docker info` should show both Client and Server details. If Docker works in PowerShell but not in WSL, you can run the Docker commands in this section directly from PowerShell.

### 2. Open the project directory

```powershell
cd C:\Users\JAYJAY\CPE179P_E01_1Q2627\Project
```

Check that the required files are present:

```powershell
Get-ChildItem Dockerfile, requirements.txt
```

### 3. Build the Docker image

Run this from the directory containing the `Dockerfile`:

```powershell
docker build -t container-bic-ocr .
```

The first build can take a while because the project uses machine-learning and OCR libraries. The application may also need to download OCR model files the first time it performs OCR.

### 4. Start the container

```powershell
docker run --rm -p 8001:8000 container-bic-ocr
```

- `8001` is the port on your Windows machine.
- `8000` is the port used by Uvicorn inside the container.
- `--rm` removes the stopped container after it exits. It does **not** delete the built image.

Keep this terminal open while using the application.

### 5. Open the application

Open this address in your browser:

**http://localhost:8001/**

### 6. Stop the application

Return to the terminal running the container and press **Ctrl+C**.

### 7. Rebuild after code changes

After changing application code or the Dockerfile, stop the running container and rebuild the image:

```powershell
docker build -t container-bic-ocr .
docker run --rm -p 8001:8000 container-bic-ocr
```

If port `8001` is already in use, use another host port, such as `8002`:

```powershell
docker run --rm -p 8002:8000 container-bic-ocr
```

Then visit `http://localhost:8002/`.

### Dataset note

The current Dockerfile copies the Python files, `templates/`, and `static/`, but does not explicitly copy `data/` into the image. Since the application has already been tested successfully in Docker, don't add the dataset automatically unless the application needs it at runtime.

If the application reads the host's `data/` directory at runtime and expects it at `/app/data`, run this from the project directory:

```powershell
docker run --rm -p 8001:8000 -v "${PWD}/data:/app/data" container-bic-ocr
```

Confirm the path expected by the code before relying on this mount.

## Run locally with Python

Use this option if you want to run the app without Docker. Run the commands from the project directory.

### 1. Create and activate a virtual environment

In PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

In Ubuntu / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If PowerShell blocks activation because of its execution policy, you can use the environment's Python directly instead of changing the system-wide policy.

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Some OCR and machine-learning packages are large, so installation may take time and require a working internet connection.

### 3. Start the server

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Open the application

On the same machine, open:

**http://localhost:8000/**

To stop the local server, press **Ctrl+C** in the terminal.

## Using the application

1. Open the application in your browser.
2. Upload an image containing a container identification number.
3. Start the OCR process using the interface.
4. Review the extracted text and validation result.
5. Use the Excel export option to save results if needed.

OCR accuracy depends on image quality, focus, lighting, viewing angle, and whether characters are obstructed or worn. Review extracted values before using them in operational records.

## Dataset

==============================

This dataset was exported via [roboflow.com](https://universe.roboflow.com/aya-mahmoud/detect-vakdt/dataset/1)

Roboflow is an end-to-end computer vision platform that helps you
* collaborate with your team on computer vision projects
* collect & organize images
* understand unstructured image data
* annotate, and create datasets
* export, train, and deploy computer vision models
* use active learning to improve your dataset over time

It includes 2290 images.
Detection are annotated in COCO format.

The following pre-processing was applied to each image:
* Auto-orientation of pixel data (with EXIF-orientation stripping)
* Resize to 416x416 (Stretch)

No image augmentation techniques were applied.


## Troubleshooting

### `docker` is not recognized in PowerShell

Install Docker Desktop for Windows, start it, and reopen PowerShell. Verify with:

```powershell
docker --version
docker info
```

### Docker works in PowerShell but not in WSL

Use PowerShell for the Docker build and run commands. This avoids relying on WSL's Docker CLI integration while it is not working.

### `docker info` reports a connection or permission error

Make sure Docker Desktop is running and its engine has finished starting. If the error occurs only in WSL, try running the commands from Windows PowerShell. Avoid changing Docker socket permissions or installing a second Docker engine without diagnosing the cause.

### The image build fails

Read the first error in the build output, not only the final failure line. Common causes include dependency installation failures, network interruptions, or missing files referenced by `COPY` instructions. Make sure `docker build` is being run from the directory containing the Dockerfile.

### The web page does not open

- Confirm the container is still running and the terminal has not reported an error.
- Confirm you're using the correct host port: `8001` for the Docker instructions above, or `8000` for a local Python run.
- If you selected another host port, use that port in the browser address.

### OCR takes a long time the first time

The application may need to download OCR model files on first use. Ensure the machine has an internet connection and allow the download to finish. Later runs may be faster if model files are cached or retained by the environment.

## Quick reference

| Task | Command |
|---|---|
| Build image | `docker build -t container-bic-ocr .` |
| Run Docker container | `docker run --rm -p 8001:8000 container-bic-ocr` |
| Open Docker app | `http://localhost:8001/` |
| Run locally | `python -m uvicorn main:app --host 0.0.0.0 --port 8000` |
| Open local app | `http://localhost:8000/` |
| Stop server/container | Press `Ctrl+C` in the running terminal |
