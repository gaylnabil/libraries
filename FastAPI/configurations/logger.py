import sys
import logging
from logging.handlers import RotatingFileHandler


class LibraryLogger:
    def __init__(self, name: str):
        # logging.setLoggerClass(LibraryLogger)
        self.logger = logging.getLogger(name)
        filename = 'logs/app.log'
        # custom formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s - %(func_name)s: %(message)s, Line:%(lineno)d',
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # create handlers
        # file_handler = logging.FileHandler(filename)
        # file_handler.setFormatter(formatter)
        # self.logger.addHandler(file_handler)

        # create rotating file handler
        rotating_file_handler = RotatingFileHandler(
            filename=filename,
            mode='a',
            maxBytes=1024,
            backupCount=1,
            encoding='utf-8',
            delay=False
        )
        rotating_file_handler.setFormatter(formatter)
        self.logger.addHandler(rotating_file_handler)
        # create stream handlers
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.INFO)
        # logger.handlers = [stream_handler, file_handler]
    def log(self, level, msg, *args, exc_info = None, stack_info = True, stack_level = 2, func_name = None, extra = None):
        extra = {'func_name': func_name} if extra is None else {'func_name': func_name, **extra}
        self.logger.log(level, msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stack_level, extra=extra)

    def debug(self, msg, *args, exc_info = None, stack_info = True, stack_level = 2, func_name = None, extra = None):
        extra = {'func_name': func_name} if extra is None else {'func_name': func_name, **extra}
        self.logger.debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stack_level, extra=extra)
    def info(self, msg, *args, exc_info = None, stack_info = False, stack_level = 2, func_name = __name__, extra = None):
        extra = {'func_name': func_name} if extra is None else {'func_name': func_name, **extra}
        self.logger.info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stack_level, extra=extra)

    def warning(self, msg, *args, exc_info = None, stack_info = False, stack_level = 2, func_name = __name__, extra = None):
        extra = {'func_name': func_name} if extra is None else {'func_name': func_name, **extra}
        self.logger.warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stack_level, extra=extra)

    def error(self, msg, *args, exc_info = None, stack_info = False, stack_level = 2, func_name = None, extra = None):
        extra = {'func_name': func_name} if extra is None else {'func_name': func_name, **extra}
        self.logger.error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stack_level, extra=extra)

    def critical(self, msg, *args, exc_info = None, stack_info = False, stack_level = 2, func_name = None, extra = None):
        extra = {'func_name': func_name} if extra is None else {'func_name': func_name, **extra}
        self.logger.critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stack_level, extra=extra)

logger = LibraryLogger(__name__)