from database_crafting.logging.interfaces import LoggingService
from singleton_decorator import singleton  # type: ignore
import logging


@singleton
class DefaultLogger(LoggingService):

    def __init__(self):
        logging.config.fileConfig("logging.ini")

    def info(self, msg: str) -> None:
        logger = logging.getLogger()
        logger.info(msg)

    def debug(self, msg: str) -> None:
        logger = logging.getLogger()
        logger.debug(msg)

    def error(self, msg: str) -> None:
        logger = logging.getLogger()
        logger.error(msg)

    def critical(self, msg: str) -> None:
        logger = logging.getLogger()
        logger.critical(msg)
