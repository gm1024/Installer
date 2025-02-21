# coding=utf-8
import ctypes
import logging
import os
import platform
import shutil
import sys
from pathlib import Path

import app_setup
import mysql_inst
import PySimpleGUI as sg
import redis_inst
import sqlany_inst

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# if not is_admin():
#     ctypes.windll.shell32.ShellExecuteW(
#         None, "runas", sys.executable, __file__, None, 1
#     )
#     sys.exit()


fmt = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)

UI_THEME = "LightGrey3"

__is_win = platform.system().lower() == "windows"
UI_FONT_SIZE = sg.DEFAULT_FONT[1] if __is_win else 18
UI_FONT = f"_ {UI_FONT_SIZE}"

UI_DEFAULT_INPUT_SIZE = (25, 1)
UI_DEFAULT_ELEMENT_SIZE = (8, 1)

UI_DEFAULT_BUTTON_SIZE = (10, 2)
UI_SHORT_BUTTON_SIZE = (5, 2)

sg.change_look_and_feel(UI_THEME)
sg.set_options(font=UI_FONT)

TITLE = "app 安装器"

SUB_DIRS = ["mysql-win32", "redis-win32", "service", "client", "sqlany"]

KEY_SOURCE_DIR = "source_dir"

KEY_INSTALL_DEST_DIR = "install_dest_dir"
default_install_dir = Path("c:\\app8")

KEY_app_OLD_DIR = "app_old_dir"
default_app_old_dir = Path("c:\\app")

KEY_SERVICE_PORT = "service_port"
default_service_port = "8000"

KEY_INSTRUMENT = "instrument"
default_instrument = "XN"

KEY_SQLANY_HOST = "sqlany_host"
default_sqnany_host = "localhost"
KEY_SQLANY_PORT = "sqlany_port"
default_sqnany_port = "2638"
KEY_SQLANY_UID = "sqlany_uid"
default_sqnany_uid = "dba"
KEY_SQLANY_PASSWORD = "sqlany_password"
default_sqnany_password = "sic_slj"
KEY_SQLANY_SERVER = "sqlany_server"
default_sqnany_server = ""


KEY_MYSQL_SERVICE = "mysql_service"
default_mysql_service = "app-MySQL"
KEY_MYSQL_PASSWORD = "mysql_passsword"
default_mysql_password = "app"
KEY_MYSQL_PORT = "mysql_port"
default_mysql_port = "23306"

KEY_REDIS_SERVICE = "redis_service"
default_redis_service = "app-Redis"
KEY_REDIS_PORT = "redis_port"
default_redis_port = "26379"

KEY_START_INSTALL = "start_install"

KEY_START_UNINSTALL = "start_uninstall"

SHORT_INPUT = 15

KEY_ADVANCE_SETTINGS = "advance_settings"
KEY_TOGGLE_ADVANCE_SETTINGS = "toggle_advance_settings"


