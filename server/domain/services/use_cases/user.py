from server.domain.models.user import User
from server.domain.services.db import UserDB, AuthDB
from fastapi import HTTPException
from pydantic import Field, validate_call, BaseModel
from typing_extensions import Annotated
from typing import NamedTuple, Optional
from enum import Enum


class Operations(str, Enum):
    GE = "ge"
    LE = "le"


class LocationTuple(NamedTuple):
    latitude: float
    longitude: float


class Filters(BaseModel):

    class Kinky_mtr_type(NamedTuple):
        value: Annotated[float, Field(ge=0, le=1, default=0.0)]
        opretation: Annotated[Operations, Field(default=Operations.GE)]

    class Active_mtr_type(NamedTuple):
        value: Annotated[float, Field(ge=0, le=1, default=0.0)]
        opretation: Annotated[Operations, Field(default=Operations.GE)]

    vibes: Annotated[Optional[list[str]], Field(kw_only=True)]
    kinky_mtr: Annotated[
        Optional[dict], Field(default_factory=Kinky_mtr_type, kw_only=True)
    ]
    active_mtr: Annotated[
        Optional[dict], Field(default_factory=Active_mtr_type, kw_only=True)
    ]
    only_active: Annotated[Optional[bool], Field(default=False, kw_only=True)]
    location: Annotated[
        LocationTuple,
        Field(
            kw_only=True,
        ),
    ]
    distance: Annotated[float, Field(default=5, kw_only=True)]


class UpdateUserBody(BaseModel):
    username: Annotated[str, Field(kw_only=True)]
    age: Annotated[int, Field(kw_only=True)]
    kinky_mtr: Annotated[float, Field(ge=0, le=1, kw_only=True)]
    active_mtr: Annotated[float, Field(ge=0, le=1, kw_only=True)]
    vibes: Annotated[list[str], Field(kw_only=True)]
    location: Annotated[
        Optional[LocationTuple], Field(kw_only=True, default=None)
    ]


class UserUseCases:

    user_db: UserDB
    auth_db: AuthDB

    def __init__(self, /, user_db: UserDB, auth_db: AuthDB):
        self.user_db = user_db
        self.auth_db = auth_db

    def _can_perform_action(self, caller_id: str, user_id: str) -> bool:
        return caller_id == user_id or self.auth_db.user_is_admin(caller_id)

    @validate_call
    def get_user(self, caller: User, user_id: str) -> User:
        user = self.user_db.findOne(user_id)
        user_is_admin = self.auth_db.user_is_admin(caller.id)

        if user_id in caller.blocked:
            raise HTTPException(
                status_code=403, detail="You cannot view this resource."
            )

        if user is not None:
            if not user_is_admin and caller.id in user.blocked:
                raise HTTPException(
                    status_code=403, detail="You cannot view this resource."
                )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"User with id: {user_id} not found on database",
            )

        if not user_is_admin and caller.id != user_id:
            user.blocked = []
            user.location = ""
            user.photos = [photo for photo in user.photos if photo.public]

        return user

    @validate_call
    def update_user(
        self, caller: User, user_id: str, body: UpdateUserBody
    ) -> User:
        if not self._can_perform_action(caller.id, user_id):
            raise HTTPException(
                status_code=403, detail="You cannot perform this action."
            )

        user = self.user_db.findOne(user_id)
        body = body.model_dump()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"User with id: {user_id} not found on database",
            )

        if "username" in body:
            # business.validate_username(user, body.username)
            user.username = body["username"]

        if "age" in body:
            # business.validate_age(user, body.age)
            user.age = body["age"]

        if "kinky_mtr" in body:
            user.kinky_mtr = body["kinky_mtr"]

        if "active_mtr" in body:
            user.active_mtr = body["active_mtr"]

        if "vibes" in body:
            user.vibes = body["vibes"]

        return (
            self.user_db.update(user, body["location"])
            if "location" in body
            else self.user_db.update(user)
        )

    @validate_call
    def block_user(self, caller: User, user_id: str) -> User:
        # admins cannot perform these tasks
        caller.blocked.append(user_id)
        return self.user_db.update(caller)

    @validate_call
    def unblock_user(self, caller: User, user_id: str) -> User:
        # admins cannot perform these tasks
        caller.blocked.remove(user_id)
        return self.user_db.update(caller)

    @validate_call
    def delete_user(self, caller: User, user_id: str):
        user = self.user_db.findOne(user_id)
        if not self._can_perform_action(caller.id, user_id):
            raise HTTPException(
                status_code=403, detail="You cannot perform this action."
            )
        self.user_db.delete(user)

    @validate_call
    def get_users(
        self,
        caller: User,
        filters: Filters,
        skip: int = 0,
        limit: int = 20,
    ) -> list[User]:

        is_admin = self.auth_db.user_is_admin(caller)

        users = self.user_db.findMany(
            skip,
            limit,
            location=filters.location,
            distance=filters.distance,
            active_mtr=filters.active_mtr["value"],
            active_mtr_op=filters.active_mtr["operation"],
            kinky_mtr=filters.kinky_mtr["value"],
            kinky_mtr_op=filters.kinky_mtr["operation"],
            exclude_from_results=caller.blocked if not is_admin else [],
            excluded_from=caller.id if not is_admin else None,
            only_acitve=filters.only_active,
            vibes=filters.vibes,
        )

        def delete_uneccesary(u: User):
            u.blocked = []
            u.location = ""
            u.photos = [photo for photo in u.photos if photo.public]

        if not is_admin:
            map(delete_uneccesary, users)

        return users
