import json
from typing import Union, Dict

from configs.app import AppConfig


class ProxyParser:
    """
    class for initialize and checking proxy
    """
    def __init__(self, proxy: Union[Dict[str, str], str]):
        self.cfg = AppConfig()
        self.proxy = proxy or None

        self._use_proxy = False
        self._is_valid_proxy = False
        self._with_auth = False

        self.__init_proxy()

    def __init_proxy(self) -> None:
        """
        Initialize proxy and determines
        use proxy or not
        :return: None
        """
        if self.proxy is None:
            return None

        if self.proxy == 'default':
            self.proxy = self.cfg.PROXY

        self._use_proxy = True
        self.__check_proxy(self.proxy)

    def __check_proxy(self, proxy: Union[Dict[str, str], str]) -> bool:
        """
        Check syntax proxy
        :param proxy: Dict of proxy for check
        :return: bool
        """
        # convert proxy from str to dict
        if isinstance(proxy, str):
            proxy = json.loads(proxy.replace("'", "\""))
            self.proxy = proxy

        set_keys = set(proxy.keys())
        if {'username', 'password'}.issubset(set_keys):
            available_keys = ('host', 'port', 'username', 'password')
        else:
            available_keys = ('host', 'port')

        # check that have all the required keys
        if not set(available_keys).issubset(set_keys):
            return False

        # check length all values
        for value in proxy.values():
            length_val = len(value)
            if length_val <= 1 or length_val > 100:
                return False

        if 'http' in proxy['host']:
            rm_elements = ['http', 'https', '://', ':', '/']
            for el in rm_elements:
                proxy['host'] = proxy['host'].replace(el, '')

        self._is_valid_proxy = True

        return True
