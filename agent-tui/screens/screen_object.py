import re
import sys
import time

from core.logger import get_logger


class ScreenObject:
    def __init__(self, session):
        self.session = session
        self.logger = get_logger()

    def expect_text(self, text: str, timeout: int = 10):
        self.logger.info(f"Expecting: '{text}' (timeout={timeout}s)")
        try:
            self.session.expect(text, timeout=timeout)
            self.logger.info(f"Found expected text: '{text}'")
            return True
        except Exception:
            self.logger.error(f"Text not found: '{text}'")
            return False

    def send(self, value: str, wait: int = 2):
        self.logger.info(f"Send: {value}")
        self.session.send(value)
        time.sleep(wait)

    def press_tab(self, times: int = 1):
        for _ in range(times):
            self.logger.info("Pressing Tab")
            self.send("\t")

    def press_enter(self, times: int = 1):
        for _ in range(times):
            self.logger.info("Pressing Enter")
            self.send("\r")

    def fail(self, message: str):
        self.logger.error(f"FAIL: {message}")
        if self.session:
            try:
                self.session.terminate(force=True)
            except Exception:
                self.logger.warning("Failed to deactivate session.")
            sys.exit(1)

    def wait_for_ui_text(self, expected_text: str, timeout_seconds: int = 600):
        ansi_escape = re.compile(rb'\x1B\[[0-9;]*[mK]')  # Remove ANSI color codes
        start_time = time.time()

        self.logger.info(f"Waiting for text (timeout: {timeout_seconds}s)")

        while time.time() - start_time < timeout_seconds:
            try:
                line = self.session.readline()
                cleaned_line = ansi_escape.sub(b'', line).decode(errors="ignore").strip()

                if expected_text in cleaned_line:
                    self.logger.info(f"Found expected text: '{expected_text}'")
                    return True

            except Exception:
                self.logger.error(f"Error reading serial output, trying again...")

        self.logger.error(f"Timeout exceeded. Text not found")
        return False
