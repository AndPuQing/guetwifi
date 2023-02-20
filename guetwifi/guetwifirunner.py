import requests
import re
import time
import logging
import os
import json
import platform
import subprocess
import click
_path = os.path.dirname(os.path.abspath(__file__))


class NetWorkConnectLog:
    def __init__(self, log_file) -> None:
        self.log_file = log_file
        self.logger = logging.getLogger("NetWorkConnectLog")
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self._set_file_handler()

    def _set_file_handler(self):
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)


class NetWork:
    def __init__(self) -> None:
        self._loadConfig()
        self.logger = NetWorkConnectLog("network.log").logger
        self.wlan_user_ip = ""
        self.wlan_ac_ip = ""
        self.wlan_user_mac = ""
        self.base_url = "http://10.0.1.5:801/eportal/portal/login"

    def _loadConfig(self):
        config_path = os.path.join(_path, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                try:
                    self.account = config["account"]
                    self.password = config["password"]
                    self.operator = config["operator"]
                except KeyError:
                    click.echo("Please config your account and password")

    def _getParams(self):
        URL = "http://www.msftconnecttest.com/connecttest.txt"
        HEADERS = {
            "Connection": "Close",
            "User-Agent": "Microsoft NCSI",
            "Host": "www.msftconnecttest.com",
        }
        res = requests.get(URL, headers=HEADERS, allow_redirects=False)
        html = res.text
        pattern = r"wlanuserip=([\d\.]+).*?wlanacip=([\d\.]+).*?wlanusermac=([\w\-]+)"
        m = re.search(pattern, html)
        if m:
            self.wlan_user_ip = m.group(1)
            self.wlan_ac_ip = m.group(2)
            self.wlan_user_mac = m.group(3)
            self.logger.info(
                f"Get params: wlan_user_ip:{self.wlan_user_ip},wlan_ac_ip:{self.wlan_ac_ip},wlan_user_mac:{self.wlan_user_mac}"
            )
        else:
            self.logger.error("Get params failed")
            self.logger.error(f"Response:{html}")

    def login(self):
        self.logger.info(f"Login with account:{self.account}")
        self._getParams()
        pararms = {
            "callback": "dr1003",
            "login_method": "1",
            "user_account": f",0,{self.account}@{self.operator}",
            "user_password": self.password,
            "wlan_user_ip": self.wlan_user_ip,
            "wlan_user_ipv6": "",
            "wlan_user_mac": self.wlan_user_mac,
            "wlan_ac_ip": self.wlan_ac_ip,
            "wlan_ac_name": "HJ-BRAS-ME60-01",
        }
        self.logger.debug(f"Login params:{pararms}")
        res = requests.get(self.base_url, params=pararms)
        self.logger.debug(f"Login response:{res.text}")
        if self.checkResult(res.text):
            self.logger.info("Login success")
        else:
            self.logger.error("Login failed")
            self.logger.error(f"Response:{res.text}")

    def checkResult(self, html):
        match = re.search(r"{.*}", html)
        if match:
            json_text = match.group(0)
            response_data = json.loads(json_text)
            result = response_data["result"]
            msg = response_data["msg"]
            if result == 1 or "已经在线" in msg:
                return True
            else:
                return False

    @staticmethod
    def checkNet():
        # ping www.baidu.com
        command = "ping -c 5 www.baidu.com" if platform.system() == "Darwin" else "ping -n 5 www.baidu.com"
        res = subprocess.run(command, shell=True)
        return res.returncode == 0
    
    def run(self):
        while True:
            if not self.checkNet():
                self.logger.info("Network is not connected, start login......")
                self.login()
            time.sleep(5)


if __name__ == "__main__":
    net = NetWork()
    net.run()
