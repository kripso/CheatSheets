import serial_asyncio
import aioserial
from serial import Serial
import concurrent
import asyncio
import serial
import sys
import pyautogui
import binascii
import select
import os

port = '/dev/cu.usbmodem03'
baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=0.001)

STENO_KEY_CHART = ("Fn", "#1", "#2", "#3", "#4", "#5", "#6",
                   "S1-", "S2-", "T-", "K-", "P-", "W-", "H-",
                   "R-", "A-", "O-", "*1", "*2", "res1", "res2",
                   "pwr", "*3", "*4", "-E", "-U", "-F", "-R",
                   "-P", "-B", "-L", "-G", "-T", "-S", "-D",
                   "#7", "#8", "#9", "#A", "#B", "#C", "-Z")

BYTES_PER_STROKE = 6


# while True:
#     packet = ser.readline()
#     if packet:
#         if not (packet[0] & 0x80) or sum(b & 0x80 for b in packet[1:]):
#             print('discarding invalid packet: %s', binascii.hexlify(packet))
#             continue
#         steno_keys = []
#         for i, b in enumerate(packet):
#             for j in range(1, 8):
#                 if (b & (0x80 >> j)):
#                     steno_keys.append(STENO_KEY_CHART[i * 7 + j - 1])
#         print(steno_keys)


async def read_and_print(aioserial_instance: aioserial.AioSerial):
    while True:
        a_line_of_at_most_certain_size_of_bytes_read: bytes = await aioserial_instance.readline_async(6)
        print(a_line_of_at_most_certain_size_of_bytes_read)
        # print((await aioserial_instance.read_async()).decode(errors='ignore'), end='', flush=True)

asyncio.run(read_and_print(aioserial.AioSerial(port='/dev/cu.usbmodem03')))
