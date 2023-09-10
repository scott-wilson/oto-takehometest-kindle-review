# Use an official Python runtime as the base image
FROM python:3.9-slim

EXPOSE 5000

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY "./app" /app
COPY "./user_library" /app
COPY "./requirements.txt" /app
COPY "./data.json" /app

# Install dependencies listed in a requirements.txt file, 
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py when the container launches
CMD ["python", "main.py"]