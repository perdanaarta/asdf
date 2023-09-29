from collections.abc import Mapping
import logging
import logging.handlers
from typing import Any

class StreamFormatter(logging.Formatter):
    LEVEL_COLOURS = [
        (logging.DEBUG, '\x1b[40;1m'),
        (logging.INFO, '\x1b[34;1m'),
        (logging.WARNING, '\x1b[33;1m'),
        (logging.ERROR, '\x1b[31m'),
        (logging.CRITICAL, '\x1b[41m'),
    ]

    FORMATS = {
        level: logging.Formatter(
            f'\x1b[30;1m%(asctime)s \x1b[0m{colour}%(levelname)s\x1b[0m \x1b[35m%(name)s [\x1b[35m%(filename)s:%(lineno)d]\x1b[0m %(message)s',
            '[%Y-%m-%d %H:%M:%S]',
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[logging.DEBUG]

        # Override the traceback to always print in red
        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f'\x1b[31m{text}\x1b[0m'

        output = formatter.format(record)

        # Remove the cache layer
        record.exc_text = None
        return output


class FileFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__(
            '[{asctime}] [{levelname}] {name}: {message}',
            '%Y-%m-%d %H:%M:%S',
            '{',
        )

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(StreamFormatter())
logger.addHandler(stream_handler)

file_handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
file_handler.setFormatter(FileFormatter())
logger.addHandler(file_handler)
