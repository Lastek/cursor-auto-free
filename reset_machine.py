import os
import sys
import json
import uuid
import hashlib
import shutil
from colorama import Fore, Style, init

# Initialize colorama
init()

# Define emoji and color constants
EMOJI = {
    "FILE": "",
    "BACKUP": "",
    "SUCCESS": "✅",
    "ERROR": "❌",
    "INFO": "ℹ️",
    "RESET": "",
}


class MachineIDResetter:
    def __init__(self):
        # Determine the operating system
        if sys.platform == "win32":  # Windows
            appdata = os.getenv("APPDATA")
            if appdata is None:
                raise EnvironmentError("APPDATA environment variable is not set")
            self.db_path = os.path.join(
                appdata, "Cursor", "User", "globalStorage", "storage.json"
            )
        elif sys.platform == "darwin":  # macOS
            self.db_path = os.path.abspath(
                os.path.expanduser(
                    "~/Library/Application Support/Cursor/User/globalStorage/storage.json"
                )
            )
        elif sys.platform == "linux":  # Linux and other Unix-like systems
            self.db_path = os.path.abspath(
                os.path.expanduser("~/.config/Cursor/User/globalStorage/storage.json")
            )
        else:
            raise NotImplementedError(f"Unsupported operating system: {sys.platform}")

    def generate_new_ids(self):
        """Generate new machine IDs"""
        # Generate a new UUID
        dev_device_id = str(uuid.uuid4())

        # Generate a new machineId (64-character hexadecimal)
        machine_id = hashlib.sha256(os.urandom(32)).hexdigest()

        # Generate a new macMachineId (128-character hexadecimal)
        mac_machine_id = hashlib.sha512(os.urandom(64)).hexdigest()

        # Generate a new sqmId
        sqm_id = "{" + str(uuid.uuid4()).upper() + "}"

        return {
            "telemetry.devDeviceId": dev_device_id,
            "telemetry.macMachineId": mac_machine_id,
            "telemetry.machineId": machine_id,
            "telemetry.sqmId": sqm_id,
        }

    def reset_machine_ids(self):
        """Reset machine IDs and back up the original file"""
        try:
            print(f"{Fore.CYAN}{EMOJI['INFO']} Checking configuration file...{Style.RESET_ALL}")

            # Check if the file exists
            if not os.path.exists(self.db_path):
                print(
                    f"{Fore.RED}{EMOJI['ERROR']} Configuration file does not exist: {self.db_path}{Style.RESET_ALL}"
                )
                return False

            # Check file permissions
            if not os.access(self.db_path, os.R_OK | os.W_OK):
                print(
                    f"{Fore.RED}{EMOJI['ERROR']} Cannot read or write to configuration file, please check file permissions!{Style.RESET_ALL}"
                )
                print(
                    f"{Fore.RED}{EMOJI['ERROR']} If you have used go-cursor-help to modify the ID; please modify the file read-only permission {self.db_path} {Style.RESET_ALL}"
                )
                return False

            # Read existing configuration
            print(f"{Fore.CYAN}{EMOJI['FILE']} Reading current configuration...{Style.RESET_ALL}")
            with open(self.db_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            # Generate new IDs
            print(f"{Fore.CYAN}{EMOJI['RESET']} Generating new machine identifiers...{Style.RESET_ALL}")
            new_ids = self.generate_new_ids()

            # Update configuration
            config.update(new_ids)

            # Save the new configuration
            print(f"{Fore.CYAN}{EMOJI['FILE']} Saving new configuration...{Style.RESET_ALL}")
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Machine identifiers reset successfully!{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}New machine identifiers:{Style.RESET_ALL}")
            for key, value in new_ids.items():
                print(f"{EMOJI['INFO']} {key}: {Fore.GREEN}{value}{Style.RESET_ALL}")

            return True

        except PermissionError as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Permission error: {str(e)}{Style.RESET_ALL}")
            print(
                f"{Fore.YELLOW}{EMOJI['INFO']} Please try running this program as administrator{Style.RESET_ALL}"
            )
            return False
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Error during reset process: {str(e)}{Style.RESET_ALL}")

            return False


if __name__ == "__main__":
    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{EMOJI['RESET']} Cursor Machine ID Reset Tool{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")

    resetter = MachineIDResetter()
    resetter.reset_machine_ids()

    print(f"\n{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    input(f"{EMOJI['INFO']} Press Enter to exit...")