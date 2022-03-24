import re

from functools import wraps
from hashlib import blake2b
from pathlib import Path
from urllib.parse import urlparse


def api_result(function):
    """
    Decorator: create json response for api
    """
    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)

            if result is None:
                return {'status': 'error', 'message': 'Undefined result'}
            elif result.success:
                return {'status': 'success', 'result': result.content}
            else:
                return {'status': 'error', 'message': result.error}
        except Exception as error:
            return {'status': 'error', 'message': '[API] ' + str(error)}

    return wrapper


def auto_close_browser(function):
    """
    Decorator: after using selenium browser closing him
    """
    @wraps(function)
    def _close(self, *args, **kwargs):
        result = function(self, *args, **kwargs)
        if hasattr(self, "__close_browser"):
            self.__close_browser()
        return result
    return _close


def create_file_name(url: str, file_ext: str = 'xml') -> str:
    """
    Create file name from url
    :param url: link to website
    :param file_ext: file extension, default 'xml'
    :return: new string of file name
    """
    _hex = blake2b(digest_size=8)
    _hex.update(url.encode())
    url_hex = _hex.hexdigest()

    if '://' not in url and not url.startswith('/'):
        url = '//' + url  # adding "//" to correctly parse url using method: urlparse()

    url = re.sub(r'^http\w?|[\W_]+', '', url)  # Remove all characters except letters and numbers
    url = urlparse(url, allow_fragments=False)

    return f'{url.netloc}{url.path}-{url_hex}.{file_ext}'


def create_dirs(*dirs: str) -> None:
    """
    Creating dir if this not exists
    :param dirs: path to dir
    """
    for directory in dirs:
        if not Path(directory).exists():
            Path(directory).mkdir()
