import os
import sys

from base.browser_instance import BrowserInstance
from base.logger import get_logger


class AgentUiDriver(BrowserInstance):
    def __init__(self):
        super().__init__()
        self.logger = get_logger()
        self.cluster_name = os.getenv("CLUSTER_NAME")
        self.pull_secret = os.getenv("PULL_SECRET")
        self.base_domain = os.getenv("BASE_DOMAIN")
        self.rendezvous_ip = os.getenv("RENDEZVOUS_IP")
        self.api_ip = os.getenv("API_IP")
        self.ingress_ip = os.getenv("INGRESS_IP")
        self.umn = os.getenv("USER_MANAGED_NETWORKING", "false").lower() == "true"

        required_fields = [
            'cluster_name',
            'pull_secret',
            'base_domain',
            'rendezvous_ip'
        ]
        if self.umn:
            required_fields.append('umn')
        else:
            required_fields.extend(['api_ip','ingress_ip'])

        missing = [field for field in required_fields if not getattr(self, field)]
        if missing:
            self.logger.error(f"Error: Missing required environment variables: {', '.join(missing)}")
            sys.exit(1)

        self.app = BrowserInstance()

    def run(self):
        self.logger.info("=== Starting assisted-ui automation ===")
        try:
            cluster_details_page = self.app.start(f"http://{self.rendezvous_ip}:3001/")

            virtualization_page = (cluster_details_page
                                   .type_cluster_name(self.cluster_name)
                                   .type_base_domain(self.base_domain)
                                   .type_pull_secret(self.pull_secret)
                                   .click_next_button())

            host_discovery_page = (virtualization_page
                                   .click_operators_navigation()
                                   .click_virtualization_checkbox()
                                   .click_next_button())

            storage_page = (host_discovery_page
                            .verify_host_count(3)
                            .click_next_button())

            networking_details_page = (storage_page
                                       .click_next_button())

            download_credentials_page = (networking_details_page
                                         .select_user_managed_networking()
                                         .click_next_button()
                                         if self.umn else
                                         networking_details_page
                                         .type_api_ip(self.api_ip)
                                         .type_ingress_ip(self.ingress_ip)
                                         .click_next_button())

            review_page = (download_credentials_page
                           .check_confirmation()
                           .click_download_credentials())

            installation_progress = review_page.click_install_cluster()

            installation_progress.verify_text("Installation progress")
        except Exception:
            self.logger.error(f"Exception occurred during the execution.")
        finally:
            self.app.stop()
