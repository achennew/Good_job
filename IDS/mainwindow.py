from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets import (NavigationItemPosition, FluentWindow)
from qfluentwidgets import FluentIcon as FIF


from home.homeInterface import homeInterface
from model.modelInterface import modelInterface


class temporaryWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setObjectName(text)


#fluentwindow自带边侧栏， 继承即可
class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        #亚克力效果
        self.navigationInterface.setAcrylicEnabled(True)
        #背景色， 先不管
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))

        #子界面
        #添加界面
        #实时监控界面
        self.monitorInterface = homeInterface()
        #特征库
        self.featureInterface = modelInterface()
        #设备
        self.equipmentInterface = temporaryWidget('equipment')
        #数据包分析
        self.dataAnalyseInterface = temporaryWidget("22")
        #日志
        self.logInterface = temporaryWidget('log')
        #......
        self.settingInterface = temporaryWidget('setting')

        self.initNavigation()

    def initWindow(self):
        self.resize(960, 720)

        self.setWindowTitle('L_D_Z_T')

        #初始位置生成
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def initNavigation(self):
        self.addSubInterface(self.monitorInterface, FIF.HOME, "Home")
        self.addSubInterface(self.featureInterface, FIF.BUS, "Model")

        # 分隔线
        self.navigationInterface.addSeparator()

        self.addSubInterface(self.equipmentInterface, FIF.CAR, "Statistics")
        self.addSubInterface(self.dataAnalyseInterface, FIF.GITHUB, "Traffic")


        #分隔线
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.logInterface, FIF.CAR, 'Account', position=NavigationItemPosition.BOTTOM)

        # 分隔线
        self.navigationInterface.addSeparator(position=NavigationItemPosition.BOTTOM)
        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Setting', position=NavigationItemPosition.BOTTOM)

        pass


#方便测试
import sys
from PyQt5.QtCore import Qt

QApplication.setHighDpiScaleFactorRoundingPolicy(
    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
app = QApplication(sys.argv)

w = MainWindow()
w.show()
app.exec_()
