
from loggy import Loggy

if __name__ == "__main__":
    Loggy.configure(
        context={"app": "my_app", "version": "1.0"}
    )

    # Log with additional per-message context
    Loggy.info("order", "Order placed", extra={"order_id": 123, "user_id": 42})
    Loggy.error("payment", "Payment failed", extra={"payment_method": "card"})
