import logging
from typing import Any, Dict


class Loggy:
    _loggers: Dict[str, logging.Logger] = {}
    _global_context: Dict[str, Any] = {}
    _global_handlers: list[logging.Handler] = []
    _global_formatters: list[logging.Formatter] = []

    @classmethod
    def set_context(cls, **kwargs: Any):
        cls._global_context.update(kwargs)

    @classmethod
    def clear_context(cls):
        cls._global_context.clear()

    @classmethod
    def add_handler(cls, handler: logging.Handler):
        cls._global_handlers.append(handler)

    @classmethod
    def add_formatter(cls, formatter: logging.Formatter):
        cls._global_formatters.append(formatter)

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Add handlers with formatters
        for handler in cls._global_handlers:
            # Clone a new handler instance (assumes stateless handlers like StreamHandler)
            new_handler = type(handler)()
            new_handler.setLevel(handler.level)

            for fmt in cls._global_formatters:
                new_handler.setFormatter(fmt)

            logger.addHandler(new_handler)

        # Wrap the logger’s methods to inject context
        cls._wrap_logger_methods(logger)

        cls._loggers[name] = logger
        return logger

    @classmethod
    def _wrap_logger_methods(cls, logger: logging.Logger):
        for method_name in ['debug', 'info', 'warning', 'error', 'critical', 'exception']:
            original = getattr(logger, method_name)

            def wrapper(msg, *args, _original=original, **kwargs):
                context_str = " ".join(
                    f"[{key}={value}]" for key, value in cls._global_context.items()
                )
                full_msg = f"{context_str} {msg}" if context_str else msg
                return _original(full_msg, *args, **kwargs)

            setattr(logger, method_name, wrapper)
