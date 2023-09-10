import tkinter as tk
from tkinter.scrolledtext import ScrolledText

window = tk.Tk()
window.title("フリーメモ")
window.geometry("600x200")

text_frame = tk.Frame(window, width=500, height=100, bg="#ff0000")
text_frame.pack()
entry = ScrolledText(text_frame, font=("メイリオ", 14), height=5, width=40)
entry.pack()

frame = tk.Frame(window)
frame.pack(padx=20, pady=10)

send_button = tk.Button(frame, text="送信", width="50")
send_button.grid(row=0, column=0)

text_count = tk.Label(frame, text="20", width="20", font=("メイリオ", 14))
text_count.grid(row=0, column=1)

window.mainloop()
