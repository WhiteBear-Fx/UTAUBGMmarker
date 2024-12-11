from waveform_canvas_widget import WaveformCanvas
from waveform_canvas_controller import WaveformCanvasController
from load_audio import AudioLoader

from ruler_widget import RulerWidget

import tkinter as tk
from tkinter import ttk
import ctypes


class Oscilloscope(ttk.Frame):
    """
    Oscilloscope 类该控件的主容器，控制器、模型和视图在此处组合。
    该类还负责管理控件的布局。
    """

    def __init__(self, master):
        """
        初始化 Oscilloscope 实例。

        :param master: 父窗口或框架
        """
        super().__init__(master)
        self.audio_loader = AudioLoader()  # 初始化音频加载器
        self.waveform_canvas_controller = WaveformCanvasController(self.audio_loader)  # 初始化控制器并将其音频加载器传入作为模型
        self.waveform_canvas = WaveformCanvas(self, self.waveform_canvas_controller)  # 初始化波形画布
        self.waveform_canvas_controller.view = self.waveform_canvas  # 将控制器视图指向波形画布
        self.columnconfigure(0, weight=1)  # 配置第一列权重
        self.rowconfigure(1, weight=1)  # 配置第一行权重
        self.waveform_canvas.grid(row=1, column=0, sticky="news")  # 将波形画布放置在网格中

        self.ruler_widget = RulerWidget(self)  # 初始化标尺控件
        self.ruler_widget.grid(row=0, column=0, sticky="news")  # 将标尺控件放置在网格中

    def open_file(self, file_path):
        """
        打开指定路径的音频文件。
        本方法只是代理，实际的文件打开操作由控制器处理。

        :param file_path: 音频文件的路径
        """
        self.waveform_canvas_controller.open_file(file_path)  # 调用控制器的 open_file 方法打开文件
        self.ruler_widget.draw_ruler(self.audio_loader.get_duration())  # 调用ruler_widget的draw_ruler方法绘制标尺，传入音频的总时长


# 使用示例
if __name__ == "__main__":
    from tkinter import filedialog

    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 设置进程DPI感知

    root = tk.Tk()
    oscilloscope = Oscilloscope(root)  # 创建Oscilloscope实例
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    oscilloscope.grid(row=0, column=0, sticky="news")

    def open_filedialog():
        """
        打开文件选择对话框，让用户选择一个WAV格式的音频文件。
        """
        file_path = filedialog.askopenfilename(
            title="选择 WAV 文件",
            filetypes=[("WAV files", "*.wav"), ("所有文件", "*.*")]
        )
        if file_path is not None and file_path != "":
            oscilloscope.open_file(file_path)

    button = ttk.Button(root, text="点击打开文件", command=open_filedialog)  # 创建按钮
    button.grid(row=1, column=0)
    tk.mainloop()  # 运行主循环
