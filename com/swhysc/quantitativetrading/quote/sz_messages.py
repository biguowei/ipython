# -*- coding: utf-8 -*-

import struct

MSG_TYPE_LOGON = 1
MSG_TYPE_LOGOUT = 2
MSG_TYPE_HEATBEAT = 3

# 390019
# 390012
# 309011
# 309111
# 300111
# 300192
# 300191
# 300592
# 300792
# 300591
# 300791
# 306311
# 390090
# 390095
MSG_TYPE_MKT_RT_STATUS = 390010
MSG_TYPE_BOARDCAST = 390012

MSG_TYPE_CATEGORY_SNASHOT = 300011
MSG_TYPE_CATEGORY_ORDER = 300092
MSG_TYPE_CATEGORY_DEAL = 300091

CTG_JZJJ = 1

HEADER_LEN = 8
TAILER_LEN = 4


def msg_type_belong_category(msg_type, msg_type_category):
    return msg_type > msg_type_category and (msg_type - msg_type_category) % 100 == 0


def msg_is_snapshot(msg):
    return msg_type_belong_category(msg.header.MsgType, MSG_TYPE_CATEGORY_SNASHOT)


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
        self._unpack_body_from(buffer, body_begin, self.header.BodyLength)
        tailer_begin = body_begin + self.header.BodyLength
        self.tailer.unpack_from(buffer, tailer_begin)

    def __str__(self):
        return 'Message'

    def _pack_body(self):
        return b''

    def _unpack_body_from(self, buffer, offset, bodylength):
        pass


class ExtendFields():
    def pack(self):
        return b''


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

    def _unpack_body_from(self, buffer, offset, bodylength):
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

    def _unpack_body_from(self, buffer, offset, bodylength):
        unpack_tuple = struct.unpack_from('!i200s', buffer, offset)
        self.SessionStatus = unpack_tuple[0]
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


class ExtendFields:
    def pack(self):
        return b''

    def unpack_from_buffer(self, buffer, offset):
        return


# 300011
class JZJJSnapshotExtendFields(ExtendFields):
    def __init__(self):
        ExtendFields.__init__(self)
        self.NoMdEntries = 0
        self.MdEntries = []

    def pack(self):
        b1 = struct.pack('!I', self.NoMdEntries)
        entry_bstrings = [entry.pack() for entry in self.MdEntries]
        return b1 + b''.join(entry_bstrings)

    def unpack_from_buffer(self, buffer, offset, totallength):
        unpack_tuple = struct.unpack_from('!I', buffer, offset)
        self.NoMdEntries = unpack_tuple[0]
        pos = offset + 4
        self.MdEntries.clear()
        for i in range(self.NoMdEntries):
            entry = JZJJSnapshotEFEntry()
            length = entry.unpack_from_buffer(buffer, pos)
            self.MdEntries.append(entry)
            pos += length

    def __str__(self):
        return ('NoMdEntries=%u:' % self.NoMdEntries) + ''.join([str(entry) for entry in self.MdEntries])


