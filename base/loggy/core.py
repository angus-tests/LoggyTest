import logging
from logging import StreamHandler
from typing import Any, Optional

from base.loggy.formatters import JsonFormatter


class Loggy:
    _loggers: dict[str, logging.Logger] = {}
    _global_context: dict[str, Any] = {}
    _handlers: list[logging.Handler] = []

    # TODO keep as kwargs or use dictionary?
    @classmethod
    def set_context(cls, **kwargs: Any):
        cls._global_context.update(kwargs)

    @classmethod
    def clear_context(cls):
        cls._global_context.clear()

    @classmethod
    def add_handler(cls, handler: logging.Handler):
        cls._handlers.append(handler)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        for handler in cls._handlers:
            logger.addHandler(handler)

        cls._loggers[name] = logger
        return logger

    @classmethod
    def _merge_context(cls, extra: Optional[dict[str, Any]]) -> dict[str, Any]:
        """
        Merges the global context with any extra context provided for a specific log message.
        :param extra: The extra context to merge with the global context.
        :return: A dictionary containing the merged context of the global context and the extra context.
        """
        merged = cls._global_context.copy()
        if extra:
            merged.update(extra)
        return {"context": merged}

    @classmethod
    def debug(cls, name: str, msg: str, extra: Optional[dict[str, Any]] = None):
        cls.get_logger(name).debug(msg, extra=cls._merge_context(extra))

    @classmethod
    def info(cls, name: str, msg: str, extra: Optional[dict[str, Any]] = None):
        cls.get_logger(name).info(msg, extra=cls._merge_context(extra))

    @classmethod
    def warning(cls, name: str, msg: str, extra: Optional[dict[str, Any]] = None):
        cls.get_logger(name).warning(msg, extra=cls._merge_context(extra))

    @classmethod
    def error(cls, name: str, msg: str, extra: Optional[dict[str, Any]] = None):
        cls.get_logger(name).error(msg, extra=cls._merge_context(extra))

    @classmethod
    def critical(cls, name: str, msg: str, extra: Optional[dict[str, Any]] = None):
        cls.get_logger(name).critical(msg, extra=cls._merge_context(extra))

    @classmethod
    def exception(cls, name: str, msg: str, extra: Optional[dict[str, Any]] = None):
        cls.get_logger(name).exception(msg, extra=cls._merge_context(extra))

    @classmethod
    def configure(
        cls,
        context: Optional[dict[str, Any]] = None,
        handlers: list[logging.Handler] = None,
        level: int = logging.INFO,
        formatter: Optional[logging.Formatter] = None
    ):
        """
        Configure Loggy with default context and handlers.

        Args:
            context: Global context to add to all logs.
            handlers: A list of logging handlers to add. (default to StreamHandler)
            level: Minimum logging level. (defaults to logging.INFO)
            formatter: Custom formatter (defaults to JsonFormatter).
        """
        cls._loggers.clear()
        cls._handlers.clear()
        cls._global_context.clear()

        if context:
            cls.set_context(**context)

        formatter = formatter or JsonFormatter()

        if handlers:
            for handler in handlers:
                if not isinstance(handler, logging.Handler):
                    raise ValueError("All handlers must be instances of logging.Handler")
                handler.setFormatter(formatter)
                handler.setLevel(level)
                cls.add_handler(handler)
        else:
            # Default to a stream handler if no handlers are provided
            handler = StreamHandler()
            handler.setFormatter(formatter)
            handler.setLevel(level)
            cls.add_handler(handler)
