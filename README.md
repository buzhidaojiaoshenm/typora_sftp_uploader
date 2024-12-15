# typora_sftp_uploader
用于typora图片上传服务，使用sftp上传到服务器指定路径，并返回相应的链接

## 修改配置
配置区域
- SFTP_HOST = "xxx.xxx.xxx.xxx"  # SFTP服务器地址
- SFTP_PORT = 22  # SFTP端口号
- SFTP_USER = "xxx"  # SFTP用户名
- SFTP_PASSWORD = "xxxxxxxx"  # SFTP密码
- REMOTE_PATH = "xxx/xxx/xxx/xxx"  # 服务器存储图片的根目录
- BASE_URL = "https://xxx.xxx.xxx/"  # 图片的基础访问URL

## 设置typora上传服务
- 上传服务：选择custom comman
- 命令 python your_path/typora_sftp_uploader.py
