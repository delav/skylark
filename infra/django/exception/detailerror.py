

class DetailError(object):
    """
    Custom error detail, help for the custom global exception handler
    """
    def __init__(self, data, default_code=10000):
        self.text = data
        self.code = default_code
