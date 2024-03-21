from wamp import messages

CLIENT_ROLES = {
    "caller": {"features": {}},
    "callee": {"features": {}},
    "publisher": {"features": {}},
    "subscriber": {"features": {}},
}


class IClientAuthenticator:
    def details(self) -> dict:
        raise NotImplementedError()

    def authenticate(self, challenge: messages.Challenge) -> messages.Authenticate:
        raise NotImplementedError()


class Request:
    def __init__(self, method: str, realm: str, authid: str, auth_extra: dict):
        self._method = method
        self._realm = realm
        self._authid = authid
        self._auth_extra = auth_extra

    @property
    def method(self) -> str:
        return self._method

    @property
    def realm(self) -> str:
        return self._realm

    @property
    def authid(self) -> str:
        return self._authid

    @property
    def auth_extra(self) -> dict:
        return self._auth_extra


class Response:
    def __init__(self, authid: str, authrole: str):
        self._authid = authid
        self._authrole = authrole

    @property
    def authid(self) -> str:
        return self._authid

    @property
    def authrole(self) -> str:
        return self._authrole


class WAMPCRAResponse(Response):
    def __init__(self, authid: str, authrole: str, secret: str):
        super().__init__(authid, authrole)
        self._secret = secret

    @property
    def secret(self) -> str:
        return self._secret


class IServerAuthenticator:
    def methods(self) -> list[str]:
        raise NotImplementedError()

    def authenticate(self, request: Request) -> Response:
        raise NotImplementedError()
