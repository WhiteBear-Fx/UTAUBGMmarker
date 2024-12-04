from widget import WaveformCanvas
from load_audio import AudioLoader

import tkinter as tk
from tkinter import ttk
import ctypes


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
        分析音频数据并在波形画布上显示。
        """
        width, height, y_center = self.oscilloscope.get_canvas_info()  # 获取画布信息
        self.audio_data = self.audio_loader.get_audio_data(width)  # 获取音频数据
        if self.audio_data is not None:
            print(self.audio_data)  # 打印音频数据


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
