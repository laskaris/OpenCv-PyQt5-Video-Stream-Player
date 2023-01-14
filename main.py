import os
import sys
import time
from init import config as c
from init import pinger as pn
from init import cameraFeed as caf

from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import pyqtSlot


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        uic.loadUi('init/main.ui', self)
        self.setWindowTitle(c.appTitle)

        self.pingSart()

        self.show()

    @QtCore.pyqtSlot(bool)
    def get_ping_status(self, camera):

        if not camera:
            self.startCameraFeed.setEnabled(False)
            self.stopCameraFeed.setEnabled(False)

        return str(camera)

    @pyqtSlot()
    def pingSart(self):
        self.p = pn.PingThread(self)
        self.p.pingerSignal.connect(self.get_ping_status)
        self.p.start()

    @pyqtSlot()
    def pingStopNow(self):
        self.p.s_stop()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.mainScreen.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot()
    def cameraManuelStart(self):
        self.t = caf.VideoThread(self)
        self.t.changePixmap.connect(self.setImage)
        self.t.start()

        self.startCameraFeed.setEnabled(False)
        self.stopCameraFeed.setEnabled(True)

    @pyqtSlot()
    def cameraManuelStop(self):
        self.t.cameraStopNow()
        self.p.s_stop()

        self.startCameraFeed.setEnabled(True)
        self.stopCameraFeed.setEnabled(False)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()


if __name__ == '__main__':
    main()
