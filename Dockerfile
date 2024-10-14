# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .


# Ensure the application has permission to read the file
RUN chmod 600 /app/private_key.pem
RUN chmod 600 /app/public_key.pem

# Create logs directory
RUN mkdir -p /app/logs && chmod -R 755 /app/logs

# Create the database directory and set permissions
RUN mkdir -p /app/db_data && chmod 755 /app/db_data

# Expose the port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]