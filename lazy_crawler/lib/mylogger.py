"""Default Logger for our Whole project. This will be used instead of print statement as this enables us to enable
switching between logs to debugging mode(development) and  Error mode(for production)
https://docs.python.org/2/howto/logging.html#logging-basic-tutorial
"""
import logging
import os


class Logger:
    def __init__(self, name='LazyCrawler'):
        self.name = name
        self.LOG_LEVEL_DICT = {
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG,
            'ERROR': logging.ERROR,
        }
        self.LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

        logging.basicConfig(format='%(asctime)s - [%(name)s] - %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=self.LOG_LEVEL_DICT[self.LOG_LEVEL])

        self.logger = logging.getLogger(self.name)

    def set_logger(self, logger_name):
        """
        Changes the name of logger
        :param logger_name: Name of the logger to set (str)
        :return:  None
        """
        self.name = logger_name
        self.logger = logging.getLogger(self.name)

    def __str__(self):
        return self.name
