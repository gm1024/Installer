# coding=utf-8
import logging
import os
import time
from pathlib import Path


class RedisInstaller(object):
    # https://github.com/winsw/winsw
    config_template = """
<service>
  <id>{service_name}</id>
  <name>{service_name}</name>
  <description></description>
  <executable>%BASE%\\redis-server.exe</executable>
  <arguments>--port {port}</arguments>
  <log mode="roll"></log>
</service>
""".strip()

    def __init__(
        self,
        base_dir: Path,
        service_name="Redis",
        port: int = 6379,
    ) -> None:
        self.base_dir = base_dir
        self.service_name = service_name
        self.port = port

    def install(self) -> bool:
        self.write_config_file()

        retries = 5
        for i in range(retries):
            self.remove_service()
            time.sleep(2)
            succ = self.install_service()
            if not succ:
                logging.error("failed to install service")
            if succ:
                succ = self.start_service()
                if not succ:
                    logging.error("failed to start service")
            if succ:
                break
            logging.error("retrying...")
            time.sleep(5)
        return succ

    def uninstall(self) -> bool:
        self.remove_service()
        return True

    @property
    def config_file(self) -> Path:
        file = self.base_dir.joinpath("redis-service.xml")
        return file

    @property
    def service_bin(self) -> Path:
        file = self.base_dir.joinpath("redis-service.exe")
        return file

    def write_config_file(self):
        content = self.config_template.format(
            service_name=self.service_name, port=self.port
        )
        self.config_file.write_text(content, encoding="utf-8")

    def remove_service(self):
        cmd = f"sc stop {self.service_name}"
        retcode = os.system(cmd)
        if retcode == 0:
            time.sleep(5)
        cmd = f"sc delete {self.service_name}"
        os.system(cmd)

    def install_service(self) -> bool:
        cmd = f"{self.service_bin} install"
        ret = os.system(cmd)
        return ret == 0

    def start_service(self) -> bool:
        cmd = f"{self.service_bin} start"
        ret = os.system(cmd)
        return ret == 0
