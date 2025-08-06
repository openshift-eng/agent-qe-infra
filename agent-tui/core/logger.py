import functools
import os
import logging

def get_logger(name="agent_tui", base_dir="/tmp", ext=".log"):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        count = 0
        while True:
            suffix = f"_{count}" if count > 0 else ""
            log_path = os.path.join(base_dir, f"{name}{suffix}{ext}")
            if not os.path.exists(log_path):
                break
            count += 1

        fh = logging.FileHandler(log_path)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(fh)

    return logger


def log_page_activity(cls):
    """Class decorator to log entry and wrap all public methods."""
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        self.logger = getattr(self, "logger", None)
        if not self.logger:
            self.logger = get_logger()
        self.logger.info(f"Entered screen: {cls.__name__}")
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
                    self.logger.error(f"{_method.__name__} failed")
                    raise

            setattr(cls, attr_name, method_wrapper)

    return cls
