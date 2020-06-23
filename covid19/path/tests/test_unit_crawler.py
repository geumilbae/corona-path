import pytest

from common.log import LoggerFactory
from path.pkg.crawler import SeleniumCrawler, Bucheon, Seoul


LOGGER = LoggerFactory(name=__name__).logger


class TestUnitCrawler:

    @classmethod
    def setup_class(cls):
        cls.crawler = SeleniumCrawler(headless=False)

    @classmethod
    def teardown_class(cls):
        cls.crawler.close()

    @pytest.mark.skip(reason="tested")
    def test_bucheon_get_path_data(self):
        bucheon = Bucheon()
        df = bucheon.get_path_data(self.crawler)
        LOGGER.info(f"df: {df}")
        assert df.shape == (26, 3)

    @pytest.mark.skip(reason="tested")
    def test_seoul_get_path_data(self):
        seoul = Seoul()
        df = seoul.get_path_data(self.crawler)
        LOGGER.info(f"df: {df}")
        assert df.shape == (1230, 6)
