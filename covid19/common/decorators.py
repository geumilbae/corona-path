import time
from selenium.common.exceptions import WebDriverException
from common.log import LoggerFactory


MAX_WAIT = 10


LOGGER = LoggerFactory(name=__name__).logger


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                LOGGER.error(f"Error: {e}")
                if time.time() - start_time > MAX_WAIT:
                    LOGGER.error(f"Timeout, raise Error: {e}")
                    raise e
                time.sleep(1)
    return modified_fn
