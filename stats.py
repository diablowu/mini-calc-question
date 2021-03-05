import time
import sys
sys.path.append('/home/pi/apps/input/drive')
import SPI
import SSD1305
import random

import sys
fp = open('/dev/hidraw0', 'rb')

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess


def clean_screen(display,img_draw):
    img_draw.rectangle([(0,0),(width,height)], outline=0, fill=0)
    display.image(image)
    display.display()


key_num  =  83
key_div = 84
key_times = 85
key_backspace = 42
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


# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0


disp = SSD1305.SSD1305_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

disp.begin()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# # Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

padding = 0
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
# font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype('/home/pi/apps/input/msyhbd.ttc',16)


min_font = ImageFont.truetype('/home/pi/apps/input/msyhbd.ttc',10)

clean_screen(disp, draw)


def random_question():
    a = random.randint(0,15)
    b = random.randint(0,15)
    oper = random.randint(0,1)
    current_question = ""
    r = 0
    if oper == 1:
        current_question = f'{a} + {b} = ?'
        r = a + b
    else:
        if a > b:
            current_question = f'{a} - {b} = ?'
            r = a - b
        else:
            current_question = f'{b} - {a} = ?'
            r = b - a
        
    
    draw.text((0, 0), current_question,  font=font, fill=255)
    disp.image(image)
    disp.display()
    return r




if __name__ == '__main__':
    input_seq = []
    enter_input = False
    stats_input = False
    answer = 0
    result = dict(total = 0, good = 0,bad = 0)

    while True:
        answer = random_question()
        result['total'] = result['total'] + 1
        while True:
            key = read_key(fp)
            if key == 88:
                if len(input_seq) > 0:
                    if enter_input:
                        enter_input = False
                        x = 0
                        input_seq = []
                        clean_screen(disp, draw)
                        break
                    else:
                        enter_input = True
                        if answer == int(''.join(input_seq)):
                            result['good'] = result['good'] + 1
                            draw.text((100, 5), "正确",  font=min_font, fill=255)
                        else:
                            result['bad'] = result['bad'] + 1
                            draw.text((100, 5), "错误",  font=min_font, fill=255)
                        
                        disp.image(image)
                        disp.display()
                        continue
                
            elif key == key_backspace:
                pass
                # if x > 0:
                #     input_seq = input_seq[:len(input_seq)-1]
                #     clean_screen(disp, draw)
                #     draw.text((0, count), ''.join(input_seq),  font=font, fill=255)
                #     x = x - 10
                #     disp.image(image)
                #     disp.display()
            elif key >= 0 and key <= 9:
                if not enter_input:
                    curr_key = str(key)
                    input_seq.append(curr_key)
                    draw.text((x, 15), curr_key,  font=font, fill=255)
                    x = x + 10
                    disp.image(image)
                    disp.display()
            elif key == key_div: #print stats
                clean_screen(disp, draw)
                draw.text((0, 0), f"你一共完成了 {result['total']} 道题",  font=min_font, fill=255)
                draw.text((0, 10), f"做对了 {result['good']} 道题",  font=min_font, fill=255)
                draw.text((0, 20), f"做错了 {result['bad']} 道题",  font=min_font, fill=255)
                disp.image(image)
                disp.display()
                result = dict(total = 0, good = 0,bad = 0)
            elif key == key_times:
                enter_input = False
                x = 0
                input_seq = []
                clean_screen(disp, draw)
                break
            else:
                print(key)
    # disp.clear()
