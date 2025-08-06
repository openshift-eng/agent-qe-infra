from playwright.sync_api import Page, expect

from base.logger import log_page_activity


@log_page_activity
class InstallationProgress:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.verify_heading = page.locator("h2")

    def verify_text(self, text: str):
        expect(self.verify_heading).to_contain_text(text)
