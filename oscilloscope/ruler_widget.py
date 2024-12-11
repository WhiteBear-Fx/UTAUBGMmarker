import tkinter as tk


class RulerWidget(tk.Canvas):
    """
    RulerWidget 类用于创建一个标尺控件，显示音频波形的时间轴。
    """

    def __init__(self, master, time, scale_factor="auto", scale_width=1):
        """
        初始化 RulerWidget 实例。

        :param master: 父窗口或框架
        :param time: 音频的总时间（秒）
        :param scale_factor: 标尺的刻度因子，即如何展示刻度（默认为 "auto"）
        :param scale_width: 刻度线的宽度（默认为 1）
        """
        super().__init__(master, bg="#222", bd=0, highlightthickness=0)
        self.one_scale = None  # 每秒对应的像素数
        self.time = time  # 音频总时长（秒）
        self.scale_factor = scale_factor  # 刻度因子，默认为自动调整
        self.scale_width = scale_width  # 刻度线的宽度
        # 绑定 <Configure> 事件到 on_resize 方法，以便在窗口大小改变时重新绘制标尺
        self.bind("<Configure>", self.on_resize)
        self.last_size = None  # 上一次窗口大小

    def draw_ruler(self):
        """
        根据当前窗口大小和刻度因子绘制标尺。
        如果刻度因子设置为 "auto"，则调用 draw_ruler_auto 自动调整刻度。
        """
        self.delete("all")  # 清除所有绘图元素
        self.update_idletasks()  # 更新待处理的任务
        if self.scale_factor == "auto":
            self.draw_ruler_auto()

    def draw_ruler_auto(self):
        """
        根据窗口大小自动调整刻度因子并绘制标尺。

        计算每秒对应的像素数，并根据这个值选择合适的刻度因子。
        """
        self.one_scale = self.winfo_width() / self.time  # 计算每秒的像素数
        print(f"每秒的像素数: {self.one_scale}")
        # 定义不同刻度因子对应的阈值
        thresholds = {
            "XS": 10000,
            "S": 1000,
            "M": 100,
            "L": 10,
            "XL": 1,
            "XXL": 0.1
        }

        for factor in ["XS", "S", "M", "L", "XL", "XXL"]:
            if self.one_scale >= thresholds[factor]:
                self.auto_scale_factor = factor
                print(f"自动选择的刻度因子: {self.auto_scale_factor}")
                break
        else:
            self.auto_scale_factor = "XXL"

        self.draw_ruler_actual(self.auto_scale_factor)

    def draw_ruler_actual(self, scale_factor):
        """
        根据给定的刻度因子绘制具体的标尺。

        :param scale_factor: 选定的刻度因子
        """
        # 定义不同刻度因子对应的大刻度和小刻度间隔
        scale_dict = {
            "XS": {
                "l_interval": 0.01,  # 大刻度间隔（长线） 百分之一秒
                "s_interval": 0.001  # 小刻度间隔（短线） 千分之一秒
            },
            "S": {
                "l_interval": 0.1,  # 大刻度间隔（长线） 十分之一秒
                "s_interval": 0.01  # 小刻度间隔（短线） 百分之一秒
            },
            "M": {
                "l_interval": 1,
                "s_interval": 0.1
            },
            "L": {
                "l_interval": 10,
                "s_interval": 1  # 当不需要绘制小刻度时，可以使用 None 或其他标识符
            },
            "XL": {
                "l_interval": 30,
                "s_interval": 10
            },
            "XXL": {
                "l_interval": 60,
                "s_interval": 30  # 当不需要绘制小刻度时，可以使用 None 或其他标识符
            }
        }

        l_interval = scale_dict[scale_factor]["l_interval"]  # 获取大刻度间隔
        s_interval = scale_dict[scale_factor]["s_interval"]  # 获取小刻度间隔

        # 绘制大刻度
        for i in range(0, int(self.time * (1 / l_interval)) + 1):
            x = i * l_interval * self.one_scale
            self.create_line(x, 0, x, 20, fill="#fff", width=self.scale_width)  # 长刻度线

        # 绘制小刻度
        if s_interval is not None:
            for i in range(0, int(self.time * (1 / s_interval)) + 1):
                x = i * s_interval * self.one_scale
                self.create_line(x, 0, x, 10, fill="#f00", width=self.scale_width)  # 短刻度线

    def on_resize(self, event):
        """
        在窗口大小改变时调用此方法以重新绘制标尺。

        :param event: 包含窗口大小信息的事件对象
        """
        if (event.width, event.height) != self.last_size:
            self.last_size = (event.width, event.height)
            self.draw_ruler()


if __name__ == "__main__":
    root = tk.Tk()
    ruler = RulerWidget(root, 400)
    ruler.grid(row=0, column=0, sticky="news")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()



