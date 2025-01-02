import tkinter as tk
from tkinter import ttk


class MyFrame(ttk.Frame):
    """自定义的 Frame 组件，允许设置宽度和高度，并禁用自动调整大小"""

    def __init__(self, master=None, width=None, height=None):
        """
        初始化自定义 Frame。

        参数:
            master (Tk): 父容器。
            width (int): Frame 的宽度（可选）。
            height (int): Frame 的高度（可选）。
        """
        super().__init__(master, padding=(5, 0, 5, 0))
        if width is not None:
            self.config(width=width)
        if height is not None:
            self.config(height=height)
        self.pack_propagate(False)  # 禁用自动调整，保持固定大小


class MyLabel(MyFrame):
    """自定义的 Label 组件，居中显示文本"""

    def __init__(self, master, text, width=None, height=30):
        """
        初始化自定义 Label。

        参数:
            master (Tk): 父容器。
            text (str): 显示的文本。
            width (int): Label 的宽度（可选）。
            height (int): Label 的高度，默认为 30。
        """
        super().__init__(master, width=width, height=height)

        self.label = ttk.Label(self, text=text, anchor="center")
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True, anchor="w")  # 让 Label 填充整个 Frame


class MySpinbox(MyFrame):
    """自定义的 Spinbox 组件"""

    def __init__(self, master, width=None, height=30):
        """
        初始化自定义 Spinbox。

        参数:
            master (Tk): 父容器。
            width (int): Spinbox 的宽度（可选）。
            height (int): Spinbox 的高度，默认为 30。
        """
        super().__init__(master, width=width, height=height)

        self.spinbox = ttk.Spinbox(self)
        self.spinbox.pack(side=tk.LEFT, fill=tk.X, expand=True, anchor="w")


class MyRangeButton(MyFrame):
    """自定义的 RangeButton 组件，当前仅包含一个 Canvas"""

    def __init__(self, master, width=None, height=30, background="#000"):
        """
        初始化自定义 RangeButton。

        参数:
            master (Tk): 父容器。
            width (int): RangeButton 的宽度（可选）。
            height (int): RangeButton 的高度，默认为 30。
            background (str): Canvas 的背景颜色，默认为黑色 (#000)。
        """
        super().__init__(master, width=width, height=height)

        self.canvas = tk.Canvas(self, background=background, highlightthickness=0)
        self.canvas.pack()


class MyEntry(MyFrame):
    """自定义的 Entry 组件"""

    def __init__(self, master, width=None, height=30):
        """
        初始化自定义 Entry。

        参数:
            master (Tk): 父容器。
            width (int): Entry 的宽度（可选）。
            height (int): Entry 的高度，默认为 30。
        """
        super().__init__(master, width=width, height=height)

        self.entry = ttk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, anchor="w")


class MyButton(MyFrame):
    """自定义的 Button 组件"""

    def __init__(self, master, width=None, height=30):
        """
        初始化自定义 Button。

        参数:
            master (Tk): 父容器。
            width (int): Button 的宽度（可选）。
            height (int): Button 的高度，默认为 30。
        """
        super().__init__(master, width=width, height=height)

        self.button = ttk.Button(self)
        self.button.pack()


class TitleLine(ttk.Frame):
    """一个包含多个标题（Label）的自定义Frame组件"""

    def __init__(self, master=None, title_dict: dict = None):
        """
        初始化Title组件。

        参数:
            master (Tk): 父容器，通常是Tk主窗口或其他Frame。
            title_dict (dict): 包含索引和标题信息的字典，值为(标题文本, 标题宽度)元组。
        """
        super().__init__(master)
        self.title_dict = {}  # 用于保存每个Label的字典。

        # 如果提供了title_dict，则遍历创建对应的Label
        if title_dict is not None:
            for i in title_dict.keys():
                title_text, title_width = title_dict[i]
                title_label = MyLabel(self, text=title_text, width=title_width)
                title_label.configure(style="TitleLine.TFrame")
                title_label.label.config(style="TitleLine.TLabel")
                title_label.pack(side=tk.LEFT, anchor="w")
                self.title_dict[i] = title_label  # 将Label存储到字典中。

    def set_title(self, index, title_text):
        """
        更新特定索引处的标题文本。

        参数:
            index (int): 要更新的Label的索引。
            title_text (str): 新的标题文本。
        """
        # 检查index是否存在于字典中，如果存在则更新Label的文本属性
        if index in self.title_dict:
            my_label = self.title_dict[index]
            my_label.label.config(text=title_text)  # 更新Label的文本属性。


