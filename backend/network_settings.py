import os

def configure_ethernet(ip, mask, gateway, dhcp_enabled):
    """
    Nastavenie Ethernet pripojenia.
    """
    if dhcp_enabled:
        os.system("sudo dhclient eth0")
    else:
        if not ip or not mask or not gateway:
            raise ValueError("IP, mask, and gateway are required for static configuration.")
        os.system(f"sudo ifconfig eth0 {ip} netmask {mask}")
        os.system(f"sudo route add default gw {gateway}")

def configure_wifi(ssid, password):
    """
    Nastavenie Wi-Fi pripojenia.
    """
    if not ssid:
        raise ValueError("SSID is required for Wi-Fi configuration.")
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as file:
        file.write(f"""
network={{
    ssid="{ssid}"
    psk="{password}"
}}
""")
    os.system("sudo systemctl restart networking")

def configure_can(address, speed):
    """
    Nastavenie CAN rozhrania.
    """
    if not address or not speed:
        raise ValueError("CAN address and speed are required.")
    os.system(f"sudo ip link set can0 type can bitrate {speed}")
    os.system(f"sudo ip link set can0 up")
