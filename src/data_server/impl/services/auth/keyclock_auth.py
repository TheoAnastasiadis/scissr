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

    client = KeycloakOpenID(
        server_url=config["OIC_SERVER_URL"],
        client_id=config["OIC_CLIENT_ID"],
        realm_name=config["OIC_REALM"],
        client_secret_key=config["OIC_CLIENT_SECRET"],
        verify=True,
    )

    oauth2_scheme = OAuth2AuthorizationCodeBearer(
        authorizationUrl=config["AUTH_URL"],
        tokenUrl=config["TOKEN_URL"],
    )

    token: str = None
    caller: APICaller = None

    def __init__(self, user_db: UserDB):
        self.user_db = user_db

    def get_caller(self, token: str = Security(oauth2_scheme)) -> APICaller:
        self.token = token
        payload = self.get_payload()
        if "data_id" in payload:
            return APICaller(
                data_id=payload.get("data_id"),
                roles=payload.get("roles"),
                email=payload.get("email"),
            )
        else:
            user = self.user_db.findOne(by_email=payload.get("email"))
            id = user.id
            # insert data_id to keycloack payload
            return APICaller(
                data_id=id,
                roles=payload.get("roles"),
                email=payload.get("email"),
            )
            pass

    def get_payload(self) -> dict:

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
