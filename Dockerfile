FROM python:3.11-slim

# Instalar dependencias del sistema necesarias, incluido tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p uploads

ENV PORT=10000

CMD ["python", "app.py"]
