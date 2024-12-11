from widget import WaveformCanvas
from load_audio import AudioLoader

import tkinter as tk
from tkinter import ttk
import ctypes
import numpy as np


class OscilloscopeController:
    def __init__(self, model=None):
        self.audio_loader = model  # 初始化音频加载器
        self.audio_data = None  # 存储音频数据
        self.view = None  # 创建视图属性

    def open_file(self, file_path):
        """
        加载并分析指定路径的音频文件。

        :param file_path: 音频文件的路径
        """
        try:
            max_width = self.view.get_max_width()  # 获取屏幕最大宽度
            self.audio_loader.load_audio(file_path, max_width)  # 加载音频文件
            self.analyze_audio()  # 分析音频数据
        except Exception as e:
            print(f"Error loading file: {e}")  # 打印错误信息

    def analyze_audio(self):
        """
        分析音频数据，并在示波器画布上显示波形。
        """
        # 获取画布的宽度和高度信息，用于适配音频数据的显示
        canvas_width, canvas_height = self.view.get_canvas_info()

        # 从音频加载器中获取与画布宽度相匹配的音频样本
        self.audio_data = self.audio_loader.get_audio_data(canvas_width)

        if self.audio_data is not None and len(self.audio_data) == canvas_width:
            # 计算波形的中心线位置
            center_line = canvas_height // 2

            # 将音频数据映射到画布的高度范围内，使用 NumPy 向量化运算提高效率
            # 假设 audio_samples 的范围是 [-1, 1]，我们需要将其缩放到画布高度的一半
            scale_factor = (canvas_height / 2)
            waveform_y = (self.audio_data * scale_factor).astype(int) + center_line

            # 创建两个列表来分别存储波形的上下部分 Y 值
            waveform_top = np.clip(waveform_y, center_line, canvas_height - 1)  # 限制在画布下半部
            waveform_bottom = np.clip(waveform_y, 0, center_line)  # 限制在画布上半部

            # 使用处理好的波形数据更新示波器显示
            self.view.draw_waveform(waveform_top, waveform_bottom)

    def on_resize_over(self):
        """
        当窗口大小发生变化时，重新分析音频数据并更新示波器显示。
        """
        if self.audio_data is not None:  # 如果音频数据存在
            self.analyze_audio()  # 重新分析音频数据并更新示波器显示

    def on_resize(self):
        if self.audio_data is not None:  # 如果音频数据存在
            self.view.draw_on_resize_info()  # 绘制调整信息


class Oscilloscope(ttk.Frame):
    """
    Oscilloscope 类该控件的主容器，控制器模型和视图在此处组合。
    同时管理控件的布局。
    """

    def __init__(self, master):
        """
        初始化 Oscilloscope 实例。

        :param master: 父窗口或框架
        """
        super().__init__(master)
        self.oscilloscope_audio_loader = AudioLoader()  # 初始化音频加载器
        self.oscilloscope_controller = OscilloscopeController(self.oscilloscope_audio_loader)  # 初始化控制器并将其音频加载器传入作为模型
        self.oscilloscope = WaveformCanvas(self, self.oscilloscope_controller)  # 初始化波形画布
        self.oscilloscope_controller.view = self.oscilloscope  # 将控制器视图指向波形画布
        self.columnconfigure(0, weight=1)  # 配置第一列权重
        self.rowconfigure(0, weight=1)  # 配置第一行权重
        self.oscilloscope.grid(row=0, column=0, sticky="news")  # 将波形画布放置在网格中

    def open_file(self, file_path):
        """
        打开指定路径的音频文件。
        本方法只是代理，实际的文件打开操作由控制器处理。

        :param file_path: 音频文件的路径
        """
        self.oscilloscope_controller.open_file(file_path)  # 调用控制器的 open_file 方法打开文件


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
        oscilloscope.open_file(file_path)

    button = ttk.Button(root, text="点击打开文件", command=open_filedialog)  # 创建按钮
    button.grid(row=1, column=0)
    tk.mainloop()  # 运行主循环
