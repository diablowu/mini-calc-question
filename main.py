import sys
fp = open('/dev/hidraw0', 'rb')


while True:
    buffer = fp.read(8)
    key = buffer[2]
    print("buff: ",buffer.hex())