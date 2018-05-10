import logging

def setup_logging(location):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    hdlr = logging.FileHandler(location)
    hdlr.setFormatter(formatter)

    logger = logging.getLogger('prawcore')
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger
