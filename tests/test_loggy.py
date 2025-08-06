import time

from base.loggy.core import Loggy, JsonFormatter
from base.loggy.handlers import InMemoryLogHandler
import threading


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


def test_concurrent_logging():

    handler = setup_test_loggy(context={"env": "test"})

    def run(tx_id: str, n: int):
        Loggy.add_context(tx_id=tx_id)
        Loggy.info("test_logger", f"First Message from {n}")
        time.sleep(2)
        Loggy.clear_context()

    t1 = threading.Thread(target=run, args=("123", 1))
    t1.start()
    run("456", 2)
    t1.join()
    logs = handler.get_json_logs()

    l1 = logs[0]
    l2 = logs[1]

    assert l1["context"]["tx_id"] == "123"
    assert l2["context"]["tx_id"] == "456"

