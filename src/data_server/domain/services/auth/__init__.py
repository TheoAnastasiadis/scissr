class AuthDB:
    def user_is_admin(self, user_id: str) -> bool:
        raise NotImplementedError("AuthDB.user_is_admin()")
