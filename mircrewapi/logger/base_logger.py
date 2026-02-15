from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler


class BaseLogger:
    def __init__(
        self,
        name: str,
        log_dir: str,
        filename: str,
        debug: bool = False,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5,
    ) -> None:
        self._name = name
        self._log_path = os.path.join(log_dir, filename)
        self._level = logging.DEBUG if debug else logging.INFO
        self._max_bytes = max_bytes
        self._backup_count = backup_count
        self._logger: logging.Logger | None = None

    def get_logger(self) -> logging.Logger:
        if self._logger is not None:
            return self._logger
        logger = logging.getLogger(self._name)
        logger.setLevel(self._level)
        if not any(isinstance(handler, RotatingFileHandler) for handler in logger.handlers):
            handler = RotatingFileHandler(
                self._log_path,
                maxBytes=self._max_bytes,
                backupCount=self._backup_count,
            )
            handler.setLevel(self._level)
            handler.setFormatter(
                logging.Formatter(
                    fmt="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                )
            )
            logger.addHandler(handler)
        logger.propagate = False
        self._logger = logger
        return logger
