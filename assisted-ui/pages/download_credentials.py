import os
import time

from playwright.sync_api import Download
from playwright.sync_api import Page

from base.logger import log_page_activity
from pages.review import Review


@log_page_activity
class DownloadCredentials:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.download_confirmation = page.get_by_role("checkbox", name="I understand that I need to")
        self.download_credentials = page.get_by_test_id("wizard-step-actions").get_by_role("button",
                                                                                           name="Download credentials")
        self.next_button = page.get_by_role("button", name="Next")
        self.page.on("download", self._on_download)

    def check_confirmation(self):
        self.download_confirmation.check()
        return self

    def _on_download(self, download: Download):
        filename = download.suggested_filename  # it's a property, not a method
        save_path = os.path.join("/tmp", filename)
        download.save_as(save_path)
        print(f"Downloaded: {save_path}")

    def click_download_credentials(self):
        time.sleep(5)
        self.download_credentials.click()
        time.sleep(10)
        return Review(self.page)
