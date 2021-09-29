from threading import Thread
import threading
import sys
import pyautogui
import keyboard  # using module keyboard
import time
# while True:  # making a loop
#     try:  # used try so that if user pressed other than the given key error will not be shown
#         if keyboard.is_pressed('c'):  # if key 'q' is pressed
#             print(pyautogui.position())
#             # break  # finishing the loop 347 206
#             # break  # finishing the loop 1334 947
#         if keyboard.is_pressed('s'):
#             # img = pyautogui.screenshot(f'/Users/rolandrajcsanyi/Documents/programing/PySnippets/screenshots/page_{pageNumber}.png', region=(347, 206, 1334, 947))
#             img = pyautogui.screenshot(f'/Users/rolandrajcsanyi/Documents/programing/PySnippets/screenshots/page_{pageNumber}.png', region=(700, 404, 1900, 1490))
#             pageNumber += 1
#         if keyboard.is_pressed('d'):
#             pyautogui.click(940, 961)
#     except:
#         break

# time.sleep(10)
# for i in range(34):
#     time.sleep(2)
#     img = pyautogui.screenshot(f'/Users/rolandrajcsanyi/Documents/programing/PySnippets/screenshots/page_{i+1}.png', region=(700, 404, 1900, 1490))
#     pyautogui.click(940, 961)


def do_work(id, stop):
    time.sleep(10)

    pageNumber = 1
    while True:
        if stop():
            break
        time.sleep(2)
        pyautogui.screenshot(f'/Users/rolandrajcsanyi/Documents/programing/PySnippets/screenshots/page_{pageNumber}.png', region=(700, 404, 1900, 1490))
        pageNumber += 1
        pyautogui.click(940, 961)

    print("Thread {}, signing off".format(id))


def main():

    stop_threads = False
    workers = []

    worker = threading.Thread(target=do_work, args=(1, lambda: stop_threads))
    workers.append(worker)
    worker.start()

    pageNumber = 1

    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('c'):  # if key 'q' is pressed
                print(pyautogui.position())
                # break  # finishing the loop 347 206
                # break  # finishing the loop 1334 947
            if keyboard.is_pressed('s'):
                # img = pyautogui.screenshot(f'/Users/rolandrajcsanyi/Documents/programing/PySnippets/screenshots/page_{pageNumber}.png', region=(347, 206, 1334, 947))
                img = pyautogui.screenshot(f'/Users/rolandrajcsanyi/Documents/programing/PySnippets/screenshots/page_{pageNumber}.png', region=(700, 404, 1900, 1490))
                pageNumber += 1
            if keyboard.is_pressed('d'):
                pyautogui.click(940, 961)
            if keyboard.is_pressed('f'):
                break
        except:
            break
    print('main: done sleeping; time to stop the threads.')
    stop_threads = True
    for worker in workers:
        worker.join()
    print('Finish.')


if __name__ == '__main__':
    main()
