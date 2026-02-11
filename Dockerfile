# Use an official lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies (if any are added later)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variable to bind to 0.0.0.0 inside the container
ENV HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 5050

# Command to run the application
CMD ["python", "server.py"]