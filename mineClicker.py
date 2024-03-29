from pynput.mouse import Button, Controller, Listener
import threading
import time
import ctypes
import tkinter as tk
import pygame
from tkinter import messagebox

VK_CONTROL = 0x11

mouse = Controller()
clicking_left = False
clicking_right = False
click_interval = 0.044  # デフォルトのクリック間隔
play_click_sound = True  # クリック音を再生するかどうかのフラグ

pygame.init()
click_sound = pygame.mixer.Sound("click.mp3")
click_sound.set_volume(0.5)  # クリック音の音量を設定

listener = None  # Listenerオブジェクトをグローバルに定義

def click_left():
    global clicking_left, click_interval
    while clicking_left:
        mouse.press(Button.left)
        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0x0002, 0)
        mouse.release(Button.left)
        time.sleep(click_interval)

def click_right():
    global clicking_right, click_interval
    while clicking_right:
        mouse.press(Button.right)
        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0, 0)
        time.sleep(0.01)
        ctypes.windll.user32.keybd_event(VK_CONTROL, 0, 0x0002, 0)
        mouse.release(Button.right)
        time.sleep(click_interval)

def play_click_sound_loop():
    while clicking_left or clicking_right:
        if play_click_sound:
            click_sound.play()
        time.sleep(0.1)  # チェック間隔

def on_click(x, y, button, pressed):
    global clicking_left, clicking_right
    if button == Button.x2:
        if pressed:
            clicking_right = True
            threading.Thread(target=click_right).start()
            threading.Thread(target=play_click_sound_loop).start()
        else:
            clicking_right = False
    elif button == Button.x1:
        if pressed:
            clicking_left = True
            threading.Thread(target=click_left).start()
            threading.Thread(target=play_click_sound_loop).start()
        else:
            clicking_left = False

def on_release(x, y, button):
    if button == Button.x2:
        print("Stopped clicking right.")
    elif button == Button.x1:
        print("Stopped clicking left.")

def start_clicking():
    global click_interval, listener
    click_interval = float(interval_entry.get())
    if listener is not None:
        listener.stop()
    listener = Listener(on_click=on_click, on_release=on_release)
    listener.start()

def stop_clicking():
    global clicking_left, clicking_right, listener
    clicking_left = False
    clicking_right = False
    if listener is not None:
        listener.stop()

def toggle_click_sound():
    global play_click_sound
    play_click_sound = not play_click_sound
    if play_click_sound:
        messagebox.showinfo("Click Sound", "クリック音を再生します。")
    else:
        messagebox.showinfo("Click Sound", "クリック音を再生しません。")

# Tkinterアプリケーションの作成
app = tk.Tk()
app.title("Mine Clicker")

# アイコンの設定
ICON_PATH = "yuzu.ico"
app.iconbitmap(default=ICON_PATH)

# ラベルとエントリーの作成
interval_label_text = "0.044=CPS 18\nCPSを上げたい場合は数値を低くしてください。"
interval_label = tk.Label(app, text=interval_label_text)
interval_label.pack()

interval_entry = tk.Entry(app)
interval_entry.insert(0, "0.044")  # デフォルト値を設定
interval_entry.pack()

# クリック開始と停止ボタンの作成
start_button = tk.Button(app, text="Start", command=start_clicking)
start_button.pack()

stop_button = tk.Button(app, text="Stop", command=stop_clicking)
stop_button.pack()

# クリック音を制御するボタンの作成
toggle_sound_button = tk.Button(app, text="Click Sound ON/OFF", command=toggle_click_sound)
toggle_sound_button.pack()

# マウスの説明文
mouse_instruction_text = "マウスの戻るボタンは左クリック\n進むボタンは右クリックです"
mouse_instruction_label = tk.Label(app, text=mouse_instruction_text)
mouse_instruction_label.pack()

# Tkinterアプリケーションの実行
app.mainloop()