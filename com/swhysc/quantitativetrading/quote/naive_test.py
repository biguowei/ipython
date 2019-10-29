# -*- coding: utf-8 -*-

"""
深圳交易所binary行情v1.04
socket连接测试脚本

1 没有实现心跳包
2 没有体现重传等功能

@author 申万宏源证券信息技术开发总部 
@email xukai@swhysc.com
"""

import socket
import threading
import sys
from sz_messages import *
from sz_util import *


class MdReceiver(threading.Thread):
    def __init__(self, conn_parameter):
        threading.Thread.__init__(self)
        self.conn_parameter = conn_parameter
        self.socket = None
        self.stopped = False
        self.buffer = None
        self.app_ids = set()

    def run(self):
        address = (self.conn_parameter.ip, self.conn_parameter.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        logon_msg = Logon()
        logon_msg.HeartBtInt = self.conn_parameter.HeartBtInt
        buffer = bytearray(4096)
        # logon_msg.pack_to_buffer(buffer)
        buffer = logon_msg.pack()
        send_buffer(self.socket, buffer, len(buffer))
        while not self.stopped:
            self.receive_and_check_msg()

    def receive_and_check_msg(self):
        data = self.socket.recv(BUFFER_LEN)
        if self.buffer is None:
            self.buffer = data
        else:
            self.buffer = self.buffer + data
        self.try_parse_messages()

    def try_parse_messages(self):
        while True:
            parse_result = self.try_parse_message()
            if not parse_result:
                break

    def try_parse_message(self):
        header = MessageHeader()
        if len(self.buffer) < HEADER_LEN + TAILER_LEN:
            return False
        header.unpack_from(self.buffer, 0)
        forsee_len = (header.BodyLength + HEADER_LEN + TAILER_LEN)
        if len(self.buffer) < forsee_len:
            return False
        msg = create_message(header.MsgType)
        if msg is not None:
            msg.unpack_from(self.buffer)
            print(msg)
        else:
            if header.MsgType not in self.app_ids:
                print(header.MsgType)
                self.app_ids.add(header.MsgType)

        # process_msg(msg)
        # print("MessageType:%d" % header.MsgType)
        self.buffer = self.buffer[forsee_len:]


if __name__ == '__main__':
    conn_parameter = ConnectParameter()
    conn_parameter.ip = '192.168.26.199'
    conn_parameter.port = 9016
    receiver = MdReceiver(conn_parameter)
    receiver.run()
    sys.stdin.readline()
