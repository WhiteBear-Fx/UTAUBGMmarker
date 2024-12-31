import tkinter as tk


class MarkWidget:
    """
    MarkWidget 是一个自定义的 Tkinter 小部件，设计用于在父容器内作为滑动条或标记来测量位置。
    它可以在用户拖动时跟随鼠标移动，并显示相对于父容器宽度的比例位置。
    """

    def __init__(self, canvas, color: str, width: int, position):
        """
        初始化 MarkWidget 实例。

        参数:
            canvas (tk.Canvas): 父画布，通常是 Tkinter 的 Canvas 小部件。
            color (str): 小部件的背景颜色，使用 Tkinter 支持的颜色字符串。
            width (int): 小部件的宽度，以像素为单位。
        """
        self.mark_position = position

        self.canvas = canvas
        self.width = width

        self.motion_callback = None
        self.release_callback = None

        self.canvas.update_idletasks()

        self.mark_id = self.canvas.create_rectangle(0, 0, width,  self.canvas.winfo_height(),
                                                    fill=color, outline='')

        self.canvas.tag_bind(self.mark_id, "<ButtonRelease-1>", self._button_release, add="+")
        self.canvas.tag_bind(self.mark_id, "<B1-Motion>", self._button_motion, add="+")
        self.canvas.bind("<Configure>", self._on_master_configure, add="+")

        self.master_last_size = None

        self.set_position(self.mark_position)

    def del_mark(self):
        self.canvas.delete(self.mark_id)

    def _clamp_position(self, position):
        """
        钳制给定的位置在画布的有效范围内。

        参数:
            position (float): 要钳制的小部件位置。

        返回:
            float: 钳制后的位置。
        """
        canvas_width = self.canvas.winfo_width()
        half_width = self.width / 2
        return max(- half_width, min(position, canvas_width - half_width))

    def _update_mark_position(self, x_position):
        """
        更新小部件的位置并重新定位它。

        参数:
            x_position (float): 小部件新的x轴位置。
        """
        clamped_x = self._clamp_position(x_position)

        self.mark_position = (clamped_x + self.width / 2) / self.canvas.winfo_width()
        self.canvas.coords(self.mark_id, clamped_x, 0,
                           clamped_x + self.width, self.canvas.winfo_height())

    def _get_position_ratio(self, event):
        """
        根据鼠标事件更新小部件的位置比例，并重新定位小部件。

        参数:
            event (tk.Event): 鼠标事件对象，包含鼠标当前位置信息。
        """
        self.canvas.update_idletasks()
        # Calculate the new position and update the widget's location
        self._update_mark_position(event.x)

    def set_position(self, ratio: float):
        """
        设置小部件的位置为指定的比例值。

        参数:
            ratio (float): 新的位置比例，范围是 [0.0, 1.0]。
        """
        self.canvas.update_idletasks()
        # Convert ratio to absolute position and clamp it before updating
        absolute_position = ratio * self.canvas.winfo_width() - self.width / 2
        self._update_mark_position(absolute_position)

    def _on_master_configure(self, event):
        """
        当父容器大小改变时更新小部件的位置和边界条件。

        参数:
            event (tk.Event): 配置事件对象，包含父容器的新尺寸信息。
        """
        if (event.width, event.height) != self.master_last_size:
            self.set_position(self.mark_position)
            self.master_last_size = (event.width, event.height)

    def _button_release(self, event):
        """
        处理鼠标左键释放事件，更新位置并触发回调函数。

        参数:
            event (tk.Event): 鼠标事件对象。
        """
        self._get_position_ratio(event)
        if self.release_callback and callable(self.release_callback[0]):
            callback, *args = self.release_callback
            callback(self.mark_position, *args)

    def _button_motion(self, event):
        """
        处理按住鼠标左键并移动事件，更新位置并触发回调函数。

        参数:
            event (tk.Event): 鼠标事件对象。
        """
        self._get_position_ratio(event)
        if self.motion_callback and callable(self.motion_callback[0]):
            callback, *args = self.motion_callback
            callback(self.mark_position, *args)

    def set_button_release(self, callback, *args):
        """
        设置当鼠标左键释放时调用的回调函数。

        参数:
            callback (Callable): 回调函数，接受一个参数，即当前的比例位置。
            *args: 其他传递给回调函数的参数。
        """
        if not callable(callback):
            raise TypeError("The provided callback is not callable.")
        self.release_callback = [callback, *args]

    def set_button_motion(self, callback, *args):
        """
        设置当按住鼠标左键并移动时调用的回调函数。

        参数:
            callback (Callable): 回调函数，接受一个参数，即当前的比例位置，浮点数，取值范围[0，1]。
            *args: 其他传递给回调函数的参数。
        """
        if not callable(callback):
            raise TypeError("The provided callback is not callable.")
        self.motion_callback = [callback, *args]


if __name__ == "__main__":
    import random
    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=50, bg="lightgray")
    canvas.pack(fill=tk.BOTH)

    # List to keep track of MarkWidget instances
    marks = []
    # Listbox to show the current positions of all marks
    listbox = tk.Listbox(root)
    listbox.pack(side=tk.RIGHT, fill=tk.Y)

    def on_move(index):
        return lambda position: update_listbox(index, position)

    def on_release(position):
        print(f"Released at position: {position}")

    def add_mark():
        # Create a new mark and add it to the list
        index = len(marks)
        color = "red" if index % 2 else "blue"  # Alternate colors for visibility
        new_mark = MarkWidget(canvas, color, 10, random.random())
        new_mark.set_button_motion(on_move(index))
        new_mark.set_button_release(on_release)
        marks.append(new_mark)
        update_listbox(index, new_mark.mark_position)

    def update_listbox(index, position):
        # Update or insert the position in the listbox
        pos_str = f"Mark {index}: {position:.2f}"
        if listbox.size() <= index:
            listbox.insert(tk.END, pos_str)
        else:
            listbox.delete(index)
            listbox.insert(index, pos_str)

    # Button to add a new mark dynamically
    add_button = tk.Button(root, text="Add Mark", command=add_mark)
    add_button.pack(side=tk.BOTTOM)

    # Start with one mark by default
    add_mark()

    root.mainloop()
