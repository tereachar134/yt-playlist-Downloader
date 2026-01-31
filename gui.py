import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import threading
import os
from downloader import PlaylistDownloader

class GuiLogger:
    def __init__(self, log_widget, root):
        self.log_widget = log_widget
        self.root = root

    def debug(self, msg):
        if msg.startswith('[debug] '): # Filter debug noise
            pass
        else:
            self.write_log(msg)

    def warning(self, msg):
        self.write_log(f"[WARNING] {msg}")

    def error(self, msg):
        self.write_log(f"[ERROR] {msg}")

    def write_log(self, msg):
        def _append():
            self.log_widget.config(state='normal')
            self.log_widget.insert(tk.END, msg + "\n")
            self.log_widget.see(tk.END)
            self.log_widget.config(state='disabled')
        self.root.after(0, _append)

class ContextMenu:
    def __init__(self, widget):
        self.widget = widget
        self.menu = tk.Menu(widget, tearoff=0)
        self.menu.add_command(label="Copy", command=self.copy_text)
        self.menu.add_command(label="Paste", command=self.paste_text)
        self.menu.add_command(label="Clear", command=self.clear_text)
        
        widget.bind("<Button-3>", self.show_menu)
        widget.bind("<Button-2>", self.show_menu) 

    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def copy_text(self):
        try:
            sel = self.widget.selection_get()
            self.widget.clipboard_clear()
            self.widget.clipboard_append(sel)
        except tk.TclError:
            pass

    def paste_text(self):
        try:
            text = self.widget.clipboard_get()
            if isinstance(self.widget, ttk.Entry):
                self.widget.insert(tk.INSERT, text)
            elif isinstance(self.widget, tk.Text):
                self.widget.insert(tk.INSERT, text)
        except tk.TclError:
            pass

    def clear_text(self):
        if isinstance(self.widget, ttk.Entry):
            self.widget.delete(0, tk.END)
        elif isinstance(self.widget, tk.Text):
            self.widget.delete("1.0", tk.END)

