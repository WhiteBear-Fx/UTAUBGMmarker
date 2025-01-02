from tkinter import ttk
from json_loader import JsonLoader


class ThemeLoader:
    """
    从JSON文件加载主题设置，并应用到基于Tkinter的GUI应用程序中。
    使用ttk.Style来配置不同组件（如框架、标签、输入框、按钮等）的样式。
    """

    def __init__(self, style: ttk.Style):
        """
        初始化ThemeLoader对象。

        :param style: Tkinter的ttk.Style对象，用于管理组件的外观。
        """
        self.style = style
        # 使用clam主题以确保所有平台上的样式一致
        self.style.theme_use("clam")
        self.json_loader = None  # JSON加载器，用于解析主题文件
        self.canvas_bg = {}  # 存储画布背景颜色，如果需要的话

    def set_theme(self, file_path: str):
        """
        根据提供的文件路径加载并应用主题。

        :param file_path: 指向包含主题定义的JSON文件的路径。
        """
        self.json_loader = JsonLoader(file_path)
        # 先设置参数表单的主题，因为这可能是最复杂的部分
        self._set_parameter_form_theme()
        # 加载通用主题设置
        theme = self.json_loader.get_json("general")

        frame_bg = theme["frame"]["background"]
        self.style.configure("TFrame", background=frame_bg)

        label_bg = theme["label"]["background"]
        label_fg = theme["label"]["foreground"]
        self.style.configure("TLabel", background=label_bg, foreground=label_fg)

        entry_bg = theme["entry"]["background"]
        entry_fg = theme["entry"]["foreground"]
        entry_text = theme["entry"]["text"]
        entry_hl = theme["entry"]["highlight"]
        self.style.configure("TEntry",
                             background=entry_bg,
                             fieldbackground=entry_bg,
                             foreground=entry_text,
                             darkcolor=entry_fg,
                             lightcolor=entry_fg,
                             bordercolor=entry_fg)
        self.style.map("TEntry",
                       lightcolor=[("focus", entry_hl)],
                       darkcolor=[("focus", entry_hl)],
                       bordercolor=[("focus", entry_hl)])

        button_bg = theme["button"]["background"]
        button_fg = theme["button"]["foreground"]
        button_text = theme["button"]["text"]
        self.style.configure("TButton",
                             background=button_bg,
                             lightcolor=button_fg,
                             darkcolor=button_fg,
                             bordercolor=button_fg,
                             foreground=button_text)
        self.style.map("TButton", background=[("active", button_fg)])

    def _set_parameter_form_theme(self):
        """
        设置参数表单内的组件主题，包括标题行和信息行。
        """
        theme = self.json_loader.get_json("parameter_form")

        # 设置标题行样式
        bg = theme["title_line"]["background"]
        fg = theme["title_line"]["foreground"]
        self.style.configure("TitleLine.TLabel", background=bg, foreground=fg)
        self.style.configure("TitleLine.TFrame", background=bg)

        # 设置信息行样式
        bg = theme["info_line"]["background"]
        fg = theme["info_line"]["foreground"]
        text = theme["info_line"]["text"]
        hl = theme["info_line"]["highlight"]

        self.style.configure("InfoLine.TLabel", background=bg, foreground=text)
        self.style.configure("InfoLine.TFrame", background=bg)
        self.style.configure("InfoLine.TEntry",
                             background=bg,
                             fieldbackground=bg,
                             relief="flat",
                             lightcolor=fg,
                             darkcolor=fg,
                             bordercolor=fg,
                             foreground=text)
        self.style.map("InfoLine.TEntry",
                       lightcolor=[("focus", hl)],
                       darkcolor=[("focus", hl)],
                       bordercolor=[("focus", hl)])

        self.style.configure("InfoLine.TButton",
                             background=bg,
                             fieldbackground=bg,
                             relief="flat",
                             lightcolor=fg,
                             darkcolor=fg,
                             bordercolor=fg,
                             foreground=text)
        self.style.map("InfoLine.TButton",
                       background=[("active", fg)])

        self.style.configure("InfoLine.Vertical.TScrollbar",
                             background=fg,
                             lightcolor=fg,
                             darkcolor=fg,
                             bordercolor=fg,
                             gripcount=0)
        self.style.map("InfoLine.Vertical.TScrollbar",
                       background=[("active", hl)],
                       lightcolor=[("active", hl)],
                       darkcolor=[("active", hl)],
                       bordercolor=[("active", hl)])

    def get_info_line_form_canvas_style(self):
        """
        获取参数表单信息行的主题样式，主要用于手动设置无法通过ttk.Style配置的组件（例如画布）。

        :return: 包含信息行样式的字典。
        """
        theme = self.json_loader.get_json("parameter_form")
        return theme["info_line"]


if __name__ == "__main__":
    from parameter_form import ParameterFormWidget
    import tkinter as tk

    root = tk.Tk()

    app_style = ttk.Style()
    t = ThemeLoader(app_style)
    # 加载并应用指定路径下的主题文件
    t.set_theme(r"D:\Project\Pycharm\BGMmarker\resource\theme\dark.json")

    p = ParameterFormWidget(root)
    p.pack(fill=tk.Y, expand=True)

    # 因为画布不能使用ttk.Style对象进行配置，所以这里获取信息行的主题样式，并手动设置给画布
    p.set_style("info_line_form_canvas", t.get_info_line_form_canvas_style())

    root.mainloop()
