import functools
import logging
import os


def get_logger(name="assisted_ui"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        fh = logging.FileHandler("/tmp/assisted_ui.log")
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(fh)

    return logger


def log_page_activity(cls):
    """Class decorator to log entry and wrap all public methods."""
    original_init = cls.__init__
    screenshot_dir = "/tmp/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)

    def new_init(self, *args, **kwargs):
        self.logger = getattr(self, "logger", None)
        if not self.logger:
            self.logger = get_logger()
        self.logger.info(f"Entered page: {cls.__name__}")
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init

    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and not attr_name.startswith("__"):
            @functools.wraps(attr_value)
            def method_wrapper(self, *args, _method=attr_value, **kwargs):
                try:
                    self.logger.info(f"Executing {_method.__name__}")
                    return _method(self, *args, **kwargs)
                except Exception as e:
                    self.logger.error(f"{_method.__name__} failed: {e}")
                    if self.__class__.__name__ == "ClusterDetails":
                        textbox = self.page.get_by_role("textbox", name="Pull secret")
                        textbox.fill("REDACTED")
                    screenshot_name = f"{cls.__name__}_{_method.__name__}.png"
                    self.page.screenshot(path=f"{screenshot_dir}/{screenshot_name}")
                    raise

            setattr(cls, attr_name, method_wrapper)

    return cls
