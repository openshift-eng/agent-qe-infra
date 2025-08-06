from playwright.sync_api import Page, expect

from base.logger import log_page_activity
from pages.virtualization_bundle import VirtualizationBundle


@log_page_activity
class ClusterDetails:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cluster_name = page.get_by_role("textbox", name="Cluster name")
        self.base_domain = page.get_by_role("textbox", name="Base domain")
        self.pull_secret = page.get_by_role("textbox", name="Pull secret")
        self.next_button = page.get_by_role("button", name="Next")
        self.verify_text = page.get_by_role("main")

    def type_cluster_name(self, cluster_name: str):
        self.cluster_name.fill(cluster_name)
        return self

    def type_base_domain(self, base_domain: str):
        self.base_domain.fill(base_domain)
        return self

    def type_pull_secret(self, pull_secret: str):
        self.pull_secret.fill(pull_secret)
        return self

    def click_next_button(self):
        self.next_button.click()
        expect(self.verify_text).not_to_contain_text("Saving changes...", timeout=90000)
        self.page.reload()
        return VirtualizationBundle(self.page)
