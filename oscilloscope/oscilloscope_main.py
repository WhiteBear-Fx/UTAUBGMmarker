from .waveform_canvas import WaveformCanvas
from .ruler import Ruler
from .mark import Mark

import audio_model

import tkinter as tk
from tkinter import ttk


class Oscilloscope(ttk.Frame):
    """
    Oscilloscope的主要类，负责管理波形画布、标尺和标记管理器，
    并提供加载音频文件、创建和管理标记的方法。
    """

    def __init__(self, master, waveform_style: dict, ruler_style: dict):
        """
        初始化Oscilloscope实例，配置布局并初始化子组件。

        :param master: 父容器（如Tkinter窗口或框架），用于容纳本组件。
        :type master: tkinter.Tk 或 tkinter.Frame 或 其他 Tkinter 容器

        :param waveform_style: 一个包含波形画布样式的字典，应包括"background"（背景色）和"foreground"（前景色）键。
        :type waveform_style: dict

        :param ruler_style: 一个包含标尺样式的字典，应包括"background"（背景色）和"foreground"（前景色）键。
        :type ruler_style: dict

        波形画布和标尺控件将根据提供的样式信息进行创建和放置，并设置网格布局权重以适应窗口大小的变化。
        """
        super().__init__(master)
        self.mark_manage = MarkManage()
        self.audio_loader = audio_model.AudioLoader()

        # 创建并放置波形画布和标尺控件
        self.waveform_canvas = WaveformCanvas(self, self.audio_loader, waveform_style["background"],
                                              waveform_style["foreground"])
        self.waveform_canvas.grid(row=1, column=0, sticky="news")

        self.ruler_widget = Ruler(self, self.audio_loader, ruler_style["background"], ruler_style["foreground"])
        self.ruler_widget.grid(row=0, column=0, sticky="news")

        # 设置网格布局权重以适应窗口大小变化
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def set_style(self, widget: str, style: dict):
        if widget == "waveform_canvas":
            self.waveform_canvas.set_style((style["background"], style["foreground"]))
        elif widget == "ruler":
            self.ruler_widget.set_style((style["background"], style["foreground"]))
        else:
            raise IndexError("指定控件不存在，目前可选项：\"waveform_canvas\",\"ruler\"。")

    def open_file(self, file_path):
        """
        加载指定路径的音频文件，并更新波形画布和标尺显示。

        :param file_path: 音频文件的路径
        """
        max_width = self.winfo_screenwidth()  # 获取屏幕最大宽度
        self.audio_loader.load_audio(file_path, max_width)
        self.waveform_canvas.draw_waveform()
        self.ruler_widget.draw_ruler()

    def create_mark(self, color: str, width: int = 10, position: float = 0.0):
        """
        在指定位置创建一个新的标记。

        :param color: 标记的颜色
        :param width: 标记的宽度，默认为10像素
        :param position: 标记的位置，默认为0秒（音频起始）
        """
        if self.audio_loader.audio_data is not None:
            ruler_mark_width = width
            waveform_canvas_mark_width = max(2, width // 10)

            self.mark_manage.create_mark(
                [(self.ruler_widget, ruler_mark_width),
                 (self.waveform_canvas, waveform_canvas_mark_width)],
                color, position)
        else:
            raise FileNotFoundError("创建标记出错，当前没有打开音频文件")

    def del_mark(self, mark_id):
        """
        删除指定ID的标记。

        :param mark_id: 要删除的标记ID
        """
        self.mark_manage.del_mark(mark_id)

    def set_mark_position(self, mark_id, position):
        """
        更新指定ID的标记的位置。

        :param mark_id: 要更新位置的标记ID
        :param position: 新的位置
        """
        self.mark_manage.set_mark_position(mark_id, position)

    def set_mark_motion_callback(self, mark_id, callback, *args):
        """
        设置拖动标记时触发的回调函数。

        :param mark_id: 关联的标记ID
        :param callback: 回调函数
        :param args: 传递给回调函数的额外参数
        """
        self.mark_manage.set_mark_motion_callback(mark_id, callback, *args)

    def set_mark_release_callback(self, mark_id, callback, *args):
        """
        设置释放标记时触发的回调函数。

        :param mark_id: 关联的标记ID
        :param callback: 回调函数
        :param args: 传递给回调函数的额外参数
        """
        self.mark_manage.set_mark_release_callback(mark_id, callback, *args)


class MarkManage:
    """标记管理器类，用于管理所有标记的创建、位置更新和事件绑定。"""

    def __init__(self):
        self.mark_dict = {}
        self.mark_release_callback = {}
        self.mark_motion_callback = {}
        self.mark_id = 0

    def create_mark(self, widget_list: list, color: str, position: float):
        """
        创建一个新的标记，并将其添加到提供的小部件中。

        :param widget_list: 包含要添加标记的小部件及其宽度的列表
        :param color: 标记的颜色
        :param position: 标记的位置
        """
        mark_group = []
        for w in widget_list:
            mark = Mark(w[0], color, w[1])
            mark.set_position(position)
            mark.set_button_motion(self.change_position, self.mark_id, "motion")
            mark.set_button_release(self.change_position, self.mark_id, "release")
            mark_group.append(mark)
        self.mark_dict[self.mark_id] = mark_group
        self.mark_id += 1

    def del_mark(self, mark_id):
        """
        销毁并移除指定ID的标记。

        :param mark_id: 要销毁的标记ID
        """
        if mark_id in self.mark_dict:
            for m in self.mark_dict[mark_id]:
                m.destroy()
            del self.mark_dict[mark_id]
            if mark_id in self.mark_motion_callback:
                del self.mark_motion_callback[mark_id]
            if mark_id in self.mark_release_callback:
                del self.mark_release_callback[mark_id]
        else:
            raise IndexError("尝试销毁不存在的标记：mark_id 不存在！")

    def set_mark_position(self, mark_id, position):
        """
        更新指定ID的标记的位置。

        :param mark_id: 要更新位置的标记ID
        :param position: 新的位置
        """
        if mark_id in self.mark_dict:
            for m in self.mark_dict[mark_id]:
                m.set_position(position)
        else:
            raise IndexError("尝试设置位置时出错，mark_id不存在！")

    def set_mark_motion_callback(self, mark_id, callback, *args):
        """
        设置拖动标记时触发的回调函数。

        :param mark_id: 关联的标记ID
        :param callback: 回调函数
        :param args: 传递给回调函数的额外参数
        """
        self.mark_motion_callback[mark_id] = [callback, *args]

    def set_mark_release_callback(self, mark_id, callback, *args):
        """
        设置释放标记时触发的回调函数。

        :param mark_id: 关联的标记ID
        :param callback: 回调函数
        :param args: 传递给回调函数的额外参数
        """
        self.mark_release_callback[mark_id] = [callback, *args]

    def change_position(self, position, mark_id, status):
        """
        当标记的位置改变时调用此方法，根据状态调用相应的回调函数。

        :param position: 新的位置
        :param mark_id: 标记ID
        :param status: 操作的状态，"motion" 或 "release"
        """
        self.set_mark_position(mark_id, position)
        if status == "motion":
            self._mark_motion(position, mark_id)
        elif status == "release":
            self._mark_release(position, mark_id)

    def _mark_motion(self, position, mark_id):
        """
        触发与拖动标记关联的回调函数。

        :param position: 标记的新位置
        :param mark_id: 标记ID
        """
        if mark_id in self.mark_dict:
            try:
                callback, *args = self.mark_motion_callback.get(mark_id, [])
                callback(position, *args)
            except ValueError:
                print("请设置回调函数，方法：set_mark_motion_callback")
        else:
            raise IndexError("设置motion回调函数时出错，mark_id不存在！")

    def _mark_release(self, position, mark_id):
        """
        触发与释放标记关联的回调函数。

        :param position: 标记的新位置
        :param mark_id: 标记ID
        """
        if mark_id in self.mark_dict:
            try:
                callback, *args = self.mark_release_callback.get(mark_id, [])
                callback(position, *args)
            except ValueError:
                print("请设置回调函数，方法：set_mark_release_callback")
        else:
            raise IndexError("设置release回调函数时出错，mark_id不存在！")


# 使用示例
if __name__ == "__main__":
    from tkinter import filedialog

    root = tk.Tk()
    oscilloscope = Oscilloscope(root, {"background": "#4b704c",
                                       "foreground": "#000"},
                                {"background": "#4b704c",
                                 "foreground": "#000"})  # 创建Oscilloscope实例
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    oscilloscope.grid(row=0, column=0, sticky="news")

    oscilloscope.set_style("ruler", ("#f00", "#fff"))


    def open_filedialog():
        """
        打开文件选择对话框，让用户选择一个WAV格式的音频文件，
        并将其加载到振荡器中显示。
        """
        file_path = filedialog.askopenfilename(
            title="选择 WAV 文件",
            filetypes=[("WAV files", "*.wav"), ("所有文件", "*.*")]
        )
        if file_path:
            oscilloscope.open_file(file_path)
            oscilloscope.create_mark("#fff", 10)  # 创建白色标记
            oscilloscope.create_mark("#f00", 10, 0.5)  # 创建红色标记，初始位置为音频的50%
            oscilloscope.set_mark_position(0, 1)  # 移动第一个标记到末尾
            oscilloscope.set_mark_motion_callback(0, print_info, "id = 0")
            oscilloscope.set_mark_motion_callback(1, print_info, "id = 1")


    def print_info(p, info):
        print(f"{p:.2f} {info}")


    def add_random_mark():
        """
        添加一个随机颜色和位置的标记。
        """
        import random
        colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"]
        position = random.random()
        oscilloscope.create_mark(random.choice(colors), 10, position)


    def delete_last_mark():
        """
        删除最后一个创建的标记。
        """
        if oscilloscope.mark_manage.mark_dict:
            last_id = list(oscilloscope.mark_manage.mark_dict.keys())[-1]
            oscilloscope.del_mark(last_id)


    # 创建按钮以实现各种操作
    button_frame = ttk.Frame(root)
    button_frame.grid(row=1, column=0, pady=10)

    ttk.Button(button_frame, text="打开文件", command=open_filedialog).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="添加随机标记", command=add_random_mark).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="删除最后一个标记", command=delete_last_mark).pack(side=tk.LEFT, padx=5)

    tk.mainloop()  # 运行主循环
