import subprocess
import shutil
import os


def build(specfile):
    """
    使用 PyInstaller 构建应用程序。
    """

    try:
        print("开始构建应用程序...")
        result = subprocess.run(
            ["pyinstaller", specfile, "-y"],
            capture_output=True,
            text=True,  # 确保输出为文本格式
            shell=True,
            check=True  # 如果命令失败，则抛出 CalledProcessError
        )
        print("构建完成。")
        if result.stdout:
            print("标准输出:")
            print(result.stdout)
        if result.stderr:
            print("标准错误:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"构建过程中发生错误: {e}")
        if e.output:
            print("标准输出:")
            print(e.output)
        if e.stderr:
            print("标准错误:")
            print(e.stderr)
    except Exception as e:
        print(f"发生未知错误: {e}")


def copy_item(old, new):
    """
    复制文件或目录。
    如果目标已存在，则询问用户是否覆盖。
    """
    try:
        # 检查源路径是否存在
        if not os.path.exists(old):
            print(f"错误: 源路径 '{old}' 不存在。")
            return

        # 判断源路径是文件还是目录
        if os.path.isfile(old):
            copy_single_file(old, new)
        elif os.path.isdir(old):
            copy_directory(old, new)
        else:
            print(f"错误: 源路径 '{old}' 既不是文件也不是目录。")

    except Exception as e:
        print(f"发生未知错误: {e}")


def copy_single_file(old, new):
    """复制单个文件"""
    if os.path.exists(new):
        response = input(f"文件 '{new}' 已存在，是否覆盖? (y/n): ").strip().lower()
        if response != 'y':
            print("操作取消。")
            return

    try:
        shutil.copy2(old, new)  # 使用 copy2 保留元数据
        print(f"文件已成功复制到 '{new}'。")
    except FileNotFoundError as e:
        print(f"错误: {e}")
        print("源文件不存在，请检查路径。")
    except PermissionError as e:
        print(f"错误: {e}")
        print("权限不足，无法复制文件。")
    except Exception as e:
        print(f"发生未知错误: {e}")


def copy_directory(old, new):
    """递归复制整个目录树"""
    if os.path.exists(new):
        response = input(f"目录 '{new}' 已存在，是否覆盖? (y/n): ").strip().lower()
        if response != 'y':
            print("操作取消。")
            return

    try:
        shutil.copytree(old, new, dirs_exist_ok=True)  # Python 3.8+ 支持 dirs_exist_ok 参数
        print(f"目录已成功复制到 '{new}'。")
    except FileExistsError:
        print(f"目录 '{new}' 已存在，但未选择覆盖。")
    except PermissionError as e:
        print(f"错误: {e}")
        print("权限不足，无法复制目录。")
    except Exception as e:
        print(f"发生未知错误: {e}")


if __name__ == "__main__":
    build("./test.spec")

    directory = "测试"
    # 示例：复制构建后的文件或目录
    source_path = 'resource'  # 替换为实际的源路径
    destination_path = f'dist/{directory}/resource'  # 替换为实际的目标路径
    copy_item(source_path, destination_path)
