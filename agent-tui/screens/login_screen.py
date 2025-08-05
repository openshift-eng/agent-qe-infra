from core.logger import log_page_activity
from screens.screen_object import ScreenObject


@log_page_activity
class LoginScreen(ScreenObject):
    def verify_rendezvous_node_info(self, expected_text):
        if not self.expect_text(expected_text, 500):
            self.fail("Login screen is not present")
        return self

    def verify_assisted_ui_url_info(self, expected_text):
        return self.wait_for_ui_text(expected_text, 600)
