from core.logger import log_page_activity
from screens.screen_object import ScreenObject

@log_page_activity
class EditConnection(ScreenObject):
    def __init__(self, session):
        super().__init__(session)
        if not self.expect_text("CONFIGURATION"):
            self.fail("Edit Connection screen for IPv4 configuration is not present")

    def change_ipv4_to_manual(self):
        self.press_tab(times=4)
        self.press_enter()
        self.press_key_down(times=2)
        self.press_enter()
        if not self.expect_text("Manual", 5):
            self.fail("Failed to change IPv4 configuration to 'Manual'")
        self.logger.info("IPv4 configuration changed to 'Manual'")
        return self

    def expand_ipv4_configuration(self):
        self.press_tab()
        self.press_enter()
        if not self.expect_text("Hide", 5):
            self.fail("Failed to expand IPv4 configuration")
        self.logger.info("IPv4 configuration expanded")
        return self

    def type_ipv4_address(self, ip_address: str):
        self.press_tab()
        self.press_enter()
        self.send(ip_address)
        return self

    def type_gateway_address(self, gateway_address: str):
        self.press_tab(times=3)
        self.send(gateway_address)
        return self

    def type_dns_address(self, dns_address: str):
        self.press_tab()
        self.press_enter()
        self.send(dns_address)
        return self

    def disable_ipv6_configuration(self):
        self.press_tab(times=9)
        self.press_enter()
        self.press_key_down(times=5)
        self.press_enter()
        self.expect_text("Disabled", 5)
        return self

    def save_configuration(self):
        from screens.network_manager_tui import NetworkManagerTui
        self.logger.info("Saving configuration and going back to network manager TUI")
        self.capture_screen("EditConnection")
        self.press_tab(times=5)
        self.press_enter()
        self.press_esc()
        return NetworkManagerTui(self.session)

    def add_ipv4_configuration(self, ip_address: str, gateway_address: str, dns_address: str):
        return (self.change_ipv4_to_manual()
                .expand_ipv4_configuration()
                .type_ipv4_address(ip_address)
                .type_gateway_address(gateway_address)
                .type_dns_address(dns_address)
                .disable_ipv6_configuration()
                .save_configuration())