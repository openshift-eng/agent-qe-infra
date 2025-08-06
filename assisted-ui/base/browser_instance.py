import logging
import os
from typing import Optional
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, ProxySettings

from pages.cluster_details import ClusterDetails


class BrowserInstance:
    def __init__(self, headless: bool = True):
        self.logger = logging.getLogger("assisted_ui")
        self.proxy = None
        self.headless = headless

        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.proxy_url = os.getenv("PROXY_URL")
        parsed = urlparse(self.proxy_url)
        self.username = parsed.username
        self.password = parsed.password
        self.server = f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"

    def start(self, app_url: str) -> ClusterDetails:
        self.logger.info(f"Starting browser instance headless={self.headless}")
        self.playwright = sync_playwright().start()
        self.proxy: ProxySettings = {
            "server": self.server,
            "username": self.username,
            "password": self.password
        }

        self.browser = self.playwright.firefox.launch(headless=self.headless, proxy=self.proxy, downloads_path="/tmp",
                                                      firefox_user_prefs={
                                                          "security.enterprise_roots.enabled": True,
                                                          "security.ssl.enable_ocsp_stapling": False,
                                                          "security.cert_pinning.enforcement_level": 0,
                                                          "security.ssl.errorReporting.enabled": False
                                                      })

        self.context = self.browser.new_context(
            accept_downloads=True
        )

        self.page = self.context.new_page()
        self.page.goto(app_url)
        return ClusterDetails(self.page)

    def stop(self):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
