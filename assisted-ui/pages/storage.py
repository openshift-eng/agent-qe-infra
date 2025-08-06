from playwright.sync_api import Page

from base.logger import log_page_activity
from pages.networking_details import NetworkingDetails


@log_page_activity
class Storage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.next_button = page.get_by_role("button", name="Next")

    def click_next_button(self):
        self.next_button.is_enabled(timeout=90000)
        self.next_button.click()
        return NetworkingDetails(self.page)
