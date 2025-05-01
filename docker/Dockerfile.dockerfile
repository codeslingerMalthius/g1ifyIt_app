# Use the official Python image as a base
FROM python:3.9-slim

# Set environment variables to avoid interactive installs
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies (for OpenCV, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Set up the virtual environment
RUN python3 -m venv venv

# Install dependencies
RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt

# Expose the port that Gradio will run on
EXPOSE 7860

# Command to run the app
CMD ["./venv/bin/python", "app.py"]
