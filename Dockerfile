# Use the official Python image from the Docker Hub
FROM python:3.9-slim-buster

# Install system dependencies (if any)
RUN apt-get update && apt-get install -y git

# Set the working directory inside the container
WORKDIR /app

# NOTE: set-up username + email b/c github needs them when making a new commit
# Set Git credentials
RUN git config --global user.name "FooBar"
RUN git config --global user.email "foobar@example.com"

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the local project files into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Specify the command to run when the container starts
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]