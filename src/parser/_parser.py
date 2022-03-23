import trafilatura
import requests

from requests import Timeout, RequestException
from requests.auth import HTTPProxyAuth
from typing import Tuple, Optional

from configs.app import AppConfig
from .parser_result import ParserResult
from .proxy_parser import ProxyParser
from .selenium_parser import SeleniumParser


class Parser(ProxyParser):

    def __init__(self, url: str, timeout: Optional[int], method_parse: str, **kwargs) -> None:
        self.cfg = AppConfig()

        self.url = url
        self.timeout = timeout or self.cfg.REQUEST_TIMEOUT
        self.method_parse = method_parse

        self.headers = {'user-agent': self.cfg.USER_AGENT}

        super().__init__(**kwargs)

    def parse(self) -> ParserResult:
        if self.method_parse == 'request':
            return self.__extract_content(self.__parse_from_request)
        elif self.method_parse == 'selenium':
            return self.__extract_content(self.__parse_from_selenium)

    def __extract_content(self, extract_method) -> ParserResult:
        result = ParserResult()
        is_success, content = extract_method()

        if not is_success:
            result.error = content
            return result

        try:
            result.content = trafilatura.extract(
                filecontent=content,
                # xml_output=self.cfg.XML_OUTPUT,
                output_format=self.cfg.OUTPUT_FORMAT,
                include_comments=self.cfg.INCLUDE_COMMENTS,
                include_tables=self.cfg.INCLUDE_TABLES,
                deduplicate=self.cfg.DEDUPLICATE,
            )
            result.metadata = trafilatura.metadata.extract_metadata(filecontent=content, default_url=self.url)
        except Exception as err:
            result.error = str(err)
        else:
            result.success = True

        if not result.content:
            result.success = False

        return result

    def __parse_from_request(self) -> Tuple[bool, str]:
        """
        Getting html from request
        :return: tuple with status code and result
        """
        try:
            # USAGE PROXY
            if self._use_proxy and self._is_valid_proxy:
                # create session
                with requests.Session() as session:
                    session.proxies = {
                       'http': f"http://{self.proxy['host']}:{self.proxy['port']}",
                       'https': f"https://{self.proxy['host']}:{self.proxy['port']}"
                    }

                    if self._with_auth:
                        session.auth = HTTPProxyAuth(self.proxy['username'], self.proxy['password'])

                    response = session.get(url=self.url, headers=self.headers, timeout=self.timeout)

            # IF PROXY INVALID
            elif self._use_proxy and not self._is_valid_proxy:
                return False, 'Proxy is not valid'
            # WITHOUT PROXY
            else:
                response = requests.get(url=self.url, headers=self.headers, timeout=self.timeout)
        except (ConnectionError, RequestException, Timeout) as error:
            return False, '[Request] ' + str(error)

        # check response
        if response.status_code == requests.codes.OK:
            return True, response.text
        else:
            return False, str(response.status_code)

    def __parse_from_selenium(self) -> Tuple[bool, str]:
        """
        Getting html from request
        :return: tuple with status code and result
        """
        selenium_parser = SeleniumParser(proxy=self.proxy, timeout=self.timeout)
        try:
            return True, selenium_parser.get_html(self.url)
        except Exception as error:
            return False, '[Selenium] ' + str(error)
