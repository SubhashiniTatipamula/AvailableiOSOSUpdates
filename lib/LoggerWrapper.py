# -----------------------------------------------------------
# Original Author: Subhashini Tatipamula
# Last Modified By:
# Created Date : 13-Aug-2017
# Last Modified Date:
# ------------------------------------------------------------
"""
This module implements the logging functionality
"""

# imports required for logger module implementation
import logging
import logging.handlers
import traceback
import platform


class LoggerWrapper:
    """
    This is class prepares the logger object required for logging purposes
    """

    def __init__(self):
        self.logger = None

    def get_logger(self, file_name="LogFile.log"):
        """
        This method initializes logger object
            - Arg: None
            - Returns: logger object
        """
        try:
            # Initialize logger object
            hostname = platform.node()
            prefix = "[" + hostname + "]"
            self.logger = logging.getLogger(prefix)
            if not len(self.logger.handlers):
                logger_hdlr = logging.handlers.RotatingFileHandler(file_name, backupCount=50000, maxBytes=1073741824)
                log_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(threadName)s - %(process)d - %(processName)s - %(message)s')
                logger_hdlr.setFormatter(log_formatter)
                self.logger.addHandler(logger_hdlr)
                self.logger.setLevel(logging.DEBUG)
            return self.logger
        except Exception:
            print("Failed to get the logger object")
            print(traceback.format_exc())
