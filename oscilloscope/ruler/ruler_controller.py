class RulerController:
    def __init__(self, model, scale_factor="auto", scale_width=2):
        self.module = model
        self.view = None  # 创建视图属性
        self.scale_factor = scale_factor  # 保存刻度因子, 默认为自动调整
        self.scale_width = scale_width  # 刻度线的宽度
        self.time = None  # 音频总时长

        self.one_scale = None  # 每秒对应的像素数
        self.auto_scale_factor = None  # 自动计算的刻度因子

    def draw_ruler(self):
        """
        根据当前窗口大小和刻度因子绘制标尺。
        如果刻度因子设置为 "auto"，则调用 draw_ruler_auto 自动调整刻度。
        """
        self.time = self.module.get_duration()  # 更新音频总时长
        if self.time is not None:
            self.view.delete("ruler")  # 清除所有绘图元素
            self.view.update_idletasks()  # 更新待处理的任务
            if self.scale_factor == "auto":
                self.draw_ruler_auto()
            elif self.scale_factor in ["XS", "S", "M", "L", "XL", "XXL"]:
                self.draw_ruler_actual(self.scale_factor)
            else:
                raise ValueError("Invalid scale_factor")

    def draw_ruler_auto(self):
        """
        根据窗口大小自动调整刻度因子并绘制标尺。

        计算每秒对应的像素数，并根据这个值选择合适的刻度因子。
        """
        self.one_scale = self.view.winfo_width() / self.time  # 计算每秒的像素数
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

        # 确定时间标签的小数位数
        decimal_places = 0
        temp_l_interval = l_interval
        while temp_l_interval < 1:
            temp_l_interval *= 10
            decimal_places += 1

        l_interval_x_list = []
        l_interval_text_list = []
        # 绘制大刻度
        for i in range(0, int(self.time * (1 / l_interval)) + 1):
            x = i * l_interval * self.one_scale
            l_interval_x_list.append(x)

            l_interval_text = f"{i * l_interval:.{decimal_places}f}s"
            l_interval_text_list.append(l_interval_text)

        self.view.draw_ruler_l(l_interval_x_list, l_interval_text_list, self.scale_width)

        # 绘制小刻度
        if s_interval is not None:
            s_interval_x_list = []
            for i in range(0, int(self.time * (1 / s_interval)) + 1):
                x = i * s_interval * self.one_scale
                s_interval_x_list.append(x)

            self.view.draw_ruler_s(s_interval_x_list, self.scale_width)

    def on_resize(self):
        self.draw_ruler()
