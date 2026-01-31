import yt_dlp
import os

class PlaylistDownloader:
    def __init__(self, output_dir, progress_callback=None, logger=None):
        self.output_dir = output_dir
        self.progress_callback = progress_callback
        self.logger = logger
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def progress_hook(self, d):
        if self.progress_callback:
            self.progress_callback(d)
        
        if d['status'] == 'downloading':
            print(f"Downloading: {d.get('_percent_str', 'N/A')} of {d.get('_total_bytes_str', 'N/A')} at {d.get('_speed_str', 'N/A')} ETA {d.get('_eta_str', 'N/A')}", end='\r')
        elif d['status'] == 'finished':
            print(f"\nFinished downloading: {d['filename']}")

    def fetch_playlist_info(self, playlist_url):
        ydl_opts = {
            'extract_flat': True,  # Don't download, just get info
            'ignoreerrors': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(playlist_url, download=False)

    def download_playlist(self, playlist_url, items_to_download=None, stop_event=None):
        def check_stop(d):
            if stop_event and stop_event.is_set():
                raise Exception("Download cancelled by user.")

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(self.output_dir, '%(playlist_index)s - %(title)s.%(ext)s'),
            'noplaylist': False,
            'progress_hooks': [self.progress_hook, check_stop],
            'ignoreerrors': True,
        }
        
        if items_to_download:
            # yt-dlp expects 1-based indices for --playlist-items
            # items_to_download should be a list of integers (1-based indices)
            ydl_opts['playlist_items'] = ",".join(map(str, items_to_download))

        if self.logger:
            ydl_opts['logger'] = self.logger

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([playlist_url])
            except Exception as e:
                # If it's our cancellation exception, re-raise or handle gracefully
                if "Download cancelled" in str(e):
                    if self.logger: self.logger.write_log("Download cancelled.")
                    return # Stop
                print(f"An error occurred: {e}")
                if self.logger: self.logger.error(f"Error: {e}")

if __name__ == "__main__":
    # Test block
    pass
