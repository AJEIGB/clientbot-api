# Use official Python base image 
FROM python:3.11-slim

# Set working directory
WORKDIR /my-api-project

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Start FastAPI using Uvicorn and use the environment variable PORT
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
