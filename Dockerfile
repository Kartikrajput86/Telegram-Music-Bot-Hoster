FROM python:3.12-slim

# Install required system packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       libopus0 \
       build-essential \
       pkg-config \
       git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependencies
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN python -m pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# Copy bot source code
COPY . /app

# Optional: run as non-root user
# RUN useradd -m botuser
# USER botuser

CMD ["python", "main.py"]

