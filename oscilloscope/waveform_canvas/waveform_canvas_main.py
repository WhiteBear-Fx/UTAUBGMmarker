from .waveform_canvas_widget import WaveformCanvasWidget
from .waveform_canvas_controller import WaveformCanvasController
from tkinter import ttk


class WaveformCanvas(ttk.Frame):
    """
    波形展示器的主类，可以实例化该类以实现波形展示器的功能。
    """
    def __init__(self, master, model, background, foreground):
        super().__init__(master)
        self.audio_loader = model  # 初始化音频加载器
        self.waveform_canvas_controller = WaveformCanvasController(self.audio_loader)  # 初始化控制器并将其音频加载器传入作为模型
        self.waveform_canvas = WaveformCanvasWidget(self, self.waveform_canvas_controller, foreground=foreground,
                                                    background=background)  # 初始化波形画布
        self.waveform_canvas_controller.view = self.waveform_canvas  # 将控制器视图指向波形画布
        self.columnconfigure(0, weight=1)  # 配置第一列权重
        self.rowconfigure(0, weight=1)  # 配置第一行权重
        self.waveform_canvas.grid(row=0, column=0, sticky="news")  # 将波形画布放置在网格中

    def draw_waveform(self):
        """
        从模型获取波形并绘制
        """
        self.waveform_canvas_controller.draw_waveform()  # 调用控制器的 绘制方法绘制波形

    def set_style(self, style: tuple):
        self.waveform_canvas.set_style(*style)
