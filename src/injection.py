from dependency_injector import containers, providers
from database import PostgresDatabase, PostgresConfig
from services.auth import AuthCredentialsEncoder, AuthInfoValidationService, AuthService
from services.auth.hasher import PasswordHasher
from adapters.bcrypt import  BcryptPasswordHasher
from adapters.jwt import JwtAuthCredentialsEncoder

from utils.logger.get import getLogger

import sys
import logging

from models import ActivistRepository, SessionRepository, TimeslotRepository, OrganizerRepository

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

    passwordHasher: PasswordHasher = providers.Singleton(BcryptPasswordHasher)
    authCredentialsEncoder: AuthCredentialsEncoder = providers.Singleton(
        JwtAuthCredentialsEncoder,
        secret=config.jwt.secret,
        algorithm="HS256",
        expires_minutes=config.jwt.expire_minutes,
    )
    authInfoValidationService: AuthInfoValidationService = providers.Singleton(AuthInfoValidationService)


    dbconfig = providers.Resource(PostgresConfig, 
        host=config.database.host,
        port=config.database.port,
        user=config.database.user,
        password=config.database.password,
        database=config.database.database,
        echo=config.database.echo
    )

    db = providers.Singleton(PostgresDatabase, config=dbconfig)

    activistRepository: ActivistRepository = providers.Factory(ActivistRepository)
    sessionRepository: SessionRepository = providers.Factory(SessionRepository)
    timeslotRepository: TimeslotRepository = providers.Factory(TimeslotRepository)
    organizerRepository: OrganizerRepository = providers.Factory(OrganizerRepository)

    authService: AuthService = providers.Singleton(AuthService,
        activist_repository = activistRepository,
        organization_repository=organizerRepository,
        hasher=passwordHasher,
        encoder=authCredentialsEncoder,
        validator=authInfoValidationService,
    )