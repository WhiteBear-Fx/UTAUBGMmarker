from waveform_canvas import WaveformCanvas
from ruler import Ruler
from mark import Mark

import audio_model

import tkinter as tk
from tkinter import ttk


class Oscilloscope(ttk.Frame):
    """
    Oscilloscope 的主要类，该控件的子容器在此处被放置，并封装了方法。
    使用该控件应实例化该类。

    该类负责管理波形画布（WaveformCanvas）、标尺（Ruler）和标记管理器（MarkManage），
    并提供加载音频文件、创建标记和设置标记事件回调的方法。
    """

    def __init__(self, master):
        """
        初始化 Oscilloscope 实例，包括初始化标签管理器、音频加载器，
        波形画布控件和标尺控件，并将它们放置在网格布局中。

        :param master: 父窗口或框架
        """
        super().__init__(master)
        self.mark_manage = MarkManage()  # 标记管理器，用于管理和创建时间轴上的标记
        self.audio_loader = audio_model.AudioLoader()  # 音频加载器，用于加载音频数据

        self.waveform_canvas = WaveformCanvas(self, self.audio_loader)  # 创建波形画布控件实例
        self.waveform_canvas.grid(row=1, column=0, sticky="news")  # 将波形画布放置在网格中

        self.ruler_widget = Ruler(self, self.audio_loader)  # 创建标尺控件实例
        self.ruler_widget.grid(row=0, column=0, sticky="news")  # 将标尺控件放置在网格中

        self.columnconfigure(0, weight=1)  # 设置列权重，使组件可以随着窗口大小调整
        self.rowconfigure(1, weight=1)  # 设置行权重，使组件可以随着窗口大小调整

    def open_file(self, file_path):
        """
        打开指定路径的音频文件并加载到音频加载器中。
        更新波形画布和标尺以反映新加载的音频数据。

        :param file_path: 音频文件的路径
        """
        max_width = self.winfo_screenwidth()  # 获取屏幕最大宽度
        self.audio_loader.load_audio(file_path, max_width)  # 加载音频文件
        self.waveform_canvas.draw_waveform()  # 在波形画布上绘制波形
        self.ruler_widget.draw_ruler()  # 绘制标尺

    def create_mark(self, color: str, width: int = 10, position: float = 0):
        """
        创建一个新的标记，并添加到波形画布和标尺上。

        :param color: 标记的颜色
        :param width: 标记的宽度，默认为10像素
        :param position: 标记的位置，默认为0秒
        """
        ruler_mark_width = width
        waveform_canvas_mark_width = max(2, width // 10)

        self.mark_manage.create_mark(
            [(self.ruler_widget, ruler_mark_width),
             (self.waveform_canvas, waveform_canvas_mark_width)],
            color, position)

    def set_mark_position(self, mark_id, position):
        """
        设置指定ID的标记的新位置。

        :param mark_id: 要移动的标记的ID
        :param position: 新的位置
        """
        self.mark_manage.set_mark_position(mark_id, position)

    def set_mark_motion_callback(self, mark_id, callback, *args):
        """
        设置当拖动标记时触发的回调函数，回调函数第一个参数为标尺位置比例，范围[1, 0]。

        :param mark_id: 关联的标记ID
        :param callback: 回调函数
        :param args: 传递给回调函数的额外参数
        """
        self.mark_manage.set_mark_motion_callback(mark_id, callback, *args)

    def set_mark_release_callback(self, mark_id, callback, *args):
        """
        设置当释放标记时触发的回调函数，回调函数第一个参数为标尺位置比例，范围[1, 0]。

        :param mark_id: 关联的标记ID
        :param callback: 回调函数
        :param args: 传递给回调函数的额外参数
        """
        self.mark_manage.set_mark_release_callback(mark_id, callback, *args)


class MarkManage:
    """
    标记管理器类，用于管理所有标记的创建、位置更新和事件绑定。
    """

    def __init__(self):
        self.mark_dict = {}
        self.mark_release_callback = {}
        self.mark_motion_callback = {}
        self.mark_id = 0

    def create_mark(self, widget: list, color: str, position: float):
        """
        在提供的小部件列表中创建一个标记。

        :param widget: 包含要添加标记的小部件及其宽度的列表
        :param color: 标记的颜色
        :param position: 标记的位置
        """
        mark_group = []  # 使用局部变量来存储当前创建的一组标记
        for w in widget:
            mark = Mark(w[0], color, w[1])
            mark.set_position(position)
            mark.set_button_motion(self.change_position, self.mark_id, "motion")
            mark.set_button_release(self.change_position, self.mark_id, "release")
            mark_group.append(mark)
        self.mark_dict[self.mark_id] = mark_group
        self.mark_id += 1

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
            raise IndexError("mark_id不存在！")

    def set_mark_motion_callback(self, mark_id, callback, *args):
        """
        设置当拖动指定ID的标记时触发的回调函数。

        :param mark_id: 关联的标记ID
        :param callback: 回调函数
        :param args: 传递给回调函数的额外参数
        """
        self.mark_motion_callback[mark_id] = [callback, *args]

    def set_mark_release_callback(self, mark_id, callback, *args):
        """
        设置当释放指定ID的标记时触发的回调函数。

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
        if status == "release":
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
            raise IndexError("mark_id不存在！")

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
            raise IndexError("mark_id不存在！")


# 使用示例
if __name__ == "__main__":
    from tkinter import filedialog

    root = tk.Tk()
    oscilloscope = Oscilloscope(root)  # 创建Oscilloscope实例
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    oscilloscope.grid(row=0, column=0, sticky="news")


    def open_filedialog():
        """
        打开文件选择对话框，让用户选择一个WAV格式的音频文件，
        并将其加载到振荡器中显示。
        """
        file_path = filedialog.askopenfilename(
            title="选择 WAV 文件",
            filetypes=[("WAV files", "*.wav"), ("所有文件", "*.*")]
        )
        if file_path is not None and file_path != "":
            oscilloscope.open_file(file_path)
            oscilloscope.create_mark("#fff", 10)  # 创建白色标记
            oscilloscope.create_mark("#f00", 10, 0.5)  # 创建红色标记，初始位置为音频的50%
            oscilloscope.set_mark_position(0, 1)  # 移动第一个标记到末尾
            oscilloscope.set_mark_motion_callback(0, print_info, "id = 0")
            oscilloscope.set_mark_motion_callback(1, print_info, "id = 1")


    def print_info(p, info):
        print(f"{p:.2f} {info}")


    button = ttk.Button(root, text="点击打开文件", command=open_filedialog)  # 创建按钮
    button.grid(row=1, column=0)
    tk.mainloop()  # 运行主循环
