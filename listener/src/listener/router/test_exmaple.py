from router.router_model import Router


def get_device_by_mac(device_list, mac):
    items = [a for a in device_list if a["mac"] == mac]
    return items[0] if len(items)> 0 else None

def is_device_connect_to_wan(self, router: Router, mac: str):
    l = router.get_device_list()
    device = get_device_by_mac(l, mac)
    return str(device["authority"]["wan"]) == "1"


def run():
    router = Router("192.168.31.1")
    status_login = router.login("noayairitamar")
    if status_login is True:
        print("Logged in")
    else:
        print("Auth Failed")
    
    # devices  = router.get_device_list()
    # tv = get_device_by_mac(devices, "4A:9D:E3:A2:24:DB")
    # router.toggle_device_connection( "4A:9D:E3:A2:24:DB", True)
    router.toggle_device_connection( "D4:5E:EC:A0:82:C5", False)

    
    pass
    


if __name__ == "__main__":
    run()