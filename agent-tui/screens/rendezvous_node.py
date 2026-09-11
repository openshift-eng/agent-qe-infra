from core.logger import log_page_activity
from screens.ip_selection import RendezvousNodeIpSelectionScreen
from screens.login_screen import LoginScreen
from screens.screen_object import ScreenObject
from screens.warning_screen import WarningScreen
from screens.network_manager_tui import NetworkManagerTui


@log_page_activity
class RendezvousNodeSetupScreen(ScreenObject):
    def __init__(self, session):
        super().__init__(session)
        if not self.expect_text("Rendezvous IP", timeout= 15 * 60):
            self.fail("Rendezvous node setup screen is not present")
            self.press_esc()

    def _enter_ip(self, ip):
        self.send(ip)
        return self

    def rendezvous_node(self):
        self.press_tab(times=2)
        self.press_enter()
        return RendezvousNodeIpSelectionScreen(self.session)

    def non_rendezvous_node(self, ip):
        self._enter_ip(ip)
        self.press_enter(times=2)
        success_msg = f"Successfully saved"
        if not self.expect_text(success_msg):
            return WarningScreen(self.session).confirm_warning()
        else:
            self.press_enter()
        return LoginScreen(self.session)

    def configure_network(self):
        self.press_tab(times=3)
        self.press_enter()
        return NetworkManagerTui(self.session)