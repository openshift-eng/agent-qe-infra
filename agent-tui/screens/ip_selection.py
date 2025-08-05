from core.logger import log_page_activity
from screens.login_screen import LoginScreen
from screens.screen_object import ScreenObject


@log_page_activity
class RendezvousNodeIpSelectionScreen(ScreenObject):
    def select_ip(self):
        if not self.expect_text("Rendezvous node IP selection"):
            self.fail("IP Selection prompt missing")
        self.press_enter()
        success_msg = f"Successfully saved"
        if not self.expect_text(success_msg):
            self.fail(f"Did not find success message: {success_msg}")
        self.press_enter()
        return LoginScreen(self.session)
