# YouTube Playlist Downloader

A robust, cross-platform tool to download entire YouTube playlists with a modern GUI. Built with Python and `yt-dlp`.

## Features

*   **GUI & CLI**: Easy-to-use graphical interface and powerful command-line backend.
*   **Modern UI**: Clean table view with checkbox selection (☑/☐).
*   **Selective Download**: "Fetch" playlist info first, then choose specific videos or ranges to download.
*   **Resumable**: Skips already downloaded files.
*   **Organized**: Saves files with `Index - Title` format.
*   **Detailed Logging**: View real-time download logs.
*   **Control**: Stop/Cancel downloads at any time.

## Installation

### Prerequisites
*   Python 3.6+
*   `ffmpeg` (Required for merging high-quality video/audio)

### One-Click Setup (Recommended)

**Linux:**
1.  Run `./install_and_run.sh` in the terminal.

**Windows:**
1.  Double-click `install_and_run.bat`.

### Manual Setup
1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the GUI:
    ```bash
    python gui.py
    ```

## Usage

1.  **Load Playlist**: Paste the YouTube playlist URL and click "Load Playlist".
2.  **Select Videos**:
    *   By default, all videos are selected.
    *   Uncheck videos you don't want, or use "Deselect All" / "Select Range".
3.  **Download**: Click "Download Selected".
4.  **Stop**: Click "STOP" to cancel the process at any time.

## Credits
Created by **13_4**
