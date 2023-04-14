import sys
import os
import requests
from pytube import YouTube, exceptions
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from threading import Thread


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('main.ui', self)
        
        self.download_button.clicked.connect(self.get_video)
        self.url_input.textChanged.connect(self.video_info)
        self.show()
    
    def get_video(self):
        url = self.url_input.text()
        mp3 = self.mp3_radio
        mp4 = self.mp4_radio

        try:
            video_input = YouTube(url)
            
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
        
    

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()