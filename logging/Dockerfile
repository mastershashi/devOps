# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy your app files into the container
COPY requirements.txt .
COPY patient.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 5050

# Command to run the app
CMD ["python", "patient.py"]

# step
# runtime
# workspace dir
# copy you app code
# installation instruction 
# app host & port 
# instruct to run 