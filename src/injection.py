from dependency_injector import containers, providers
from database.postgres import PostgresDatabase, PostgresConfig

from utils.logger.get import getLogger

import sys
import logging
import time

from typing import List, Dict, Any
class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["config/app.yaml"])

    # Logging config options
    LOGGING_KWARGS = {
        "format": "[%(levelname)s, %(asctime)s, %(filename)s] func %(funcName)s, line %(lineno)d: %(message)s;",
        "datefmt": "%d.%m.%Y %H:%M:%S",
        "stream": sys.stdout,
        "level": logging.INFO if (config.app.log_level != 'debug') else logging.DEBUG,
    }

    logger = providers.Factory(getLogger, name="sopkbot", **LOGGING_KWARGS)

    dbconfig = providers.Resource(PostgresConfig, 
        host=config.database.host,
        port=config.database.port,
        user=config.database.user,
        password=config.database.password,
        database=config.database.database,
        echo=config.database.echo
    )

    db = providers.Singleton(PostgresDatabase, config=dbconfig)