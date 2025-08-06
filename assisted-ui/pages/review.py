from playwright.sync_api import Page

from base.logger import log_page_activity
from pages.installation_progress import InstallationProgress


@log_page_activity
class Review:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.install_cluster = page.get_by_test_id("button-install-cluster")

    def click_install_cluster(self):
        self.install_cluster.click(timeout=60000)
        return InstallationProgress(self.page)
