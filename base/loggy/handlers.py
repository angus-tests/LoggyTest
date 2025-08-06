import json
import logging


class InMemoryLogHandler(logging.Handler):
    """
    A logging handler that stores log messages in memory for testing purposes.
    e.g

    handler = InMemoryLogHandler()
    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    Loggy.configure(
        context={"app": "TestApp", "version": "1.0"},
        handlers=[handler],
        formatter=formatter
    )

    Loggy.info("Test message", extra={"user_id": 42})

    logs = handler.get_json_logs()

    # Do assertions on logs
    """
    def __init__(self):
        super().__init__()
        self.logs = []

    def emit(self, record):
        msg = self.format(record)
        self.logs.append(msg)

    def reset(self):
        self.logs.clear()

    def get_logs(self):
        return self.logs

    def get_json_logs(self):
        return [json.loads(log) for log in self.logs]

