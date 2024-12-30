import tkinter as tk


class RulerWidget(tk.Canvas):
    """
    RulerWidget 类用于创建一个标尺控件，显示音频波形的时间轴。
    """

    def __init__(self, master, controller, background="000", foreground="#4b704c"):
        """
        初始化 RulerWidget 实例。

        :param master: 父窗口或框架
        """
        super().__init__(master, bg=background, bd=0, highlightthickness=0, height=45)
        self.controller = controller
        # 绑定 <Configure> 事件到 on_resize 方法，以便在窗口大小改变时重新绘制标尺
        self.bind("<Configure>", self.on_resize)
        self.last_size = None  # 上一次窗口大小
        self.foreground = foreground

    def draw_ruler_l(self, l_interval_x_list, l_interval_text_list, scale_width):
        # 绘制大刻度
        for i in range(len(l_interval_x_list)):
            # 长刻度线
            self.create_line(l_interval_x_list[i], 0, l_interval_x_list[i], 20, fill=self.foreground, width=scale_width + 2)
            # 刻度数值
            self.create_text(l_interval_x_list[i], 30, text=f"{l_interval_text_list[i]}",
                             fill=self.foreground, font=("Helvetica", 10))

    def draw_ruler_s(self, s_interval_x_list, scale_width):
        # 绘制小刻度
        for i in range(len(s_interval_x_list)):
            self.create_line(s_interval_x_list[i], 0, s_interval_x_list[i], 10, fill=self.foreground, width=scale_width)

    def on_resize(self, event):
        """
        在窗口大小改变时调用此方法以重新绘制标尺。

        :param event: 包含窗口大小信息的事件对象
        """
        if (event.width, event.height) != self.last_size:
            self.last_size = (event.width, event.height)
            self.controller.on_resize()

    def set_style(self, background, foreground):
        self.foreground = foreground
        self.config(bg=background)
        for i in self.find_all():
            self.itemconfig(i, fill=self.foreground)
