import sys
from PyQt6.QtWidgets import QApplication
from ui import YouTubeDownloader

STYLE = """
QWidget {
    font-family: Arial;
    font-size: 11pt;
}

#titleLabel {
    font-size: 18pt;
    font-weight: bold;
    color: #2E8B57;
}

#downloadButton {
    background-color: #4CAF50;
    color: white;
    font-size: 13pt;
    padding: 8px;
    border-radius: 6px;
}

#downloadButton:hover {
    background-color: #45a049;
}
"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)

    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())
