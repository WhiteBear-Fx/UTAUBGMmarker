import tkinter as tk


class WaveformCanvas(tk.Canvas):
    """
    WaveformCanvas 类继承自 tk.Canvas，用于绘制音频波形。
    """

    def __init__(self, master):
        """
        初始化 WaveformCanvas 实例。

        :param master: 父窗口或框架
        """
        super().__init__(master, background="#385434")  # 设置背景颜色
        self.grid(row=0, column=0, sticky="news")  # 布局设置

    def get_canvas_info(self):
        """
        获取画布的信息，包括宽度、高度和垂直中心位置。

        :return: 宽度、高度和垂直中心位置的元组
        """
        self.update_idletasks()  # 更新待处理的任务
        return self.winfo_width(), self.winfo_height()

    def draw_waveform(self, waveform_y1, waveform_y2):
        """
        绘制音频波形。

        :param waveform_y1: 波形的上半部分 Y 坐标列表
        :param waveform_y2: 波形的下半部分 Y 坐标列表
        """
        self.delete("waveform")  # 清除画布上的波形内容
        if len(waveform_y1) == len(waveform_y2):
            for i in range(len(waveform_y1)):
                self.create_rectangle(i, waveform_y1[i], i, waveform_y2[i], fill="#000", tags="waveform")
        else:
            print("y1, y2长度不一致")  # 暂时这样写，实际上需要报错

    def on_resize(self):
        """
        处理画布大小调整事件。目前该方法为空，需要实现具体的调整逻辑。
        """
        pass
