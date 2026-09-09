FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# clicks.db is created on first run inside the container.
# Mount a volume on /app if you want it to survive container restarts:
#   docker run -v zenni_clicks:/app ...
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
