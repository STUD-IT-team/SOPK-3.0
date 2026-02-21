from dependency_injector.wiring import inject, Provide
from injection import Container
from typing import Any, Dict
from enum import Enum

from aiogram.types import Update
from models import BaseActivistRepository, BaseOrganizerRepository, MainOrganizerRepository
from aiogram.fsm.context import FSMContext
from handlers.states import UndefinedStatesGroup
import logging



__all__ = ["RoleMiddleware"]

class Role(str, Enum):
    activist = "activist"
    organizer = "organizer"
    mainOrg = "mainorg"

@inject
class RoleMiddleware:
    logger: logging.Logger = Provide[Container.logger]
    orgRepo: BaseOrganizerRepository = Provide[Container.baseOrganizerRepository]
    actRepo: BaseActivistRepository = Provide[Container.baseActivistRepository]
    mainOrgRepo: MainOrganizerRepository = Provide[Container.mainOrganizerLstRepository]

    async def __call__(
        self, 
        handler: callable, 
        event: Update,
        data: Dict[str, Any]
    ):
        if not event.message or not event.message.from_user:
            return await handler(event, data)

        tgid = event.message.chat.id
        fsm: FSMContext = data["state"]

        old_role: Optional[Role] = data.get("role")
        new_role = await self._resolve_role(tgid)

        if old_role != new_role:
            self.logger.info(
                "Role changed: %s → %s (chatid=%s)",
                old_role,
                new_role,
                tgid,
            )
            await fsm.set_state(self._undefined_state_for_role(new_role))
        
        data["role"] = new_role
        return await handler(event, data)
    
    async def _resolve_role(self, tgid: int) -> Role:
        try:
            if await self.mainOrgRepo.get(tgid):
                return Role.mainOrg
        except KeyError:
            pass

        if await self.orgRepo.gettgid(tgid):
            return Role.organizer

        if await self.actRepo.gettgid(tgid):
            return Role.activist

        return Role.activist
    
    def _undefined_state_for_role(self, role: Role):
        match role:
            case Role.mainOrg:
                return UndefinedStatesGroup.UndefinedMainOrg
            case Role.organizer:
                return UndefinedStatesGroup.UndefinedOrganizer
            case Role.activist:
                return UndefinedStatesGroup.UndefinedActivist
        




