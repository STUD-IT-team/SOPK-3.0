import logging

def getLogger(name, **options):
    logging.basicConfig(**options)
    return logging.getLogger(name)