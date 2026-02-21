from models import MainOrganizer, MainOrganizerRepository

__all__ = ["MainOrganizerLstRepository"]

class MainOrganizerLstRepository(MainOrganizerRepository):
    def __init__(self):
        self.lst = {}
    
    def get(self, id: int) -> MainOrganizer:
        if id in self.lst:
            return self.lst[id]
        else:
            raise KeyError(f"Organizer with id {id} not found")
    
    def save(self, model: MainOrganizer) -> MainOrganizer:
        self.lst[model.TgID] = model
        return model
    

    
    