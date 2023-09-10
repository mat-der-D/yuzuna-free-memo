import tkinter as tk
import tkinter as t
from tkinter.scrolledtext import ScrolledText

word_count = 0


def entry_count():
    global word_count
    word_count = entry.get(0.0, t.END)
    count_label["text"] = len(word_count) - 1
    root.after(1000, entry_count)


# メインウィンドウ作成
root = tk.Tk()
root.title("フリーメモ")
root.geometry("600x220")

# テキストフレーム・テキストボックス作成
text_frame = tk.Frame(root, width=500, height=100)
text_frame.pack()
entry = ScrolledText(text_frame, font=("メイリオ", 14), height=5, width=40)
entry.pack()

# 送信・文字数カウントラベル作成
frame = tk.Frame(root, width=500, height=30)
frame.pack(padx=20, pady=10)

count_label = tk.Label(frame, text=0, width="10", font=("BIZ UDゴシック", 14))
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
    font=("BIZ UDゴシック", 14),
    anchor="center",
)
send_button.grid(row=0, column=1)

root.mainloop()
