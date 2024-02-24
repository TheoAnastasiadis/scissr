from fastapi import HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
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

    def __init__(self, user_db: UserDB, client: KeycloakOpenID):
        self.user_db = user_db
        self.client = client

    _oauth2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=config["AUTH_URL"],  # type: ignore
        tokenUrl=config["TOKEN_URL"],  # type: ignore
    )

    def _get_payload(self, token: str) -> dict[str, str]:

        public_key = (
            "-----BEGIN PUBLIC KEY-----\n"
            + f"{self.client.public_key()}"
            + "\n-----END PUBLIC KEY-----"
        )

        try:
            return self.client.decode_token(
                token,
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
        payload = self._get_payload(token)
        return APICaller(
            sub=payload.get("sub"),  # type: ignore
            email=payload.get("email"),  # type: ignore
            p_username=payload.get("preferred_username"),  # type: ignore
        )
