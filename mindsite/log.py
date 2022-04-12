import logging
from datetime import datetime
from typing import Optional


class LoggingMixin:
    """Convenience super-class to have a logger configured with the class name"""

    _log: Optional[logging.Logger] = None

    @property
    def log(self) -> logging.Logger:
        """Returns a logger."""
        if self._log is None:
            self._log = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
            log_name = datetime.utcnow().strftime("%Y%m%d")
            logging.basicConfig(
                filename=f"logs/{log_name}.txt",
                filemode='a',
                format='%(asctime)s %(levelname)s %(funcName)s %(message)s',
                level=logging.INFO,
            )
            self.log.info(f"logger initialized: {log_name}")
        return self._log
