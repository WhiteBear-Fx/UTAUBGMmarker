import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import oscilloscope as osc
import ui_theme


if __name__ == "__main__":

    root = tk.Tk()
    root.title("Oscilloscope with Theme Switching")

    # 主题路径
    # noinspection SpellCheckingInspection
    dark_theme_path = r"./resource/theme/dark.json"
    # noinspection SpellCheckingInspection
    light_theme_path = r"./resource/theme/light.json"

    # 创建ThemeLoader实例，并应用“dark.json”主题文件中的样式
    theme_loader = ui_theme.ThemeLoader(dark_theme_path)
    osc_style = theme_loader.get_style("Oscilloscope")

    # 创建Oscilloscope组件，并将其放置在主窗口内
    osc_w = osc.Oscilloscope(root, waveform_style=osc_style["waveform_canvas"],
                             ruler_style=osc_style["ruler"])
    osc_w.grid(row=0, column=0, sticky="news")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)


    def switch_theme():
        # 确保路径处理正确
        current_theme_path = dark_theme_path if status_label.cget("text") == "当前主题：暗色" else light_theme_path
        new_theme_path = light_theme_path if current_theme_path == dark_theme_path else dark_theme_path

        try:
            theme_loader.load_theme(new_theme_path)
            new_osc_style = theme_loader.get_style("Oscilloscope")
            osc_new_style(new_osc_style)

            # 更新状态栏文本以反映新的主题
            new_theme_text = "亮色" if current_theme_path == dark_theme_path else "暗色"
            status_label.config(text=f"当前主题：{new_theme_text}")

            # 强制刷新界面，确保所有更改都显示出来
            root.update_idletasks()

        except KeyError as e:
            messagebox.showerror("Error", str(e))


    def osc_new_style(style):
        osc_w.set_style("ruler", style["ruler"])
        osc_w.set_style("waveform_canvas", style["waveform_canvas"])


    def open_filedialog():
        file_path = filedialog.askopenfilename(
            title="选择 WAV 文件",
            filetypes=[("WAV files", "*.wav"), ("所有文件", "*.*")]
        )
        if file_path:
            osc_w.open_file(file_path)
            mark_1 = osc_w.create_mark("#fff", 10)  # 创建白色标记
            mark_2 = osc_w.create_mark("#f00", 10, 0.8)  # 创建红色标记，初始位置为示波器的80%
            osc_w.set_mark_position(mark_1, 0.2)  # 移动第一个标记到示波器的20%
            osc_w.set_mark_motion_callback(mark_1, print_info, f"id = {mark_1}")
            osc_w.set_mark_motion_callback(mark_2, print_info, f"id = {mark_2}")


    def print_info(p, info):
        print(f"{p:.2f} {info}")


    # 创建按钮框架
    button_frame = ttk.Frame(root)
    button_frame.grid(row=1, column=0, pady=10)

    # 添加打开文件按钮
    ttk.Button(button_frame, text="打开文件", command=open_filedialog).pack(side=tk.LEFT, padx=5)

    # 添加主题切换按钮
    ttk.Button(button_frame, text="切换主题", command=switch_theme).pack(side=tk.LEFT, padx=5)

    # 状态栏显示当前主题
    status_label = ttk.Label(root, text="当前主题：暗色", relief=tk.SUNKEN, anchor=tk.W)
    status_label.grid(row=2, column=0, sticky="ew")

    # 启动Tkinter主事件循环
    root.mainloop()