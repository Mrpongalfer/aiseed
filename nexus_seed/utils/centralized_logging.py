import logging

class CentralizedLogging:
    def __init__(self, log_file: str = "nexus.log"):
        logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger()

    def log_info(self, message: str) -> None:
        self.logger.info(message)
        print(f"INFO: {message}")

    def log_error(self, message: str) -> None:
        self.logger.error(message)
        print(f"ERROR: {message}")

