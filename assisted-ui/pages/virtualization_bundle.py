import logging
import time

from playwright.sync_api import Page

from base.logger import log_page_activity
from pages.host_discovery import HostDiscovery


@log_page_activity
class VirtualizationBundle:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.virtualization = page.get_by_label("", exact=True)
        self.expand_operators_list = page.locator('[id^="expandable-section-toggle-"]')
        self.next_button = page.get_by_role("button", name="Next")
        self.logger = logging.getLogger("assisted_ui")

    def click_virtualization_checkbox(self, topology_type: str):
        if topology_type == "SNO":
            return self
        time.sleep(2)
        self.virtualization.check()
        time.sleep(2)
        return self

    def select_operators(self, operators: list):
        if operators:
            self.expand_operators_list.click()
            for operator in operators:
                self.logger.info(f"Selecting operator '{operator}'")
                self.page.get_by_test_id(f"operator-checkbox-{str(operator).strip().lower()}").check()
                time.sleep(2)
        else:
            self.logger.info("No additional operators are provided")
        return self

    def click_next_button(self):
        self.next_button.click()
        return HostDiscovery(self.page)
