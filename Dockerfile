# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy all files to /app in the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV BOT_TOKEN=${BOT_TOKEN}

# Run the bot using Gunicorn & Flask
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
