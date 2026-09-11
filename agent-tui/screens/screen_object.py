import re
import sys
import time
from pathlib import Path
import pyte

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

    def expect_text_capture(self, text: str, timeout: int = 10):
        self.logger.info(f"Expecting: '{text}' (timeout={timeout}s)")
        try:
            self.session.expect(text, timeout=timeout)
            before = self.session.before
            match = self.session.match
            if isinstance(before, bytes):
                before = before.decode("utf-8", errors="ignore")
            match_text = match.group(0) if match else ""
            if isinstance(match_text, bytes):
                match_text = match_text.decode("utf-8", errors="ignore")
            self.logger.info(f"Found expected text: '{text}'")
            return before, match_text
        except Exception:
            self.logger.error(f"Text not found: '{text}'")
            return None, None

    def send(self, value: str, wait: int = 2):
        self.logger.info(f"Send: {value}")
        self.session.send(value)
        time.sleep(wait)

    def press_key_down(self, times: int = 1, wait: int = 2):
        for _ in range(times):
            self.logger.info("Pressing Key Down")
            self.send("\x1b[B")
            time.sleep(wait)

    def press_key_up(self, times: int = 1, wait: int = 2):
        for _ in range(times):
            self.logger.info("Pressing Key Up")
            self.send('\x1b[A')
            time.sleep(wait)

    def press_esc(self, times: int = 1, wait: int = 2):
        for _ in range(times):
            self.logger.info("Pressing Escape")
            self.send("\x1b")
            time.sleep(wait)

    def press_tab(self, times: int = 1, wait: int = 2):
        for _ in range(times):
            self.logger.info("Pressing Tab")
            self.send("\t")
            time.sleep(wait)

    def press_enter(self, times: int = 1, wait: int = 2):
        for _ in range(times):
            self.logger.info("Pressing Enter")
            self.send("\r")
            time.sleep(wait)

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

    def capture_screen(self, page_name: str):
        screen = pyte.Screen(80, 20)
        stream = pyte.Stream(screen)
        separator = "=" * 80
        data = self.session.before

        if isinstance(data, bytes):
            data = data.decode("utf-8", errors="replace")

        stream.feed(data)

        with Path(self.logger.handlers[0].baseFilename).open("a", encoding="utf-8") as f:
            f.write("\n\n")
            f.write(separator + "\n")
            f.write(f"PAGE: {page_name}\n")
            f.write(separator + "\n")

            for line in screen.display:
                f.write(line.rstrip() + "\n")
            f.write(separator + "\n")

        return screen