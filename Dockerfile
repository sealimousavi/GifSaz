# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to /app in the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (these will be replaced by Doprax)
ENV BOT_TOKEN=${BOT_TOKEN}

# Run the bot script
CMD ["python", "bot.py"]

