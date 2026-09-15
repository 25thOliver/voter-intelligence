FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY locate_county.py .
COPY debug_page.py .
COPY debug_tolerance.py .
COPY debug_chars.py .

CMD ["python", "locate_county.py"]