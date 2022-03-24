

class ParserConfig:

    # XML_OUTPUT = True

    OUTPUT_FORMAT = 'xml'

    INCLUDE_COMMENTS = False

    INCLUDE_TABLES = False

    DEDUPLICATE = True

    REQUEST_TIMEOUT = 15  # of seconds

    METHOD_OF_PARSE = ('request', 'selenium')  # first value always default

    PROXY = {
        "host": "50.250.75.153",
        "port": "39593"
        # "username": "",
        # "password": ""
    }

    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'

    TEMP_DIR_XML = 'xml/'

    TEMP_DIR_MD = 'md/'
