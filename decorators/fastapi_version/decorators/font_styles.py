
def make_bold(function):
    def decorator_function():
        return f'<b>{function()}</b>'
    return decorator_function


def make_emphasis(function):
    def decorator_function():
        return f'<em>{function()}</em>'
    return decorator_function


def make_underlined(function):
    def decorator_function():
        return f'<u>{function()}</u>'
    return decorator_function
