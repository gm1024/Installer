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
