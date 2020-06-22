import os
import sys
from selenium import webdriver as wd
from common.log import LoggerFactory

APP_DIR = os.path.dirname(os.path.dirname(__file__))

LOGGER = LoggerFactory(name=__name__).logger


def _construct_init_headers(platform: str) -> dict:
    init_headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': ('text/html,application/xhtml+xml,' +
                   'application/xml;q=0.9,image/webp,' +
                   'image/apng,*/*;q=0.8'),
        'Accept-Language': 'ko,ja;q=0.9,en;q=0.8',
        'Host': '',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': '',
        'Content-Type': '',
        'Referer': '',
    }
    if platform == 'win32':
        init_headers['User-Agent'] = \
            ('Mozilla/5.0 (Windows NT 10.0; Win64;' +
             'x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
             'Chrome/71.0.3578.98 Safari/537.36')
    elif platform == 'darwin':
        init_headers['User-Agent'] = \
            ('Mozilla/5.0 (Macintosh;' +
             'Intel Mac OS X 10_13_6) AppleWebKit/537.36 ' +
             '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    elif platform == 'linux':
        init_headers['User-Agent'] = \
            ('Mozilla/5.0 (X11; Linux x86_64) ' +
             'AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/16.04 ' +
             'Chromium 73.0.3683.68 Chrome/73.0.3683.68 Safari/534.30')
    else:
        pass
    return init_headers


def _construct_webdriver_path(platform: str) -> str:
    if platform == 'win32':
        webdriver_name = 'chromedriver_win.exe'
    elif platform == 'darwin':
        webdriver_name = 'chromedriver_mac'
    elif platform == 'linux':
        webdriver_name = 'chromedriver_linux'
    else:
        webdriver_name = 'chromedriver_linux'
    webdriver_path = os.path.join(APP_DIR,
                                  'webdrivers/chromedrivers', webdriver_name)
    LOGGER.info(f"webdriver_path: { webdriver_path }")
    return webdriver_path


def _construct_webdriver(platform: str, headless: bool = False):
    if headless:
        chrome_options = wd.ChromeOptions()
        chrome_options.add_argument('--headless')
        webdriver = wd.Chrome(
            options=chrome_options,
            executable_path=_construct_webdriver_path(platform)
        )
    else:
        webdriver = wd.Chrome(
            executable_path=_construct_webdriver_path(platform))
    return webdriver


def try_finding_element_by_xpath(selenium_input, xpath: str):
    """셀레늄 웹엘리먼트나 웹드라이버를 받아서 해당 xpath 에서 엘리먼트를 찾을 수 있는지 확인하기
    위해 try-except 구문을 추가한 보조 메소드.

    Args:
        selenium_input: 셀레늄 웹드라이버 또는 웹엘리먼트.
        (selenium.webdriver.remote.webelement.WebEelement)
        (selenium.webdriver.remote.webdriver.WebDriver)
        xpath (str): 엘리먼트 내에 존재하리라 생각되는 아이템의 xpath.

    Returns:
        selenium_output: 셀레늄 웹엘리먼트 또는 None.
    """
    try:
        selenium_output = selenium_input.find_element_by_xpath(xpath=xpath)
    except Exception as e:
        LOGGER.exception(f"Error: { e }")
        raise e
    return selenium_output


def try_finding_elements_by_xpath(selenium_input, xpath: str):
    """셀레늄 웹엘리먼트나 웹드라이버를 받아서 해당 xpath 에서 엘리먼트들을 찾을 수 있는지 확인하기
    위해 try-except 구문을 추가한 보조 메소드.

    Args:
        selenium_input: 셀레늄 웹드라이버 또는 웹엘리먼트.
        (selenium.webdriver.remote.webelement.WebEelement)
        (selenium.webdriver.remote.webdriver.WebDriver)
        xpath (str): 엘리먼트 내에 존재하리라 생각되는 아이템의 xpath.

    Returns:
        list_selenium_output (list): 셀레늄 웹엘리먼트들을 담고 있는 리스트 또는 None.
    """
    try:
        list_selenium_output = \
            selenium_input.find_elements_by_xpath(xpath=xpath)
    except Exception as e:
        LOGGER.exception(f"Error: { e }")
        raise e
    return list_selenium_output


class WebdriverFactory:
    def __init__(self, headless: bool = False):
        self._platform = sys.platform  # win32, darwin, linux 중 하나
        self._headers = _construct_init_headers(platform=self._platform)
        self._webdriver = _construct_webdriver(platform=self._platform,
                                               headless=headless)

    @property
    def webdriver(self):
        return self._webdriver

    def close(self):
        self._webdriver.close()

