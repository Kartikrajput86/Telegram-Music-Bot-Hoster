# Lightweight Python base image
FROM python:3.12-slim

# Prevent interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies for audio/streaming and building Python wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       libopus0 \
       build-essential \
       pkg-config \
       git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first (for better Docker layer caching)
COPY telegram-music-bot/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# Copy bot source code
COPY telegram-music-bot /app

# Optional: run as non-root user for security
RUN useradd -m botuser \
    && chown -R botuser:botuser /app
USER botuser

# Default environment variables (override via Docker run or docker-compose)
ENV API_ID=0 \
    API_HASH="" \
    BOT_TOKEN="" \
    ASSISTANT_SESSION="" \
    YT_COOKIES="" \
    SUDO_USER_IDS="" \
    LOG_CHAT_ID="" \
    SPOTIFY_CLIENT_ID="" \
    SPOTIFY_CLIENT_SECRET=""

# Set working directory again for clarity
WORKDIR /app

# Healthcheck to ensure process is running
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD pgrep -f "python main.py" || exit 1

# Start the bot
CMD ["python", "main.py"]
