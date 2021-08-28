import coloredlogs, logging

def config_logger():
    coloredlogs.install()
    logging.basicConfig(level=logging.DEBUG)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)