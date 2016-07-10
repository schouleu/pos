#!/usr/bin/env python

from serial import Serial
import sys
import curses.ascii

def generate_lrc(real_msg_with_etx):
    lrc = 0
    for char in real_msg_with_etx:
        lrc ^= ord(char)
    return lrc

msg = ""
def read_tpe(serial):
    global msg
    ascii_names = curses.ascii.controlnames
    c = serial.read(1)
    print "Read 0x%02x (%s)"%(ord(c),c)
    if c == chr(ascii_names.index('ENQ')):
        print "<ENQ"
        serial.write(chr(ascii_names.index('ACK')))
        print ">ACK"
        return
    if c == chr(ascii_names.index('STX')):
        print "<STX"
        msg = serial.read(35)
        print "msg (%d)= %s"%(len(msg),msg)
        serial.write(chr(ascii_names.index('ACK')))
        print ">ACK"
        return
    if c == chr(ascii_names.index('ETX')):
        print "<ETX"
        c = serial.read(1)
        print "<0x%02x"%ord(c)
        serial.write(chr(ascii_names.index('ACK')))
        print ">ACK"
        return
    if c == chr(ascii_names.index('EOT')):
        print "<EOT"
        serial.write(chr(ascii_names.index('ENQ')))
        print "<ENQ"
        c = serial.read(1)
        if c != chr(ascii_names.index('ACK')):
            print "Expected ACK!"
            return
        print "<ACK"
        serial.write(chr(ascii_names.index('STX')))
        print ">STX"
        msg2 = msg[0:2]         # pos number
        msg2 += "1"             # transaction result
        msg2 += msg[2:10]       # amount
        msg2 += msg[11]         # payment mode
        msg2 += msg[13:16]      # currency numeric
        msg2 += msg[16:26]      # private
        msg2 += chr(ascii_names.index('ETX'))
        print "ETX=%s == 0x%x"%(chr(ascii_names.index('ETX')), ascii_names.index('ETX'))
        lrc = generate_lrc(msg2)
        serial.write(msg2)
        print ">msg=%s"%msg2
        serial.write(chr(lrc))
        print ">lrc=0x%02x"%lrc
        c = serial.read(1)
        if c != chr(ascii_names.index('ACK')):
            print "Expected ACK2!"
            return
        print "<ACK"
        serial.write(chr(ascii_names.index('EOT')))
        print ">EOT"
        


def main():
    if len(sys.argv) != 2:
        print "Usage: %s <tty device>"%sys.argv[0]
        sys.exit(1)
    fd = Serial(sys.argv[1])
    while True:
        read_tpe(fd)

if __name__ == '__main__':
    main()
