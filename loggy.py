import logging
import json
from typing import Any, Dict, Optional


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include full extra context under "context" if present
        context = getattr(record, "context", None)
        if context:
            log_record["context"] = context

        return json.dumps(log_record)


class Loggy:
    _loggers: Dict[str, logging.Logger] = {}
    _global_context: Dict[str, Any] = {}
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
    def _merge_context(cls, extra: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        merged = cls._global_context.copy()
        if extra:
            merged.update(extra)
        return {"context": merged}

    @classmethod
    def debug(cls, name: str, msg: str, extra: Optional[Dict[str, Any]] = None):
        cls.get_logger(name).debug(msg, extra=cls._merge_context(extra))

    @classmethod
    def info(cls, name: str, msg: str, extra: Optional[Dict[str, Any]] = None):
        cls.get_logger(name).info(msg, extra=cls._merge_context(extra))

    @classmethod
    def warning(cls, name: str, msg: str, extra: Optional[Dict[str, Any]] = None):
        cls.get_logger(name).warning(msg, extra=cls._merge_context(extra))

    @classmethod
    def error(cls, name: str, msg: str, extra: Optional[Dict[str, Any]] = None):
        cls.get_logger(name).error(msg, extra=cls._merge_context(extra))

    @classmethod
    def critical(cls, name: str, msg: str, extra: Optional[Dict[str, Any]] = None):
        cls.get_logger(name).critical(msg, extra=cls._merge_context(extra))

    @classmethod
    def exception(cls, name: str, msg: str, extra: Optional[Dict[str, Any]] = None):
        cls.get_logger(name).exception(msg, extra=cls._merge_context(extra))
