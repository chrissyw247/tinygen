# Use the official Python image from the Docker Hub
FROM python:3.9-slim-buster

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y git

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local project files into the container
COPY . .

# Specify the command to run when the container starts
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]