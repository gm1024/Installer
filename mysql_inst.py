# coding=utf-8

import configparser
import logging
import os
import shutil
import time
from pathlib import Path


class MySqlInstaller(object):
    def __init__(
        self,
        base_dir: Path,
        data_dir: Path = None,
        password: str = "1234",
        service_name="MySQL",
        port: int = 3306,
        sql_file: Path = None,
    ):
        self.base_dir = base_dir.absolute()
        if data_dir is None:
            data_dir = base_dir.joinpath("data")
        self.data_dir = data_dir.absolute()
        self.password = password
        self.service_name = service_name
        self.port = port
        self.sql_file = sql_file

        self.write_my_ini()

    def install(self) -> bool:
        while True:
            self.uninstall()

            ret = self.initialize_data_dir()
            if not ret:
                logging.error("failed to init data")
                break
            ret = self.install_service()
            if not ret:
                logging.error("failed to install service")
                break
            ret = self.start_service()
            if not ret:
                logging.error("failed to start service")
                break

            sql = self.alter_password_sql()
            ret = self.mysql_exec_sql(sql, with_password=False)
            if not ret:
                logging.error("failed to alter password")
                break

            sql = self.post_install_sql()
            ret = self.mysql_exec_sql(sql, with_password=True)
            if not ret:
                logging.error("failed to execute sql")
                break
            break
        return ret

    def uninstall(self) -> bool:
        self.stop_service()
        self.remove_service()
        try:
            shutil.rmtree(self.data_dir)
        except:
            pass
        return True

    @property
    def mysqld_bin(self) -> Path:
        ret = self.base_dir.joinpath("bin", "mysqld")
        return ret

    @property
    def mysql_bin(self) -> Path:
        ret = self.base_dir.joinpath("bin", "mysql")
        return ret

    @property
    def myini_file(self) -> Path:
        ret = self.base_dir.joinpath("my.ini")
        return ret

    def write_my_ini(self):
        self.myini_file.parent.mkdir(parents=True, exist_ok=True)

        ini = configparser.ConfigParser()

        section = "mysqld"
        ini.add_section(section)
        ini.set(section, "basedir", str(self.base_dir))
        ini.set(section, "datadir", str(self.data_dir))
        ini.set(section, "port", str(self.port))

        with open(self.myini_file, "w") as f:
            ini.write(f)

    def initialize_data_dir(self) -> bool:
        cmd = f"{self.mysqld_bin} --defaults-file={self.myini_file} --initialize-insecure --user=mysql"
        retcode = os.system(cmd)
        return retcode == 0

    def install_service(self) -> bool:
        cmd = f"{self.mysqld_bin} --install {self.service_name} --defaults-file={self.myini_file}"
        retcode = os.system(cmd)
        return retcode == 0

    def remove_service(self) -> bool:
        cmd = f"{self.mysqld_bin} --remove {self.service_name}"
        retcode = os.system(cmd)
        return retcode == 0

    def start_service(self) -> bool:
        cmd = f"sc start {self.service_name}"
        retcode = os.system(cmd)
        time.sleep(5)
        return retcode == 0

    def stop_service(self) -> bool:
        cmd = f"sc stop {self.service_name}"
        retcode = os.system(cmd)
        if retcode == 0:
            time.sleep(5)
        return retcode == 0

    def mysql_exec_sql(self, sql: str, with_password: bool = True) -> bool:
        temp_file = self.data_dir.joinpath("temp.sql")
        temp_file.write_text(sql, encoding="utf-8")

        cmd = f"{self.mysql_bin} --port={self.port} -u root "
        if with_password:
            cmd += f" -p{self.password} "

        cmd += f" < {str(temp_file)}"
        retcode = os.system(cmd)

        temp_file.unlink()
        return retcode == 0

    def alter_password_sql(self) -> str:
        sql = f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{self.password}';"
        return sql

    def post_install_sql(self) -> str:
        sql = ""
        if self.sql_file.exists():
            sql = self.sql_file.read_text(encoding="utf-8")
        return sql
