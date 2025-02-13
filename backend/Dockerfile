# Use a larger Python base image with a specific version to avoid breaking changes
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Upgrade pip and install smaller dependencies first
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn pillow python-multipart

# Install larger dependencies in separate layers to avoid memory overload
RUN pip install --no-cache-dir torch torchvision

# Expose port 8000 for FastAPI
EXPOSE 8000

# Ensure your FastAPI app is named "app" in the deploy.py file
CMD ["uvicorn", "deploy:app", "--host", "0.0.0.0", "--port", "8000"]
