import logging

from playwright.sync_api import Page, expect

from base.logger import log_page_activity


@log_page_activity
class InstallationProgress:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = logging.getLogger("assisted_ui")

    def verify_text(self, text: str):
        if "Installation" in text:
            self.logger.info(f"Verifying '{text}' is present")
            expect(self.page.get_by_text(text)).to_be_visible()
            return self
        self.logger.info(f"Verifying '{text}' is present")
        self.page.get_by_text(text).wait_for(
            state="visible",
            timeout=4 * 60 * 60 * 1000
        )
        self.logger.info("Console URL is available.")
        return None