# Use a slim Python 3.9 base image
FROM python:3.9-slim

# Set a working directory within the container
WORKDIR /app

# Install required dependencies using pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your Flask application code
COPY . .

# Expose the port used by your Flask application (typically 5000)
EXPOSE 5000

# Install gunicorn
RUN pip install gunicorn

# Run the Flask application using gunicorn as a production server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
