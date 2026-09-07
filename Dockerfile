FROM python:3.11-slim

# System dependencies (kuch ML libraries ko yeh chahiye hote hain)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Requirements pehle copy karke install karein (Docker layer caching ke liye)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki poora code copy karein
COPY . .

# Hugging Face Spaces default port 7860 use karta hai
ENV PORT=7860
EXPOSE 7860

# Non-root user banana best practice hai (Hugging Face isko recommend karta hai)
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
