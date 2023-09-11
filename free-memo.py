import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import datetime


def original():
    # def用変数定義
    word_count = 0
    daily_dir = "i:\\Knowledge_BackUP\\Daily"
    today_data = datetime.date.today()
    date_format = "%Y-%m-%d"
    time_format = "%H:%M"
    daily_today = today_data.strftime(date_format)
    file_path = f"{os.path.join(daily_dir, daily_today)}.md"

    # 文字数カウントdef
    def entry_count():
        global word_count
        word_count = entry.get(0.0, tk.END)
        count_label["text"] = len(word_count) - 1
        root.after(1000, entry_count)

    # ボタンクリックdef
    def send_button_click():
        daily_file = open(file_path, mode="a", encoding="UTF-8")
        daily_file.write(f"**{now()}**\n{entry.get(0.0, tk.END)}\n")
        entry.delete(0.0, tk.END)
        daily_file.close()

    # 現在の取得を取得def
    def now():
        global time_format
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
    entry = ScrolledText(text_frame, font=("Meiryo UI", 12), height=7, width=55)
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


# ==================================================================================

def create_text_frame(master):
    text_frame = tk.Frame(master, width=500, height=100)
    text_field = ScrolledText(text_frame, font=("Meiryo UI", 12), height=7, width=55)
    text_field.pack()
    return text_frame, text_field


def create_counter(master):
    counter = tk.Label(master, text=0, width="10", font=("Meiryo UI", 14))
    return counter


def create_send_button(master, command):
    send_button = tk.Button(
        master,
        text="送信",
        width="35",
        pady=5,
        fg="#ffffff",
        bg="#1E88E5",
        relief=tk.FLAT,
        font=("Meiryo UI", 14),
        anchor="center",
        command=command,
    )
    return send_button


def save_and_clear_text(target_path: str, text_widget: ScrolledText, timestamp_format: str):
    template = "**{:" + timestamp_format + "}**\n{}\n"

    with open(target_path, mode="a", encoding="UTF-8") as f:
        timestamp = datetime.datetime.now()
        body = text_widget.get(0.0, tk.END)
        f.write(template.format(timestamp, body))

    text_widget.delete(0.0, tk.END)


def create_main_window(master, file_path, timestamp_format):
    main_window = tk.Frame(master)

    text_frame, text_field = create_text_frame(main_window)
    text_frame.pack()

    counter_button_frame = tk.Frame(main_window, width=500, height=30)
    counter_button_frame.pack(padx=20, pady=10)
    counter = create_counter(counter_button_frame)
    counter.grid(row=0, column=0)

    def send_button_click():
        # 変数のスコープを犯す(引数でもらっていない変数を処理に使う)という「変な」ことをするので、
        # それ以外の変わったことを極力同じところでしないことで認知負荷を下げる
        return save_and_clear_text(file_path, text_field, timestamp_format)

    send_button = create_send_button(counter_button_frame, send_button_click)
    send_button.grid(row=0, column=1)

    def launch_auto_sync(root, *, period_ms=1000):  # 普通はクラスで実現する
        def one_step():
            text = text_field.get(0.0, tk.END)
            counter["text"] = len(text) - 1
            root.after(period_ms, one_step)

        one_step()

    return main_window, launch_auto_sync


def launch_app(save_file_path: str, timestamp_format: str, *, sync_period_ms=1000):
    root = tk.Tk()
    root.title("フリーメモ")
    root.geometry("600x220")

    main_window, launch_auto_sync = create_main_window(root, save_file_path, timestamp_format)
    main_window.pack()

    launch_auto_sync(root, period_ms=sync_period_ms)
    root.mainloop()


def main():
    # 平時にいじる部分は一か所にまとめる
    save_dir = "i:\\Knowledge_BackUP\\Daily"
    file_name = f"{datetime.date.today():%Y-%m-%d}.md"
    file_path = os.path.join(save_dir, file_name)
    timestamp_format = "%H:%M"

    launch_app(file_path, timestamp_format, sync_period_ms=10)


if __name__ == '__main__':
    main()
