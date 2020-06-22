import pytest

from common.log import LoggerFactory
from path.pkg.crawler import SeleniumCrawler, Bucheon


LOGGER = LoggerFactory(name=__name__).logger


class TestUnitCrawler:

    @classmethod
    def setup_class(cls):
        cls.crawler = SeleniumCrawler(headless=False)

    @classmethod
    def teardown_class(cls):
        cls.crawler.close()

    def test_bucheon_get_path_data(self):
        bucheon = Bucheon()
        df = bucheon.get_path_data(self.crawler)
        LOGGER.info(f"df: {df}")
        assert df.shape == (0, 0)

