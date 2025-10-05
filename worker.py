import os
from PyQt6.QtCore import QThread, pyqtSignal
import yt_dlp

class DownloadThread(QThread):
    finished = pyqtSignal(str, str)

    def __init__(self, url, save_path, ignore_ssl, media_format):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.ignore_ssl = ignore_ssl
        self.media_format = media_format

    def run(self):
        os.makedirs(self.save_path, exist_ok=True)

        # קונפיגורציה בסיסית של yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
            'nocheckcertificate': self.ignore_ssl
        }

        match self.media_format:
            case "אודיו (mp3)":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '0'
            }]
            case "וידאו (mp4)":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'
            case _:
                ydl_opts['format'] = 'bestaudio/best'

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                self.finished.emit("סיום", "ההורדה הסתיימה בהצלחה!")
        except yt_dlp.utils.DownloadError as e:
            msg = str(e)
            if "ffmpeg" in msg.lower():
                self.finished.emit("סיום", "ההורדה הסתיימה ללא המרה מ-webm כיוון שFFmpeg לא נמצא במחשב.")
            else:
                self.finished.emit("שגיאה", msg)
        except Exception as e:
            self.finished.emit("שגיאה", str(e))