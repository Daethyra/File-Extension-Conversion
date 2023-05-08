# Use the official Python base image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Pandoc
RUN apt-get update && \
    apt-get install -y pandoc texlive texlive-latex-extra && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["python", "main.py"]
