import os
import subprocess
import time
from init import config as c
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QThread


class PingThread(QThread):
    pingerSignal = pyqtSignal(bool)
    pingStoped = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(PingThread, self).__init__(*args, **kwargs)
        self.stopped = False
        self.ping_ip = [c.ip]
        self.ping_status = [False]

    @QtCore.pyqtSlot()
    def s_stop(self):
        self.stopped = True
        self.pingerSignal.emit(False)

    def run(self):
        while not self.stopped:
            time.sleep(1)
            try:
                for i, s_ip in enumerate(self.ping_ip):
                    self.ping_status[i] = self.ping(s_ip)
                self.pingerSignal.emit(self.ping_status[0])
            except Exception as ex:
                self.pingerSignal.emit(False)
                print("Ping Err", str(ex))
        self.finished.emit()

    def ping(self, ip):
        try:
            subprocess.check_output(["ping", "-c", "1", "-W", "1", str(ip)])
            return True
        except subprocess.CalledProcessError as e:
            print("IP erişilemiyor:", str(ip))
            return False