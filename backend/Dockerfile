# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application code to the working directory
COPY . .

# Expose the port on which the app will run
EXPOSE 8000

# Define the command to run your application
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
