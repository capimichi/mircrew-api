from __future__ import annotations

import logging

from mircrewapi.logger.base_logger import BaseLogger


class AppLogger(BaseLogger):
    def __init__(self, log_dir: str, debug: bool = False) -> None:
        super().__init__("mircrewapi.app", log_dir, "app.log", debug=debug)

    def configure_root(self) -> None:
        logger = self.get_logger()
        root = logging.getLogger()
        if not any(handler in root.handlers for handler in logger.handlers):
            for handler in logger.handlers:
                root.addHandler(handler)
        root.setLevel(logger.level)
