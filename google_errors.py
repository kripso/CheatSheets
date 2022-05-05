import pyautogui
import time


def main():
    # pyautogui.leftClick()
    time.sleep(10)
    r = 143  # number of errors
    while True:
        print(pyautogui.position())
        pyautogui.click(x=1298, y=449)
        time.sleep(0.1)
        pyautogui.click(x=1233, y=540)
        time.sleep(0.1)
        if r == 0:
            break
        r -= 1


if __name__ == '__main__':
    main()
