
from base.loggy.core import Loggy, JsonFormatter
from base.loggy.handlers import InMemoryLogHandler


# Setup test logging
def setup_test_loggy(context=None) -> InMemoryLogHandler:
    handler = InMemoryLogHandler()
    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    Loggy.configure(
        context=context or {},
        handlers=[handler],
        formatter=formatter
    )

    return handler


def test_info_log_with_extra():
    handler = setup_test_loggy(context={"env": "test"})

    Loggy.info("test_logger", "Something happened", extra={"user_id": 123})

    logs = handler.get_json_logs()

    assert len(logs) == 1
    log_entry = logs[0]

    assert log_entry["message"] == "Something happened"
    assert log_entry["level"] == "INFO"
    assert log_entry["logger"] == "test_logger"
    assert log_entry["context"]["env"] == "test"
    assert log_entry["context"]["user_id"] == 123


def test_error_log_with_global_context_no_extra():
    handler = setup_test_loggy(context={"env": "test"})
    Loggy.info("test_logger", "Hello world")

    logs = handler.get_json_logs()

    assert len(logs) == 1
    log_entry = logs[0]

    assert log_entry["message"] == "Hello world"
    assert log_entry["level"] == "INFO"
    assert log_entry["logger"] == "test_logger"
    assert log_entry["context"]["env"] == "test"



