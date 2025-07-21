这是一个Windows应用安装程序， 主界面使用CustomTinker编写，包含MySQL服务注册，Redis服务注册等


1. 打包
运行 build.bat
在 dist 目录下得到 appInstaller.exe


2. 准备源文件目录

源文件目录/
    service/
    client/
    mysql-win32/
    redis-win32/
    appInstaller.exe
    create_mysql_db.sql

(源文件目录可以放在U盘或压缩包)


3. 安装

1) 启动 appInstaller.exe
2) 设置信息
3) 点击 "开始安装"

MySQL 及 Redis 将被注册成系统服务自动启动。

4. 卸载
1) 启动 appInstaller.exe
2) 切换到 "卸载"
3) 点击 "卸载"

<img width="1304" height="1060" alt="安装界面1" src="https://github.com/user-attachments/assets/39a98507-ebf4-4f98-af53-6a4264f253b3" />

<img width="1304" height="1060" alt="安装界面2" src="https://github.com/user-attachments/assets/5ba4ab22-1aa1-4527-b179-de203d11dc6f" />

<img width="1304" height="1060" alt="安装界面3" src="https://github.com/user-attachments/assets/43b45d03-a0e7-4b9d-a7fd-6ca44ad32fd9" />
