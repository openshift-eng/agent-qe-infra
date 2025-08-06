from playwright.sync_api import Page, expect

from base.logger import log_page_activity
from pages.storage import Storage


@log_page_activity
class HostDiscovery:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.host_count = page.get_by_test_id("host-name")
        self.next_button = page.get_by_role("button", name="Next")

    def verify_host_count(self, count: int):
        expect(self.host_count).to_have_count(count, timeout=90000)
        return self

    def click_next_button(self):
        self.next_button.is_enabled(timeout=90000)
        self.next_button.click()
        return Storage(self.page)
