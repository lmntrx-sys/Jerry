class JLXRuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.tokn = token
