import os

def configure_ethernet(ip, mask, gateway, dhcp_enabled):
    if dhcp_enabled:
        os.system("sudo dhclient eth0")
    else:
        os.system(f"sudo ifconfig eth0 {ip} netmask {mask}")
        os.system(f"sudo route add default gw {gateway}")

def configure_wifi(ssid, password):
    with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as file:
        file.write(f"""
network={{
    ssid="{ssid}"
    psk="{password}"
}}
""")
    os.system("sudo systemctl restart networking")
