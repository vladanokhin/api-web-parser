import trafilatura

from functools import wraps
from typing import Tuple, Any

from src.class_result import BaseResult
from configs import AppConfig


def api_result(function):
    """
    Decorator: create json response for api requests
    """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        try:
            result = function(self, *args, **kwargs)
            if result is None:
                return {'status': 'error', 'message': 'Undefined result'}

            if isinstance(result, BaseResult):
                if result.success:
                    return {'status': 'success', 'result': result.content}
                elif not result.content:
                    return {'status': 'error', 'message': 'No content found on the page'}
                else:
                    return {'status': 'error', 'message': result.error}
        except Exception as error:
            return {'status': 'error', 'message': f'[{self.__class__.__name__}] ' + str(error)}

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


def extract_content_from_html(content: str, with_metadata: bool) -> Tuple[Any, str]:
    """
    Extract content from html text
    :param content: html text
    :param with_metadata: is it also necessary to extract metadata
    :return: Tuple with metadata and content
    """
    cfg = AppConfig()
    metadata = None

    content = trafilatura.extract(
        filecontent=content,
        output_format=cfg.OUTPUT_FORMAT,
        include_comments=cfg.INCLUDE_COMMENTS,
        include_tables=cfg.INCLUDE_TABLES,
        deduplicate=cfg.DEDUPLICATE,
    )

    if with_metadata:
        metadata = trafilatura.metadata.extract_metadata(filecontent=content)

    return metadata, content
