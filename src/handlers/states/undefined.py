from aiogram.fsm.state import StatesGroup, State

__all__ = ["UndefinedStatesGroup"]

class UndefinedStatesGroup(StatesGroup):
    UndefinedActivist = State()
    UndefinedOrganizer = State()
    UndefinedMainOrg = State()