FROM python:3.10-slim

# Install system libraries needed by OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install project dependencies
COPY ["Source Codes/Requirements.txt", "."]

# Increase socket timeout and retry count to prevent connection dropouts
RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 -r Requirements.txt

# Copy application files
COPY ["Main Project/container-bic-ocr/", "."]

EXPOSE 8000

CMD ["python", "edge_api.py"]