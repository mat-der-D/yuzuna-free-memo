import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import os
import datetime
from typing import Callable, Optional


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
        self.height = tk.IntVar()
        self.width = tk.IntVar()
        self.count = tk.StringVar(value="0")  # bind to Counter
        self.text = tk.StringVar(value="\n")  # bind to TextField
        self.text.trace_add("write", self.sync_text_count)

    def sync_text_count(self, *_):
        self.count.set(str(len(self.text.get()) - 1))

    def send_button_click(self):
        self.model.save_text(self.text.get())


# ======================================================================================
#  View
# ======================================================================================
def auto_resizable_widget(
        width_map: Optional[Callable[[int], int]],
        height_map: Optional[Callable[[int], int]],
        *, vm: str = "vm", height: str = "height", width: str = "width"):
    def _auto_resize(self):
        if width_map is not None:
            self["width"] = width_map(getattr(getattr(self, vm), width).get())
        if height_map is not None:
            self["height"] = height_map(getattr(getattr(self, vm), height).get())
        self.after(100, self._auto_resize)

    def create_init(cls):
        original = cls.__init__

        def __init__(self, *args, **kwargs):
            original(self, *args, **kwargs)
            self.after(100, self._auto_resize)

        return __init__

    def deco_impl(cls):
        cls._auto_resize = _auto_resize
        cls.__init__ = create_init(cls)
        return cls

    return deco_impl


@auto_resizable_widget(lambda x: max(x // 20 - 5, 0), None)
class SendButton(tk.Button):
    def __init__(self, master=None, *, view_model: MainViewModel, **kwargs):
        super().__init__(master, **kwargs)
        self.vm = view_model
        self["command"] = self.vm.send_button_click


class Counter(tk.Label):
    def __init__(self, master=None, *, view_model: MainViewModel, **kwargs):
        super().__init__(master, **kwargs)
        self.vm = view_model
        self["textvariable"] = self.vm.count


@auto_resizable_widget(lambda x: int(x / 10.8), lambda x: x // 25)
class TextField(ScrolledText):
    text_change_notification_period_ms = 10

    def __init__(self, master=None, *, view_model: MainViewModel, **kwargs):
        super().__init__(master, **kwargs)
        self.vm = view_model
        self._text_cache = self.get(0.0, tk.END)
        self.after(self.text_change_notification_period_ms, self.notify_text_change)

    def notify_text_change(self):
        text = self.get(0.0, tk.END)
        if text != self._text_cache:
            self.vm.text.set(text)  # bind text to self.vm.text
        self._text_cache = text
        self.master.after(self.text_change_notification_period_ms, self.notify_text_change)


class MainWindow(tk.Frame):
    def __init__(self, master=None, *, view_model: MainViewModel):
        super().__init__(master)
        self.vm = view_model

        TextField(
            self,
            view_model=self.vm,
            font=("Meiryo UI", 12),
        ).grid(column=0, row=0, columnspan=2, padx=5, pady=5)

        Counter(
            self,
            view_model=self.vm,
            height=1,
            width=10,
            font=("Meiryo UI", 14),
        ).grid(column=0, row=1)

        SendButton(
            self,
            view_model=self.vm,
            width=10,
            pady=5,
            text="送信",
            font=("Meiryo UI", 14),
            fg="#ffffff",
            bg="#1E88E5",
            relief=tk.FLAT,
        ).grid(column=1, row=1, padx=5, pady=5)

        self.master.bind("<Configure>", self.on_resize_frame)

    def on_resize_frame(self, _):
        self.vm.height.set(self.winfo_height())
        self.vm.width.set(self.winfo_width())


# ======================================================================================
#  Entry Point
# ======================================================================================
class FreeMemoApp:
    def __init__(self, save_dir: str, filename_format: str):
        self.root = tk.Tk()
        self.root.title("フリーメモ")

        model = MainModel(save_dir, filename_format)
        vm = MainViewModel(model)
        MainWindow(view_model=vm).pack(expand=True, fill=tk.BOTH)

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
