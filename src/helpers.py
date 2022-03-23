from functools import wraps


# Decorator: create json response for api
def api_result(function):
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


# Decorator: after using selenium browser closing him
def auto_close_browser(function):
    @wraps(function)
    def _close(self, *args, **kwargs):
        result = function(self, *args, **kwargs)
        if hasattr(self, "__close_browser"):
            self.__close_browser()
        return result
    return _close
