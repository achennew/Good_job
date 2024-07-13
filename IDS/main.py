from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

import sys

from mainwindow import MainWindow

if __name__ == '__main__':
    #与系统设置的大小相匹配
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    app.exec_()
    pass