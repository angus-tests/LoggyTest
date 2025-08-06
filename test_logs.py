

def test_concurrent_logging(self):
    configure_loggers("INFO", {})

    def run(tx_id: str, n: int):
        bind_to_loggers("tx_id", tx_id)
        logger.info(f"First Message from {n}")
        time.sleep(2)
        logger.info(f"Second Message from {n}")
        unbind_from_loggers("tx_id")

    t1 = threading.Thread(target=run, args=("123", 1))
    t1.start()
    run("456", 2)
    t1.join()