import logging
import threading
from typing import Any, Dict, Optional


class LoggyLogger(logging.Logger):
    """
    Custom Logger that injects thread-local context into each log record.
    """
    _context_storage = threading.local()

    def makeRecord(
        self,
        name,
        level,
        fn,
        lno,
        msg,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None
    ):
        # Create the standard LogRecord
        record = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

        # Inject thread-local context into the record
        context = getattr(self._context_storage, "context", {})
        for key, value in context.items():
            setattr(record, key, value)
        return record

    @classmethod
    def set_context(cls, **kwargs: Any):
        if not hasattr(cls._context_storage, "context"):
            cls._context_storage.context = {}
        cls._context_storage.context.update(kwargs)

    @classmethod
    def clear_context(cls):
        cls._context_storage.context = {}


class Loggy:
    _lock = threading.Lock()
    _loggers: Dict[str, LoggyLogger] = {}
    _global_handlers: list[logging.Handler] = []
    _global_formatters: list[logging.Formatter] = []

    @classmethod
    def set_context(cls, **kwargs: Any):
        LoggyLogger.set_context(**kwargs)

    @classmethod
    def clear_context(cls):
        LoggyLogger.clear_context()

    @classmethod
    def add_global_handler(cls, handler: logging.Handler):
        with cls._lock:
            cls._global_handlers.append(handler)

    @classmethod
    def add_global_formatter(cls, formatter: logging.Formatter):
        with cls._lock:
            cls._global_formatters.append(formatter)

    @classmethod
    def get_logger(cls, name: str) -> LoggyLogger:
        with cls._lock:
            if name in cls._loggers:
                return cls._loggers[name]

            # Use our custom logger class
            logging.setLoggerClass(LoggyLogger)
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)

            # Attach new handlers with formatters
            for handler in cls._global_handlers:
                h = type(handler)()
                h.setLevel(handler.level)
                for fmt in cls._global_formatters:
                    h.setFormatter(fmt)
                logger.addHandler(h)

            cls._loggers[name] = logger
            return logger
