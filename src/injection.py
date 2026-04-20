from typing import Dict, Type

from dependency_injector import containers, providers

from adapters.postgres import SqlAlchemyActivistRepository, SqlAlchemyOrganizerRepository, SqlAlchemyUnitOfWork, \
    SqlAlchemyTimeslotRepository, SqlAlchemySessionRepository
from database import PostgresDatabase, PostgresConfig
from models.common.uow import UnitOfWork
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

    # activistRepository: ActivistRepository = providers.Factory(ActivistRepository)
    # sessionRepository: SessionRepository = providers.Factory(SessionRepository)
    # timeslotRepository: TimeslotRepository = providers.Factory(TimeslotRepository)
    # organizerRepository: OrganizerRepository = providers.Factory(OrganizerRepository)

    repo_map: Dict[Type, Type]  = providers.Object({
        ActivistRepository: SqlAlchemyActivistRepository,
        OrganizerRepository: SqlAlchemyOrganizerRepository,
        SessionRepository: SqlAlchemySessionRepository,
        TimeslotRepository: SqlAlchemyTimeslotRepository,
    })

    uow: UnitOfWork = providers.Factory(SqlAlchemyUnitOfWork, db=db, repo_map=repo_map)

    authService: AuthService = providers.Factory(AuthService,
        uow=uow,
        hasher=passwordHasher,
        encoder=authCredentialsEncoder,
        validator=authInfoValidationService,
    )