import sys
import os
import requests
import shutil
from pytube import YouTube, exceptions
from pytube.cli import on_progress
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QFileDialog
from threading import Thread


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        
        self.download_button.clicked.connect(self.multi)
        self.url_input.textChanged.connect(self.video_info)
        self.show()

    def multi(self):
        thread = Thread(target=self.get_video)
        thread.start()
    
    def get_video(self):
        url = self.url_input.text()
        mp3 = self.mp3_radio
        mp4 = self.mp4_radio

        try:
            video_input = YouTube(url)
            video_input.register_on_progress_callback(self.on_progress)
            if mp3.isChecked():
                mp4.setChecked(False)
                output = str(QFileDialog.getExistingDirectory(self, "Selecione uma pasta"))
                video = video_input.streams.filter(only_audio=True).first()
                downloaded_file = video.download(output_path=output)
                base, ext = os.path.splitext(downloaded_file)
                new_file = base + '.mp3'
                os.rename(downloaded_file, new_file)
                
            elif mp4.isChecked():
                mp3.setChecked(False)
                output = str(QFileDialog.getExistingDirectory(self, "Selecione uma pasta"))
                video_input.streams.get_highest_resolution().download(output_path=output)
                
        except exceptions.RegexMatchError:
            pass
        
    def video_info(self):
        url = self.url_input.text()
        title = self.title
        author = self.author
        if 'youtube.com/watch' in url:
            if len(url) == 43:
                try:
                    video = YouTube(url)
                    title.setText(video.title)
                    author.setText(video.author)
                    res = requests.get(video.thumbnail_url)
                    
                    with open('https.png', 'wb') as file:
                        file.write(res.content)

                    self.thumbnail.setPixmap(QtGui.QPixmap('https.png').scaled(600, 1200, QtCore.Qt.KeepAspectRatio))
                     
                except:
                    pass
        else:
            title.setText('Insira uma URL válida')
        
    def closeEvent(self, event):
        os.remove('https.png')
        event.accept()
        
    def on_progress(self, vid, chunk, bytes_remaining):
        total_size = vid.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        totalsz = (total_size/1024)/1024
        totalsz = round(totalsz,1)
        remain = (bytes_remaining / 1024) / 1024
        remain = round(remain, 1)
        dwnd = (bytes_downloaded / 1024) / 1024
        dwnd = round(dwnd, 1)
        percentage_of_completion = round(percentage_of_completion,2)

        #print(f'Total Size: {totalsz} MB')
        print(f'Download Progress: {percentage_of_completion}%, Total Size:{totalsz} MB, Downloaded: {dwnd} MB, Remaining:{remain} MB')
        self.bar.setText(str(percentage_of_completion))

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()