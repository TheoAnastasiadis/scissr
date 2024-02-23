from src.common.models.user import User
from src.data_server.domain.services.auth.auth_serivce import APICaller
from src.data_server.domain.services.cache.user_cache import UserCache
from src.data_server.domain.services.db.contacts import ContactsDB
from src.data_server.domain.services.db.user import UserDB
from src.data_server.domain.use_cases.models.onboard_body import (
    OnboardUserBody,
)
from src.data_server.domain.use_cases.models.search_filters import (
    SearchFilters,
)
from src.data_server.domain.use_cases.models.update_body import UpdateUserBody
from fastapi import HTTPException
from pydantic import validate_call


class UserUseCases:

    user_db: UserDB
    user_cache: UserCache
    contacts_db: ContactsDB

    def __init__(
        self,
        /,
        user_db: UserDB,
        user_cache: UserCache,
        contacts_db: ContactsDB,
    ):
        self.user_db = user_db
        self.user_cache = user_cache
        self.contacts_db = contacts_db

    @validate_call
    def profile(self, caller: APICaller) -> User:
        user = self.user_db.findOne(caller.sub)
        if user is None:
            raise HTTPException(
                status_code=307, detail="User has not completed their profile"
            )
        else:
            return user

    @validate_call
    def complete_profile(self, caller: APICaller, body: OnboardUserBody):
        user_exists = self.user_db.findOne(by_email=caller.email)
        if user_exists:
            raise HTTPException(
                status_code=500,
                detail="User has already completed their profile",
            )

        user = User(
            _id=caller.sub,
            username=caller.p_username[
                :10
            ],  # limit username to fit user db schema
            email=caller.email,
            pronouns=body.pronouns,
            age=body.age,
            active_mtr=body.active_mtr,
            kinky_mtr=body.kinky_mtr,
            location=(body.location.latitude, body.location.longitude),
        )
        self.user_db.insert(user)

    @validate_call
    def get_user(self, caller: APICaller, user_id: str) -> User:
        user = self.user_db.findOne(user_id)

        if user is not None and caller.sub in user.blocked:
            raise HTTPException(
                status_code=403, detail="You cannot view this resource."
            )
        elif user is None:
            raise HTTPException(
                status_code=404,
                detail=f"User with id: {user_id} not found on database",
            )

        if caller.sub != user_id:
            user.blocked = []
            user.location = None
            user.email = None
            user.photos = [photo for photo in user.photos if photo.public]

        return user

    @validate_call
    def update_user(self, caller: APICaller, body: UpdateUserBody) -> User:

        user = self.user_db.findOne(caller.sub)
        print(body)

        if body.username:
            # business.validate_username(user, body.username)
            user.username = body.username

        if body.age:
            # business.validate_age(user, body.age)
            user.age = body.age

        if body.kinky_mtr:
            user.kinky_mtr = body.kinky_mtr

        if body.active_mtr:
            user.active_mtr = body.active_mtr

        if body.vibes:
            user.vibes = body.vibes

        if body.pronouns:
            user.pronouns = body.pronouns

        if body.location:
            user.location = (body.location.latitude, body.location.longitude)
        self.user_db.update(user)

    @validate_call
    def block_user(self, caller: APICaller, user_id: str):
        user = self.user_db.findOne(caller.sub)
        if user is not None:
            user.blocked.append(user_id)
            self.contacts_db.remove(pair=[caller.sub, user_id])
            self.user_db.update(user)

    @validate_call
    def unblock_user(self, caller: APICaller, user_id: str):
        user = self.user_db.findOne(caller.sub)
        user.blocked.remove(user_id)
        self.user_db.update(caller)

    @validate_call
    def get_users(
        self,
        caller: APICaller,
        filters: SearchFilters,
        skip: int = 0,
        limit: int = 20,
    ) -> list[User]:

        filters_dict = filters.model_dump(exclude=["location", "distance"])
        location_hash = ""

        users = []
        user = self.user_db.findOne(caller.sub)
        # check if results are already in cache
        # (only when filters.only_active == False)
        if (
            self.user_cache.cache_has(filters_dict, location_hash)
            and not filters.only_active
        ):
            users = self.user_cache.cache_get(filters_dict, location_hash)
        # otherwise fetch from db
        # and append to cache
        else:
            users = self.user_db.findMany(
                skip,
                limit,
                location=filters.location,
                distance=filters.distance,
                active_mtr=filters.active_mtr["value"],
                active_mtr_op=filters.active_mtr["operation"],
                kinky_mtr=filters.kinky_mtr["value"],
                kinky_mtr_op=filters.kinky_mtr["operation"],
                exclude_from_results=user.blocked,
                excluded_from=user.id,
                only_acitve=filters.only_active,
                vibes=filters.vibes,
            )
            self.user_cache.cache_set(filters_dict, users, location_hash)

        def delete_uneccesary(u: User):
            u.blocked = []
            u.location = None
            u.email = None
            u.photos = [photo for photo in u.photos if photo.public]

        map(delete_uneccesary, users)

        return users