class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
        self.root.geometry("900x700")
        
        # Styles
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat")
        style.configure("Treeview", rowheight=25)
        
        # Symbols
        self.CHECKED = "☑"
        self.UNCHECKED = "☐"

        # --- Top Bar: Input & One-Click Actions ---
        top_frame = ttk.Frame(root, padding=10)
        top_frame.pack(fill="x")

        # URL Input
        ttk.Label(top_frame, text="Playlist URL:").pack(anchor="w")
        url_box = ttk.Frame(top_frame)
        url_box.pack(fill="x", pady=(0, 10))
        
        self.url_entry = ttk.Entry(url_box)
        self.url_entry.pack(side="left", fill="x", expand=True)
        ContextMenu(self.url_entry)
        
        self.fetch_btn = ttk.Button(url_box, text="Load Playlist", command=self.start_fetch_thread)
        self.fetch_btn.pack(side="right", padx=(5, 0))

        # Directory Input
        ttk.Label(top_frame, text="Download To:").pack(anchor="w")
        dir_box = ttk.Frame(top_frame)
        dir_box.pack(fill="x")
        
        self.dir_entry = ttk.Entry(dir_box)
        self.dir_entry.insert(0, os.path.join(os.getcwd(), "downloads"))
        self.dir_entry.pack(side="left", fill="x", expand=True)
        ContextMenu(self.dir_entry)
        
        self.browse_btn = ttk.Button(dir_box, text="Browse...", command=self.browse_directory)
        self.browse_btn.pack(side="right", padx=(5, 0))

        # --- Middle Section: Video List (Treeview) ---
        mid_frame = ttk.Frame(root, padding=(10, 0))
        mid_frame.pack(fill="both", expand=True)

        cols = ("check", "index", "title", "duration")
        self.tree = ttk.Treeview(mid_frame, columns=cols, show="headings", selectmode="extended")
        
        # Columns Config
        self.tree.heading("check", text="Sel")
        self.tree.column("check", width=40, anchor="center", stretch=False)
        
        self.tree.heading("index", text="#")
        self.tree.column("index", width=50, anchor="center", stretch=False)
        
        self.tree.heading("title", text="Title")
        self.tree.column("title", anchor="w")
        
        self.tree.heading("duration", text="Duration")
        self.tree.column("duration", width=80, anchor="center", stretch=False)

        # Scrollbar
        scrollbar = ttk.Scrollbar(mid_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind clicks
        self.tree.bind("<Button-1>", self.on_tree_click)

        # Selection Toolbar
        toolbar = ttk.Frame(mid_frame)
        toolbar.pack(side="bottom", fill="x", pady=5)

        # --- Bottom Section: Actions & Logs ---
        btm_frame = ttk.Frame(root, padding=10)
        btm_frame.pack(fill="both", expand=True)
        
        # Action Buttons
        act_frame = ttk.Frame(btm_frame)
        act_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(act_frame, text="Select All", command=self.select_all).pack(side="left", padx=2)
        ttk.Button(act_frame, text="Deselect All", command=self.deselect_all).pack(side="left", padx=2)
        
        spacer = ttk.Frame(act_frame)
        spacer.pack(side="left", fill="x", expand=True)
        
        self.stop_btn = ttk.Button(act_frame, text="STOP", command=self.stop_download, state="disabled")
        self.stop_btn.pack(side="right", padx=5)
        
        self.download_btn = ttk.Button(act_frame, text="Download Selected", command=self.start_download_thread, state="disabled")
        self.download_btn.pack(side="right")

        # Progress
        self.pbar = ttk.Progressbar(btm_frame, orient="horizontal", mode="determinate")
        self.pbar.pack(fill="x", pady=(0, 5))
        
        self.status_label = ttk.Label(btm_frame, text="Welcome! Paste a URL and click Load Playlist.")
        self.status_label.pack(anchor="w")

        # Logs
        self.log_text = tk.Text(btm_frame, height=8, state='disabled')
        self.log_text.pack(fill="both", expand=True, pady=(5, 0))
        ContextMenu(self.log_text)

        # Footer
        ttk.Label(root, text="Created by 13_4", font=("Arial", 8, "italic"), foreground="gray").pack(side="bottom", pady=2)

        # State
        self.logger = GuiLogger(self.log_text, self.root)
        self.stop_event = None
        self.playlist_entries = []

    # --- Interaction Logic ---
    def on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            col = self.tree.identify_column(event.x)
            if col == "#1": # Checked Header - Toggle All
                self.toggle_all_check()
        elif region == "cell":
            col = self.tree.identify_column(event.x)
            if col == "#1": # Checkbox column
                item_id = self.tree.identify_row(event.y)
                self.toggle_check(item_id)

    def toggle_check(self, item_id):
        current_vals = self.tree.item(item_id, "values")
        new_status = self.UNCHECKED if current_vals[0] == self.CHECKED else self.CHECKED
        self.tree.item(item_id, values=(new_status, *current_vals[1:]))

    def toggle_all_check(self):
        # Determine target state based on first item
        children = self.tree.get_children()
        if not children: return
        
        first_val = self.tree.item(children[0], "values")[0]
        target = self.UNCHECKED if first_val == self.CHECKED else self.CHECKED
        
        for item in children:
            vals = self.tree.item(item, "values")
            self.tree.item(item, values=(target, *vals[1:]))

    def select_all(self):
        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            self.tree.item(item, values=(self.CHECKED, *vals[1:]))

    def deselect_all(self):
        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            self.tree.item(item, values=(self.UNCHECKED, *vals[1:]))

    # --- Functional Logic ---
    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.dir_entry.get())
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def start_fetch_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a playlist URL")
            return
        
        self.fetch_btn.config(state="disabled")
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        self.logger.write_log(f"Fetching playlist info: {url}...")
        
        thread = threading.Thread(target=self.run_fetch, args=(url,))
        thread.daemon = True
        thread.start()

    def run_fetch(self, url):
        try:
            downloader = PlaylistDownloader(self.dir_entry.get())
            info = downloader.fetch_playlist_info(url)
            
            self.playlist_entries = []
            if 'entries' in info:
                self.playlist_entries = list(info['entries'])
            else:
                self.playlist_entries = [info]

            self.root.after(0, self.populate_list)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch info: {e}"))
            self.root.after(0, lambda: self.logger.error(str(e)))
        finally:
            self.root.after(0, lambda: self.fetch_btn.config(state="normal"))

    def populate_list(self):
        for idx, entry in enumerate(self.playlist_entries, 1):
            title = entry.get('title', 'Unknown Title')
            duration = str(entry.get('duration', 'N/A'))
            # Format duration if possible
            if duration.isdigit():
                 m, s = divmod(int(duration), 60)
                 if m > 60:
                     h, m = divmod(m, 60)
                     duration = f"{h}:{m:02d}:{s:02d}"
                 else:
                     duration = f"{m}:{s:02d}"
            
            self.tree.insert("", "end", iid=idx, values=(self.CHECKED, idx, title, duration))
        
        self.logger.write_log(f"Fetched {len(self.playlist_entries)} videos.")
        self.download_btn.config(state="normal")

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        path = self.dir_entry.get().strip()
        
        # Find indices where checkbox is CHECKED
        indices = []
        for item_id in self.tree.get_children():
            vals = self.tree.item(item_id, "values")
            if vals[0] == self.CHECKED:
                # item_id is 1-based index string (set in populate_list)
                indices.append(int(item_id)) 

        if not indices:
            messagebox.showwarning("Warning", "No videos selected!")
            return

        self.stop_event = threading.Event()
        self.download_btn.config(state='disabled')
        self.fetch_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        
        thread = threading.Thread(target=self.run_download, args=(url, path, indices))
        thread.daemon = True
        thread.start()

    def run_download(self, url, path, indices):
        try:
            downloader = PlaylistDownloader(path, progress_callback=self.progress_callback, logger=self.logger)
            downloader.download_playlist(url, items_to_download=indices, stop_event=self.stop_event)
            
            if not self.stop_event.is_set():
                 self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed!"))
        except Exception as e:
            self.root.after(0, lambda: self.logger.error(str(e)))
        finally:
             self.root.after(0, self.reset_ui)

    def stop_download(self):
        if self.stop_event:
            self.stop_event.set()
            self.logger.write_log("Stopping download... please wait...")
            self.stop_btn.config(state='disabled')

    def reset_ui(self):
        self.download_btn.config(state='normal')
        self.fetch_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="Ready")
        self.pbar['value'] = 0

    def progress_callback(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                val = float(p)
                self.pbar['value'] = val
            except:
                pass
            
            status = f"Downloading: {d.get('_percent_str', 'N/A')} | Speed: {d.get('_speed_str', 'N/A')}"
            self.root.after(0, lambda: self.status_label.config(text=status))
            
        elif d['status'] == 'finished':
            self.pbar['value'] = 100

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderGUI(root)
    root.mainloop()
