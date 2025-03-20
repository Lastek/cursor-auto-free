from dotenv import load_dotenv
import os
import sys
from logger import logging


class Config:
    def __init__(self):
        # Get the application root directory path
        if getattr(sys, "frozen", False):
            # If it's a packaged executable
            application_path = os.path.dirname(sys.executable)
        else:
            # If in development environment
            application_path = os.path.dirname(os.path.abspath(__file__))

        # Specify .env file path
        dotenv_path = os.path.join(application_path, ".env")

        if not os.path.exists(dotenv_path):
            raise FileNotFoundError(f"File {dotenv_path} does not exist")

        # Load .env file
        load_dotenv(dotenv_path)

        self.imap = False
        self.temp_mail = os.getenv("TEMP_MAIL", "").strip().split("@")[0]
        self.temp_mail_epin = os.getenv("TEMP_MAIL_EPIN", "").strip()
        self.temp_mail_ext = os.getenv("TEMP_MAIL_EXT", "").strip()
        self.domain = os.getenv("DOMAIN", "").strip()

        # Load IMAP if temporary email is null
        if self.temp_mail == "null":
            self.imap = True
            self.imap_server = os.getenv("IMAP_SERVER", "").strip()
            self.imap_port = os.getenv("IMAP_PORT", "").strip()
            self.imap_user = os.getenv("IMAP_USER", "").strip()
            self.imap_pass = os.getenv("IMAP_PASS", "").strip()
            self.imap_dir = os.getenv("IMAP_DIR", "inbox").strip()

        self.check_config()

    def get_temp_mail(self):
        return self.temp_mail

    def get_temp_mail_epin(self):
        return self.temp_mail_epin

    def get_temp_mail_ext(self):
        return self.temp_mail_ext

    def get_imap(self):
        if not self.imap:
            return False
        return {
            "imap_server": self.imap_server,
            "imap_port": self.imap_port,
            "imap_user": self.imap_user,
            "imap_pass": self.imap_pass,
            "imap_dir": self.imap_dir,
        }

    def get_domain(self):
        return self.domain

    def get_protocol(self):
        """Get email protocol type
        
        Returns:
            str: 'IMAP' or 'POP3'
        """
        return os.getenv('IMAP_PROTOCOL', 'POP3')

    def check_config(self):
        """Check if configuration items are valid

        Check rules:
        1. If using tempmail.plus, need to configure TEMP_MAIL and DOMAIN
        2. If using IMAP, need to configure IMAP_SERVER, IMAP_PORT, IMAP_USER, IMAP_PASS
        3. IMAP_DIR is optional
        """
        # Basic configuration check
        required_configs = {
            "domain": "Domain",
        }

        # Check basic configuration
        for key, name in required_configs.items():
            if not self.check_is_valid(getattr(self, key)):
                raise ValueError(f"{name} not configured, please set {key.upper()} in .env file")

        # Check email configuration
        if self.temp_mail != "null":
            # tempmail.plus mode
            if not self.check_is_valid(self.temp_mail):
                raise ValueError("Temporary email not configured, please set TEMP_MAIL in .env file")
        else:
            # IMAP mode
            imap_configs = {
                "imap_server": "IMAP Server",
                "imap_port": "IMAP Port",
                "imap_user": "IMAP Username",
                "imap_pass": "IMAP Password",
            }

            for key, name in imap_configs.items():
                value = getattr(self, key)
                if value == "null" or not self.check_is_valid(value):
                    raise ValueError(
                        f"{name} not configured, please set {key.upper()} in .env file"
                    )

            # IMAP_DIR is optional, check its validity if set
            if self.imap_dir != "null" and not self.check_is_valid(self.imap_dir):
                raise ValueError(
                    "IMAP inbox directory configuration invalid, please set IMAP_DIR correctly in .env file"
                )

    def check_is_valid(self, value):
        """Check if configuration item is valid

        Args:
            value: Value of configuration item

        Returns:
            bool: Whether configuration item is valid
        """
        return isinstance(value, str) and len(str(value).strip()) > 0

    def print_config(self):
        if self.imap:
            logging.info(f"\033[32mIMAP Server: {self.imap_server}\033[0m")
            logging.info(f"\033[32mIMAP Port: {self.imap_port}\033[0m")
            logging.info(f"\033[32mIMAP Username: {self.imap_user}\033[0m")
            logging.info(f"\033[32mIMAP Password: {'*' * len(self.imap_pass)}\033[0m")
            logging.info(f"\033[32mIMAP Inbox Directory: {self.imap_dir}\033[0m")
        if self.temp_mail != "null":
            logging.info(
                f"\033[32mTemporary Email: {self.temp_mail}{self.temp_mail_ext}\033[0m"
            )
        logging.info(f"\033[32mDomain: {self.domain}\033[0m")


# Usage example
if __name__ == "__main__":
    try:
        config = Config()
        print("Environment variables loaded successfully!")
        config.print_config()
    except ValueError as e:
        print(f"Error: {e}")