# Use a multi-stage build for efficiency
FROM python:3.9-slim AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Build the final image (slim Python image + application)
FROM mongo:latest AS final

# Set working directory
WORKDIR /app

# Copy application code from builder stage
COPY --from=builder /app /app

# Expose Flask application port
EXPOSE 5000

# Run gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
