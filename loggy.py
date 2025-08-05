import logging
import threading
from typing import Any, Dict


class ContextFilter(logging.Filter):
    """
    Logging filter that injects thread-local context into log records.
    """
    def __init__(self, context_storage: threading.local):
        super().__init__()
        self._context_storage = context_storage

    def filter(self, record: logging.LogRecord) -> bool:
        context = getattr(self._context_storage, "context", {})
        for key, value in context.items():
            setattr(record, key, value)
        return True


class Loggy:
    _lock = threading.Lock()
    _loggers: Dict[str, logging.Logger] = {}
    _context_storage = threading.local()
    _global_handlers: list[logging.Handler] = []
    _global_formatters: list[logging.Formatter] = []

    @classmethod
    def set_context(cls, **kwargs: Any):
        """
        Set thread-local context to be injected into log records.
        """
        if not hasattr(cls._context_storage, "context"):
            cls._context_storage.context = {}
        cls._context_storage.context.update(kwargs)

    @classmethod
    def clear_context(cls):
        """
        Clear thread-local context.
        """
        cls._context_storage.context = {}

    @classmethod
    def add_global_handler(cls, handler: logging.Handler):
        with cls._lock:
            cls._global_handlers.append(handler)

    @classmethod
    def add_global_formatter(cls, formatter: logging.Formatter):
        with cls._lock:
            cls._global_formatters.append(formatter)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get a thread-safe logger instance with context support.
        """
        with cls._lock:
            if name in cls._loggers:
                return cls._loggers[name]

            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG)

            # Add handlers and formatters
            for handler in cls._global_handlers:
                # Clone handler so each logger gets its own copy
                new_handler = type(handler)()
                new_handler.setLevel(handler.level)
                for fmt in cls._global_formatters:
                    new_handler.setFormatter(fmt)
                logger.addHandler(new_handler)

            # Add context filter
            logger.addFilter(ContextFilter(cls._context_storage))

            cls._loggers[name] = logger
            return logger
