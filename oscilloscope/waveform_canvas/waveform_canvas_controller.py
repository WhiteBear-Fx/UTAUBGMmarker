import numpy as np


class WaveformCanvasController:
    """
    示波器的控制器类，用于沟通模型和视图。
    """
    def __init__(self, model=None):
        self.audio_loader = model  # 初始化音频加载器
        self.audio_data = None  # 存储音频数据
        self.view = None  # 创建视图属性

    def draw_waveform(self):
        """
        分析音频数据，并在示波器画布上显示波形。
        """
        # 获取画布的宽度和高度信息，用于适配音频数据的显示
        canvas_width, canvas_height = self.view.get_canvas_info()

        # 从音频加载器中获取与画布宽度相匹配的音频样本
        self.audio_data = self.audio_loader.get_audio_data(canvas_width)

        if self.audio_data is not None :
            # 计算波形的中心线位置
            center_line = canvas_height // 2

            # 将音频数据映射到画布的高度范围内，使用 NumPy 向量化运算提高效率
            # audio_samples 的范围是 [-1, 1]，我们需要将其翻转并缩放到画布高度的一半
            scale_factor = (canvas_height / 2)
            waveform_y = center_line - (self.audio_data * scale_factor)

            # 创建两个列表来分别存储波形的上下部分 Y 值
            waveform_top = np.clip(waveform_y, 0, center_line)  # 限制在画布上半部
            waveform_bottom = np.clip(waveform_y, center_line, canvas_height - 1)  # 限制在画布下半部

            # 使用处理好的波形数据更新示波器显示
            self.view.show_waveform(waveform_top, waveform_bottom)

    def on_resize_over(self):
        """
        当窗口大小发生变化时，重新分析音频数据并更新示波器显示。
        """
        if self.audio_data is not None:  # 如果音频数据存在
            self.draw_waveform()  # 重新分析音频数据并更新示波器显示

    def on_resize(self):
        if self.audio_data is not None:  # 如果音频数据存在
            self.view.draw_on_resize_info()  # 绘制调整信息
