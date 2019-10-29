# -*- coding: utf-8 -*-

import struct

MSG_TYPE_LOGON = 1
MSG_TYPE_LOGOUT = 2
MSG_TYPE_HEATBEAT = 3

HEADER_LEN = 8
TAILER_LEN = 4


def generate_check_sum(buf, bufLen):
    idx = 0
    cks = 0
    for idx in range(0, bufLen):
        cks += buf[idx]
    return cks % 256


def sz_decode(bstr):
    return bstr.strip(b'\x00').decode()


def sz_encode(string):
    return string.encode()


class MessageHeader:
    def __init__(self):
        self.MsgType = 0
        self.BodyLength = 0

    def get_length(self):
        return HEADER_LEN

    def pack(self):
        return struct.pack('!II', self.MsgType, self.BodyLength)

    def unpack_from(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!II', buffer, offset)
        self.MsgType = unpack_tuple[0]
        self.BodyLength = unpack_tuple[1]


class MessageTailer:
    def __init__(self):
        self.Checksum = 0

    def get_length(self):
        return TAILER_LEN

    def pack(self):
        return struct.pack('!I', self.Checksum)

    def unpack_from(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!I', buffer, offset)
        self.Checksum = unpack_tuple[0]


class Message:
    def __init__(self):
        self.header = MessageHeader()
        self.tailer = MessageTailer()

    def pack(self):
        body_buffer = self._pack_body()
        self.header.BodyLength = len(body_buffer)
        header_buffer = self.header.pack()
        buffer = body_buffer + header_buffer
        self.tailer.Checksum = generate_check_sum(buffer, len(buffer))
        return header_buffer + body_buffer + self.tailer.pack()

    # def get_length(self):
    #    return HEADER_LEN + TAILER_LEN + self.header.BodyLength

    def unpack_from(self, buffer, offset=0):
        self.header.unpack_from(buffer, offset)
        body_begin = offset + HEADER_LEN
        self._unpack_body_from(buffer, body_begin)
        tailer_begin = body_begin + self.header.BodyLength
        self.tailer.unpack_from(buffer, tailer_begin)

    def __str__(self):
        return 'Message'

    def _pack_body(self):
        return b''

    def _unpack_body_from(self, buffer, offset):
        pass


class Logon(Message):

    def __init__(self):
        Message.__init__(self)
        self.header.MsgType = 1

        self.SenderCompID = ''
        self.TargetCompID = ''
        self.HeartBtInt = 0
        self.Password = ''
        self.DefaultApplVerID = ''

    def _pack_body(self):
        return struct.pack('!20s20si16s32s',
                           sz_encode(self.SenderCompID),
                           sz_encode(self.TargetCompID),
                           self.HeartBtInt,
                           sz_encode(self.Password),
                           sz_encode(self.DefaultApplVerID))

    def _unpack_body_from(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!20s20si16s32s', buffer, offset)
        self.SenderCompID = sz_decode(unpack_tuple[0])
        self.TargetCompID = sz_decode(unpack_tuple[1])
        self.HeartBtInt = unpack_tuple[2]
        self.Password = sz_decode(unpack_tuple[3])
        self.DefaultApplVerID = sz_decode(unpack_tuple[4])

    def __str__(self):
        return '[%d:%d]SenderCompID=%s,TargetCompID=%s,HeartBtInt=%s,' \
               'Password=%s,DefaultApplVerID=%s' % (
                   self.header.MsgType, self.header.BodyLength, self.SenderCompID, self.TargetCompID,
                   self.HeartBtInt, self.Password, self.DefaultApplVerID)


class Logout(Message):

    def __init__(self):
        Message.__init__(self)
        self.header.MsgType = 2

        self.SessionStatus = 0
        self.Text = ''

    def _pack_body(self):
        return struct.pack('!i200s',
                           self.SessionStatus,
                           sz_encode(self.Text))

    def _unpack_body_from(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!i200s', buffer, offset)
        self.SessionStatus = sz_decode(unpack_tuple[0])
        self.Text = sz_decode(unpack_tuple[1])

    def __str__(self):
        return '[%d:%d]SessionStatus=%d,Text=%s' % (
            self.header.MsgType, self.header.BodyLength, self.SessionStatus, self.Text)


class Heartbeat(Message):
    def __init__(self):
        Message.__init__(self)
        self.header.MsgType = MSG_TYPE_HEATBEAT
        self.header.BodyLength = 0

    def __str__(self):
        return 'Heartbeat'
