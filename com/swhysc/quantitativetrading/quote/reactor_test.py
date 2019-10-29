# -*- coding: utf-8 -*-

"""
深圳交易所binary行情v1.04
连接测试脚本

1 实现心跳包
2 自动重连
3 没有体现重传等功能

@author 申万宏源证券
@email xukai@swhysc.com
"""

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from sz_messages import *
from sz_util import *
import time
import threading
import sys
import signal


def signal_handler(signum, frame):
    receiver.disconnect()
    sys.exit()


class SZBinProtocol(Protocol):
    def __init__(self, conn_parameter, receiver):
        Protocol.__init__(self)
        self.buffer = None
        self.conn_parameter = conn_parameter
        self.last_receive_ts = 0.0
        self.last_send_ts = 0.0
        self.connected = False
        self.receiver = receiver

    def dataReceived(self, data):
        last_receive_ts = time.time()
        if self.buffer is None:
            self.buffer = data
        else:
            self.buffer = self.buffer + data
        self.try_parse_messages()

    def connectionMade(self):
        print("connectionMade")
        self.connected = True
        self.last_receive_ts = time.time()
        logon_msg = Logon()
        logon_msg.HeartBtInt = self.conn_parameter.HeartBtInt
        logon_msg.DefaultApplVerID = self.conn_parameter.DefautApplVerID
        logon_msg.Password = self.conn_parameter.Password
        logon_msg.SenderCompID = self.conn_parameter.SenderCompID
        logon_msg.TargetCompID = self.conn_parameter.TargetCompID
        buffer = logon_msg.pack()
        self.transport.write(buffer)

    def sendMessage(self, msg):
        self.transport.write(msg.pack())
        self.last_send_ts = time.time()

    def test_heartbeat(self):
        now = time.time()
        if self.connected:
            if now - self.last_send_ts > self.conn_parameter.HeartBtInt:
                self.sendMessage(Heartbeat())
        if now - self.last_receive_ts > 2 * self.conn_parameter.HeartBtInt:
            # self.connected = False
            # self.receiver.disconnect()
            pass

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
            self.receiver.on_msg(msg)
        self.buffer = self.buffer[forsee_len:]


class SZBinProtocolFactory(ReconnectingClientFactory):
    def __init__(self, conn_parameter, receiver):
        ReconnectingClientFactory.__init__(self)
        self.conn_parameter = conn_parameter
        self.receiver = receiver

    def startedConnecting(self, connector):
        print('Started to connect')

    def buildProtocol(self, addr):
        self.resetDelay()

        protocol = SZBinProtocol(self.conn_parameter, self.receiver)
        self.receiver.register_protocol(protocol)
        return protocol

    def clientConnectionLost(self, connector, reason):
        print('Lost connection.  Reason:', reason)
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


class SZReceiver:
    def __init__(self, conn_parameter):
        self.conn_parameter = conn_parameter
        self.protocol = None
        self.sz_thread = None
        self.usr_msg_callback = None

    def start(self):
        # point = TCP4ClientEndpoint(reactor,  self.conn_parameter.ip, self.conn_parameter.port)
        # connectProtocol(point, self.protocol)
        reactor.callWhenRunning(self.test_heartbeat)
        reactor.connectTCP(self.conn_parameter.ip, self.conn_parameter.port,
                           SZBinProtocolFactory(self.conn_parameter, self))
        reactor.run(installSignalHandlers=False)

    def connect(self):
        self.sz_thread = threading.Thread(target=self.start)
        self.sz_thread.start()

    def register_protocol(self, protocol):
        self.protocol = protocol

    def test_heartbeat(self):
        if self.protocol is not None:
            self.protocol.test_heartbeat()
        reactor.callLater(1, self.test_heartbeat)

    def on_msg(self, msg):
        if self.usr_msg_callback is not None:
            self.usr_msg_callback(msg)

    def register_usr_msg_callback(self, callback):
        self.usr_msg_callback = callback

    def disconnect(self):
        reactor.stop()


def on_msg(msg):
    if msg is not None:
        print(msg)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    conn_parameter = ConnectParameter()
    conn_parameter.ip = '192.168.26.199'
    conn_parameter.port = 9016
    receiver = SZReceiver(conn_parameter)
    receiver.register_usr_msg_callback(on_msg)
    receiver.connect()
    sys.stdin.read()
