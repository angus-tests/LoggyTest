import logging


class LoggyContextFilter(logging.Filter):
    """
    Injects Loggy global context into each LogRecord under record.context
    """
    def __init__(self, global_context_getter):
        super().__init__()
        self._get_context = global_context_getter

    def filter(self, record: logging.LogRecord) -> bool:
        global_context = self._get_context()

        if hasattr(record, "context") and isinstance(record.context, dict):
            # Merge without overwriting record's own context
            merged = {**global_context, **record.context}
        else:
            merged = global_context.copy()

        record.context = merged
        return True
