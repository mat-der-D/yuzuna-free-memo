import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import datetime


# ======================================================================================
#  Model
# ======================================================================================
class MainModel:
    def __init__(self, save_dir: str, filename_format: str):
        self.save_dir = save_dir
        self.filename_format = filename_format  # e.g. "{:%Y-%m-%d}.md"

    def save_text(self, raw_text: str):
        timestamp = datetime.datetime.now()
        save_path = os.path.join(self.save_dir, self.filename_format.format(timestamp))
        with open(save_path, "a") as f:
            f.write(self.format_log_message(raw_text, timestamp))

    @staticmethod
    def format_log_message(raw_text: str, timestamp: datetime) -> str:
        return f"**{timestamp:%H:%M:%S}**\n{raw_text}\n"


# ======================================================================================
#  View Model
# ======================================================================================
class MainViewModel:
    def __init__(self, model: MainModel):
        self.model = model
        self.count = tk.StringVar(value="0")
        self.text = tk.StringVar(value="\n")
        self.text.trace_add("write", lambda *_: self.sync_text_count())

    def sync_text_count(self):
        self.count.set(str(len(self.text.get()) - 1))

    def send_button_click(self):
        self.model.save_text(self.text.get())

    def text_change_handler(self, text: str):
        self.text.set(text)


# ======================================================================================
#  View
# ======================================================================================
class SendButton(tk.Button):
    def __init__(self, master=None, *, view_model):
        config = dict(
            text="送信",
            width="35",
            pady=5,
            fg="#ffffff",
            bg="#1E88E5",
            relief=tk.FLAT,
            font=("Meiryo UI", 14),
            anchor="center",
        )
        super().__init__(master, **config)
        self.vm = view_model
        self["command"] = self.vm.send_button_click


class Counter(tk.Label):
    def __init__(self, master=None, *, view_model):
        config = dict(
            text=0,
            width="10",
            font=("Meiryo UI", 14),
        )
        super().__init__(master, **config)

        self.vm = view_model
        self["textvariable"] = self.vm.count


class TextField(ScrolledText):
    text_change_notification_period_ms = 10

    def __init__(self, master=None, *, view_model):
        config = dict(
            font=("Meiryo UI", 12),
            height=7,
            width=55,
        )
        super().__init__(master, **config)

        self.vm = view_model
        self._text_cache = self.get(0.0, tk.END)
        self.master.after(self.text_change_notification_period_ms, self.notify_text_change)

    def notify_text_change(self):
        text = self.get(0.0, tk.END)
        if text != self._text_cache:
            self.vm.text_change_handler(text)
        self._text_cache = text
        self.master.after(self.text_change_notification_period_ms, self.notify_text_change)


class MainWindow(tk.Frame):
    def __init__(self, master=None, *, view_model: MainViewModel):
        super().__init__(master)
        self.vm = view_model

        text_frame = tk.Frame(master, width=500, height=100)
        TextField(text_frame, view_model=self.vm).pack()
        text_frame.pack()

        counter_button_frame = tk.Frame(master, width=500, height=30)
        Counter(counter_button_frame, view_model=self.vm).grid(column=0, row=0)
        SendButton(counter_button_frame, view_model=self.vm).grid(column=1, row=0)
        counter_button_frame.pack(padx=20, pady=10)


# ======================================================================================
#  Entry Point
# ======================================================================================
class FreeMemoApp:
    def __init__(self, save_dir: str, filename_format: str):
        self.root = tk.Tk()
        self._setup_window(self.root)
        model = MainModel(save_dir, filename_format)
        vm = MainViewModel(model)
        MainWindow(view_model=vm).pack()

    @staticmethod
    def _setup_window(root):
        root.title("フリーメモ")
        root.geometry("600x200")

    def launch(self):
        self.root.mainloop()


def main():
    # save_dir = "i:\\Knowledge_BackUP\\Daily"
    save_dir = r"C:\Temp"
    filename_format = "{:%Y-%m-%d}.md"
    app = FreeMemoApp(save_dir, filename_format)
    app.launch()


if __name__ == '__main__':
    main()
