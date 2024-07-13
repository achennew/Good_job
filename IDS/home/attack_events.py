import threading

from PyQt5.QtWidgets import QWidget, QApplication, QHeaderView
from scapy.sendrecv import sniff

from Ui_attack_events import Ui_Form

from mean.Packet_processing import packet_processing

class attack_eventsInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.packets = []
        self.pp = packet_processing()
        table = self.ui.data
        # 设置每一列的大小可以自由拉动
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # 最后一列自动填充
        table.horizontalHeader().setStretchLastSection(True)

        self.create_sniff_thread()
    # 监听
    def packet_callback(self, packet):
        # 在这里处理你的数据包
        self.packets.append(packet)
        self.pp.listen_processing(packet, table=self.ui.data)

    def sniff_in_thread(self, interface=""):
        # 在单独的线程中运行sniff函数
        sniff(iface=interface, prn=self.packet_callback, store=0)


    # 创建一个新的线程来运行sniff函数
    def create_sniff_thread(self):
        sniff_thread = threading.Thread(target=self.sniff_in_thread, args=(), daemon=True)
        sniff_thread.start()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = attack_eventsInterface()
    window.show()
    sys.exit(app.exec_())