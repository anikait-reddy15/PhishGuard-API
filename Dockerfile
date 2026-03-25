# 1. Use an official, lightweight Python image
FROM python:3.10-slim

# 2. Stop Python from writing .pyc files and buffer the output for cloud logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy your requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Expose the port Cloud Run expects
EXPOSE 8080

# 7. Start the application using Gunicorn (production web server)
# We set timeout to 120s to give the AI plenty of time to respond
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "120", "main:app"]