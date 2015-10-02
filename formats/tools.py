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

'''Tools for parse ascii hex files'''

def getint(string, bpos, bnum):
    '''Get int with bnum bytes from bpos byte position'''

    return int(string[bpos*2:(bpos+bnum)*2], base=16)

def getarray(string, bpos, bnum):
    '''Get byte array with bnum bytes from bpos byte position'''

    return bytearray.fromhex(string[bpos*2:(bpos+bnum)*2])

