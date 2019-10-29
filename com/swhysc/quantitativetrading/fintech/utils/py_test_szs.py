# -*- coding: utf-8 -*-

import socket
import threading
import sys
from com.swhysc.utils.sz_messages import *

BUFFER_LEN = 4096


def send_buffer(s, buf, len):
    send_len = 0
    while send_len < len:
        last_send = s.send(buf[send_len:len])
        send_len += last_send


def create_message(msg_type):
    result = None
    if MSG_TYPE_LOGON == msg_type:
        return Logon()
    if MSG_TYPE_LOGOUT == msg_type:
        return Logout()
    if MSG_TYPE_HEATBEAT == msg_type:
        return Heartbeat()
    return result


class ConnectParameter:
    def __init__(self):
        self.ip = ''
        self.port = 0
        self.SenderCompID = ''
        self.TargetCompID = ''
        self.HeartBtInt = 3
        self.Password = 'password'
        self.DefautApplVerID = 'ver1.1'


class MdReceiver(threading.Thread):
    def __init__(self, conn_parameter):
        threading.Thread.__init__(self)
        self.conn_parameter = conn_parameter
        self.socket = None
        self.stopped = False
        self.buffer = None

    def run(self):
        address = (self.conn_parameter.ip, self.conn_parameter.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(address)
        logon_msg = Logon()
        logon_msg.HeartBtInt = conn_parameter.HeartBtInt
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
        msg.unpack_from(self.buffer)
        print(msg)
        # process_msg(msg)
        # print("MessageType:%d" % header.MsgType)
        self.buffer = self.buffer[forsee_len:]


if __name__ == '__main__':
    conn_parameter = ConnectParameter()
    conn_parameter.ip = '192.168.26.199'
    conn_parameter.port = 9016
    receiver = MdReceiver(conn_parameter)
    receiver.start()
    sys.stdin.readline()
