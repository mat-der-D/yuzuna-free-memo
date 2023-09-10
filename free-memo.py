import tkinter as tk
import tkinter as t
from tkinter.scrolledtext import ScrolledText

imput_word = 0


def entry_count():
    global input_word
    input_word = entry.get(0.0, t.END)
    text_count["text"] = len(input_word) - 1
    window.after(1000, entry_count)


# メインウィンドウ作成
window = tk.Tk()
window.title("フリーメモ")
window.geometry("600x200")

# テキストフレーム・テキストボックス作成
text_frame = tk.Frame(window, width=500, height=100, bg="#ff0000")
text_frame.pack()
entry = ScrolledText(text_frame, font=("メイリオ", 14), height=5, width=40)
entry.pack()

# 送信・文字数カウントラベル作成
frame = tk.Frame(window)
frame.pack(padx=20, pady=10)

send_button = tk.Button(frame, text="送信", width="50")
send_button.grid(row=0, column=0)

text_count = tk.Label(frame, text=0, width="20", font=("メイリオ", 14))
entry_count()
text_count.grid(row=0, column=1)

window.mainloop()
