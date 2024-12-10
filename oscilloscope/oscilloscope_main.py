from widget import WaveformCanvas
from load_audio import AudioLoader

import tkinter as tk
from tkinter import ttk
import ctypes
import numpy as np


class Oscilloscope(ttk.Frame):
    """
    Oscilloscope 类用于创建一个图形用户界面 (GUI)，允许用户加载和显示音频文件的波形。
    """

    def __init__(self, master):
        """
        初始化 Oscilloscope 实例。

        :param master: 父窗口或框架
        """
        super().__init__(master)
        self.oscilloscope = WaveformCanvas(self)  # 初始化波形画布
        self.audio_loader = AudioLoader()  # 初始化音频加载器
        self.audio_data = None  # 存储音频数据

    def open_file(self, file_path):
        """
        加载并分析指定路径的音频文件。

        :param file_path: 音频文件的路径
        """
        try:
            max_width = self.master.winfo_screenwidth()  # 获取屏幕最大宽度
            self.audio_loader.load_audio(file_path, max_width)  # 加载音频文件
            self.analyze_audio()  # 分析音频数据
        except Exception as e:
            print(f"Error loading file: {e}")  # 打印错误信息

    def analyze_audio(self):
        """
        分析音频数据，并在示波器画布上显示波形。

        此方法从 `audio_loader` 获取音频数据，然后根据画布尺寸调整这些数据，
        最后将处理后的波形数据传递给 `oscilloscope` 以进行绘制。
        """
        # 获取画布的宽度和高度信息，用于适配音频数据的显示
        canvas_width, canvas_height = self.oscilloscope.get_canvas_info()

        # 从音频加载器中获取与画布宽度相匹配的音频样本
        audio_samples = self.audio_loader.get_audio_data(canvas_width)

        if audio_samples is not None and len(audio_samples) == canvas_width:
            # 计算波形的中心线位置
            center_line = canvas_height // 2

            # 将音频数据映射到画布的高度范围内，使用 NumPy 向量化运算提高效率
            waveform_y = (center_line * audio_samples + center_line).astype(int)

            # 创建两个列表来分别存储波形的上下部分 Y 值
            waveform_top = []
            waveform_bottom = []

            # 处理波形数据，确保其对称地围绕中心线显示
            for y in waveform_y:
                if y > center_line:
                    # 对于超过中心线的点，计算对应的底部反射点
                    waveform_top.append(y)
                    waveform_bottom.append(center_line - (y - center_line))
                elif y < center_line:
                    # 对于低于中心线的点，计算对应顶部反射点
                    waveform_top.append(center_line - (center_line - y))
                    waveform_bottom.append(y)
                else:
                    # 当值等于中心线时，直接添加到两个列表中
                    waveform_top.append(y)
                    waveform_bottom.append(y)

            # 使用处理好的波形数据更新示波器显示
            self.oscilloscope.draw_waveform(waveform_top, waveform_bottom)

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
