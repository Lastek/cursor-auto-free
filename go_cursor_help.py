import platform
import os
import subprocess
from logger import logging

def go_cursor_help():
    system = platform.system()
    logging.info(f"Current operating system: {system}")

    base_url = "https://aizaozao.com/accelerate.php/https://raw.githubusercontent.com/yuaotian/go-cursor-help/refs/heads/master/scripts/run"

    if system == "Darwin":  # macOS
        cmd = f'curl -fsSL {base_url}/cursor_mac_id_modifier.sh | sudo bash'
        logging.info("Executing macOS command")
        os.system(cmd)
    elif system == "Linux":
        cmd = f'curl -fsSL {base_url}/cursor_linux_id_modifier.sh | sudo bash'
        logging.info("Executing Linux command")
        os.system(cmd)
    elif system == "Windows":
        cmd = f'irm {base_url}/cursor_win_id_modifier.ps1 | iex'
        logging.info("Executing Windows command")
        # Execute command using PowerShell on Windows
        subprocess.run(["powershell", "-Command", cmd], shell=True)
    else:
        logging.error(f"Unsupported operating system: {system}")
        return False

    return True