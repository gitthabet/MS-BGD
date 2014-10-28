class JSONError(StandardError):
    pass

class JSONDecodeError(JSONError):
    pass

class JSONEncodeError(JSONError):
    pass
