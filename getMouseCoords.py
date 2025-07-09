import pyautogui as p
import keyboard

while True :
    while keyboard.is_pressed("F10") :
        print(p.position())