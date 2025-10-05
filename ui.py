from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QFileDialog, QCheckBox, QVBoxLayout, QHBoxLayout,
    QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt
from worker import DownloadThread
from platformdirs import user_config_dir
import os, json

CONFIG_DIR = user_config_dir("YouTubeDownloader")
os.makedirs(CONFIG_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTubeDownloader")
        self.setGeometry(300, 300, 700, 300)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.init_ui()
        self.load_config()
        self.reset_gui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        # כותרת
        title = QLabel("הורדת תוכן מ-YouTube")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        # URL
        url_layout = QHBoxLayout()
        url_label = QLabel("כתובת:")
        url_label.setFixedWidth(80)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("הכנס כתובת סרטון")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # תיקייה
        folder_layout = QHBoxLayout()
        folder_label = QLabel("תיקייה:")
        folder_label.setFixedWidth(80)
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("בחר תיקיית שמירה")
        browse_button = QPushButton("עיון")
        browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(browse_button)
        main_layout.addLayout(folder_layout)

        # פורמט
        format_layout = QHBoxLayout()
        format_label = QLabel("פורמט:")
        format_label.setFixedWidth(80)
        self.format_combo = QComboBox()
        self.format_combo.addItems(["אודיו (mp3)", "וידאו (mp4)"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        main_layout.addLayout(format_layout)

        # SSL
        self.ssl_checkbox = QCheckBox("התעלם מבעיות אבטחת תקשורת (חיוני באינטרנט מסונן)")
        self.ssl_checkbox.setChecked(True)
        main_layout.addWidget(self.ssl_checkbox)

        # כפתור הורדה
        self.download_button = QPushButton()
        self.download_button.clicked.connect(self.start_download)
        self.download_button.setObjectName("downloadButton")
        main_layout.addWidget(self.download_button)

        self.setLayout(main_layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "בחר תיקיית שמירה")
        if folder:
            self.folder_input.setText(folder)

    def start_download(self):
        url = self.url_input.text().strip()
        save_path = self.folder_input.text().strip()
        ignore_ssl = self.ssl_checkbox.isChecked()
        media_format = self.format_combo.currentText()

        if not url:
            QMessageBox.critical(self, "שגיאה", "אנא הזן URL")
            return
        if not save_path:
            QMessageBox.critical(self, "שגיאה", "אנא בחר תיקיית שמירה")
            return

        self.download_button.setEnabled(False)
        self.download_button.setText("מוריד...")
        self.thread = DownloadThread(url, save_path, ignore_ssl, media_format)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()


    def download_finished(self, title, text):
        QMessageBox.information(self, title, text)
        self.reset_gui()

    def reset_gui(self):
        self.download_button.setEnabled(True)
        self.download_button.setText("הורד")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.url_input.setText(data.get("url", ""))
                    self.folder_input.setText(data.get("folder", ""))
                    fmt = data.get("format", "אודיו (mp3)")
                    idx = self.format_combo.findText(fmt)
                    if idx >= 0:
                        self.format_combo.setCurrentIndex(idx)
            except Exception:
                pass
    def closeEvent(self, event):
        data = {
            "url": self.url_input.text().strip(),
            "folder": self.folder_input.text().strip(),
            "format": self.format_combo.currentText()
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        event.accept()
