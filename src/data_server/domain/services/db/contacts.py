class ContactsDB:

    def update(self, parties: tuple[str, str], last_message: str):
        raise NotImplementedError("ContactsDB.update()")

    def findMany(self, user_id: str, skip: int, limit: int):
        raise NotImplementedError("ContactsDB.findMany()")

    def remove(self, pair: tuple[str, str]):
        raise NotImplementedError("ContactsDB.remove()")
