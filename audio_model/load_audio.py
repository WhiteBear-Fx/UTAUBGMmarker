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
        time (float): 音频的总时长（秒）。

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

        get_duration():
            计算音频的总时长（秒）。

            返回:
                float: 音频的总时长（秒）。
    """

    def __init__(self):
        """
        初始化AudioLoader类实例。
        """
        self.rate = None  # 存储采样率
        self.frames = None  # 存储帧数
        self.max_audio_data = None  # 存储可能的最大音频数据
        self.audio_data = None  # 存储音频数据
        self.n_channels = None  # 存储声道数
        self.time = None  # 存储音频的总时长（秒）

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
            self.frames = wav_file.getnframes()  # 获取帧数
            self.rate = wav_file.getframerate()  # 获取采样率

            self.get_duration()  # 计算音频的总时长（秒）

            raw_data = wav_file.readframes(self.frames)  # 读取所有帧的数据
            audio_data = self._convert_raw_to_numpy(raw_data, sample_width)  # 将原始数据转换为numpy数组

            # 动态计算下采样因子
            if self.frames > max_size:
                audio_data = self._downsample(audio_data, max_size)

            if self.n_channels == 2:
                average_audio_data = self._compute_stereo_average(audio_data)  # 计算立体声平均值
            else:
                average_audio_data = audio_data  # 单声道直接使用原始数据

            self.max_audio_data = self._normalize_audio(average_audio_data, sample_width)  # 归一化音频数据

    def get_duration(self):
        if self.rate is not None:
            # 计算时长
            self.time = self.frames / float(self.rate)
            return self.time

    @staticmethod
    def _convert_raw_to_numpy(raw_data, sample_width):
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
    def _downsample(audio_data, target_length):
        """
        对音频数据进行下采样，保证输出长度为 target_length。
        每个窗口取一个正值最大和一个负值最小的点。

        :param audio_data: 音频数据数组。
        :param target_length: 目标长度。
        :return: 下采样的音频数据数组。
        """
        original_length = len(audio_data)

        if original_length <= target_length:
            return np.array(audio_data)

        # 因为每个窗口要取两个点，所以实际窗口数量应该是 target_length 的一半
        effective_target_length = target_length // 2

        # 计算浮点数类型的下采样因子
        downsampling_factor = original_length / effective_target_length

        # 初始化结果数组
        downsampled_data = []

        # 计算每个窗口的起点索引
        indices = np.arange(0, original_length, downsampling_factor)

        for i in range(effective_target_length):
            start_index = int(np.floor(indices[i]))
            end_index = int(np.ceil(indices[i + 1])) if i + 1 < len(indices) else original_length

            window = audio_data[start_index:end_index]

            if len(window) > 0:
                # 分别获取窗口中的最大正值和最小负值
                max_val = np.max(window)
                min_val = np.min(window)

                # 将这两个值添加到结果数组中
                downsampled_data.extend([max_val, min_val])
            else:
                # 如果窗口为空，可以考虑添加上一个窗口的最大值和最小值，或者保持不变
                # 这里简单处理为添加两个默认值，比如0
                downsampled_data.extend([0, 0])

        # 如果目标长度是奇数，则最后一个窗口只添加一个值（可以是最大值或最小值）
        if target_length % 2 != 0:
            if len(downsampled_data) >= 2:
                # 使用最后已知的最大值或最小值作为填充
                last_known_value = downsampled_data[-2] if downsampled_data[-1] == 0 else downsampled_data[-1]
                downsampled_data.append(last_known_value)
            else:
                # 如果downsampled_data不足两个元素，使用0作为默认值
                downsampled_data.append(0)

        return np.array(downsampled_data[:target_length])  # 确保返回的数组长度等于 target_length

    @staticmethod
    def _compute_stereo_average(audio_data):
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
    def _normalize_audio(audio_data, sample_width):
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
            self.audio_data = self._downsample(self.max_audio_data, control_size)
        else:
            # 理论上这里应该插值，不过在这个项目这样写没问题
            self.audio_data = self.max_audio_data
        return self.audio_data
