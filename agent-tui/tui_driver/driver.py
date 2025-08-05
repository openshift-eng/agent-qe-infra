import os
import sys

from core.logger import get_logger
from core.session_handler import SessionHandler
from screens.login_screen import LoginScreen
from screens.rendezvous_node import RendezvousNodeSetupScreen


class AgentTuiDriver:
    def __init__(self):
        self.logger = get_logger("agent_tui")
        self.ip = os.getenv("IPMITOOL_IP")
        self.user = os.getenv("IPMITOOL_USERNAME")
        self.password = os.getenv("IPMITOOL_PASSWORD")
        self.rendezvous_ip = os.getenv("RENDEZVOUS_IP")
        self.rendezvous_node = os.getenv("RENDEZVOUS_NODE")

        required_vars = [
            'IPMITOOL_IP',
            'IPMITOOL_USERNAME',
            'IPMITOOL_PASSWORD',
            'RENDEZVOUS_IP',
            'RENDEZVOUS_NODE',
            'SSH_PRIVATE_KEY',
            'AUX_HOST'
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            self.logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            sys.exit(1)

        self.session_handler = SessionHandler(self.ip, self.user, self.password)

    def run(self):
        self.logger.info("=== Starting agent-tui automation ===")
        session = self.session_handler.sol_activate()
        assisted_ui_message = f"Please go to http://{self.rendezvous_ip}:3001/ in your browser"
        rendezvous_login_message = fr"This host \({self.rendezvous_ip}\) is the rendezvous host"
        non_rendezvous_login_message = f"This host is not the rendezvous host"
        try:
            if self.rendezvous_node == "yes":
                if not (RendezvousNodeSetupScreen(session)
                        .rendezvous_node()
                        .select_ip()
                        .verify_rendezvous_node_info(rendezvous_login_message)
                        .verify_assisted_ui_url_info(assisted_ui_message)):
                    LoginScreen(session).fail("Assisted UI URL message not found")
            else:
                RendezvousNodeSetupScreen(session) \
                    .non_rendezvous_node(self.rendezvous_ip) \
                    .verify_rendezvous_node_info(non_rendezvous_login_message)
        except Exception:
            self.logger.error(f"Exception occurred during the execution.")
        finally:
            self.session_handler.sol_deactivate()
