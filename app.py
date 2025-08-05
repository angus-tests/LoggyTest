import logging

from loggy import Loggy


if __name__ == "__main__":

	Loggy.add_global_handler(
		logging.StreamHandler()
	)

	Loggy.add_global_formatter(
		logging.Formatter(
			"%(asctime)s - %(levelname)s - %(message)s - [%(request_id)s] [%(user_id)s]"
		)
	)

	log = Loggy.get_logger(__name__)

	# Set context (thread-local)
	Loggy.set_context(request_id="abc123", user_id="42")

	log.info("Something happened")

	# Clear context (optional, context is thread-local)
	Loggy.clear_context()
