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
