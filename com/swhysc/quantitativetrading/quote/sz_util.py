# -*- coding: utf-8 -*-
from sz_messages import *

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
    if 300111 == msg_type or 309011 == msg_type or 306311 == msg_type or 309111 == msg_type or 300611 == msg_type:
        return Snapshot()
    if 300192 == msg_type or 300592 == msg_type or 300792 == msg_type:
        return Order()
    if 300191 == msg_type or 300591 == msg_type or 300791 == msg_type:
        return Deal()
    if 390019 == msg_type:
        return MktRTStatus()
    if 390013 == msg_type:
        return SecRTStatus()
    if 390012 == msg_type:
        return Boardcast()
    return result


class ConnectParameter():
    def __init__(self):
        self.ip = ''
        self.port = 0
        self.SenderCompID = 'test'
        self.TargetCompID = 'test'
        self.HeartBtInt = 3
        self.Password = 'test'
        self.DefautApplVerID = '1.03'
