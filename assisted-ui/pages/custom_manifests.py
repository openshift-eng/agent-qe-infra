from base.logger import get_logger
from base.logger import log_page_activity
from pages.review import Review
from playwright.sync_api import Page, TimeoutError


@log_page_activity
class CustomManifests:
    def __init__(self, page: Page) -> None:
        self.logger = get_logger()
        self.page = page
        self.custom_manifests_heading = page.locator("h2", has_text="Custom manifests")
        self.next_button = page.get_by_role("button", name="Next")

    def handle_custom_manifests(self):
        try:
            self.custom_manifests_heading.wait_for(state="visible", timeout=5000)
            self.logger.info("Custom manifests page detected (OCP 4.22+)")
            self.next_button.click()
        except TimeoutError:
            self.logger.info("No Custom manifests page (OCP <4.22), already on review page")
        return Review(self.page)
