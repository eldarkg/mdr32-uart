# Copyright (C) 2015  Eldar Khayrullin <eldar.khayrullin@mail.ru>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''MDR32 standard boot loader client'''

import binascii
import serial
import time

from .msg import *

VERBOSE     = True
RCV_TIMEOUT = 0.010     # sec

class CMD:
    SYNC = b'\x00'
    CR   = b'\x0D'
    CRN  = b'\x0A\x3E'
    BAUD = b'\x42'
    LOAD = b'\x4C'
    VFY  = b'\x59'
    RUN  = b'\x52'

class ERR:
    R_OK = b'\x4B'
    ERR  = b'\x45'
    CHN  = b'\x69'
    CMD  = b'\x63'
    BAUD = b'\x62'

class MDR32BootClientException(Exception): ...

class MDR32BootClient:
    def __init__(self):
        ...

    def open(self, port):
        self._port = serial.Serial(port, 9600, 8, 'N', 1)
        if VERBOSE:
            info_msg('Serial port is opened')

    def close(self):
        self._port.close()
        if VERBOSE:
            info_msg('Serial port is closed')

    def connect(self):
        while True:
            self._send_bytes(CMD.SYNC)
            time.sleep(RCV_TIMEOUT)
            if self._port.inWaiting():
                rcv = self._rcv_bytes()
                if rcv == CMD.CR:
                    rcv = self._rcv_bytes(2)
                    if rcv != CMD.CRN:
                        raise MDR32BootClientException('received incorrect response')
                    break
                else:
                    raise MDR32BootClientException('received incorrect response')
        if VERBOSE:
            info_msg('Connected to Board')

    def cmd_sync(self):
        self._send_cmd(CMD.SYNC)
        self.cmd_cr()

    def cmd_cr(self):
        self._clean_rcv()
        self._send_bytes(CMD.CR)
        rcv = self._rcv_test()
        if rcv == CMD.CR:
            rcv = self._rcv_bytes(2)
            if rcv != CMD.CRN:
                raise MDR32BootClientException('received incorrect response')
        else:
            raise MDR32BootClientException('received incorrect response')

    def cmd_baud(self, baud):
        self._send_baud_cmd(baud)
        self.cmd_cr()

    def cmd_load(self, addr, array):
        self._send_cmd(CMD.LOAD, addr, len(array), array)
        self.cmd_cr()

    def cmd_vfy(self, addr, size):
        self._send_cmd(CMD.VFY, addr, size)
        array = self._rcv_bytes(size)
        self._rcv_reply_test()
        self.cmd_cr()
        return array

    def cmd_run(self, vtbl):
        self._send_cmd(CMD.RUN, vtbl)
        info_msg('Board is running. Start addr is ' + '0x' + '{0:X}'.format(vtbl))

    def _send_cmd(self, cmd, *params):
        self._send_bytes(cmd)
        self._rcv_test()
        if params:
            rcv = None
            for param in params:
                if type(param) is bytes:
                    bs = param
                else:
                    bs = param.to_bytes(4, 'little')
                self._send_bytes(bs)
                rcv = self._rcv_test()
            if cmd == CMD.LOAD:
                if rcv != ERR.R_OK:
                    raise MDR32BootClientException('received incorrect response')
            elif rcv != cmd:
                raise MDR32BootClientException('received incorrect response')

    def _send_baud_cmd(self, baud):
        self._send_bytes(CMD.BAUD)
        self._rcv_test()
        self._send_bytes(baud.to_bytes(4, 'little'))
        self._port.close()
        self._port.setBaudrate(baud)
        self._port.open()
        # Fix issue: set baud rate before send data
        self._send_bytes(CMD.BAUD)
        self._rcv_test()
        self._send_bytes(baud.to_bytes(4, 'little'))
        rcv = self._rcv_test()
        if rcv != CMD.BAUD:
            raise MDR32BootClientException('received incorrect response')
        info_msg('Baudrate is ' + str(baud))

    def _rcv_bytes(self, bnum=1):
        rcv = self._port.read(bnum)
        if VERBOSE:
            rcv_msg('Bytes: ' + str(binascii.hexlify(rcv)).upper())
        return rcv

    def _send_bytes(self, array):
        self._port.write(array)
        if VERBOSE:
            send_msg('Bytes: ' + str(binascii.hexlify(array)).upper())

    def _rcv_test(self):
        time.sleep(RCV_TIMEOUT)
        if self._port.inWaiting():
            rcv = self._rcv_bytes()
            if rcv == ERR.ERR:
                self._err_rcv()
            else:
                return rcv

    def _rcv_reply_test(self):
        time.sleep(RCV_TIMEOUT)
        if self._port.inWaiting():
            rcv = self._rcv_bytes()
            if rcv != ERR.R_OK:
                raise MDR32BootClientException('received incorrect response')
        else:
                raise MDR32BootClientException('rcv timeout')

    def _clean_rcv(self):
        n = self._port.inWaiting()
        self._port.read(n)

    def _err_rcv(self):
        rcv = self._rcv_bytes()
        raise MDR32BootClientException('ERR: ' + rcv.decode('utf-8'))

if __name__ == '__main__':
    import sys

    client = MDR32BootClient()
    client.open(sys.argv[1])
    client.connect()
    while True:
        print('> ', end='')
        cmd = input()
        if cmd == 'sync': client.cmd_sync()
        elif cmd == 'cr': client.cmd_cr()
        elif cmd == 'baud': client.cmd_baud(int(input('baud> ')))
        elif cmd == 'load':
            client.cmd_load(int(input('addr> '), base=16),
                            bytes.fromhex(input('array> ')))
        elif cmd == 'vfy':
            client.cmd_vfy(int(input('addr> '), base=16),
                           int(input('size> ')))
        elif cmd == 'run': client.cmd_run(int(input('addr> '), base=16))
        elif cmd == 'q': break

    client.close()
