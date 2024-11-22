import os

def set_time(date, time):
    os.system(f"sudo date -s '{date} {time}'")
    os.system("sudo hwclock -w")

def set_ntp_server(ntp_server):
    with open("/etc/ntp.conf", "w") as file:
        file.write(f"server {ntp_server}\n")
    os.system("sudo systemctl restart ntp")
