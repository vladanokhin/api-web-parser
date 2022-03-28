import requests

from requests import Timeout, RequestException
from requests.auth import HTTPProxyAuth
from typing import Tuple, Optional, Union, Dict

from configs import AppConfig
from src.convertor import Convertor
from src.helpers import extract_content_from_html
from .parser_result import ParserResult
from .proxy_parser import ProxyParser
from .selenium_parser import SeleniumParser


class Parser(ProxyParser):
    """
    Parse web page
    """

    def __init__(self, url: str,
                 timeout: Optional[int],
                 method_parse: str,
                 with_metadata: bool,
                 auto_convert_to_md: bool,
                 proxy: Union[Dict[str, str], str]
                 ) -> None:

        self.cfg = AppConfig()
        self.url = url
        self.timeout = timeout or self.cfg.REQUEST_TIMEOUT
        self.method_parse = method_parse
        self.with_metadata = with_metadata
        self.auto_convert_to_md = auto_convert_to_md
        self.headers = {'user-agent': self.cfg.USER_AGENT}

        super().__init__(proxy)

    def parse(self) -> ParserResult:
        """
        Start parsing web page
        """
        if self.method_parse == 'request':
            return self.__extract_content(self.__parse_from_request)
        elif self.method_parse == 'selenium':
            return self.__extract_content(self.__parse_from_selenium)

    def __extract_content(self, extract_method) -> ParserResult:
        """
        Extract content from html to xml
        :param extract_method: method to get html
        :return: ParserResult
        """
        result = ParserResult()
        is_success, content = extract_method()

        if not is_success:
            result.error = content
            return result

        try:
            result.metadata, result.content = extract_content_from_html(content, self.with_metadata)
        except Exception:
            result.error = '[Extract] Cannot extract content from html'
        else:
            result.success = True

        if not result.content:
            result.success = False
        elif result.content and self.auto_convert_to_md:
            convertor = Convertor()
            result.content = convertor.convert(result.content)

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
        except (ConnectionError, RequestException, Timeout):
            return False, '[Request] Parsing web page error'

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
        except Exception:
            return False, '[Selenium] Parsing web page error'
