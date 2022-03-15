from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import APIKeyCookie
from starlette import status
from app import models, paths
import requests
from cryptography.fernet import Fernet
import ast


cookie_sec = APIKeyCookie(name="key")

router = APIRouter()

@router.post("/uonetplus-uczen/notes")
def get_notes(data: models.UonetPlusUczen, key: str = Depends(cookie_sec)):
    data.vulcan_cookies = encrypt_cookies(key, data.vulcan_cookies)
    path = paths.UCZEN.UWAGIIOSIAGNIECIA_GET
    response = get_response(data, path)
    notes = []
    for note in response.json()["data"]["Uwagi"]:
        note = models.Note(
           date=note["DataWpisu"],
           teacher=note["Nauczyciel"],
           category=note["Kategoria"],
           content=note["TrescUwagi"],
           points=note["Punkty"],
           show_points=int(note["PokazPunkty"]),
           category_type=bool(note["KategoriaTyp"])
        )
        notes.append(note)
    notes_and_achievements = {
        "notes": notes,
        "achievements": response.json()["data"]["Osiagniecia"]
    }

    return notes_and_achievements

def build_url(subd: str = None, host: str = None, path: str = None, ssl: bool = True, **kwargs):
    if ssl:
        url = 'https://'
    else:
        url = 'http://'
    if subd:
        url += subd + '.'
    url += host
    if path:
        url += path
    if not kwargs.get("symbol"):
        kwargs["symbol"] = "Deflaut"

    for k in kwargs:
        url = url.replace(f"{{{k.upper()}}}", str(kwargs[k]))

    return url


def get_response(data, path):
    session = requests.Session()
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
    }
    data.vulcan_cookies.update(data.student)
    url = build_url(
        subd="uonetplus-uczen",
        path=path,
        symbol=data.symbol,
        host=data.host,
        schoolid=data.school_id,
        ssl=data.ssl
    )
    response = session.post(
        url=url,
        headers=headers,
        cookies=data.vulcan_cookies,
    )
    if response.status_code != 200:
        detail = "UONET+ error code: " + response.status_code
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
    if "Wystąpił błąd aplikacji. Prosimy zalogować się ponownie. Jeśli problem będzie się powtarzał, prosimy o kontakt z serwisem." in response.text:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="UONET+ error"
        )

    return response

def encrypt_cookies(key: str, vulcan_cookies: str):
    fernet = Fernet(bytes(key, "utf-8"))
    cookies = fernet.decrypt((vulcan_cookies).encode())
    cookies = ast.literal_eval(cookies.decode("utf-8"))

    return cookies