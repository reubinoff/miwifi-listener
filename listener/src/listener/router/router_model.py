import requests
import urllib.parse

from listener.router.encrypt import Encrypt

class Router:
    MAC = "88:66:5a:24:46:db"
    TYPE = 0
    def __init__(self, router_ip) -> None:
        self._router_ip = router_ip
        self._logged_in = False
        self._session = requests.Session()

    def login(self, password):
        url = f"http://{self._router_ip}/cgi-bin/luci/api/xqsystem/login"
        enc = Encrypt(type=Router.TYPE, device_id=Router.MAC)
        nonce = enc.get_none()
        enc_pass = enc.encrypt(password=password, nonce=nonce)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "username": "admin",
            "password": enc_pass,
            "logtype": 2,
            "nonce": nonce
        }
        status = self._session.post(url, headers=headers, data=data)
        if status.ok:
            self._token = status.json()["token"]
            self._url = status.json()["url"] 
            self._logged_in = True
            return True
        return False

    def logout(self) -> bool:
        url = f"http://{self._router_ip}/cgi-bin/luci/;stok={self._token}/web/logout"
        status = self._session.post(url)
     
        # print(status.text)
        if status.ok:
            return True
        return False

    def get_device_list(self):
        url = f"http://{self._router_ip}/cgi-bin/luci/;stok={self._token}/api/misystem/devicelist"
        status = self._session.get(url)
        headers = {
            "Referer": self._url
        }
        print(status.text)
        if status.ok:
            return status.json()["list"]
        return None
    
    def toggle_device_connection(self, mac_addr, connection_alive):
        on_state = 1 if connection_alive else 0
        encoded_mac = urllib.parse.quote(mac_addr)
        url = f"http://{self._router_ip}/cgi-bin/luci/;stok={self._token}/api/xqsystem/set_mac_filter?mac={encoded_mac}&wan={on_state}"
        status = self._session.get(url)
        if status.ok:
            print(f"Toggled connection to {mac_addr} to {connection_alive} Succeed")
            return True
        else:
            print(f"Toggled connection to {mac_addr} to {connection_alive} Failed")
            return False


        
if __name__ == "__main__":
    r = Router("192.168.31.1")
    print(r.login("noayairitamar"))
    r.get_device_list()
        