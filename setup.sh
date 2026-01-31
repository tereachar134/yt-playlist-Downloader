#!/bin/bash

INSTALL_DIR="$HOME/ytp-downloader"
echo "=== YouTube Playlist Downloader Installer ==="
echo "Installing to: $INSTALL_DIR"

# Create directory
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download
echo "Downloading..."
if command -v wget &> /dev/null; then
    wget -q https://github.com/tereachar134/yt-playlist-Downloader/archive/refs/heads/main.zip -O main.zip
elif command -v curl &> /dev/null; then
    curl -L -o main.zip https://github.com/tereachar134/yt-playlist-Downloader/archive/refs/heads/main.zip
else
    echo "Error: neither wget nor curl found."
    exit 1
fi

# Unzip
echo "Extracting..."
if ! command -v unzip &> /dev/null; then
    echo "Error: unzip not found. Please install unzip."
    exit 1
fi
unzip -o -q main.zip

# Run
cd yt-playlist-Downloader-main
echo "Starting..."
chmod +x install_and_run.sh
./install_and_run.sh
