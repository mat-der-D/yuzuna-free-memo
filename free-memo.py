import tkinter as tk
import tkinter as t
from tkinter.scrolledtext import ScrolledText
import os
import datetime

# def用変数定義
word_count = 0
daily_dir = "i:\\Knowledge_BackUP\\Daily"
today_data = datetime.date.today()
date_format = "%Y-%m-%d"
time_format = "%H:%M"
daily_today = today_data.strftime(date_format)
file_path = f"{os.path.join(daily_dir,daily_today)}.md"


# 文字数カウントdef
def entry_count():
    global word_count
    word_count = entry.get(0.0, t.END)
    count_label["text"] = len(word_count) - 1
    root.after(1000, entry_count)


# ボタンクリックdef
def send_button_click():
    daily_file = open(file_path, mode="a", encoding="UTF-8")
    daily_file.write(f"**{now()}**\n{entry.get(0.0, t.END)}\n")
    entry.delete(0.0, t.END)
    daily_file.close()


# 現在の取得を取得def
def now():
    time_data = datetime.datetime.now().time()
    time_now = time_data.strftime(time_format)
    return time_now


# メインウィンドウ作成
root = tk.Tk()
root.title("フリーメモ")
root.geometry("600x220")

# テキストフレーム・テキストボックス作成
text_frame = tk.Frame(root, width=500, height=100)
text_frame.pack()
entry = ScrolledText(
    text_frame,
    font=("Meiryo UI", 12),
    height=7,
    width=55,
)
entry.pack()

# 送信・文字数カウントラベル作成
frame = tk.Frame(root, width=500, height=30)
frame.pack(padx=20, pady=10)

count_label = tk.Label(frame, text=0, width="10", font=("Meiryo UI", 14))
entry_count()
count_label.grid(row=0, column=0)

send_button = tk.Button(
    frame,
    text="送信",
    width="35",
    pady=5,
    fg="#ffffff",
    bg="#1E88E5",
    relief=tk.FLAT,
    font=("Meiryo UI", 14),
    anchor="center",
    command=send_button_click,
)

send_button.grid(row=0, column=1)
root.mainloop()
