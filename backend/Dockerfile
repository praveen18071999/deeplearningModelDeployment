# Use a larger Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip and install smaller dependencies first
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn pillow python-multipart

# Install larger dependencies (torch and torchvision)
RUN pip install --no-cache-dir torch torchvision

# Command to run the FastAPI application
CMD ["uvicorn", "deploy:app", "--host", "0.0.0.0", "--port", "8000"]
