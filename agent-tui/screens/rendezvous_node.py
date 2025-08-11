from core.logger import log_page_activity
from screens.ip_selection import RendezvousNodeIpSelectionScreen
from screens.login_screen import LoginScreen
from screens.screen_object import ScreenObject
from screens.warning_screen import WarningScreen


@log_page_activity
class RendezvousNodeSetupScreen(ScreenObject):
    def _enter_ip(self, ip):
        self.send(ip)
        return self

    def rendezvous_node(self):
        self.press_tab()
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
