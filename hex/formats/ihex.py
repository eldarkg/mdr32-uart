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

'''ihex 32-bit format file processing'''

import struct

from hex import *
import tools

class IHexReaderException(HexReaderException): ...

class IHexRecType:
    DATA = 0
    EOF = 1
    ESEGADDR = 2
    SSEGADDR = 3
    ELINADDR = 4
    SLINADDR = 5

class IHexReader(HexReader):
    '''ihex 32-bit format file reader'''

    def __init__(self):
        self._base = 0

    def __next__(self):
        entry = HexReader.__next__(self)
        if entry:
            result = IHexReader.decode(entry.rstrip())
            if result['rectype'] == IHexRecType.EOF:
                raise StopIteration
            else:
                self._rec_handle(result)

            return result
        else:
            raise IHexReaderException("didn't find end of file")

    def decode(entry):
        '''Decode ihex entry from string to dict'''
        out = {}

        if entry[0] != ':':         # record mark
            raise IHexReaderException("didn't find record mark")
        entry = entry[1:]

        out['reclen'] = tools.getint(entry, 0, 1)
        if len(entry) / 2 != 5 + out['reclen']:
            raise IHexReaderException('incorrect length')

        out['offset'] = tools.getint(entry, 1, 2)
        out['rectype'] = tools.getint(entry, 3, 1)
        out['data'] = tools.getarray(entry, 4, out['reclen'])
        out['chksum'] = tools.getint(entry, 4 + out['reclen'], 1)

        chksum = (out['reclen'] + (out['offset'] & 0xFF) + (out['offset'] >> 8) +
                  out['rectype'] + sum(out['data'])) & 0xFF

        if (chksum + out['chksum']) & 0xFF != 0:
            raise IHexReaderException('incorrect checksum')

        return out

    def _rec_handle(self, rec):
        '''Check record type and call events'''
        if rec['rectype'] == IHexRecType.ELINADDR:
            self._base = struct.unpack('>H', rec['data'])[0] << 16
        elif rec['rectype'] == IHexRecType.DATA:
            offs = rec['offset']
            addr = self._base + offs
            self.event_write_data(addr, rec['data'])
        elif rec['rectype'] == IHexRecType.SLINADDR:
            addr = struct.unpack('>I', rec['data'])[0]
            self.event_execute(addr)


if __name__ == '__main__':
    import sys

    reader = IHexReader()
    reader.open(sys.argv[1])

    for entry in reader:
        print(entry)

    reader.close()
