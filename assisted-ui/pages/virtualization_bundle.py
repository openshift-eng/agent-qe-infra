import time

from playwright.sync_api import Page

from base.logger import log_page_activity
from pages.host_discovery import HostDiscovery


@log_page_activity
class VirtualizationBundle:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.navigate_operators = page.get_by_role("button", name="Operators")
        self.virtualization = page.get_by_label("", exact=True)
        self.next_button = page.get_by_role("button", name="Next")

    def click_operators_navigation(self):
        self.navigate_operators.click()
        return self

    def click_virtualization_checkbox(self):
        time.sleep(2)
        self.virtualization.check()
        time.sleep(2)
        return self

    def click_next_button(self):
        self.next_button.click()
        return HostDiscovery(self.page)
