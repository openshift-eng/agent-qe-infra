import re

from core.logger import log_page_activity
from screens.screen_object import ScreenObject
from screens.edit_connection import EditConnection

@log_page_activity
class NetworkManagerTui(ScreenObject):
    def __init__(self, session):
        super().__init__(session)
        if not self.expect_text("NetworkManager", 2):
            self.fail("Network Manager TUI screen is not present")

    def set_hostname(self, hostname: str):
        self.press_key_down(times=2)
        self.press_enter()
        self.send(hostname)
        self.press_key_down(times=2)
        self.press_enter(wait=3)
        self.press_enter(wait=3)
        self.press_key_up(times=2)
        return self

    def click_edit_a_connection(self):
        self.press_enter()
        self.press_enter()
        return EditConnection(self.session)

    def click_activate_a_connection(self, interface: str):
        self.press_key_down()
        self.press_enter()
        before, match = self.expect_text_capture(fr"Ethernet \(({interface})\)")
        screen_text = before + match

        if match:
            interfaces = re.findall(r'Ethernet \(([^)]+)\)',screen_text)
            self.logger.info(f"Ethernet list {interfaces}")

            if interface in interfaces:
                position = interfaces.index(interface)
                for _ in range(position):
                    self.press_key_down(times=position)
                    self.press_enter(wait=5)
                self.press_esc()
        return self

    def go_back_to_rendezvous_node_setup_screen(self):
        self.press_esc()
        self.press_esc()
        self.press_tab()
        return self