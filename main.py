import sys
import os
from downloader import PlaylistDownloader

def main():
    print("=== YouTube Playlist Downloader ===")
    
    url = input("Enter the YouTube playlist URL: ").strip()
    if not url:
        print("Error: No URL provided.")
        return

    default_path = os.path.join(os.getcwd(), "downloads")
    path = input(f"Enter the download directory (default: {default_path}): ").strip()
    
    if not path:
        path = default_path

    # Normalize path for cross-platform support
    path = os.path.abspath(os.path.expanduser(path))

    print(f"\nStarting download to: {path}")
    print("Press Ctrl+C to cancel at any time.\n")

    downloader = PlaylistDownloader(path)
    
    try:
        downloader.download_playlist(url)
        print("\nAll tasks completed!")
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
