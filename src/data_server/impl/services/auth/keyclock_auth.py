from fastapi import HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakAdmin, KeycloakOpenID
from src.common.config import config
from src.data_server.domain.services.auth.auth_serivce import (
    APICaller,
    AuthService,
)
from src.data_server.domain.services.db.user import UserDB


class KeyCloackAuth(AuthService):

    # client = KeycloakOpenID(
    #     server_url=config["AUTH_CLIENT_SERVER_URL"],
    #     client_id=config["AUTH_DATA_SERVER_CLIENT_ID"],
    #     realm_name=config["AUTH_REALM"],
    #     client_secret_key=config["AUTH_DATA_SERVER_CLIENT_SECRET"],
    #     verify=True,
    # )

    # KeycloakAdmin(
    #     server_url=config["AUTH_ADMIN_SERVER_URL"],
    #     username=congif["ADMIN_USERNAME"],
    #     password=config["ADMIN_SERCERT"],
    #     realm_name=config["AUTH_REALM"],
    # )

    token: str = None
    caller: APICaller = None

    def __init__(
        self, user_db: UserDB, client: KeycloakOpenID, admin: KeycloakAdmin
    ):
        self.user_db = user_db
        self.client = client
        self.admin = admin

    _oauth2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=config["AUTH_URL"],
        tokenUrl=config["TOKEN_URL"],
    )

    def _get_payload(self) -> dict:

        public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            + f"{self.client.public_key()}"
            + "\n-----END PUBLIC KEY-----"
        )

        try:
            return self.client.decode_token(
                self.token,
                key=public_key,
                options={
                    "verify_signature": True,
                    "verify_aud": False,
                    "exp": True,
                },
            )
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_caller(self, token: str = Security(_oauth2_scheme)) -> APICaller:
        self.token = token
        payload = self._get_payload()
        return APICaller(
            sub=payload.get("sub"),
            email=payload.get("email"),
            p_username=payload.get("preferred_username"),
        )
