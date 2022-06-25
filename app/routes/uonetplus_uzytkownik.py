from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from app import models, paths, resources
import requests
from datetime import datetime
from cryptography.fernet import Fernet
import ast

router = APIRouter()


@router.post("/get-inbox-messages", response_model=list[models.InboxMessage])
def get_inbox_messages(data: models.UonetPlusUzytkownik, start: str, end: str, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UZYTKOWNIK.WIADOMOSC_GETINBOXMESSAGES
    url = build_url(
        subd="uonetplus-uzytkownik",
        path=path,
        symbol=data.symbol,
        host=data.host,
        ssl=data.ssl,
        start=start,
        end=end
    )
    response = get_response(data, url, session_cookies, "get")
    messages = []
    for message in response.json()["data"]:
        messages.append(
            models.InboxMessage(
                id=message["Id"],
                title=message["Temat"],
                unreaded=message["Nieprzeczytana"],
                date=datetime.fromisoformat(message["Data"]).strftime("%d.%m.%Y %H:%M"),
                sender=message["Nadawca"]["Name"],
                has_attachments=message["HasZalaczniki"]
            )
        )
    return messages


def build_url(subd: str = None, host: str = None, path: str = None, ssl: bool = True, **kwargs) -> str:
    if ssl:
        url = "https://"
    else:
        url = "http://"
    if subd:
        url += subd + "."
    url += host
    if path:
        url += path
    if not kwargs.get("symbol"):
        kwargs["symbol"] = "Default"

    for k in kwargs:
        url = url.replace(f"{{{k.upper()}}}", str(kwargs[k]))
    return url


def get_response(data: dict, url: str, session_cookies: dict, method: str) -> requests.models.Response:
    session = requests.Session()
    session_cookies.update(data.student)
    if method == "post":
        response = session.post(
            url=url,
            cookies=session_cookies,
        )
    else:
        response = session.get(
            url=url,
            cookies=session_cookies,
        )
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=resources.UNKNOWN_ERROR)
    if (
        "uonet_error"
        in response.text
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=resources.UNKNOWN_ERROR
        )
    return response


def decrypt_session_data(request, session_data: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=resources.AUTHENTICATION_REQUIRED
    )
    try:
        if request.session.get('session_key'):
            session_key = request.session.get('session_key')
        else:
            raise credentials_exception
        fernet = Fernet(bytes(session_key, "utf-8"))
        session_data: dict = ast.literal_eval(fernet.decrypt(session_data.encode("utf-8")).decode("utf-8"))
        if session_data['expire'] != None and session_data['session_cookies'] != None:
            if datetime.timestamp(datetime.utcnow())*1000 > float(session_data['expire']):
                raise credentials_exception
        else:
            raise credentials_exception
        return dict(session_data['session_cookies'])
    except:
        raise credentials_exception
