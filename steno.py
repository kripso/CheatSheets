import serial
import sys
import pyautogui

port = '/dev/cu.usbmodem03'
baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=0.001)

while True:
    data = ser.readline()
    if data:
        for _data in data:
            print(_data)
        if data[0] == 128:
            pass
            # if data[1] == 16:
            #     pyautogui.press("q")
            # if data[1] == 4:
            #     pyautogui.press("w")
            # if data[1] == 1:
            #     pyautogui.press("e")
            # if data[1] == 32:
            #     pyautogui.press("shift")
            # if data[1] == 8:
            #     pyautogui.press("a")
            # if data[1] == 2:
            #     pyautogui.press("s")
            # if data[2] == 8:
            #     pyautogui.press("r")
            # if data[2] == 64:
            #     pyautogui.press("d")
            # if data[2] == 4:
            #     pyautogui.press("f")

            # if data[2] == 16:
            #     pyautogui.press("ctrl")
    sys.stdout.flush()


# 128     128     128     128     128
# 64      16      4       1       0
# 0       0       0       0       8
# 0       0       0       0       0
# 0       0       0       0       0
# 0       0       0       0       0

# 128     128     128     128     128
# 32      8       2       0       0
# 0       0       0       64      4
# 0       0       0       0       0
# 0       0       0       0       0
# 0       0       0       0       0


# 160     128     128
# 0       0       0
# 0       32      16
# 0       0       0
# 0       0       0
# 0       0       0
wedsadawsddsaderrasssddad