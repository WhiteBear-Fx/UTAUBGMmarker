import tkinter as tk


class WaveformCanvasWidget(tk.Canvas):
    """
    WaveformCanvas 类继承自 tk.Canvas，用于绘制音频波形。
    """

    def __init__(self, master, controller):
        """
        初始化 WaveformCanvas 实例。

        :param master: 父窗口或框架
        """
        super().__init__(master, background="#4b704c", bd=0, highlightthickness=0)  # 设置背景颜色
        self.resize_timer = None  # 存储定时器 ID
        self.controller = controller  # 存储控制器实例
        self.last_size = (self.winfo_width(), self.winfo_height())  # 存储上一次的画布大小
        self.bind("<Configure>", self.on_resize)  # 绑定画布大小调整事件

    def get_canvas_info(self):
        """
        获取画布的信息，包括宽度、高度和垂直中心位置。

        :return: 宽度、高度和垂直中心位置的元组
        """
        self.update_idletasks()  # 更新待处理的任务
        return self.winfo_width(), self.winfo_height()

    def show_waveform(self, waveform_y1, waveform_y2):
        """
        绘制音频波形。

        :param waveform_y1: 波形的上半部分 Y 坐标列表
        :param waveform_y2: 波形的下半部分 Y 坐标列表
        """
        self.delete("waveform", "resize_info")  # 清除画布上的波形内容
        if len(waveform_y1) == len(waveform_y2):
            for i in range(len(waveform_y1)):
                self.create_rectangle(i, waveform_y1[i], i, waveform_y2[i], fill="#000", tags="waveform")
        else:
            print("y1, y2长度不一致")  # 暂时这样写，实际上需要报错

    def draw_on_resize_info(self):
        """
        绘制画布大小调整信息。
        """
        x = self.winfo_width() // 2
        y = self.winfo_height() // 2
        self.delete("resize_info")  # 清除画布上的调整信息
        self.create_text(x, y, text="绘制计划已变更，等待用户结束调整", fill="#000", tags="resize_info", font=("Helvetica", 15))

    def on_resize(self, event):
        """
        处理画布大小调整事件。
        """
        current_size = (event.width, event.height)

        # 如果是第一次调用或者大小确实发生了变化
        if current_size != self.last_size:
            self.last_size = current_size  # 更新最后的尺寸
            self.delete("waveform")  # 清除之前的波形
            self.controller.on_resize()
            # 取消之前的定时器（如果有）
            if self.resize_timer is not None:
                self.after_cancel(self.resize_timer)
                self.resize_timer = None

            # 设置一个新的定时器，在用户停止调整大小后延迟调用 analyze_audio
            self.resize_timer = self.after(200, self._on_resize_complete)

    def _on_resize_complete(self):
        """
        当用户停止调整大小后调用此方法以重新绘制波形。
        """
        self.controller.on_resize_over()
        self.resize_timer = None  # 清除定时器 ID