# coding=utf-8
import logging
import os
import time
from pathlib import Path


fmt = "%(asctime)s %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt)

class SQLAnyInstaller(object):

    def __init__(
        self,
        base_dir: Path,
    ) -> None:
        self.base_dir = base_dir.absolute()

    def install(self) -> bool:

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
    def srv_bin(self) -> Path:
        file = self.base_dir.joinpath("sqlany", "dbsrv12.exe")
        return file
    
    @property
    def srv_db(self) -> Path:
        file = self.base_dir.joinpath("sqlany", "app.db")
        return file

    @property
    def srv_dbsvc(self) -> Path:
        file = self.base_dir.joinpath("sqlany", "dbsvc.exe")
        return file
    
    def remove_service(self):
        cmd = f"{self.srv_dbsvc} -x SQLAny"
        retcode = os.system(cmd)
        if retcode == 0:
            time.sleep(5)
        cmd = f"{self.srv_dbsvc} -yd SQLAny"
        os.system(cmd)

    def install_service(self) -> bool:
        cmd = f"{self.srv_dbsvc} -as -s auto -t network -w  SQLAny {self.srv_bin} -n app {self.srv_db}"
        ret = os.system(cmd)
        return ret == 0

    def start_service(self) -> bool:
        cmd = f"{self.srv_dbsvc} -u SQLAny"
        ret = os.system(cmd)
        return ret == 0
