# Use a larger Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Upgrade pip and install smaller dependencies first
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn pillow python-multipart

# Install larger dependencies in separate layers to avoid memory overload
RUN pip install --no-cache-dir torch
RUN pip install --no-cache-dir torchvision

# Command to run the FastAPI app
EXPOSE 8000
CMD ["uvicorn", "deploy:app"]
