"""
================================================================================
:mod: `path.pkg.crawler` 확진자 동선 크롤러 모듈
================================================================================
.. moduleauthor:: 배금일 <geumil.bae@lanoir42.org>
.. note:: Copyright (c) 2020, Geumil Bae

설명
====
이 모듈은 아래 기능을 수행합니다.
    1. 각 시/도별로 흩어져 있는 확진자 동선 데이터를 셀레늄 웹드라이버로 검색해서 수집합니다.

이 기능들은 path.pkg.uploader 에서 활용됩니다.

참고
====

관련 작업자
=========
* 배금일 <geumil.bae@lanoir42.org>

작업일지
=========
* [2020/06/22] - 크롤러 작성 시작. TDD의 원칙을 준수할 것을 다짐하였습니다.
"""
import os
import pandas as pd
import re
import time
import urllib.parse

from bs4 import BeautifulSoup
from common.decorators import wait
from common.log import LoggerFactory
from common.webdriver import (
    WebdriverFactory,
    try_finding_element_by_xpath, try_finding_elements_by_xpath
)
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser as dateparser
from django.utils import timezone
from selenium.webdriver.common.keys import Keys


APP_DIR = os.path.dirname(os.path.dirname(__file__))
"""GLOBAL APP_DIR: 모듈파일 위치를 기준으로 path 디렉토리를 찾아놓았습니다."""

LOGGER = LoggerFactory(name=__name__).logger
"""GLOBAL LOGGER: 모듈에서 일어나는 일들을 모니터링하고 디버깅 하기 위한 로거입니다."""


class SeleniumCrawler:
    """이 클래스는 셀레늄을 기반으로 작동하는 확진자 동선 크롤러를 구현합니다."""

    def __init__(self, headless: bool = False):
        """SeleniumCrawler 클래스 생성자입니다.

        :param headless: 크롤링을 할 때 브라우저를 백그라운드에서 구동할 것인지 결정합니다.
        """
        self._webdriver = WebdriverFactory(headless).webdriver

    def close(self):
        """SeleniumCrawler 객체 생성 시 실행되는 webdriver를 닫는 메소드입니다."""
        self._webdriver.close()
        self._webdriver.quit()

    @property
    def webdriver(self):
        return self._webdriver

    @webdriver.setter
    def webdriver(self, headless: bool):
        """SeleniumCrawler 내 webdriver의 헤드리스 옵션을 바꿀 때 초기화하는 메소드입니다.

        :param headless: True 이면 렌더링하지 않고, False 면 렌더링 합니다 (default).
        :type headless: bool
        """
        if not self._webdriver:
            self._webdriver.close()
        self._webdriver = WebdriverFactory(headless).webdriver


class Bucheon:
    """이 클래스는 부천시의 확진자 동선 데이터를 크롤링합니다."""

    def __init__(self):
        self._home_url = "https://www.bucheon.go.kr/site/main/corona"

    @property
    def home_url(self):
        return self._home_url

    def get_path_data(self, crawler: SeleniumCrawler):
        crawler.webdriver.get(self.home_url)
        initial_script = "fn_search('148', '27434', '10000', '1', '');"
        crawler.webdriver.execute_script(initial_script)
        time.sleep(1)
        str_html = crawler.webdriver.page_source
        soup = BeautifulSoup(str_html, 'html5lib')
        soup_div = soup.find('div', {'id': 'qna_list27434'})
        list_soup_dl = soup_div.find_all('dl')
        list_s_row = []
        for soup_dl in list_soup_dl:
            s_row = pd.Series(dtype=object)
            soup_title = soup_dl.find('dt').find('button').find('span')
            s_row['summary'] = soup_title.find('strong').text
            s_row['confirmation_date'] = soup_title.find('em').text
            soup_text = soup_dl.find('dd')
            s_row['routes'] = soup_text.text
            list_s_row.append(s_row)

        df = pd.concat(
            [s_row.to_frame().T for s_row in list_s_row], ignore_index=True
        )
        return df


class Seoul:
    """이 클래스는 서울시의 확진자 동선 데이터를 크롤링합니다."""

    def __init__(self):
        self._home_url = "https://www.seoul.go.kr/coronaV/coronaStatus.do"

    @property
    def home_url(self):
        return self._home_url

    def get_path_data(self, crawler: SeleniumCrawler):
        crawler.webdriver.get(self.home_url)
        time.sleep(1)
        xpath_list_btn = "//div[@class='move-tab']/ul/li/" + \
                         "button[@data-url='#move-cont2']"
        e_btn = try_finding_element_by_xpath(
            crawler.webdriver, xpath=xpath_list_btn
        )
        time.sleep(1)
        str_html = crawler.webdriver.page_source
        data_length = crawler.webdriver.execute_script(
            "return route_table.data().length"
        )
        data_length = int(data_length)
        list_row = []
        for i in range(data_length):
            row = crawler.webdriver.execute_script(
                f"return route_table.data()[{i}];"
            )
            LOGGER.debug(f"type of row: {type(row)}")
            LOGGER.debug(f"contents of row: {row}")


        route_table = crawler.webdriver.execute_script("return route_table.data()[0];")
        LOGGER.info(route_table)
        df = self._parse_table(str_html)
        LOGGER.debug(f"table: {df}")

    def _parse_table(self, html):
        soup = BeautifulSoup(html, 'html5lib')
        soup_div = soup.find('div', {'id': 'move-cont2'})
        soup_table = soup_div.find('table', {'id': 'DataTables_Table_0'})
        soup_body = soup_table.find('tbody')
        list_soup_tr = soup_body.find_all('tr', {'id': 'patient'})
        list_soup_td = soup_body.find_all('td', {'class': 'tdl'})
        list_s_row = []
        for soup_tr, soup_td in zip(list_soup_tr, list_soup_td):
            s_row = pd.Series(dtype=object)
            list_soup_td = soup_tr.find_all('td')
            s_row['no'] = list_soup_td[0].find('p').text
            s_row['patient_id'] = list_soup_td[1].text
            s_row['infection_route'] = list_soup_td[2].text
            s_row['confirmation_date'] = list_soup_td[3].text
            s_row['residence'] = list_soup_td[4].text
            s_row['containment_facility'] = list_soup_td[5].text
            s_row['routes'] = soup_td.text.strip()
            list_s_row.append(s_row)
        df = pd.concat([s_row.to_frame().T for s_row in list_s_row],
                       ignore_index=True)
        return df
