import os

def apply_vpn_config(config_path):
    """
    Aplikovanie WireGuard VPN konfigurácie.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    # Kopírovanie konfiguračného súboru do /etc/wireguard/
    os.system(f"sudo cp {config_path} /etc/wireguard/wg0.conf")
    
    # Spustenie WireGuard VPN
    os.system("sudo wg-quick up wg0")

def disable_vpn():
    """
    Vypnutie WireGuard VPN.
    """
    os.system("sudo wg-quick down wg0")
