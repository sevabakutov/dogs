import os
import logging
from datetime import datetime

class GHLogger():
    def __init__(self, filename: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.filename = filename
        self._setup_logger()

    def _setup_logger(self) -> None:
        self.logger.setLevel("DEBUG")
        formatter = logging.Formatter("{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%m")

        console_handler = logging.StreamHandler()
        console_handler.setLevel("DEBUG")
        console_handler.setFormatter(formatter)
        console_handler.addFilter(self.shows_only_debug)
        self.logger.addHandler(console_handler)

        file_handler = logging.FileHandler(self.get_log_filename(), mode="a", encoding="utf-8")
        file_handler.setLevel("WARNING")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    
    def shows_only_debug(self, record: str) -> str:
        return record.levelname == "DEBUG"

    def get_log_filename(self) -> str:
        dirname = os.path.join(os.getcwd(), '..', '..', 'log')
        os.makedirs(dirname, exist_ok=True)
        curr_date = datetime.today().strftime('%Y-%m-%d')
        return os.path.join(dirname, f'{curr_date}_{self.filename}.log')
    
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)