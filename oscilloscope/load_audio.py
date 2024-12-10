import wave
import numpy as np


class AudioLoader:
    """
    AudioLoader 类用于加载和处理 WAV 文件中的音频数据。

    提供以下功能：
    - 加载 WAV 文件并缓存最大控件大小的归一化的音频数据、采样率和声道数。
    - 更新控件大小并重新计算下采样因子，返回更新后的归一化的音频数据数组。

    属性:
        max_audio_data (np.ndarray): 最大控件大小的归一化音频数据。
        audio_data (np.ndarray): 当前控件大小的归一化音频数据。
        frame_rate (int): 音频的采样率。
        n_channels (int): 音频的声道数。

    方法:
        load_audio(file_path, max_size):
            加载 WAV 文件并缓存最大控件大小的归一化的音频数据、采样率和声道数。

            参数:
                file_path (str): WAV 文件的路径。
                max_size (int): 控件可能的最大大小（像素数）。

        get_audio_data(control_size):
            更新控件大小并重新计算下采样因子，返回更新后的归一化的音频数据数组。

            参数:
                control_size (int): 控件实际大小（像素数），应小于 max_size。

            返回:
                np.ndarray: 更新后的归一化的音频数据数组。
    """

    def __init__(self):
        """
        初始化AudioLoader类实例。
        """
        self.max_audio_data = None  # 存储可能的最大音频数据
        self.audio_data = None  # 存储音频数据
        self.frame_rate = None  # 存储采样率
        self.n_channels = None  # 存储声道数

    def load_audio(self, file_path, max_size):
        """
        加载WAV文件并缓存最大控件大小的归一化的音频数据、采样率和声道数。
        根据控件大小动态计算下采样因子，并在计算立体声平均值和归一化之前对音频数据进行下采样。

        :param file_path: WAV文件的路径。
        :param max_size: 控件可能的最大大小（像素数）。
        :return: 归一化的音频数据数组。
        """
        with wave.open(file_path, 'r') as wav_file:
            self.n_channels = wav_file.getnchannels()  # 获取声道数
            sample_width = wav_file.getsampwidth()  # 获取采样宽度（字节）
            original_frame_rate = wav_file.getframerate()  # 获取原始采样率
            n_frames = wav_file.getnframes()  # 获取帧数

            raw_data = wav_file.readframes(n_frames)  # 读取所有帧的数据
            audio_data = self.convert_raw_to_numpy(raw_data, sample_width)  # 将原始数据转换为numpy数组

            # 动态计算下采样因子
            if n_frames > max_size:
                audio_data = self.downsample(audio_data, max_size)

            if self.n_channels == 2:
                average_audio_data = self.compute_stereo_average(audio_data)  # 计算立体声平均值
            else:
                average_audio_data = audio_data  # 单声道直接使用原始数据

            self.max_audio_data = self.normalize_audio(average_audio_data, sample_width)  # 归一化音频数据

    @staticmethod
    def convert_raw_to_numpy(raw_data, sample_width):
        """
        将原始字节数据转换为numpy数组。

        :param raw_data: 原始字节数据。
        :param sample_width: 采样宽度（字节）。
        :return: 转换后的numpy数组。
        """
        dtype_map = {1: np.uint8, 2: np.int16}  # 数据类型映射
        if sample_width not in dtype_map:
            raise ValueError(f"Unsupported sample width: {sample_width}")
        audio_data = np.frombuffer(raw_data, dtype=dtype_map[sample_width])  # 将字节数据转换为numpy数组
        return audio_data

    @staticmethod
    def downsample(audio_data, target_length):
        """
        对音频数据进行下采样，保证输出长度为 target_length。

        :param audio_data: 音频数据数组。
        :param target_length: 目标长度。
        :return: 下采样的音频数据数组。
        """
        original_length = len(audio_data)
        if original_length <= target_length:
            return np.array(audio_data)

        # 计算浮点数的下采样因子
        downsampling_factor = original_length / target_length

        # 初始化结果数组
        downsampled_data = []

        # 计算每个窗口的起点索引
        indices = np.arange(0, original_length, downsampling_factor)

        for i in range(target_length):
            start_index = int(np.floor(indices[i]))
            end_index = int(np.ceil(indices[i + 1])) if i + 1 < len(indices) else original_length

            window = audio_data[start_index:end_index]
            if len(window) > 0:
                extrema = np.max(np.abs(window))
                index = np.where(np.abs(window) == extrema)[0][0]
                downsampled_data.append(window[index])

        return np.array(downsampled_data)

    @staticmethod
    def compute_stereo_average(audio_data):
        """
        计算立体声音频数据的平均值。

        :param audio_data: 立体声音频数据数组。
        :return: 左右声道平均值组成的数组。
        """
        left_channel = audio_data[::2]  # 提取左声道数据
        right_channel = audio_data[1::2]  # 提取右声道数据
        average_audio_data = (left_channel + right_channel) / 2  # 计算左右声道平均值
        return average_audio_data

    @staticmethod
    def normalize_audio(audio_data, sample_width):
        """
        归一化音频数据。

        :param audio_data: 音频数据数组。
        :param sample_width: 采样宽度（字节）。
        :return: 归一化的音频数据数组。
        """
        if sample_width == 1:
            audio_ratio_data = (audio_data.astype(np.float32) - 128) / 128  # 归一化8位无符号整数
        elif sample_width == 2:
            audio_ratio_data = audio_data.astype(np.float32) / 32767  # 归一化16位有符号整数
        else:
            raise ValueError(f"Unsupported sample width: {sample_width}")
        return audio_ratio_data

    def get_audio_data(self, control_size):
        """
        更新控件大小并重新计算下采样因子。

        :param control_size: 控件实际大小（像素数），应小于 max_size。
        :return: 更新后的归一化的音频数据数组。
        """
        if len(self.max_audio_data) > control_size:
            self.audio_data = self.downsample(self.max_audio_data, control_size)
        else:
            # 暂时这样写，实际上这里应该报错
            self.audio_data = self.max_audio_data
        return self.audio_data
