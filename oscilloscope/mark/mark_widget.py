import tkinter as tk


class MarkWidget(tk.Canvas):
    """
        MarkWidget 是一个自定义的 Tkinter 小部件，设计用于在父容器内作为滑动条或标记来测量位置。
        它可以在用户拖动时跟随鼠标移动，并显示相对于父容器宽度的比例位置。
    """

    def __init__(self, master, color: str, width: int):
        # 调用 Canvas 的构造函数进行初始化，设置背景色、边框和高亮厚度为0，以移除默认的边框
        super().__init__(master, bg=color, bd=0, highlightthickness=0)

        # 绑定事件处理方法到相应的鼠标和窗口调整事件上
        self.bind("<ButtonRelease-1>", self.button_release)  # 鼠标左键释放事件
        self.bind("<B1-Motion>", self.button_motion)  # 按住鼠标左键并移动事件
        self.master.bind("<Configure>", self.on_master_configure)  # 父容器大小改变事件

        # 初始化变量，用来存储父容器最后的尺寸信息
        self.master_last_size = None

        # 更新所有空闲任务（如布局任务），以确保可以正确获取父容器的尺寸信息
        self.master.update_idletasks()

        # 初始化比例位置变量，包括当前、开始、结束以及实际比例位置
        self.mark_position_now = 0
        self.mark_position_star = 0 - width / 2 / self.master.winfo_width()  # 开始比例位置，减去半个宽度以居中
        self.mark_position_end = 1 - width / 2 / self.master.winfo_width()  # 结束比例位置
        self.mark_position_proportion = self.mark_position_star  # 当前比例位置
        self.mark_position = 0  # 实际比例位置，用于输出

        # 设置 MarkWidget 的宽度，并将其放置在主窗口中，初始时位于最左边
        self.config(width=width)
        self.place(relx=self.mark_position_proportion, relheight=1)  # 使用相对位置放置

    def get_position_ratio(self, event):
        # 确保所有布局更新已完成，以便正确获取尺寸信息
        self.master.update_idletasks()

        # 计算当前位置：根据鼠标事件的 x 坐标累积变化量，减去小部件的一半宽度以保持中心对齐
        self.mark_position_now = self.mark_position_now + event.x - (self.winfo_width() / 2)

        # 计算新的比例位置，限制在 start 和 end 之间
        self.mark_position_proportion = max(self.mark_position_star, min(self.mark_position_end, self.mark_position_now
                                                                         / self.master.winfo_width()))
        self.mark_position = min(1.0, max(0.0, self.mark_position_proportion + self.winfo_width() / 2
                                          / self.master.winfo_width()))

        # 使用计算出的比例位置重新配置小部件的位置
        self.place_configure(relx=self.mark_position_proportion)

    def set_position(self, ratio: float):
        # 确保所有布局更新已完成，以便正确获取尺寸信息
        self.master.update_idletasks()

        # 根据传入的比例值计算新的位置
        self.mark_position_now = self.master.winfo_width() * ratio - self.winfo_width() / 2

        # 计算新的比例位置，限制在 start 和 end 之间
        self.mark_position_proportion = max(self.mark_position_star, min(self.mark_position_end, self.mark_position_now
                                                                         / self.master.winfo_width()))
        self.mark_position = min(1.0, max(0.0, self.mark_position_proportion + self.winfo_width() / 2
                                          / self.master.winfo_width()))

        # 使用计算出的比例位置重新配置小部件的位置
        self.place_configure(relx=self.mark_position_proportion)

    def on_master_configure(self, event):
        # 如果窗口大小发生变化，则更新相关变量并重置位置
        if (event.width, event.height) != self.master_last_size:
            self.master_last_size = (event.width, event.height)
            self.mark_position_star = 0 - self.winfo_width() / 2 / self.master.winfo_width()
            self.mark_position_end = 1 - self.winfo_width() / 2 / self.master.winfo_width()
            self.set_position(self.mark_position)

    def button_release(self, event):
        # 当鼠标左键释放时，调用获取位置比例的方法
        self.get_position_ratio(event)
        print(self.mark_position)

    def button_motion(self, event):
        # 当按住鼠标左键并移动时，调用获取位置比例的方法
        self.get_position_ratio(event)
        print(self.mark_position)


if __name__ == "__main__":
    root = tk.Tk()  # 创建主窗口实例

    # 创建一个灰色背景的 Canvas 小部件作为背景，并添加到网格布局的第一行第一列
    c = tk.Canvas(root, width=500, bg="#555")
    c.grid(row=0, column=0, sticky="news")  # 使用 'news' 确保 Canvas 可以填充整个单元格

    # 实例化自定义的小部件 `MarkWidget` 并传入必要的参数，宽度设为20像素
    w = MarkWidget(root, "#200", 20)

    # 设置网格布局权重，使得当窗口大小调整时，Canvas 可以随之扩展
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # 进入 Tkinter 的主事件循环，等待用户交互
    root.mainloop()