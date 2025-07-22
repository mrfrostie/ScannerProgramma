import tkinter.messagebox
import pyautogui as p
import keyboard
import tkinter

while True :
    while keyboard.is_pressed("F10") :
        print(p.position())
