import requests
import re
import json
import base64


class NetWork:
    def __init__(self, **kwargs) -> None:
        self.wlan_user_ip = ""
        self.wlan_ac_ip = ""
        self.wlan_user_mac = ""
        self.base_url = "http://10.0.1.5:801/eportal/portal/login"
        self.session = requests.Session()
        self.account = kwargs.get("account")
        self.password = kwargs.get("password")
        self.isp = kwargs.get("isp")

    def _getParams(self):
        URL = "http://1.2.3.4"
        res = self.session.get(URL)
        html = res.url
        pattern = r"wlanuserip=([\d\.]+).*?wlanacip=([\d\.]+).*?wlanusermac=([\w\-]+)"
        m = re.search(pattern, html)
        if m:
            self.wlan_user_ip = m.group(1)
            self.wlan_ac_ip = m.group(2)
            self.wlan_user_mac = m.group(3)

    def login(self):
        self._getParams()
        pararms = {
            "callback": "dr1003",
            "login_method": "1",
            "user_account": f",0,{self.account}@{self.isp}",
            "user_password": base64.b64encode(self.password.encode()).decode(),
            "wlan_user_ip": self.wlan_user_ip,
            "wlan_user_ipv6": "",
            "wlan_user_mac": self.wlan_user_mac,
            "wlan_ac_ip": self.wlan_ac_ip,
            "wlan_ac_name": "HJ-BRAS-ME60-01",
        }
        res = self.session.get(self.base_url, params=pararms)
        if self.checkResult(res.text):
            print("Login success")
        else:
            print("Login failed")
            print(f"Error message: {res.text}")

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
    def checkNetwork():
        import urllib3

        try:
            http = urllib3.PoolManager()
            http.request("GET", "https://baidu.com")
            return True
        except:
            return False
