from .ruler_controller import RulerController
from .ruler_widget import RulerWidget
from tkinter import ttk


class Ruler(ttk.Frame):
    def __init__(self, master, model):
        super().__init__(master)
        self.audio_loader = model  # 初始化音频加载器
        self.ruler_controller = RulerController(self.audio_loader)  # 初始化控制器并传入模型
        self.ruler_widget = RulerWidget(self, self.ruler_controller)  # 初始化尺子控件并传入控制器
        self.ruler_controller.view = self.ruler_widget  # 将控件赋值给控制器
        self.ruler_widget.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)   # 允许列扩展
        self.grid_columnconfigure(0, weight=1)   # 允许行扩展

    def draw_ruler(self):
        self.ruler_controller.draw_ruler()
