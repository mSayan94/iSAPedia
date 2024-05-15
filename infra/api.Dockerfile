# Dockerfile-api

# Use an official Python runtime as a parent image
FROM python:3.9.13

# Set the working directory in the container to /app
WORKDIR /app

# Add the API directory contents into the container at /app
ADD ../src/api /app/src/api/
ADD ../src/model /app/src/model/
COPY ../requirements.txt /app/

# Add the config_model.json file
ADD ../config_model.json /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install poppler and tesseract
RUN apt-get update 
RUN apt-get install poppler-utils -y
RUN apt-get install tesseract-ocr -y

# Login to Azure to a specific Tenant
ARG TENANT_ID
RUN az login --tenant $TENANT_ID

# Set environment variables for poppler and tesseract
ENV PATH="/usr/local/bin/poppler:${PATH}"
ENV PATH="/usr/local/bin/tesseract:${PATH}"

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run routes.py when the container launches
ENTRYPOINT ["uvicorn", "src.api.routes:api_app", "--host", "0.0.0.0", "--port", "8000"]