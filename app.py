import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube
import os 

def donwload_video():
    url = entry_url.get()
    resolution = resolution_var.get()

    progress_label.pack(pady=(10, 5))
    progress_bar.pack(pady=(10, 5))
    status_label.pack(pady=(10, 5))

    try:
       yt = YouTube(url, on_progress_callback=on_progress)
       title = sanitize_filename(yt.title)

       # Check resolution for video stream selection
       if resolution == "1080p":
            video_stream = yt.streams.filter(adaptive=True).filter(mime_type='video/webm').first()
       else:
            video_stream = yt.streams.filter(res=resolution, progressive=True).first()

       audio_stream = yt.streams.filter(only_audio=True).first()

       if video_stream is None:
           raise ValueError(f"No suitable video stream found for resolution {resolution}")

       if audio_stream is None:
           raise ValueError("No suitable audio stream found.")
       
       # Download video and audio streams
       video_path = video_stream.download(output_path="downloads", filename=f"(video){title}")
       audio_path = audio_stream.download(output_path='downloads', filename=f"(audio){title}")

       # Use FFmpeg to merge the audio and video streams
       output_file_path = f"{title}.mp4"
       os.system(f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a aac -strict experimental "downloads/{output_file_path}"')
       
       # Remove the separate video and audio files
       os.remove(video_path)
       os.remove(audio_path)

       status_label.configure(text="Successfully downloaded", text_color="white", fg_color="green")

    except Exception as e:
       status_label.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")

def sanitize_filename(filename):
    # Replace characters not allowed in filenames with an underscore
    return ''.join(c if c.isalnum() or c in [' ', '.', '-', '_'] else '_' for c in filename)

def on_progress(stream, chunk, bytes_remaining):
   total_size = stream.filesize
   bytes_downloaded = total_size - bytes_remaining
   percentage_completed = bytes_downloaded / total_size * 100

   progress_label.configure(text = str(int(percentage_completed)) + "%")
   progress_label.update()
   
   progress_bar.set(float(percentage_completed / 100))


# create a root window
root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
# title of the window
root.title("Clipyx 🎞️")

# set min/max width and height
root.geometry("720x480")
root.minsize(720,480)
root.maxsize(1080,720)

#content frame
content_frame= ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

#video url entry widget
url_label= ctk.CTkLabel(content_frame, text="Enter the youtube url here : ")
entry_url= ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=(10, 5))
entry_url.pack(pady=(10, 5))

#download button
download_button= ctk.CTkButton(content_frame, text="Download", command=donwload_video)
download_button.pack(pady=(10, 5))

#resolutions combo-box
resolutions=["1080p","720p","480p","360p","240p"]
resolution_var = ctk.StringVar()
resolution_combobox= ttk.Combobox(content_frame, values=resolutions,textvariable=resolution_var)
resolution_combobox.pack(pady=(10, 5))
resolution_combobox.set("1080p")

#download progress bar
progress_label = ctk.CTkLabel(content_frame, text="0%")

progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0)

status_label = ctk.CTkLabel(content_frame, text="")


# to start the app
root.mainloop()