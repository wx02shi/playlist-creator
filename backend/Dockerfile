FROM python:3.10-slim

WORKDIR /backend

# Install dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Use Uvicorn with recommended production settings
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]