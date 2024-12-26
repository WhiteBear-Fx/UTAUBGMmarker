import tkinter as tk


class MarkWidget(tk.Canvas):
    """
        MarkWidget 是一个自定义的 Tkinter 小部件，设计用于在父容器内作为滑动条或标记来测量位置。
        它可以在用户拖动时跟随鼠标移动，并显示相对于父容器宽度的比例位置。
    """

    def __init__(self, master, color: str, width: int):
        """
        初始化 MarkWidget 实例。

        param:
            master (tk.Widget): 父容器，通常是 Tkinter 的窗口或其他小部件。
            color (str): 小部件的背景颜色，使用 Tkinter 支持的颜色字符串。
            width (int): 小部件的宽度，以像素为单位。
        """
        super().__init__(master, bg=color, bd=0, highlightthickness=0)

        self.motion_callback = None
        self.release_callback = None
        self.bind("<ButtonRelease-1>", self._button_release)
        self.bind("<B1-Motion>", self._button_motion)
        self.master.bind("<Configure>", self._on_master_configure)

        self.master_last_size = None

        self.master.update_idletasks()

        self.mark_position_now = 0
        self.mark_position_star = 0 - width / 2 / self.master.winfo_width()
        self.mark_position_end = 1 - width / 2 / self.master.winfo_width()
        self.mark_position_proportion = self.mark_position_star
        self.mark_position = 0

        self.config(width=width)
        self.place(relx=self.mark_position_proportion, relheight=1)

    def _get_position_ratio(self, event):
        """
        根据鼠标事件更新小部件的位置比例，并重新定位小部件。

        param:
            event (tk.Event): 鼠标事件对象，包含鼠标当前位置信息。
        """
        self.master.update_idletasks()

        self.mark_position_now += event.x - self.winfo_width() / 2
        self.mark_position_proportion = max(self.mark_position_star, min(self.mark_position_end, self.mark_position_now
                                                                         / self.master.winfo_width()))
        self.mark_position = min(1.0, max(0.0, self.mark_position_proportion + self.winfo_width() / 2
                                          / self.master.winfo_width()))

        self.place_configure(relx=self.mark_position_proportion)

    def set_position(self, ratio: float):
        """
        设置小部件的位置为指定的比例值。

        param:
            ratio (float): 新的位置比例，范围是 [0.0, 1.0]。
        """
        self.master.update_idletasks()

        self.mark_position_now = self.master.winfo_width() * ratio - self.winfo_width() / 2
        self.mark_position_proportion = max(self.mark_position_star, min(self.mark_position_end, self.mark_position_now
                                                                         / self.master.winfo_width()))
        self.mark_position = min(1.0, max(0.0, self.mark_position_proportion + self.winfo_width() / 2
                                          / self.master.winfo_width()))

        self.place_configure(relx=self.mark_position_proportion)

    def _on_master_configure(self, event):
        """
        当父容器大小改变时更新小部件的位置和边界条件。

        param:
            event (tk.Event): 配置事件对象，包含父容器的新尺寸信息。
        """
        if (event.width, event.height) != self.master_last_size:
            self.master_last_size = (event.width, event.height)
            self.mark_position_star = 0 - self.winfo_width() / 2 / self.master.winfo_width()
            self.mark_position_end = 1 - self.winfo_width() / 2 / self.master.winfo_width()
            self.set_position(self.mark_position)

    def _button_release(self, event):
        """
        处理鼠标左键释放事件，更新位置并触发回调函数。

        param:
            event (tk.Event): 鼠标事件对象。
        """
        self._get_position_ratio(event)
        callback, *args = self.release_callback
        if callable(callback):
            callback(self.mark_position, *args)

    def _button_motion(self, event):
        """
        处理按住鼠标左键并移动事件，更新位置并触发回调函数。

        param:
            event (tk.Event): 鼠标事件对象。
        """
        self._get_position_ratio(event)
        callback, *args = self.motion_callback
        if callable(callback):
            callback(self.mark_position, *args)

    def set_button_release(self, callback, *args):
        """
        设置当鼠标左键释放时调用的回调函数。

        :param
            callback (Callable): 回调函数，接受一个参数，即当前的比例位置。
            *args: 其他传递给回调函数的参数。
        """
        if not callable(callback):
            raise TypeError("The provided callback is not callable.")
        self.release_callback = [callback, *args]

    def set_button_motion(self, callback, *args):
        """
        设置当按住鼠标左键并移动时调用的回调函数。

        :param
            callback (Callable): 回调函数，接受一个参数，即当前的比例位置，浮点数，取值范围[0，1]。
            *args: 其他传递给回调函数的参数。
        """
        if not callable(callback):
            raise TypeError("The provided callback is not callable.")
        self.motion_callback = [callback, *args]


# 使用示例
if __name__ == "__main__":

    def on_motion(position):
        """当按住鼠标左键并移动时调用的回调函数"""
        print(f"Moving to position: {position:.2f}")


    def on_release(position):
        """当鼠标左键释放时调用的回调函数"""
        print(f"Released at position: {position:.2f}")

    # 创建主应用窗口
    root = tk.Tk()
    root.title("MarkWidget 示例")
    root.geometry("400x100")  # 设置窗口大小为 400x100 像素

    # 创建一个 MarkWidget 实例，颜色为蓝色，宽度为 10 像素
    mark_widget = MarkWidget(root, color="blue", width=10)

    # 设置鼠标事件的回调函数
    mark_widget.set_button_motion(on_motion)
    mark_widget.set_button_release(on_release)

    # 运行 Tkinter 的主事件循环
    root.mainloop()
