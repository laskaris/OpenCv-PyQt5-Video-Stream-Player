import cv2 as cv

from init import config as c
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QThread


class VideoThread(QThread):

    changePixmap = pyqtSignal(QImage)

    def __init__(self, *args, **kwargs):
        super(VideoThread, self).__init__(*args, **kwargs)
        self.mutex = QtCore.QMutex()
        self._running = True

        laskaris = cv.imread(c.logo)
        rgbImage = cv.cvtColor(laskaris, cv.COLOR_BGR2RGB)
        h, w, ch = rgbImage.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.laskarisPixmap = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)

    def alivetest(self):
        self._running = False

    def cameraStopNow(self):
        self._running = False

    def run(self):
        cap = cv.VideoCapture(c.videoSource)
        while self._running:
            self.mutex.lock()
            ret, frame = cap.read()
            if ret:
                rgbImage = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(1280, 720, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            else:
                self.changePixmap.emit(self.laskarisPixmap)
            self.mutex.unlock()
        cap.release()
        frame = 0
        ret = 0
        cv.destroyAllWindows()
        self.finished.emit()

