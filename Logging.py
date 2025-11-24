import logging
import sys
import os
from logging.handlers import BaseRotatingHandler
from termcolor import colored
import functools
from datetime import datetime
import re
from constants import LOG_COLORS, LOG_ENABLE_TRUNCATION, LOG_MAX_REPR_LENGTH, LOG_MAX_ITEMS_TO_SHOW, LOG_TRUNCATE_MESSAGE

def SmartRepr(obj) -> str:
    if not LOG_ENABLE_TRUNCATION:
        try:
            return repr(obj)
        except ValueError:
            return f"<error in repr({type(obj).__name__})>"

    try:
        String = repr(obj)
        if len(String) <= LOG_MAX_REPR_LENGTH:
            return String
    except ValueError:
        return f"<unreprable {type(obj).__name__}>"

    ObjType = type(obj).__name__

    if hasattr(obj, '__len__'):
        try:
            length = len(obj)
            if length > LOG_MAX_ITEMS_TO_SHOW * 2:
                head = ", ".join(repr(obj[i]) for i in range(min(3, length)))
                tail = ", ".join(repr(obj[i]) for i in range(max(length-3, 0), length))
                preview = head + (", ..., " + tail if tail and head != tail else "")
                return f"<{ObjType} len={length} [{preview}, {LOG_TRUNCATE_MESSAGE}]>"
            else:
                return f"<{ObjType} len={length} [{', '.join(repr(x) for x in obj)}]>"
        except ValueError:
            pass

    if hasattr(obj, '__dict__') and not isinstance(obj, type):
        try:
            items = ", ".join(f"{k}={SmartRepr(v)}" for k, v in list(obj.__dict__.items())[:5])
            extra = ", ..." if len(obj.__dict__) > 5 else ""
            return f"<{ObjType} {{{items}{extra}}}>"
        except ValueError:
            pass

    return f"<{ObjType} {LOG_TRUNCATE_MESSAGE}>"

class CleanRotatingFileHandler(BaseRotatingHandler):
    def __init__(
        self,
        base_filename: str,
        maxBytes: int = 0,
        backupCount: int = 0,
        encoding = None
    ):
        self.base_filename = base_filename
        self.maxBytes = maxBytes
        self.backupCount = backupCount
        self.encoding = encoding
        super().__init__(base_filename, mode='a', encoding=encoding, delay=False)

    def ShouldRollover(self) -> bool:
        if self.maxBytes > 0:
            if not os.path.exists(self.base_filename):
                return True
            try:
                return os.path.getsize(self.base_filename) >= self.maxBytes
            except OSError:
                return True
        return False

    def GetNextFilename(self) -> str:
        NameDirectory, NameFile = os.path.split(self.base_filename)
        stem = os.path.splitext(NameFile)[0]
        pattern = re.compile(rf"{re.escape(stem)}_(\d{{3}})\.log$", re.IGNORECASE)
        existing = []

        if os.path.isdir(NameDirectory):
            try:
                for f in os.listdir(NameDirectory):
                    m = pattern.match(f)
                    if m:
                        try:
                            existing.append(int(m.group(1)))
                        except ValueError:
                            continue
            except FileNotFoundError:
                pass

        NextNum = max(existing) + 1 if existing else 1
        return os.path.join(NameDirectory, f"{stem}_{NextNum:03d}.log")

    def DoRollover(self):
        if self.stream:
            self.stream.flush()
            self.stream.close()

        if self.maxBytes > 0 and os.path.exists(self.base_filename):
            try:
                next_name = self.GetNextFilename()
                os.replace(self.base_filename, next_name)
            except OSError as e:
                logging.getLogger(__name__).error(f"Failed to rotate log: {e}")

        if self.backupCount > 0:
            NameDirectory = os.path.dirname(self.base_filename)
            stem = os.path.splitext(os.path.basename(self.base_filename))[0]
            pattern = re.compile(rf"{re.escape(stem)}_(\d{{3}})\.log$", re.IGNORECASE)
            backups = []

            if os.path.isdir(NameDirectory):
                try:
                    for f in os.listdir(NameDirectory):
                        m = pattern.match(f)
                        if m:
                            path = os.path.join(NameDirectory, f)
                            try:
                                backups.append((int(m.group(1)), path))
                            except ValueError:
                                continue
                    backups.sort()
                    while len(backups) >= self.backupCount:
                        _, old_path = backups.pop(0)
                        try:
                            os.remove(old_path)
                        except OSError:
                            pass
                except FileNotFoundError:
                    pass

        self.stream = self._open()

    def emit(self, record: logging.LogRecord) -> None:
        try:
            if self.ShouldRollover():
                self.DoRollover()
            logging.FileHandler.emit(self, record)
        except ValueError:
            self.handleError(record)

class ColoredConsoleFormatter(logging.Formatter):
    colors = LOG_COLORS

    def format(self, record):
        msg = super().format(record)
        return colored(msg, self.colors.get(record.levelname, 'white'))

def setup_logger(LogDir: str = 'logs', console_level: int = logging.INFO, file_level: int = logging.DEBUG) -> logging.Logger:
    os.makedirs(LogDir, exist_ok=True)

    TimeStamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    LogFileName = os.path.join(LogDir, f"log_{TimeStamp}.log")

    AppLogger = logging.getLogger('MyApp')
    AppLogger.setLevel(logging.DEBUG)
    AppLogger.handlers.clear()

    ConsoleHandler = logging.StreamHandler(sys.stdout)
    ConsoleHandler.setLevel(console_level)
    ConsoleHandler.setFormatter(ColoredConsoleFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - <main_file> - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
    ))
    AppLogger.addHandler(ConsoleHandler)

    FileHandler = CleanRotatingFileHandler(
        LogFileName,
        maxBytes= 2 * 1024 * 1024,
        backupCount=30,
        encoding='utf-8'
    )
    FileHandler.setLevel(file_level)
    FileHandler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - <main_file> - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
    ))
    AppLogger.addHandler(FileHandler)

    AppLogger.info(f"start Logging → {LogFileName}")
    return AppLogger

def log_function(func=None, *, args: bool = True, result: bool = True, no_truncate_args = ()):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args_, **kwargs):
            logger = logging.getLogger('MyApp')
            ArgNames = f.__code__.co_varnames[:f.__code__.co_argcount]

            if args:
                SafeArgs = []
                for i, arg in enumerate(args_):
                    name = ArgNames[i] if i < len(ArgNames) else None
                    if name in no_truncate_args:
                        SafeArgs.append(repr(arg))
                    else:
                        SafeArgs.append(SmartRepr(arg))
                SafeKwargs = {k: repr(v) if k in no_truncate_args else SmartRepr(v) for k, v in kwargs.items()}
                logger.debug(f"Entering {f.__name__}(args={tuple(SafeArgs)}, kwargs={SafeKwargs})")
            else:
                logger.debug(f"Entering {f.__name__}()")

            try:
                res = f(*args_, **kwargs)
                if result:
                    logger.debug(f"Exiting {f.__name__} → {SmartRepr(res)}")
                return res
            except Exception as e:
                logger.error(f"Exception in {f.__name__}: {e}", exc_info=True)
                raise
        return wrapper
    return decorator if func is None else decorator(func)