import logging

from loggy import Loggy, JsonFormatter

if __name__ == "__main__":
	# Configure the handler + JSON formatter
	handler = logging.StreamHandler()
	handler.setFormatter(JsonFormatter())

	Loggy.add_handler(handler)

	# Global context applies to all logs
	Loggy.set_context(service="checkout", env="prod")

	# Log with additional per-message context
	Loggy.info("order", "Order placed", extra={"order_id": 123, "user_id": 42})
	Loggy.error("payment", "Payment failed", extra={"payment_method": "card"})
