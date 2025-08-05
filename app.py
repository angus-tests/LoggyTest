import logging

from loggy import Loggy


if __name__ == "__main__":

	# Add formatter and handler
	formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
	handler = logging.StreamHandler()

	Loggy.add_formatter(formatter)
	Loggy.add_handler(handler)

	# Set global context
	Loggy.set_context(request_id="abc123", user_id="42")

	# Get a logger and log something
	log = Loggy.get_logger("my_app")

	log.info("Started the process")
	log.warning("Something might go wrong")
	log.error("Something went wrong")
