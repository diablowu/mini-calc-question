import sys
fp = open('/dev/hidraw0', 'rb')




key_num  =  83
bytes_enter = 88
bytes_num_noop = 0x00
bytes_num_1    =  89
bytes_num_2    =  90
keys = {89,90,91,92,93,94,95,96,97,98}

def is_num_keycode(keycode:int)->bool:
    return keycode >= 89 and keycode <= 98


def not_num_keycode(keycode:int)->bool:
    return not is_num_keycode(keycode)

def numkeycode2val(keycode:int)->int:
    if not is_num_keycode(keycode):
        return keycode

    if keycode == 98:
        return 0
    else:
        return keycode - 88
    



buffer:bytes









    
    

def read_first(dev)->bytes:
    buffer = dev.read(8)
    return buffer

def read_num(dev)->int:
    ret = 0
    for i in range(6):
        buffer = dev.read(8)
        key = buffer[2]
        if is_num_keycode(key):
            ret = numkeycode2val(key)
    return ret


def read_key(dev)->int:
    ret = 0
    break_at_next = False
    for i in range(6):
        buffer = dev.read(8)

        if break_at_next:
            break
        key = buffer[2]
        # print("read key :",key, (key != key_num))

        if key != key_num and key != 0 and not_num_keycode(key):
            break_at_next = True
            ret = key
        if is_num_keycode(key):
            ret = numkeycode2val(key)

        
    return ret


if __name__ == '__main__':
    while True:
        print("read key : ",read_key(fp))