import os

from pathlib import Path
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.proxy import Proxy, ProxyType
from typing import Union, Dict, Optional

from src.helpers import auto_close_browser
from ..proxy_parser import ProxyParser


class SeleniumParser(ProxyParser):

    def __init__(self,  proxy: Union[Dict[str, str], str, None], timeout: Optional[int]):
        super().__init__(proxy)

        self.browser: Firefox = None
        self.browser_options = [
            '--headless',
            '--disable-gpu',
            '--no-sandbox'
        ]
        self.timeout = timeout
        self.__path_to_driver = Path(Path.cwd(), 'src/parser/selenium_parser/webdriver/geckodriver')
        self.__started = False

        self.__setup_and_start()


    def __setup_and_start(self) -> None:
        """
        Initialize options and startup browser
        :return: None
        """
        # init options
        browser_options = FirefoxOptions()
        for option in self.browser_options:
            browser_options.add_argument(option)

        # if need use proxy
        proxy = None
        if self._use_proxy:
            proxy_str = self.get_one_line()
            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': proxy_str,
                'ftpProxy': proxy_str,
                'sslProxy': proxy_str,
                # 'noProxy': ''
            })
        # start browser
        self.browser = Firefox(executable_path=self.__path_to_driver,
                               options=browser_options,
                               service_log_path=os.devnull,
                               proxy=proxy)

        self.browser.set_page_load_timeout(self.timeout)
        self.__started = True

    def __close_browser(self) -> None:
        """
        Close started browser
        :return: None
        """
        self.browser.close()
        self.__started = False

    @auto_close_browser
    def get_html(self, url: str) -> str:
        """
        Parse website and return html
        :param url: website
        :return: html source
        """
        if not self.__started:
            self.__setup_and_start()

        self.browser.get(url)
        html = self.browser.page_source

        return html or ''
