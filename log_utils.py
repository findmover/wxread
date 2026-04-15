import logging
import sys


def setup_logging(width=120):
    active = False

    def clear():
        nonlocal active
        if not active:
            return
        print("\r" + " " * width + "\r", end="", flush=True)
        active = False

    def refresh_print(message):
        nonlocal active
        active = True
        print(f"\r{message:<{width}}", end="", flush=True)

    class RefreshSafeHandler(logging.Handler):
        def emit(self, record):
            clear()
            message = self.format(record)
            stream = sys.stderr if record.levelno >= logging.WARNING else sys.stdout
            stream.write(message + "\n")
            stream.flush()

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(logging.INFO)

    handler = RefreshSafeHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)-8s - %(message)s"))
    root_logger.addHandler(handler)
    return refresh_print
