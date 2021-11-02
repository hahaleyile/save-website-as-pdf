from PyQt5.QtWidgets import QApplication
from time import strftime

class LogWriter:
    def __init__(self, log_savepath, widget):
        self.log_savepath = log_savepath
        self.widget = widget

    def write(self, txt, to_user=True):
        t = strftime('---%Y-%m-%d %H:%M:%S---  ')
        with open(self.log_savepath, 'a+', encoding='utf-8')as f:
            f.writelines(t + txt + '\n')
        if to_user:
            self.widget.append(txt)
            QApplication.processEvents()
        