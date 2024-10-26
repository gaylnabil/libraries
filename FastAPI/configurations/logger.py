import  logging
import sys

# class LibraryLogger(logging.Logger):
#     def __init__(self, name: str):
#         super().__init__(name)
#     def log(self, level, msg, *args, exc_info = None, stack_info = True, stacklevel = 2, extra = None):
#         super().log(level, msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
#
#     def debug(self, msg, *args, exc_info = None, stack_info = True, stacklevel = 2, extra = None):
#         super().debug(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
#     def info(self, msg, *args, exc_info = None, stack_info = False, stacklevel = 2, extra = None):
#         super().info(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
#
#     def warning(self, msg, *args, exc_info = None, stack_info = False, stacklevel = 2, extra = None):
#         super().warning(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
#
#     def error(self, msg, *args, exc_info = None, stack_info = False, stacklevel = 2, extra = None):
#         super().error(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)
#
#     def critical(self, msg, *args, exc_info = None, stack_info = False, stacklevel = 2, extra = None):
#         super().critical(msg, *args, exc_info=exc_info, stack_info=stack_info, stacklevel=stacklevel, extra=extra)


# logging.setLoggerClass(LibraryLogger)
logger = logging.getLogger(__name__)
# custom formatter
formatter = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s - %(funcName)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
# create handlers
file_handler = logging.FileHandler('logs/app.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# create stream handlers
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)
# logger.handlers = [stream_handler, file_handler]