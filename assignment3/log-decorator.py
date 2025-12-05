# Task 1

import logging
# from functools import wraps

logging.basicConfig(level=logging.DEBUG)
# logging.debug(), logging.info(), logging.warning(), and logging.error()

logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)
logger.addHandler(logging.FileHandler("./decorator.log","a"))

logger.log(logging.INFO, "This is the start of the log")

def logger_decorator(func):
    # @wraps(func)
    def wrapper(*args, **kwargs):
        logger.log(logging.INFO, f"The function name is {func.__name__}")
        if args or kwargs:
            if args:
                logger.log(logging.INFO, f"This function's positional parameters are {args}")
            if kwargs:
                logger.log(logging.INFO, f"This function's keyword parameters are {kwargs}")
        else:
            logger.log(logging.INFO, "This function takes no parameters")
        result = func()
        if result is None:
            logger.log(logging.INFO, "This function has no return value")
        else:
            logger.log(logging.INFO, f"This function returns {func()}")
    return wrapper

@logger_decorator
def hello():
    print("Hello World")
    
@logger_decorator
def positional_args(*args):
    if args:
        return True
    
@logger_decorator
def keyword_args(**kwargs):
    return logger_decorator

hello()
positional_args(1, "hello", 3.14)
keyword_args(first="1st", second="2nd", last="last")

logger.log(logging.INFO, "This is the end of the log\n")