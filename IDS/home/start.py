import socket
from socket import AF_INET

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTableWidgetItem


from Ui_start import Ui_Dialog

from mean.read_history_listener_json import Read_history_listener_json as rd


class start_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.listener_table = self.ui.listener_history_table
        self.rd = rd()

        self.Online_init()

    def Online_init(self):

        addr, ip = get_addrs()
        for add in addr:
            self.ui.listener_interface_combobox.addItem(add)

        self.listener_slotsignalconnect()

        self.history_listener()

    def scan_file(self, line):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "打开文件", "",
                                                  "*.pcap", options=options)

        if fileName:
            line.setText(fileName)

    def listener_slotsignalconnect(self):
        #浏览选择文件
        self.ui.listener_scan.clicked.connect(lambda: self.scan_file(self.ui.listener_scan_line))
        #创建文件,关闭窗口
        self.ui.listener_create.clicked.connect(self.create_listener)
        self.listener_table.cellDoubleClicked.connect(self.listener_on_cell_click)
        pass

    def listener_on_cell_click(self, row):
        print(self.rd.data['history'][row])

        self.close()
        pass

    def create_listener(self):
        #创建项目

        self.close()

    def history_listener(self):
        names, interfaces, times = self.rd.get_history_list()
        for name, interface, time in zip(names, interfaces, times):
            row = self.listener_table.rowCount()
            self.listener_table.insertRow(row)
            item1, item2, item3 = QTableWidgetItem(str(name)), QTableWidgetItem(str(interface)), QTableWidgetItem(
                str(time))
            item1.setFlags(item1.flags() & ~Qt.ItemIsEditable)
            item2.setFlags(item2.flags() & ~Qt.ItemIsEditable)
            item3.setFlags(item3.flags() & ~Qt.ItemIsEditable)
            self.listener_table.setItem(row, 0, item1)
            self.listener_table.setItem(row, 1, item2)
            self.listener_table.setItem(row, 2, item3)
        pass


def get_addrs():
    import psutil

    # 获取所有的网络接口
    if_addrs = psutil.net_if_addrs()

    ret = []
    ip = []
    for interface_name, interface_addresses in if_addrs.items():
        for addr in interface_addresses:
            if socket.AF_INET in addr:
                # print(interface_name, "  ", addr.address)
                ret.append(interface_name + ":" + addr.address)
                ip.append(addr.address)

    return ret, ip


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = start_widget()
    window.show()
    get_addrs()
    sys.exit(app.exec_())
