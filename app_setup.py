# coding=utf-8
from pathlib import Path
import json


class appSetup(object):
    def __init__(
        self,
        dest_dir: Path,
        old_app_dir: Path,
        instrument: str,
        service_port: int,
        sqlany_host: str,
        sqlany_port: int,
        sqlany_server: str,
        sqlany_user: str,
        sqlany_password: str,
        mysql_port: int,
        mysql_password: str,
        redis_port: int,
    ) -> None:
        self.dest_dir = dest_dir
        self.old_app_dir = old_app_dir
        self.instrument = instrument
        self.service_port = service_port

        self.sqlany_host = sqlany_host
        self.sqlany_port = sqlany_port
        self.sqlany_server = sqlany_server
        self.sqlany_user = sqlany_user
        self.sqlany_password = sqlany_password

        self.mysql_port = mysql_port
        self.mysql_password = mysql_password
        self.redis_port = redis_port

    @property
    def service_dir(self) -> Path:
        return self.dest_dir.joinpath("service")

    @property
    def client_dir(self) -> Path:
        return self.dest_dir.joinpath("client")

    @property
    def client_bin(self) -> Path:
        return self.client_dir.joinpath("client.exe")

    def setup(self) -> bool:
        self.setup_client()
        self.setup_service()
        self.create_shortcut()
        return True

    def setup_client(self) -> bool:
        service_exe = self.service_dir.joinpath("service.exe")
        client_config_file = self.client_dir.joinpath("config.json")
        client_config = json.loads(client_config_file.read_text(encoding="utf-8"))
        client_config["service"]["exe"] = str(service_exe)
        client_config["service"]["url"] = f"https://localhost:{self.service_port}/"
        client_config_file.write_text(
            json.dumps(client_config, indent=2, ensure_ascii=False)
        )
        return True

    def setup_service(self) -> bool:
        config_dir = self.service_dir.joinpath("config")

        app_config_file = config_dir.joinpath("app.json")
        app_config = json.loads(app_config_file.read_text(encoding="utf-8"))
        app_config["instrument"] = self.instrument
        app_config["port"] = self.service_port
        app_config["app_dir"] = str(self.old_app_dir)
        app_config_file.write_text(
            json.dumps(app_config, indent=2, ensure_ascii=False)
        )

        db_config_file = config_dir.joinpath("db.json")
        db_config = json.loads(db_config_file.read_text(encoding="utf-8"))
        db_config["host"] = f"{self.sqlany_host}:{self.sqlany_port}"
        db_config["servername"] = self.sqlany_server
        db_config["uid"] = self.sqlany_user
        db_config["password"] = self.sqlany_password
        db_config_file.write_text(json.dumps(db_config, indent=2, ensure_ascii=False))

        log_db_file = config_dir.joinpath("log_db.json")
        log_db = json.loads(log_db_file.read_text(encoding="utf-8"))
        log_db["port"] = self.mysql_port
        log_db["password"] = self.mysql_password
        log_db_file.write_text(json.dumps(log_db, indent=2, ensure_ascii=False))

        redis_config_file = config_dir.joinpath("redis.json")
        redis_config = json.loads(redis_config_file.read_text(encoding="utf-8"))
        url = f"redis://localhost:{self.redis_port}/0"
        redis_config["url"] = url
        redis_config_file.write_text(
            json.dumps(redis_config, indent=2, ensure_ascii=False)
        )

        return True

    def create_shortcut(self):
        import win32com.client

        shell = win32com.client.Dispatch("WScript.Shell")

        link_name = "app.lnk"

        lnk_path1 = str(self.dest_dir.joinpath(link_name))
        shortcut = shell.CreateShortCut(lnk_path1)
        shortcut.Targetpath = str(self.client_bin)
        shortcut.Iconlocation = str(self.client_bin)
        shortcut.WorkingDirectory = str(self.client_bin.parent)
        shortcut.save()