class InformationLine(ttk.Frame):
    """信息行组件，包含编号、时间选择、记录按钮、保存按钮、备注输入框和删除按钮"""

    def __init__(self, master):
        super().__init__(master, padding=(0, 2, 0, 2))
        self.configure(style="InfoLine.TFrame")

        self.line_number = MyLabel(self, "10", 50)
        self.line_number.label.configure(style="InfoLine.TLabel")
        self.line_number.configure(style="InfoLine.TFrame")
        self.line_number.pack(side=tk.LEFT, anchor="w")

        self.time = MyEntry(self, 100)
        self.time.entry.configure(style="InfoLine.TEntry")
        self.time.configure(style="InfoLine.TFrame")
        self.time.pack(side=tk.LEFT, anchor="w")

        self.rec_s = MyRangeButton(self, 50)
        self.rec_s.configure(style="InfoLine.TFrame")
        self.rec_s.pack(side=tk.LEFT, anchor="w")

        self.save = MyRangeButton(self, 50)
        self.save.configure(style="InfoLine.TFrame")
        self.save.pack(side=tk.LEFT, anchor="w")

        self.note = MyEntry(self, 200)
        self.note.entry.configure(style="InfoLine.TEntry")
        self.note.configure(style="InfoLine.TFrame")
        self.note.pack(side=tk.LEFT, anchor="w")

        self.del_b = MyButton(self, 50)
        self.del_b.button.configure(style="InfoLine.TButton")
        self.del_b.button.configure(text="X", width=3)
        self.del_b.configure(style="InfoLine.TFrame")
        self.del_b.pack(side=tk.LEFT, anchor="w")


class InfoLineFrame(ttk.Frame):
    """带有滚动条的信息行容器，可以添加多条信息行"""

    def __init__(self, master, background: str="#000"):
        """
        初始化信息行容器。

        参数:
            master (Tk): 父容器。
            background (str): 背景颜色。
        """
        super().__init__(master)
        self.canvas = tk.Canvas(self, background=background, highlightthickness=0, height=10)
        self.canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window(0, 0, anchor="nw", window=self.frame)

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, style="InfoLine.Vertical.TScrollbar",
                                       command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y, expand=True)

        self.frame.bind("<Configure>", self._on_frame_configure)

        self.info_line_id = 0

    def set_style(self, bg:str):
        self.canvas.configure(bg=bg)

    # noinspection PyUnusedLocal
    def _on_frame_configure(self, event):
        """当内部框架尺寸改变时，更新 Canvas 的滚动区域"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.configure(width=self.frame.winfo_width())

    def create_new_line(self) -> int:
        """创建一个新的信息行并返回其 ID"""
        info_line = InformationLine(self.frame)
        info_line.pack()
        line_id = self.info_line_id
        self.info_line_id += 1
        return line_id


class ToolBar(ttk.Frame):
    """工具栏组件，包含一个添加行的按钮、一个标签和一个 Spinbox"""

    def __init__(self, master, text: str):
        """
        初始化工具栏组件。

        参数:
            master (Tk): 父容器。
            text (str): 工具栏内的标签文本。
        """
        super().__init__(master, padding=(10, 5, 20, 5))
        self.add_line_button = ttk.Button(self, text="+", command=self._on_button_clik, width=5)
        self.add_line_button.pack(side=tk.LEFT)

        self.label = ttk.Label(self, text=text)
        self.label.pack(side=tk.RIGHT, anchor="e")
        self.entry = ttk.Entry(self)
        self.entry.pack(side=tk.RIGHT, anchor="e")

        self.callback = None

    def set_button_command(self, callback):
        """设置添加行按钮的回调函数"""
        self.callback = callback

    def _on_button_clik(self):
        """点击添加行按钮时调用的内部方法"""
        if self.callback:
            self.callback()


class ParameterFormWidget(ttk.Frame):
    """参数表单组件，结合了标题行、信息行容器和工具栏"""

    def __init__(self, master):
        super().__init__(master)
        self.title_frame = ttk.Frame(self, style="TitleLine.TFrame")
        self.title_frame.pack(side=tk.TOP, fill=tk.X, anchor="w")

        self.title = TitleLine(self.title_frame, {
            "line": ("行号", 50),
            "time": ("时间", 100),
            "rec": ("录音", 50),
            "save": ("保存", 50),
            "note": ("备注", 200),
            "del": ("删除", 50)

        })
        self.title.pack(anchor="w")

        self.info_line_frame = InfoLineFrame(self)
        self.info_line_frame.pack(side=tk.TOP, fill=tk.Y, expand=True)

        self.tool_bar = ToolBar(self, "循环索引")
        self.tool_bar.set_button_command(self.create_new_line)
        self.tool_bar.pack(anchor="w", fill=tk.X, expand=False)

    def create_new_line(self):
        """创建一条新的信息行"""
        self.info_line_frame.create_new_line()

    def set_style(self, widget: str, style: dict):
        if widget == "info_line_form_canvas":
            self.info_line_frame.set_style(style["deeper_background"])


if __name__ == "__main__":
    root = tk.Tk()
    p = ParameterFormWidget(root)
    p.pack(fill=tk.Y, expand=True)
    root.mainloop()