class JZJJSnapshotEFEntry:
    def __init__(self):
        self.MDEntryType = ''
        self.MDEntryPx = 0
        self.MDEntrySize = 0
        self.MDPriceLevel = 0
        self.NumberOfOrders = 0
        self.NoOrders = 0
        self.OrderQtyList = []

    def pack(self):
        self.NoOrders = len(self.OrderQtyList)
        qrder_qty_list_fmt = '!%dq' % self.NoOrders
        return (struct.pack('!2sqqIqI', self.MDEntryType,
                            self.MDEntryPx,
                            self.MDEntrySize,
                            self.MDPriceLevel,
                            self.NumberOfOrders,
                            self.NoOrders)
                + struct.pack(qrder_qty_list_fmt, *self.OrderQtyList))

    def unpack_from_buffer(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!2sqqHqI', buffer, offset)
        self.MDEntryType = sz_decode(unpack_tuple[0])
        self.MDEntryPx = unpack_tuple[1]
        self.MDEntrySize = unpack_tuple[2]
        self.MDPriceLevel = unpack_tuple[3]
        self.NumberOfOrders = unpack_tuple[4]
        self.NoOrders = unpack_tuple[5]
        pos = offset + struct.calcsize('!2sqqHqI')
        self.OrderQtyList = struct.unpack_from('!%dq' % self.NoOrders, buffer, pos)
        return struct.calcsize('!2sqqHqI') + struct.calcsize('!%dq' % self.NoOrders)

    def __str__(self):
        return ("[MDEntryType=%s,MDEntryPx=%ld,MDEntrySize=%ld,MDPriceLebel=%u," \
                "NumberOfOrders=%ld,NoOrders=%u" \
                % (self.MDEntryType,
                   self.MDEntryPx,
                   self.MDEntrySize,
                   self.MDPriceLevel,
                   self.NumberOfOrders,
                   self.NoOrders)) \
               + "(" + ','.join([str(qty) for qty in self.OrderQtyList]) + ')]'


# 300611
class PHDJSnapshotExtendFields(ExtendFields):
    def __init__(self):
        ExtendFields.__init__(self)
        self.NoMdEntries = 0
        self.MdEntries = []

    def pack(self):
        b1 = struct.pack('!I', self.NoMdEntries)
        entry_bstrings = [entry.pack() for entry in self.MdEntries]
        return b1 + b''.join(entry_bstrings)

    def unpack_from_buffer(self, buffer, offset, totallength):
        unpack_tuple = struct.unpack_from('!I', buffer, offset)
        self.NoMdEntries = unpack_tuple[0]
        pos = offset + 2
        self.MdEntries.clear()
        for i in range(self.NoMdEntries):
            entry = PHDJSnapshotEFEntry()
            length = entry.unpack_from_buffer(buffer, pos)
            self.MdEntries.append(entry)
            pos += length

    def __str__(self):
        return ('NoMdEntries=%u:' % self.NoMdEntries) + ''.join([str(entry) for entry in self.MdEntries])


class PHDJSnapshotEFEntry:
    def __init__(self):
        self.MDEntryType = ''
        self.MDEntryPx = 0
        self.MDEntrySize = 0

    def pack(self):
        self.NoOrders = len(self.OrderQtyList)
        return struct.pack('!2sqq', self.MDEntryType,
                           self.MDEntryPx,
                           self.MDEntrySize)

    def unpack_from_buffer(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!2sqq', buffer, offset)
        self.MDEntryType = sz_decode(unpack_tuple[0])
        self.MDEntryPx = unpack_tuple[1]
        self.MDEntrySize = unpack_tuple[2]

        return struct.calcsize('!2sqq')

    def __str__(self):
        return "[MDEntryType=%s,MDEntryPx=%ld,MDEntrySize=%ld]" \
               % (self.MDEntryType, self.MDEntryPx, self.MDEntrySize)


# 309011
class ZSHQSnapshotExtendFields(ExtendFields):
    def __init__(self):
        ExtendFields.__init__(self)
        self.NoMdEntries = 0
        self.MdEntries = []

    def pack(self):
        b1 = struct.pack('!I', self.NoMdEntries)
        entry_bstrings = [entry.pack() for entry in self.MdEntries]
        return b1 + b''.join(entry_bstrings)

    def unpack_from_buffer(self, buffer, offset, totallength):
        unpack_tuple = struct.unpack_from('!I', buffer, offset)
        self.NoMdEntries = unpack_tuple[0]
        pos = offset + 2
        self.MdEntries.clear()
        for i in range(self.NoMdEntries):
            entry = ZSHQSnapshotEFEntry()
            length = entry.unpack_from_buffer(buffer, pos)
            self.MdEntries.append(entry)
            pos += length

    def __str__(self):
        return ('NoMdEntries=%u:' % self.NoMdEntries) + ''.join([str(entry) for entry in self.MdEntries])


class ZSHQSnapshotEFEntry:
    def __init__(self):
        self.MDEntryType = ''
        self.MDEntryPx = 0

    def pack(self):
        return struct.pack('!2sq', self.MDEntryType, self.MDEntryPx)

    def unpack_from_buffer(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!2sq', buffer, offset)
        self.MDEntryType = sz_decode(unpack_tuple[0])
        self.MDEntryPx = unpack_tuple[1]
        return struct.calcsize('!2sq')

    def __str__(self):
        return "[MDEntryType=%s,MDEntryPx=%ld]" % (self.MDEntryType, self.MDEntryPx)


# 309111
class ZSHQSnapshotExtendFields(ExtendFields):
    def __init__(self):
        ExtendFields.__init__(self)
        self.StockNum = 0

    def pack(self):
        return struct.pack('!I', self.StockNum)

    def unpack_from_buffer(self, buffer, offset, totallength):
        unpack_tuple = struct.unpack_from('!I', buffer, offset)
        self.StockNum = unpack_tuple[0]

    def __str__(self):
        return 'StockNum=%u:' % self.StockNum


# 306311
class GGSSSnapshotExtendFields(ExtendFields):
    def __init__(self):
        ExtendFields.__init__(self)
        self.NoMdEntries = 0
        self.MdEntries = []
        self.NoComplexEventTimes = 0
        self.CESTEntries = []

    def pack(self):
        b1 = struct.pack('!I', self.NoMdEntries)
        entry_bstrings = [entry.pack() for entry in self.MdEntries]
        b2 = struct.pack('!I', self.NoComplexEventTimes)
        entry_bstrings2 = [entry.pack() for entry in self.CESTEntries]
        return b1 + b''.join(entry_bstrings) + b2 + b''.join(entry_bstrings2)

    def unpack_from_buffer(self, buffer, offset, totallength):
        pos = offset
        unpack_tuple = struct.unpack_from('!I', buffer, pos)
        self.NoMdEntries = unpack_tuple[0]
        pos = offset + 4
        self.MdEntries.clear()
        for i in range(self.NoMdEntries):
            entry = GGSSSnapshotEFMDEntry()
            length = entry.unpack_from_buffer(buffer, pos)
            self.MdEntries.append(entry)
            pos += length

        unpack_tuple = struct.unpack_from('!I', buffer, pos)
        self.NoComplexEventTimes = unpack_tuple[0]
        pos = offset + 4
        self.MdEntries.clear()
        for i in range(self.NoComplexEventTimes):
            entry = GGSSSnapshotEFCETEntry()
            length = entry.unpack_from_buffer(buffer, pos)
            self.CESTEntries.append(entry)
            pos += length

    def __str__(self):
        return ('NoMdEntries=%u:' % self.NoMdEntries) + ''.join([str(entry) for entry in self.MdEntries]) \
               + ('NoComplexEventTimes=%u:' % self.NoComplexEventTimes) + ''.join(
            [str(entry) for entry in self.CESTEntries])


class GGSSSnapshotEFMDEntry:
    def __init__(self):
        self.MDEntryType = ''
        self.MDEntryPx = 0
        self.MDEntrySize = 0
        self.MDPriceLevel = 0

    def pack(self):
        return struct.pack('!2sqqH', self.MDEntryType,
                           self.MDEntryPx,
                           self.MDEntrySize,
                           self.MDPriceLevel)

    def unpack_from_buffer(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!2sqqH', buffer, offset)
        self.MDEntryType = sz_decode(unpack_tuple[0])
        self.MDEntryPx = unpack_tuple[1]
        self.MDEntrySize = unpack_tuple[2]
        self.MDPriceLevel = unpack_tuple[3]
        return struct.calcsize('!2sqqH')

    def __str__(self):
        return "[MDEntryType=%s,MDEntryPx=%ld,MDEntrySize=%ld,MDPriceLevel=%u]" \
               % (self.MDEntryType, self.MDEntryPx, self.MDEntrySize, self.MDPriceLevel)


class GGSSSnapshotEFCETEntry:
    def __init__(self):
        self.ComplexEventStartTime = 0
        self.ComplexEventEndTime = 0

    def pack(self):
        return struct.pack('!qq', self.ComplexEventStartTime, self.ComplexEventEndTime)

    def unpack_from_buffer(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!qq', buffer, offset)
        self.ComplexEventStartTime = unpack_tuple[0]
        self.ComplexEventEndTime = unpack_tuple[1]
        return struct.calcsize('!qq')

    def __str__(self):
        return "[ComplexEventStartTime=%ld,ComplexEventEndTime=%ld]" \
               % (self.ComplexEventStartTime, self.ComplexEventEndTime)


class Snapshot(Message):
    def __init__(self):
        Message.__init__(self)
        self.OrigTime = 0
        self.ChannelNo = 0
        self.MDStreamID = ''
        self.SecurityID = ''
        self.SecurityIDSource = ''
        self.TradingPhaseCode = ''
        self.PrevClosePx = 0
        self.NumTrades = 0
        self.TotalVolumeTrade = 0
        self.TotalValueTrade = 0
        self.ExtendFields = None

    def _pack_body(self):
        tmp = struct.pack('!qH3s8s4s8sqqqq',
                          self.OrigTime,
                          self.ChannelNo,
                          sz_encode(self.MDStreamID),
                          sz_encode(self.SecurityID),
                          sz_encode(self.SecurityIDSource),
                          sz_encode(self.TradingPhaseCode),
                          self.PrevClosePx,
                          self.NumTrades,
                          self.TotalVolumeTrade,
                          self.TotalValueTrade)
        if self.ExtendFields is None:
            return tmp
        else:
            return tmp + self.ExtendFields.pack()

    def _unpack_body_from(self, buffer, offset, bodylength):
        unpack_tuple = struct.unpack_from('!qH3s8s4s8sqqqq', buffer, offset)
        self.OrigTime = unpack_tuple[0]
        self.ChannelNo = unpack_tuple[1]
        self.MDStreamID = sz_decode(unpack_tuple[2])
        self.SecurityID = sz_decode(unpack_tuple[3])
        self.SecurityIDSource = sz_decode(unpack_tuple[4])
        self.TradingPhaseCode = sz_decode(unpack_tuple[5])
        self.PrevClosePx = unpack_tuple[6]
        self.NumTrades = unpack_tuple[7]
        self.TotalVolumeTrade = unpack_tuple[8]
        self.TotalValueTrade = unpack_tuple[9]
        parse_length = struct.calcsize('!qH3s8s4s8sqqqq')
        if self.header.MsgType == 300111:
            self.ExtendFields = JZJJSnapshotExtendFields()
            self.ExtendFields.unpack_from_buffer(buffer, offset + parse_length, bodylength - parse_length)
            return
        if self.header.MsgType == 300611:
            self.ExtendFields = PHDJSnapshotExtendFields()
            self.ExtendFields.unpack_from_buffer(buffer, offset + parse_length, bodylength - parse_length)
            return
        if self.header.MsgType == 309011:
            self.ExtendFields = ZSHQSnapshotExtendFields()
            self.ExtendFields.unpack_from_buffer(buffer, offset + parse_length, bodylength - parse_length)
            return
        if self.header.MsgType == 306311:
            self.ExtendFields = GGSSSnapshotExtendFields()
            self.ExtendFields.unpack_from_buffer(buffer, offset + parse_length, bodylength - parse_length)
            return

    def __str__(self):
        return "[%d]OrigTime=%ld,ChannelNo=%d,MDStreamID=%s,SecurityID=%s," \
               "SecurityIDSource=%s,TradingPhaseCode=%s,PrevClosePx=%ld," \
               "NumTrades=%ld,TotalVolumeTrade=%ld,TotalValueTrade=%ld," % (
               self.header.MsgType, self.OrigTime, self.ChannelNo, self.MDStreamID,
               self.SecurityID, self.SecurityIDSource, self.TradingPhaseCode,
               self.PrevClosePx, self.NumTrades, self.TotalVolumeTrade, self.TotalValueTrade) \
               + str(self.ExtendFields)


# 300192
class JZJJOrderExtendFields(ExtendFields):
    def __init__(self):
        ExtendFields.__init__(self)
        self.OrdType = 0

    def pack(self):
        return struct.pack('!c', self.OrdType)

    def unpack_from_buffer(self, buffer, offset, length):
        unpack_tupe = struct.unpack_from('!c', buffer, offset)
        self.OrdType = sz_decode(unpack_tupe[0])

    def __str__(self):
        return "OrdType=%c" % self.OrdType


# 300592
class XYJYOrderExtendFields(ExtendFields):
    def __init__(self):
        ExtendFields.__init__(self)
        self.ConfirmID = ''
        self.Contactor = ''
        self.ContactInfo = ''

    def pack(self):
        return struct.pack('!8s12s30s', sz_encode(self.ConfirmID), sz_encode(self.Contactor),
                           sz_encode(self.ContactInfo))

    def unpack_from_buffer(self, buffer, offset, length):
        unpack_tupe = struct.unpack_from('!8s12s30s', buffer, offset)
        self.ConfirmID = sz_decode(unpack_tupe[0])
        self.Contactor = sz_decode(unpack_tupe[1])
        self.ContactInfo = sz_decode(unpack_tupe[2])

    def __str__(self):
        return "ConfirmID=%s,Contactor=%s,ContactInfo=%s" % (self.ConfirmID, self.Contactor, self.ContactInfo)


# 300792
class ZRTOrderExtendFields(ExtendFields):
    def __init__(self):
        ExtendFields.__init__(self)
        self.ExpirationDays = 0
        self.ExpirationType = '1'

    def pack(self):
        return struct.pack('!HB', self.ExpirationDays, self.ExpirationType)

    def unpack_from_buffer(self, buffer, offset, length):
        unpack_tupe = struct.unpack_from('!HB', buffer, offset)
        self.ExpirationDays = unpack_tupe[0]
        self.ExpirationType = unpack_tupe[1]

    def __str__(self):
        return "ExpirationDays=%u,ExpirationType=%c" % (self.ExpirationDays, self.ExpirationType)


class Order(Message):
    def __init__(self):
        Message.__init__(self)
        self.ChannelNo = 0
        self.ApplSeqNum = 0
        self.MDStreamID = ''
        self.SecurityID = ''
        self.SecurityIDSource = ''
        self.Price = 0
        self.OrderQty = 0
        self.Side = '1'
        self.TransactTime = 0
        self.ExtendFields = None

    def _pack_body(self):
        tmp = struct.pack('!Hq3s8s4sqqcq', self.ChannelNo,
                          self.ApplSeqNum,
                          sz_encode(self.MDStreamID),
                          sz_encode(self.SecurityID),
                          sz_encode(self.SecurityIDSource),
                          self.Price,
                          self.OrderQty,
                          self.Side,
                          self.TransactTime)
        if self.ExtendFields is not None:
            return tmp + self.ExtendFields.pack()
        else:
            return tmp

    def _unpack_body_from(self, buffer, offset, bodylength):
        unpack_tuple = struct.unpack_from('!Hq3s8s4sqqcq', buffer, offset)
        self.ChannelNo = unpack_tuple[0]
        self.ApplSeqNum = unpack_tuple[1]
        self.MDStreamID = sz_decode(unpack_tuple[2])
        self.SecurityID = sz_decode(unpack_tuple[3])
        self.SecurityIDSource = sz_decode(unpack_tuple[4])
        self.Price = unpack_tuple[5]
        self.OrderQty = unpack_tuple[6]
        self.Side = sz_decode(unpack_tuple[7])
        self.TransactTime = unpack_tuple[8]
        parse_length = struct.calcsize('!Hq3s8s4sqqcq')
        if self.header.MsgType == 300192:
            self.ExtendFields = JZJJOrderExtendFields()
            self.ExtendFields.unpack_from_buffer(buffer, offset + parse_length, bodylength - parse_length)
            return
        if self.header.MsgType == 300592:
            self.ExtendFields = XYJYOrderExtendFields()
            self.ExtendFields.unpack_from_buffer(buffer, offset + parse_length, bodylength - parse_length)
            return
        if self.header.MsgType == 300792:
            self.ExtendFields = ZRTOrderExtendFields()
            self.ExtendFields.unpack_from_buffer(buffer, offset + parse_length, bodylength - parse_length)
            return

    def __str__(self):
        return "[%d]ChannelNo=%u,ApplSeqNum=%ld,MDStreamID=%s,SecurityID=%s," \
               "SecurityIDSource=%s,Price=%ld,OrderQty=%ld,Side=%c,TransactTime=%ld" \
               % (self.header.MsgType,
                  self.ChannelNo,
                  self.ApplSeqNum,
                  self.MDStreamID,
                  self.SecurityID,
                  self.SecurityIDSource,
                  self.Price,
                  self.OrderQty,
                  self.Side,
                  self.TransactTime) + str(self.ExtendFields)


class Deal(Message):
    def __init__(self):
        Message.__init__(self)
        self.ChannelNO = 0
        self.ApplSeqNum = 0
        self.MDStreamID = ''
        self.BidApplSeqNum = 0
        self.OfferApplSeqNum = 0
        self.SecurityID = ''
        self.SecurityIDSource = ''
        self.LastPx = 0
        self.LastQty = 0
        self.ExecType = 'c'
        self.TransactTime = 0
        self.ExtendFields = None

    def _pack_body(self):
        struct.pack('!Hq3sqq8s4sqqcq', self.ChannelNO,
                    self.ApplSeqNum,
                    sz_encode(self.MDStreamID),
                    self.BidApplSeqNum,
                    self.OfferApplSeqNum,
                    sz_encode(self.SecurityID),
                    sz_encode(self.SecurityIDSource),
                    self.LastPx,
                    self.LastQty,
                    self.ExecType,
                    self.TransactTime) + \
        b'' if self.ExtendFields is None else self.ExtendFields.pack()

    def _unpack_body_from(self, buffer, offset, bodylength):
        unpack_tuple = struct.unpack_from('!Hq3sqq8s4sqqcq', buffer, offset)
        self.ChannelNO = unpack_tuple[0]
        self.ApplSeqNum = unpack_tuple[1]
        self.MDStreamID = sz_decode(unpack_tuple[2])
        self.BidApplSeqNum = unpack_tuple[3]
        self.OfferApplSeqNum = unpack_tuple[4]
        self.SecurityID = sz_decode(unpack_tuple[5])
        self.SecurityIDSource = sz_decode(unpack_tuple[6])
        self.LastPx = unpack_tuple[7]
        self.LastQty = unpack_tuple[8]
        self.ExecType = sz_decode(unpack_tuple[9])
        self.TransactTime = unpack_tuple[10]

    def __str__(self):
        return "[%d]ChannelNo=%u,ApplSeqNum=%ld,MDStreamID=%s," \
               "BidApplSeqNum=%ld,OfferApplSeqNum=%ld,SecurityID=%s," \
               "SecurityIDSource=%s,LastPx=%ld,LastQty=%ld,ExecType=%c,TransactTime=%ld" \
               % (
                   self.header.MsgType,
                   self.ChannelNO,
                   self.ApplSeqNum,
                   self.MDStreamID,
                   self.BidApplSeqNum,
                   self.OfferApplSeqNum,
                   self.SecurityID,
                   self.SecurityIDSource,
                   self.LastPx,
                   self.LastQty,
                   self.ExecType,
                   self.TransactTime)


# 390019
class MktRTStatus(Message):
    def __init__(self):
        Message.__init__(self)
        self.OrigTime = 0
        self.ChannelNo = 0
        self.MarketID = ''
        self.MarketSegmentID = ''
        self.TradingSessionID = ''
        self.TradingSessionSubID = ''
        self.TradeStatus = 0
        self.TradSesStartTime = 0
        self.TradSesEndTime = 0
        self.ThresholdAmount = 0
        self.PosAmt = 0
        self.AmountStatus = 0

    def _pack_body(self):
        return struct.pack('!qH8s8s4s4sHqqqqc',
                           self.OrigTime,
                           self.ChannelNo,
                           sz_encode(self.MarketID),
                           sz_encode(self.MarketSegmentID),
                           sz_encode(self.TradingSessionID),
                           sz_encode(self.TradingSessionSubID),
                           self.TradeStatus,
                           self.TradSesStartTime,
                           self.TradSesEndTime,
                           self.ThresholdAmount,
                           self.PosAmt,
                           self.AmountStatus)

    def _unpack_body_from(self, buffer, offset, bodylength):
        unpack_tuple = struct.unpack_from('!qH8s8s4s4sHqqqqc', buffer, offset)
        self.OrigTime = unpack_tuple[0]
        self.ChannelNo = unpack_tuple[1]
        self.MarketID = sz_decode(unpack_tuple[2])
        self.MarketSegmentID = sz_decode(unpack_tuple[3])
        self.TradingSessionID = sz_decode(unpack_tuple[4])
        self.TradingSessionSubID = sz_decode(unpack_tuple[5])
        self.TradeStatus = unpack_tuple[6]
        self.TradSesStartTime = unpack_tuple[7]
        self.TradSesEndTime = unpack_tuple[8]
        self.ThresholdAmount = unpack_tuple[9]
        self.PosAmt = unpack_tuple[10]
        self.AmountStatus = sz_decode(unpack_tuple[11])

    def __str__(self):
        return "[%d]OrigTime=%ld,ChannelNo=%u,MarketID=%s,MarketSegmentID=%s," \
               "TradingSessionID=%s,TradingSessionSubID=%s,TradeStatus=%u," \
               "TradSesStartTime=%ld,TradSesEndTime=%ld,ThresholdAmount=%ld," \
               "PosAmt=%ld,AmountStaus=%c" \
               % (self.header.MsgType,
                  self.OrigTime,
                  self.ChannelNo,
                  self.MarketID,
                  self.MarketSegmentID,
                  self.TradingSessionID,
                  self.TradingSessionSubID,
                  self.TradeStatus,
                  self.TradSesStartTime,
                  self.TradSesEndTime,
                  self.ThresholdAmount,
                  self.PosAmt,
                  self.AmountStatus)


# 390013
class SecRTStatusSwitchEntry:
    def __init__(self):
        self.SecuritySwitchType = 0
        self.SecuritySwitchStatus = 0

    def pack(self):
        return struct.pack('!HH', self.SecuritySwitchType, \
                           self.SecuritySwitchStatus)

    def unpack_from(self, buffer, offset):
        unpack_tuple = struct.unpack_from('!HH', buffer, offset)
        self.SecuritySwitchType = unpack_tuple[0]
        self.SecuritySwitchStatus = unpack_tuple[1]
        return struct.calcsize('!HH')

    def __str__(self):
        return '[SwitchType=%u,SwitchStatus=%u]' \
               % (self.SecuritySwitchType, self.SecuritySwitchStatus)


class SecRTStatus(Message):
    def __init__(self):
        Message.__init__(self)
        self.OrigTime = 0
        self.ChannelNo = 0
        self.SecurityID = ''
        self.SecurityIDSource = ''
        self.FinancialStatus = ''
        self.NoSwitch = 0
        self.Switchs = []

    def _pack_body(self):
        self.NoSwitch = len(self.Switchs)
        b1 = struct.pack('!qH8s4s8sI',
                         self.OrigTime,
                         self.ChannelNo,
                         sz_encode(self.SecurityID),
                         sz_encode(self.SecurityIDSource),
                         sz_encode(self.FinancialStatus),
                         self.NoSwitch)
        entry_bstrings = [entry.pack() for entry in self.Switchs]
        return b1 + b''.join(entry_bstrings)

    def _unpack_body_from(self, buffer, offset, bodylength):
        unpack_tuple = struct.unpack_from('!qH8s4s8sI', buffer, offset)
        self.OrigTime = unpack_tuple[0]
        self.ChannelNo = unpack_tuple[1]
        self.SecurityID = sz_decode(unpack_tuple[2])
        self.SecurityIDSource = sz_decode(unpack_tuple[3])
        self.FinancialStatus = sz_decode(unpack_tuple[4])
        self.NoSwitch = unpack_tuple[5]
        self.Switchs.clear()
        pos = offset + struct.calcsize('!qH8s4s8sI')
        for i in range(self.NoSwitch):
            entry = SecRTStatusSwitchEntry()
            parse_len = entry.unpack_from(buffer, pos)
            pos += parse_len
            self.Switchs.append(entry)

    def __str__(self):
        return ("[%d]OrigTime=%ld,ChannelNo=%u,SecurityID=%s,SecurityIDSource=%s," \
                "FinancialStatus=%s,NoSwitch=%u:" \
                % (self.header.MsgType,
                   self.OrigTime,
                   self.ChannelNo,
                   self.SecurityID,
                   self.SecurityIDSource,
                   self.FinancialStatus,
                   self.NoSwitch)) \
               + ''.join([str(entry) for entry in self.Switchs])


class Boardcast(Message):
    def __init__(self):
        Message.__init__(self)
        self.OrigTime = 0
        self.ChannelNo = 0
        self.NewsID = ''
        self.Headline = ''
        self.RawDataFormat = ''
        self.RawDataLength = 0
        self.RawData = b''

    def _pack_body(self):
        self.RawDataLength = len(self.RawData)
        b1 = struct.pack('!qH8s128s8sH', self.OrigTime, self.ChannelNo,
                         sz_encode(self.NewsID),
                         sz_encode(self.Headline),
                         sz_encode(self.RawDataFormat),
                         self.RawDataLength)
        b2 = struct.pack('!%us' % self.RawDataLength, self.RawData)
        return b1 + b2

    def _unpack_body_from(self, buffer, offset, bodylength):
        unpack_tuple = struct.unpack_from('!qH8s128s8sH', buffer, offset)
        self.OrigTime = unpack_tuple[0]
        self.ChannelNo = unpack_tuple[1]
        self.NewsID = sz_decode(unpack_tuple[2])
        self.Headline = sz_decode(unpack_tuple[3])
        self.RawDataFormat = sz_decode(unpack_tuple[4])
        self.RawDataLength = unpack_tuple[5]
        pos = offset + struct.calcsize('!qH8s128s8sH')
        self.RawData = struct.unpack_from('!qH8s128s8sH',
                                          buffer, pos)

    def __str__(self):
        return 'OrigTime=%ld,ChannelNo=%u,NewsID=%s,Headline=%s,' \
               'RawDataFormat=%s,RawDataLength=%u' \
               % (self.OrigTime, self.ChannelNo, self.NewsID, self.Headline,
                  self.RawDataFormat, self.RawDataLength)
