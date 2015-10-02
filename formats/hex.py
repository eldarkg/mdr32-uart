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

'''Common for all hex format readers'''

class HexReaderException(Exception): ...

class HexReader:
    '''Common hex format reader'''

    def __iter__(self):
        return self

    def __next__(self):
        return self._file.readline()

    def open(self, path):
        '''Open file'''
        self._file = open(path)

    def close(self):
        '''Close opened file'''
        self._file.close()

    # Callback functions (events)
    def event_write_data(self, addr, data):
        ...

    def event_execute(self, addr):
        ...