class Installer:
    def __init__(self, source_dir: Path) -> None:
        self.source_dir = source_dir
        self.advance_visible = False

    def admin_layout(self):
        admin_text = "管理员权限: "
        if is_admin():
            admin_text += "[是]"
        else:
            admin_text += "[否] (无法执行安装)"
        layout = [sg.Text(admin_text)]
        return layout

    def source_layout(self):
        layout = [
            [sg.Text("源文件目录:")],
            [
                sg.Input(
                    default_text=str(self.source_dir), key=KEY_SOURCE_DIR, readonly=True
                ),
                sg.FolderBrowse(
                    key=KEY_SOURCE_DIR, initial_folder=str(self.source_dir)
                ),
            ],
        ]
        ret = [sg.Frame("源文件", layout)]
        return ret

    def basic_layout(self):
        layout = [
            [sg.Text("安装目录:")],
            [
                sg.Input(
                    default_text=str(default_install_dir),
                    key=KEY_INSTALL_DEST_DIR,
                    readonly=True,
                ),
                sg.FolderBrowse(
                    key=KEY_INSTALL_DEST_DIR, initial_folder=str(default_install_dir)
                ),
            ],
            [sg.Text("app旧版目录:")],
            [
                sg.Input(
                    default_text=str(default_app_old_dir),
                    key=KEY_app_OLD_DIR,
                    readonly=True,
                ),
                sg.FolderBrowse(
                    key=KEY_app_OLD_DIR, initial_folder=str(default_app_old_dir)
                ),
            ],
            [
                sg.Text("仪器:"),
                sg.Input(
                    default_text=default_instrument,
                    key=KEY_INSTRUMENT,
                    size=SHORT_INPUT,
                ),
            ],
            [
                sg.Text("端口:"),
                sg.Input(
                    default_text=default_service_port,
                    key=KEY_SERVICE_PORT,
                    size=SHORT_INPUT,
                ),
            ],
        ]
        ret = [sg.Frame("安装", layout)]
        return ret

    def sqlany_layout(self):
        layout = [
            [
                sg.Text("主机:"),
                sg.Input(
                    key=KEY_SQLANY_HOST,
                    default_text=default_sqnany_host,
                    size=SHORT_INPUT,
                ),
            ],
            [
                sg.Text("端口:"),
                sg.Input(
                    key=KEY_SQLANY_PORT,
                    default_text=default_sqnany_port,
                    size=SHORT_INPUT,
                ),
            ],
            [
                sg.Text("服务:"),
                sg.Input(
                    key=KEY_SQLANY_SERVER,
                    default_text=default_sqnany_server,
                    size=SHORT_INPUT,
                ),
            ],
            [
                sg.Text("用户:"),
                sg.Input(
                    key=KEY_SQLANY_UID,
                    default_text=default_sqnany_uid,
                    size=SHORT_INPUT,
                ),
            ],
            [
                sg.Text("密码:"),
                sg.Input(
                    key=KEY_SQLANY_PASSWORD,
                    default_text=default_sqnany_password,
                    size=SHORT_INPUT,
                ),
            ],
        ]
        ret = [sg.Frame("SQL Anywhere", layout)]
        return ret

    def mysql_layout(self):
        layout = [
            [
                sg.Text("密码:"),
                sg.Input(
                    key=KEY_MYSQL_PASSWORD,
                    default_text=default_mysql_password,
                    size=SHORT_INPUT,
                ),
            ],
            [
                sg.Text("端口:"),
                sg.Input(
                    key=KEY_MYSQL_PORT,
                    default_text=default_mysql_port,
                    size=SHORT_INPUT,
                ),
            ],
            [
                sg.Text("服务:"),
                sg.Input(
                    key=KEY_MYSQL_SERVICE,
                    default_text=default_mysql_service,
                    size=20,
                ),
            ],
        ]
        ret = [sg.Frame("MySQL", layout)]
        return ret

    def redis_layout(self):
        layout = [
            [
                sg.Text("端口:"),
                sg.Input(
                    default_text=default_redis_port,
                    key=KEY_REDIS_PORT,
                    size=SHORT_INPUT,
                ),
            ],
            [
                sg.Text("服务:"),
                sg.Input(
                    key=KEY_REDIS_SERVICE,
                    default_text=default_redis_service,
                    size=20,
                ),
            ],
        ]
        ret = [sg.Frame("Redis", layout)]
        return ret

    def bottom_layout(self):
        layout = [
            sg.Button(
                "开始安装",
                key=KEY_START_INSTALL,
                disabled=not is_admin(),
                size=UI_DEFAULT_BUTTON_SIZE,
                button_color=("black", "#33CC33"),
                disabled_button_color=("grey", "#CCCCCC"),
            )
        ]
        return layout

    def advance_layout(self):
        layout = [
            self.sqlany_layout(),
            self.mysql_layout(),
            self.redis_layout(),
        ]
        return layout

    def show_window(self):
        tab_basic_layout = [
            self.source_layout(),
            self.basic_layout(),
        ]
        tab_advance_layout = self.advance_layout()
        tab_uninstall_layout = [
            [sg.Text("删除所有程序、数据、windows service。")],
            [
                sg.Button(
                    "卸载",
                    key=KEY_START_UNINSTALL,
                    disabled=not is_admin(),
                    size=UI_SHORT_BUTTON_SIZE,
                    button_color=("black", "#CC3333"),
                    disabled_button_color=("grey", "#CCCCCC"),
                )
            ],
        ]
        tab_group_layout = [
            [
                sg.Tab("基本", tab_basic_layout, key="-TAB-basic-"),
                sg.Tab("高级", tab_advance_layout, key="-TAB-advance-"),
                sg.Tab("卸载", tab_uninstall_layout, key="-TAB-uninstall-"),
            ]
        ]
        layout = [
            [self.admin_layout()],
            [sg.TabGroup(tab_group_layout, key="-TABGROUP-")],
            self.bottom_layout(),
        ]
        window = sg.Window(TITLE, layout)

        while True:
            event, values = window.read()
            if event is None:
                break
            try:
                if event == KEY_START_INSTALL:
                    succ = self.run_installing(values)
                    sg.popup("安装成功" if succ else "安装失败")
                    if succ:
                        break

                if event == KEY_START_UNINSTALL:
                    res = sg.popup_yes_no("是否确认卸载？", title="确认")
                    if res == "Yes":
                        succ = self.run_uninstalling(values)
                        sg.popup("卸载成功" if succ else "卸载失败")

            except Exception as ex:
                sg.popup("运行失败，请查看日志")
                logging.error(ex)

        window.close()

    def run_installing(self, values: dict) -> bool:
        ret = False

        logging.info("installing ...")

        while True:
            logging.info("copying files ...")
            ret = self.copy_allfiles(values)
            if not ret:
                logging.error("failed to copy files")
                break
            logging.info("all files copied.")

            logging.info("installing mysql ...")
            ret = self.mysql_install(values)
            if not ret:
                logging.error("failed to install mysql")
                break
            logging.info("mysql installed.")

            logging.info("installing redis ...")
            ret = self.redis_install(values)
            if not ret:
                logging.error("failed to install redis")
                break
            logging.info("redis installed.")


            logging.info("installing sqlany ...")
            ret = self.sqlany_install(values)
            if not ret:
                logging.error("failed to install sqlany")
                break
            logging.info("sqlany installed.")

            logging.info("setting app ...")
            ret = self.app_setup(values)
            if not ret:
                logging.error("failed to setting app")
                break
            logging.info("app setting done.")

            break
        logging.info("installing end.")
        return ret

    def run_uninstalling(self, values: dict) -> bool:
        ret = False
        dest_dir = Path(values[KEY_INSTALL_DEST_DIR])

        logging.info("uninstalling ...")
        while True:
            ret = self.mysql_install(values, install=False)
            if not ret:
                logging.error("failed to uninstall mysql")
                break

            ret = self.redis_install(values, install=False)
            if not ret:
                logging.error("failed to uninstall redis")
                break

            ret = self.sqlany_install(values, install=False)
            if not ret:
                logging.error("failed to uninstall redis")
                break

            try:
                shutil.rmtree(dest_dir)
            except:
                logging.error("failed to delete files")
                pass

            break
        logging.info("uninstalling end.")
        return ret

    def copy_allfiles(self, values: dict) -> bool:
        src_dir = Path(values[KEY_SOURCE_DIR])
        dest_dir = Path(values[KEY_INSTALL_DEST_DIR])

        if dest_dir.exists():
            shutil.rmtree(dest_dir)

        for subdir in SUB_DIRS:
            src_dir_ = src_dir.joinpath(subdir)
            dest_dir_ = dest_dir.joinpath(subdir)
            shutil.copytree(src_dir_, dest_dir_)
        return True

    def mysql_install(self, values: dict, install=True) -> bool:
        src_dir = Path(values[KEY_SOURCE_DIR])
        dest_dir = Path(values[KEY_INSTALL_DEST_DIR])
        password = values[KEY_MYSQL_PASSWORD]
        port = values[KEY_MYSQL_PORT]
        service_name = values[KEY_MYSQL_SERVICE]
        mysql_dest_dir = dest_dir.joinpath("mysql-win32")

        sql_file = src_dir.joinpath("create_mysql_db.sql")
        if not sql_file.exists():
            raise FileNotFoundError(sql_file)

        installer = mysql_inst.MySqlInstaller(
            mysql_dest_dir,
            port=port,
            password=password,
            service_name=service_name,
            sql_file=sql_file,
        )
        if install:
            succ = installer.install()
        else:
            succ = installer.uninstall()
        return succ

    def redis_install(self, values: dict, install=True) -> bool:
        dest_dir = Path(values[KEY_INSTALL_DEST_DIR])
        port = values[KEY_REDIS_PORT]
        service_name = values[KEY_REDIS_SERVICE]
        redis_dest_dir = dest_dir.joinpath("redis-win32")

        installer = redis_inst.RedisInstaller(
            redis_dest_dir, service_name=service_name, port=port
        )
        if install:
            succ = installer.install()
        else:
            succ = installer.uninstall()
        return succ

    def sqlany_install(self, values: dict, install=True) -> bool:
        dest_dir = Path(values[KEY_INSTALL_DEST_DIR])

        installer = sqlany_inst.SQLAnyInstaller(
            dest_dir
        )
        if install:
            succ = installer.install()
        else:
            succ = installer.uninstall()
        return succ

    def app_setup(self, values: dict) -> bool:
        ret = False

        dest_dir = Path(values[KEY_INSTALL_DEST_DIR])
        old_app_dir = Path(values[KEY_app_OLD_DIR])

        instrument = values[KEY_INSTRUMENT]
        service_port = values[KEY_SERVICE_PORT]

        sqlany_host = values[KEY_SQLANY_HOST]
        sqlany_port = values[KEY_SQLANY_PORT]
        sqlany_server = values[KEY_SQLANY_SERVER]
        sqlany_user = values[KEY_SQLANY_UID]
        sqlany_password = values[KEY_SQLANY_PASSWORD]

        mysql_port = values[KEY_MYSQL_PORT]
        mysql_password = values[KEY_MYSQL_PASSWORD]
        redis_port = values[KEY_REDIS_PORT]

        setup = app_setup.appSetup(
            dest_dir,
            old_app_dir,
            instrument=instrument,
            service_port=int(service_port),
            sqlany_host=sqlany_host,
            sqlany_port=int(sqlany_port),
            sqlany_server=sqlany_server,
            sqlany_user=sqlany_user,
            sqlany_password=sqlany_password,
            mysql_port=int(mysql_port),
            mysql_password=mysql_password,
            redis_port=int(redis_port),
        )

        ret = setup.setup()

        return ret


def main():
    cwd = Path(os.getcwd()).absolute()
    installer = Installer(cwd)
    installer.show_window()


if __name__ == "__main__":
    main()
