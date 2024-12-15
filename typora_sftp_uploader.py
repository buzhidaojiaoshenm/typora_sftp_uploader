import paramiko
import os
import sys
from pathlib import Path
from datetime import datetime

# 配置区域
SFTP_HOST = "xxx.xxx.xxx.xxx"  # SFTP服务器地址
SFTP_PORT = 22  # SFTP端口号
SFTP_USER = "xxx"  # SFTP用户名
SFTP_PASSWORD = "xxxxxxxx"  # SFTP密码
REMOTE_PATH = "xxx/xxx/xxx/xxx"  # 服务器存储图片的根目录
BASE_URL = "https://xxx.xxx.xxx/"  # 图片的基础访问URL

# 检查参数
if len(sys.argv) < 2:
    print("Usage: python sftp_upload.py <image_path_1> <image_path_2> ...")
    sys.exit(1)

# 提取所有图片路径
image_paths = [path.strip('"') for path in sys.argv[1:]]

# 上传结果
upload_results = []

# 添加 makedirs 方法
def makedirs(sftp, remote_path):
    dirs = []
    while len(remote_path) > 1:
        try:
            sftp.stat(remote_path)
            break
        except FileNotFoundError:
            dirs.append(remote_path)
            remote_path = os.path.dirname(remote_path)
    for d in reversed(dirs):
        try:
            sftp.mkdir(d)
        except Exception as e:
            print(f"Error creating directory {d}: {e}")

try:
    # 建立SFTP连接
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=SFTP_USER, password=SFTP_PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # 获取当前时间，用于路径和文件名生成
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")

    # 创建远程目录（如果不存在）
    remote_directory = f"{REMOTE_PATH}/{year}/{month}"
    try:
        sftp.listdir(remote_directory)
    except FileNotFoundError:
        makedirs(sftp, remote_directory)

    for local_image_path in image_paths:
        if not os.path.isfile(local_image_path):
            print(f"Error: File {local_image_path} does not exist.")
            continue

        # 获取文件名
        original_name = Path(local_image_path).name
        extension = Path(local_image_path).suffix

        # 生成唯一的文件名以避免冲突
        remote_image_path = f"{remote_directory}/{original_name}"
        counter = 1
        while True:
            try:
                sftp.stat(remote_image_path)
                # 如果文件已存在，修改文件名
                remote_image_path = f"{remote_directory}/{Path(original_name).stem}_{counter}{extension}"
                counter += 1
            except FileNotFoundError:
                break

        # 上传文件
        sftp.put(local_image_path, remote_image_path)

        # 生成Markdown格式链接
        relative_path = remote_image_path.replace(REMOTE_PATH, "").lstrip("/")
        markdown_link = f"{BASE_URL}{relative_path.replace('\\', '/')}"
        upload_results.append(markdown_link)

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'sftp' in locals():
        sftp.close()
    if 'transport' in locals():
        transport.close()

# 输出结果
print("Upload Success:")
print("\n".join(upload_results))
