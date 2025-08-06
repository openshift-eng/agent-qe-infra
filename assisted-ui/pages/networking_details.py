from playwright.sync_api import Page

from base.logger import log_page_activity
from pages.download_credentials import DownloadCredentials


@log_page_activity
class NetworkingDetails:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.api_ip = page.get_by_role("textbox", name="API IP")
        self.ingress_ip = page.get_by_role("textbox", name="Ingress IP")
        self.user_managed_networking = page.get_by_role("radio", name="User-Managed Networking")
        self.next_button = page.get_by_role("button", name="Next")

    def type_api_ip(self, api_ip: str):
        self.api_ip.fill(api_ip)
        return self

    def type_ingress_ip(self, ingress_ip: str):
        self.ingress_ip.fill(ingress_ip)
        return self

    def select_user_managed_networking(self):
        self.user_managed_networking.check()
        return self

    def click_next_button(self):
        self.next_button.click(timeout=90000)
        return DownloadCredentials(self.page)
