from core.logger import log_page_activity
from screens.login_screen import LoginScreen
from screens.screen_object import ScreenObject


@log_page_activity
class WarningScreen(ScreenObject):
    def confirm_warning(self):
        if not self.expect_text("Warning: the specified rendezvous IP was not found", 5):
            self.fail("Warning dialogue missing")
        self.press_enter()
        return LoginScreen(self.session)
