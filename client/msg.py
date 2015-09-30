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

'''Messages'''

class FontStyle:
    RED = '\033[38;5;1m'
    BLUE = '\033[38;5;39m'
    GREEN = '\033[38;5;114m'
    YELLOW = '\033[38;5;226m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def info_msg(msg):
    print(FontStyle.BOLD + FontStyle.GREEN + '[INFO]  ' + FontStyle.ENDC + msg)

def send_msg(msg):
    print(FontStyle.BOLD + FontStyle.YELLOW + '[SEND]  ' + FontStyle.ENDC + msg)

def rcv_msg(msg):
    print(FontStyle.BOLD + FontStyle.BLUE + '[RCV]   ' + FontStyle.ENDC + msg)
