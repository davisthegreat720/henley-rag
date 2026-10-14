FROM python:3.13-slim

WORKDIR /app

# Install dependencies separately so Docker can reuse this layer
# when application source code changes but requirements do not.
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Add the application source after dependencies are installed.
COPY src ./src

# Treat /app/src as the Python package root.
ENV PYTHONPATH=/app/src

CMD ["uvicorn", "henley_rag.api.main:app", "--host", "0.0.0.0", "--port", "8000"]