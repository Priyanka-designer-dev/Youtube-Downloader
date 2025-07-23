import tkinter as tk
from tkinter import filedialog, messagebox
import yt_dlp
import os

def download():
    url = url_entry.get().strip()
    option = download_option.get()
    resolution = resolution_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL.")
        return

    if option not in ["video", "audio", "both"]:
        messagebox.showerror("Error", "Please select a download type.")
        return

    # Use Toplevel to ensure the dialog appears
    folder_picker = tk.Toplevel(window)
    folder_picker.withdraw()
    folder_path = filedialog.askdirectory(title="Select folder to save the file")
    folder_picker.destroy()

    if not folder_path:
        messagebox.showinfo("Cancelled", "No folder selected. Download cancelled.")
        return

    try:
        output_template = os.path.join(folder_path, '%(title)s.%(ext)s')

        if option == "audio":
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': f'bestvideo[height<={resolution}]+bestaudio/best',
                'outtmpl': output_template,
                'merge_output_format': 'mp4',
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("✅ Success", f"Download complete.\nSaved to:\n{folder_path}")

    except Exception as e:
        messagebox.showerror("❌ Error", str(e))

# GUI
window = tk.Tk()
window.title("YouTube HD Downloader")
window.geometry("430x360")

tk.Label(window, text="YouTube Video URL:").pack(pady=5)
url_entry = tk.Entry(window, width=55)
url_entry.pack(pady=5)

download_option = tk.StringVar()
tk.Label(window, text="Download Type:").pack()
tk.Radiobutton(window, text="Video Only", variable=download_option, value="video").pack()
tk.Radiobutton(window, text="Audio Only (MP3)", variable=download_option, value="audio").pack()
tk.Radiobutton(window, text="Video + Audio (HD)", variable=download_option, value="both").pack()

tk.Label(window, text="Max Resolution (for video/both):").pack(pady=5)
resolution_var = tk.StringVar(value="1080")
res_options = ["144", "240", "360", "480", "720", "1080", "1440", "2160"]
tk.OptionMenu(window, resolution_var, *res_options).pack()

tk.Button(window, text="Download", command=download, bg="#4CAF50", fg="white", width=20).pack(pady=15)

window.mainloop()
