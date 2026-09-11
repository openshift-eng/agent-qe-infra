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
        self.ip_address = os.getenv("IP_ADDRESS")
        self.server_address = os.getenv("SERVER_ADDRESS")
        self.interface = os.getenv("INTERFACE")
        self.hostname = os.getenv("HOSTNAME")
        self.select_network = os.getenv("SELECT_NETWORK", "dhcp").lower() == "dhcp"

        required_vars = [
            'IPMITOOL_IP',
            'IPMITOOL_USERNAME',
            'IPMITOOL_PASSWORD',
            'RENDEZVOUS_IP',
            'RENDEZVOUS_NODE',
            'SSH_PRIVATE_KEY',
            'AUX_HOST'
        ]

        if self.select_network:
            required_vars.extend(['HOSTNAME', 'IP_ADDRESS', 'SERVER_ADDRESS', 'INTERFACE'])

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            self.logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            sys.exit(1)

        self.session_handler = SessionHandler(self.ip, self.user, self.password)
        self.session = self.session_handler.sol_activate()
        self.logger.info("=== Starting agent-tui automation ===")

    def run_dhcp(self):
        assisted_ui_message = f"Please go to http://{self.rendezvous_ip}:3001/ in your browser"
        rendezvous_login_message = fr"This host \({self.rendezvous_ip}\) is the rendezvous host"
        non_rendezvous_login_message = f"This host is not the rendezvous host"
        try:
            if self.rendezvous_node == "yes":
                if not (RendezvousNodeSetupScreen(self.session)
                        .rendezvous_node()
                        .select_ip()
                        .verify_rendezvous_node_info(rendezvous_login_message)
                        .verify_assisted_ui_url_info(assisted_ui_message)):
                    LoginScreen(self.session).fail("Assisted UI URL message not found")
            else:
                RendezvousNodeSetupScreen(self.session) \
                    .non_rendezvous_node(self.rendezvous_ip) \
                    .verify_rendezvous_node_info(non_rendezvous_login_message)
        except Exception:
            self.logger.error(f"Exception occurred during the execution.")
        finally:
            self.session_handler.sol_deactivate()

    def run_static(self):
        (RendezvousNodeSetupScreen(self.session)
            .configure_network()
            .set_hostname(hostname=self.hostname)
            .click_edit_a_connection()
            .add_ipv4_configuration(ip_address=self.ip_address,
                                    gateway_address=self.server_address,
                                    dns_address=self.server_address)
            .click_activate_a_connection(interface=self.interface)
            .go_back_to_rendezvous_node_setup_screen())
        self.run_dhcp()

    def run(self):
        if self.select_network:
            self.run_dhcp()
        else:
            self.run_static()