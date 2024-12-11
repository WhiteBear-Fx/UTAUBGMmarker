from waveform_canvas import WaveformCanvas
from ruler import Ruler
import audio_model

import tkinter as tk
from tkinter import ttk
import ctypes


class Oscilloscope(ttk.Frame):
    """
    Oscilloscope 的主要类，该控件的子容器在此处被放置，并封装了方法。
    使用该控件应实例化该类。
    """

    def __init__(self, master):
        """
        初始化 Oscilloscope 实例。

        :param master: 父窗口或框架
        """
        super().__init__(master)
        self.audio_loader = audio_model.AudioLoader()  # 初始化音频加载器

        self.waveform_canvas = WaveformCanvas(self, self.audio_loader)  # 初始化波形画布控件
        self.columnconfigure(0, weight=1)  # 配置第一列权重
        self.rowconfigure(1, weight=1)  # 配置第二行权重
        self.waveform_canvas.grid(row=1, column=0, sticky="news")  # 将波形画布放置在网格中

        self.ruler_widget = Ruler(self, self.audio_loader)  # 初始化标尺控件
        self.ruler_widget.grid(row=0, column=0, sticky="news")  # 将标尺控件放置在网格中

    def open_file(self, file_path):
        """
        打开指定路径的音频文件。
        :param file_path: 音频文件的路径
        """
        max_width = self.winfo_screenwidth()  # 获取屏幕最大宽度
        self.audio_loader.load_audio(file_path, max_width)  # 加载音频文件，由于模型公用，后续其他控件不用反复读取音频
        self.waveform_canvas.draw_waveform()  # 调用波形展示器的 open_file 方法打开文件
        self.ruler_widget.draw_ruler()  # 调用ruler_widget的draw_ruler方法绘制标尺


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
