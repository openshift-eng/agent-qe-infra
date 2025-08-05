import os
import subprocess
import sys
import tempfile
import time
import warnings

import pexpect
import requests
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

from core.logger import get_logger

warnings.simplefilter("ignore", InsecureRequestWarning)


class SessionHandler:
    def __init__(self, ip: str, user: str, password: str):
        self.ip = ip
        self.user = user
        self.password = password
        self.session = None
        self.ssh_key = os.environ.get("SSH_PRIVATE_KEY")
        self.ipmi_password = os.environ.get("IPMITOOL_PASSWORD")
        self.aux_host = os.environ.get("AUX_HOST")
        self.logger = get_logger()

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as key_file:
            key_file.write(self.ssh_key)
            key_file_path = key_file.name

            # Secure the key file
            os.chmod(key_file_path, 0o600)
        self.sshopts = (
            "-o ConnectTimeout=5 "
            "-o StrictHostKeyChecking=no "
            "-o UserKnownHostsFile=/dev/null "
            "-o ServerAliveInterval=90 "
            "-o LogLevel=ERROR "
            f"-i {key_file_path}"
        )
        self.cmd = f"ssh {self.sshopts} -tt -q root@{self.aux_host} ipmitool -I lanplus -H {self.ip} -U {self.user} -E sol"

    def sol_activate(self):
        """
        Activate SOL session using ipmitool and return the pexpect session process.
        Logs output to specified log file.
        """

        url = f"https://{self.ip}/redfish/v1/"
        timeout = 15 * 60
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                self.logger.info("Checking BMC readiness...")
                response = requests.get(
                    url,
                    auth=HTTPBasicAuth(self.user, self.password),
                    verify=False,
                    timeout=timeout
                )
                if response.status_code == 200:
                    self.logger.info("BMC is up and running")
                    self.session = pexpect.spawn(f"{self.cmd} activate", timeout=30)
                    self.session.expect("Password:", timeout=10)
                    self.session.sendline(self.ipmi_password)
                    self.logger.info("SOL session activated successfully...")
                    self.session.expect("type drm_connector registered", timeout=timeout)
                    self.session.logfile = open(self.logger.handlers[0].baseFilename, "wb")
                    return self.session
            except Exception:
                self.logger.warning(f"BMC not ready yet. Retrying...")
                time.sleep(30)
        self.logger.error("Timeout: Failed to activate SOL session after waiting 15 minutes.")
        sys.exit(1)

    def sol_deactivate(self):
        """
        Deactivate SOL session using ipmitool command.
        Does not print exception details to avoid leaking sensitive info.
        """
        try:
            self.session.terminate(force=True)
            self.session = pexpect.spawn(f"{self.cmd} deactivate", timeout=30)
            self.session.expect("Password:", timeout=10)
            self.session.sendline(self.ipmi_password)
            self.logger.info("SOL session deactivated successfully.")
        except Exception:
            self.logger.error(f"Exception occurred while deactivate SOL session.")
