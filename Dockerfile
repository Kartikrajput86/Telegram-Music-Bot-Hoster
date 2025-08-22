# Lightweight Python base
FROM python:3.12-slim

# Avoid interactive prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps for audio/streaming and building wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       libopus0 \
       build-essential \
       pkg-config \
       git \
    && rm -rf /var/lib/apt/lists/*

# Create app dir
WORKDIR /app

# Install Python deps first (better Docker layer caching)
COPY telegram-music-bot/requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# Copy the rest of the source
COPY telegram-music-bot /app

# Optional: create non-root user (safer)
RUN useradd -m botuser \
    && chown -R botuser:botuser /app
USER botuser

# Default environment keys (override with real values in runtime)
ENV API_ID=0 \
    API_HASH="" \
    BOT_TOKEN="" \
    ASSISTANT_SESSION="" \
    YT_COOKIES="" \
    SUDO_USER_IDS="" \
    LOG_CHAT_ID="" \
    SPOTIFY_CLIENT_ID="" \
    SPOTIFY_CLIENT_SECRET=""

# Working directory contains main.py
WORKDIR /app

# Healthcheck: ensure process is running (simple ping)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD pgrep -f "python main.py" || exit 1

# Run the bot
CMD ["python", "main.py"]
