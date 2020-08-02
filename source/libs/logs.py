"""Manage logging"""
import logging
import warnings


def init_logs(log_level):
    """
    Init the log level according to the parameter in input

    :param log_level: The desired log level
    :return: the logger object
    """
    # Init logging
    logging.basicConfig(level=getattr(logging, log_level), format='[%(asctime)s] - [%(levelname)s] - %(message)s')
    # Hide GCP warning because we use end user creds
    warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")
