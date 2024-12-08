import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import yt_dlp
import sys

class VideoDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the GUI layout
        self.setWindowTitle("Video Downloader by Gaurav")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Create widgets
        self.platform_label = QLabel("Select Platform:")
        self.platform_label.setFont(QFont("Arial", 20))
        self.platform_combo = QComboBox(self)
        self.platform_combo.addItems(["YouTube", "Instagram", "Facebook"])
        self.platform_combo.setStyleSheet("padding: 5px; font-size: 32px;")

        self.link_label = QLabel("Enter Video Link:")
        self.link_label.setFont(QFont("Arial", 16))
        self.link_input = QLineEdit(self)
        self.link_input.setPlaceholderText("Paste your video link here...")
        self.link_input.setStyleSheet("padding: 5px; font-size: 32px;")

        self.download_button = QPushButton("Download")
        self.download_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 29px; padding: 10px;")
        self.download_button.clicked.connect(self.start_download)

        self.progress_label = QLabel("Download Progress:")
        self.progress_label.setFont(QFont("Arial", 16))
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet("QProgressBar { text-align: center; font-size: 26px}")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.platform_label)
        layout.addWidget(self.platform_combo)
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_input)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def start_download(self):
        platform = self.platform_combo.currentText().lower()
        link = self.link_input.text()

        if not link:
            QMessageBox.critical(self, "Error", "No video link provided!")
            return

        # Ask the user where to save the file
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Video As", "", "MP4 files (*.mp4);;All Files (*)", options=options
        )

        if not save_path:
            QMessageBox.critical(self, "Error", "No save location selected!")
            return

        # Reset progress bar
        self.progress_bar.setValue(0)

        # Start the download
        self.download_video(link, save_path)

    def download_video(self, link, file_path):
        def progress_hook(d):
            if d['status'] == 'downloading':
                total_bytes = d.get('total_bytes', 0)
                downloaded_bytes = d.get('downloaded_bytes', 0)
                progress = (downloaded_bytes / total_bytes) * 100 if total_bytes else 0
                self.progress_bar.setValue(int(progress))

        ydl_opts = {
            'format': 'best',
            'outtmpl': file_path,  # Save with the path provided by the user
            'progress_hooks': [progress_hook],  # Hook to update progress bar
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            QMessageBox.information(self, "Download Success", f"Video saved at: {file_path}")
            self.progress_bar.setValue(100)  # Set to 100% after completion
        except yt_dlp.utils.DownloadError as e:
            QMessageBox.critical(self, "Download Failed", f"Failed to download video: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")

# Run the PyQt5 application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application icon (make sure to have an icon file in the same directory)
    app.setWindowIcon(QIcon("icon.png"))  # Replace 'icon.png' with your icon file name

    window = VideoDownloaderApp()
    window.show()

    sys.exit(app.exec_())
