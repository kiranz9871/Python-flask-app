# Use lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy files into container
COPY . .

# Install dependencies
RUN pip install flask prometheus-client

# Expose app port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]