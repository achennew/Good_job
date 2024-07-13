import binascii

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QLineEdit
from PyQt5.QtCore import Qt

from scapy.all import *

from scapy.layers.inet import IP

def format_string(s):
    result = []
    for i, ch in enumerate(s):
        result.append(ch)
        pos = i + 1
        if pos % 32 == 0:
            result.append('\n')
        elif pos % 16 == 0:
            result.append('  ')
        elif pos % 2 == 0:
            result.append(' ')

    return ''.join(result)
#封装处理不同协议数据包的方法
class packet_processing:
    def __init__(self):
        self.packets: PacketList = []# 未过滤的包
        self.showedpackets: PacketList = [] # 过滤后的包
        self.no = 0
        
    # 展示一个.pcap文件
    def processing(self, packets, table: QTableWidget):
        self.packets = packets
        self.dataclear(table)
        self.no = 0
        for pkt in packets:
            if IP in pkt:
                ret = self.IP_processing(pkt, self.no)
            else:
                ret = self.no_IP_processing(pkt, self.no)
            self.showedpackets.append(pkt)
            #数据展示
            row = table.rowCount()
            table.insertRow(row)
            for i, item in enumerate(ret):
                item.setFlags(ret[i].flags() & ~Qt.ItemIsEditable) #不可编写
                table.setItem(row, i, item)
            self.no += 1
    
    # 展示实时监听到的流量
    def listen_processing(self, pkt, table: QTableWidget):
        self.packets.append(pkt)
        ret = []
        if IP in pkt:
            ret = self.IP_processing(pkt, self.no)
        else:
            ret = self.no_IP_processing(pkt, self.no)
        self.showedpackets.append(pkt)
        #数据展示
        row = table.rowCount()
        table.insertRow(row)
        for i, item in enumerate(ret):
            item.setFlags(ret[i].flags() & ~Qt.ItemIsEditable)
            table.setItem(row, i, item)
            self.no += 1
    #清除数据
    def dataclear(self, table: QTableWidget):
        table.clear()
        table.setHorizontalHeaderLabels(['No', 'time', 'src', 'dst', 'proto', 'length', 'info'])
        cnt = table.rowCount() - 1
        if cnt < 0:  #表格内为空
            return
        for i in range(cnt, -1, -1):
            table.removeRow(i)
            
    
    def showdata(self, origin: QLineEdit, row: int, analyse: QLineEdit):
        print('len:: ', len(self.showedpackets))
        origin.setText('')
        raw_data = self.showedpackets[row]
        raw_data = bytes(raw_data)
        # 将原始数据转换为十六进制字符串
        hex_string = binascii.hexlify(raw_data)

        # 打印十六进制字符串
        out = format_string(hex_string.decode())  # decode() 将 bytes 转换为 str
        print(out)
        origin.setText(str(out))
        
        summary = self.packets[row].summary()
        
        analyse.setText(str(summary))
        

    def IP_processing(self, pkt, No):
        # ret = [QTableWidgetItem(f'{No}'), QTableWidgetItem(f'{pkt.time}'), QTableWidgetItem(pkt[IP].src),
        # QTableWidgetItem(pkt[IP].dst), QTableWidgetItem(f'{pkt[IP].proto}'), QTableWidgetItem(f'{len(pkt)}'),
        # QTableWidgetItem(f'{pkt[IP].sport}-->{pkt[IP].dport}')]
        ret = [QTableWidgetItem(f'{No}'), QTableWidgetItem(f'{pkt.time}'), QTableWidgetItem(pkt[IP].src),
               QTableWidgetItem(pkt[IP].dst), QTableWidgetItem(f'{len(pkt)}')]

        return ret

    def no_IP_processing(self, pkt, No):
        ret = [QTableWidgetItem(f'{No}'), QTableWidgetItem(f'{pkt.time}'), QTableWidgetItem(pkt.src),
               QTableWidgetItem(pkt.dst), QTableWidgetItem(f'{len(pkt)}')]

        return ret


protocols = {
    0: "IP",  # Dummy header for IP options
    1: "ICMP",  # Internet Control Message Protocol
    2: "IGMP",  # Internet Group Management Protocol
    3: "GGP",  # Gateway-to-Gateway Protocol
    4: "IPv4",  # IP (as per RFC 791)
    6: "TCP",  # Transmission Control Protocol
    8: "EGP",  # Exterior Gateway Protocol
    9: "IGP",  # any private interior gateway (Cisco uses this for their IGRP)
    12: "PUP",  # PUP protocol
    17: "UDP",  # User Datagram Protocol
    20: "HMP",  # Host Monitoring Protocol
    22: "XNS-IDP",  # Xerox NS IDP
    27: "RDP",  # Reliable Datagram Protocol
    30: "NBP",  # Network Beacon Protocol
    36: "DCCP",  # Datagram Congestion Control Protocol
    39: "SIP",  # Stream Control Transmission Protocol
    41: "IPv6",  # IPv6 (as per RFC 2460)
    46: "RSVP",  # RSVP Encapsulation
    47: "GRE",  # Generic Routing Encapsulation
    50: "ESP",  # Encapsulating Security Payload
    51: "AH",  # Authentication Header
    58: "ICMPv6",  # ICMP for IPv6
    60: "CFTP",  # CFTP
    61: "Any host internal protocol",
    88: "EIGRP",  # Cisco's IGRP for IPv6
    89: "OSPF",  # Open Shortest Path First IGP
    94: "EtherIP",  # Ethernet-within-IP Encapsulation
    98: "ENCAP",  # Encapsulation Header
    103: "PIM",  # Protocol Independent Multicast
    108: "IPComp",  # IP Payload Compression Protocol
    112: "VRRP",  # Virtual Router Redundancy Protocol
    115: "L2TP",  # Layer Two Tunneling Protocol
    124: "ISIS over IPv4",  # Intermediate System to Intermediate System (IS-IS) over IPv4
    132: "SCTP",  # Stream Control Transmission Protocol
    135: "MH",  # Mobility Header
    136: "UDPLite",  # UDP-Lite (RFC 3828)
    137: "MPLS-in-IP",  # MPLS in IP (RFC 4023)
    # ... 其他协议号  
    # 注意：并非所有协议号都已被 IANA 分配或已在实际中使用  
}
