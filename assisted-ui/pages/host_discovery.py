import logging
import os

from playwright.sync_api import Page, expect
from base.logger import log_page_activity
from pages.storage import Storage


@log_page_activity
class HostDiscovery:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.host_status = page.get_by_test_id("host-hw-status")
        self.host_name = page.get_by_test_id("host-name")
        self.host_role = page.get_by_test_id("host-role")
        self.worker = page.locator('[id="worker"]')
        self.next_button = page.get_by_role("button", name="Next")
        self.logger = logging.getLogger("assisted_ui")

    def verify_host_count_and_status(self, count: int):
        expected_statuses = ["Ready"] * count
        expect(self.host_name).to_have_count(count, timeout=90000)
        expect(self.host_status).to_have_text(expected_statuses, timeout=120000)
        return self

    def change_host_role_to_worker(self, topology_type: str):
        if topology_type == "HA":
            self.logger.info("The selected topology is HA")
            for name, role in zip(self.host_name.all(), self.host_role.all()):
                if "worker" in (name.text_content() or "").lower():
                    self.logger.info(f"Changing {name.text_content()} host role to worker..")
                    role.click()
                    self.worker.click()
        return self

    def click_next_button(self):
        self.next_button.is_enabled(timeout=90000)
        self.next_button.click()
        return Storage(self.page)
