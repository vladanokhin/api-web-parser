

def api_result(request_function):
    def wrapper(*args, **kwargs):
        # try:
        result = request_function(*args, **kwargs)

        if result is None:
            return {'status': 'error', 'message': 'Undefined result'}
        elif result.success:
            return {'status': 'success', 'result': result.content}
        else:
            return {'status': 'error', 'message': result.error}
        # except Exception as error:
        #     return {'status': 'error', 'message': 'Exception API request: ' + str(error)}

    return wrapper
