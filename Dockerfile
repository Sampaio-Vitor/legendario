# Use a Python base image
FROM python:3.11-slim

# Install build dependencies
RUN apt-get update && apt-get install -y git gcc g++ make cmake automake autoconf \
    clang libclang-dev dos2unix zlib1g zlib1g-dev zip unzip tar perl libxml2-dev bzip2 \
    xz-utils libtool libfreetype6 libfreetype6-dev libjpeg-dev libpng-dev

# Download and install FFmpeg
RUN apt-get install -y ffmpeg

# Install ImageMagick
RUN apt-get update && apt-get install -y imagemagick

# Install whisper
RUN pip install "git+https://github.com/openai/whisper.git"

# Replace the ImageMagick policy file with a modified version
COPY config/policy.xml /etc/ImageMagick-6/policy.xml

# Clean up the package manager
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt --no-cache-dir

# Copy your application code
COPY main.py /app/

# The application's entry point
CMD ["python", "main.py"]
