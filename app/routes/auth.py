from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import requests
import re
from app import models, paths, resources

router = APIRouter()


@router.post("/signin", response_model=list[models.RegisterSymbol])
def signin(data: models.Login, request: Request):
    key = Fernet.generate_key().decode("utf8")
    session: requests.sessions.session = requests.Session()
    cert: dict = send_credentials(
        data.username, data.password, data.host, "Default", data.ssl, session)
    key = Fernet.generate_key().decode("utf8")
    res = []
    symbols = extract_symbols(cert["wresult"])
    if not symbols:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=resources.no_students_account
        )
    for symbol in symbols:
        cert: dict = send_credentials(data.username, data.password, data.host, symbol, data.ssl, session)
        cert_response = send_cert(data.host, symbol, data.ssl, cert, session)
        soup = BeautifulSoup(cert_response.text, "html.parser")
        if not "nie został zarejestrowany" in cert_response.text:
            schools = []
            school_ids = extract_school_ids(cert_response.text)
            for school_id in school_ids:
                url = build_url(
                    subd="uonetplus-uczen",
                    path=paths.UCZEN.START,
                    symbol=symbol,
                    host=data.host,
                    schoolid=school_id,
                    ssl=data.ssl,
                )
                response = session.get(url)
                school_name = get_script_param(response.text, "organizationName")
                anti_forgery_token = get_script_param(response.text, "antiForgeryToken")
                app_guid = get_script_param(response.text, "appGuid")
                version = get_script_param(response.text, "version")
                students = get_students_from_school(data.host, symbol, school_id, data.ssl, session)
                schools.append(
                    models.RegisterSchool(
                        name=school_name,
                        id=school_id,
                        headers={
                            "Accept": "*/*",
                            "Accept-Encoding": "gzip, deflate, br",
                            "Connection": "keep-alive",
                            "X-V-AppVersion": version,
                            "X-V-AppGuid": app_guid,
                            "X-V-RequestVerificationToken": anti_forgery_token,
                        },
                        students=students
                    )
                )
            session_data = encrypt_session_data(session, request, key)
            res.append(
                models.RegisterSymbol(
                    name=symbol,
                    session_data=session_data,
                    schools=schools
                )
            )

    return res


def send_credentials(username: str, password: str, host: str, symbol: str, ssl: bool, session: requests.sessions.Session) -> dict:
    realm = build_url(subd="uonetplus", host=host, ssl=ssl)
    url = build_url(
        subd="cufs",
        host=host,
        path=paths.CUFS.START,
        realm=quote(quote(realm, safe=""), safe=""),
        symbol=symbol,
        ssl=ssl,
    )
    credentials = {"LoginName": username, "Password": password}
    try:
        credentials_response = session.post(url=url, data=credentials)
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=resources.INVALID_HOST)
    check_errors(credentials_response.text)
    cert = create_cert(credentials_response.text)
    return cert


def check_errors(credentials_response: str):
    soup = BeautifulSoup(credentials_response, "lxml")
    error_tag = soup.select_one(
        ".ErrorMessage, #ErrorTextLabel, #loginArea #errorText")
    if error_tag:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=resources.INCORRECT_CREDENTIALS
        )


def create_cert(credentials_response: str) -> dict:
    soup = BeautifulSoup(credentials_response, "lxml")
    wa: str = soup.select_one('input[name="wa"]')["value"]
    wresult: str = soup.select_one('input[name="wresult"]')["value"]
    wctx_tag = soup.select_one('input[name="wctx"]')
    wctx: str = wctx_tag["value"] if wctx_tag else None
    cert = {"wa": wa, "wresult": wresult, "wctx": wctx}

    return cert


def build_url(subd: str = None, host: str = None, path: str = None, ssl: bool = True, **kwargs) -> str:
    if ssl:
        url = "https://"
    else:
        url = "http://"
    if subd:
        url += subd + "."
    url += str(host)
    if path:
        url += path
    if not kwargs.get("symbol"):
        kwargs["symbol"] = "Deflaut"

    for k in kwargs:
        url = url.replace(f"{{{k.upper()}}}", str(kwargs[k]))

    return url


def encrypt_session_data(session: requests.sessions.Session, request: Request, key: str) -> str:
    expire = datetime.timestamp(datetime.utcnow() + timedelta(minutes=14))*1000
    request.session["session_key"] = key
    fernet = Fernet(bytes(key, "utf-8"))
    session_cookies = session.cookies.get_dict()
    session_data = fernet.encrypt(
        str(
            {
                "session_cookies": session_cookies,
                "expire": expire
            }
        ).encode("utf-8")
    )

    return session_data


def send_cert(host: str, symbol: str, ssl: bool, cert: dict, session: requests.sessions.Session) -> requests.models.Response:
    url = build_url(
        subd="uonetplus",
        path=paths.UONETPLUS.START,
        symbol=symbol,
        host=host, ssl=ssl
    )
    cert_response = session.post(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"
        },
        data=cert,
    )
    return cert_response


def get_students_from_school(
    host: str,
    symbol: str,
    school_id: str,
    ssl: bool,
    session: requests.sessions.Session,
) -> list[models.RegisterStudent]:
    students = []
    url = build_url(
        subd="uonetplus-uczen",
        path=paths.UCZEN.UCZENDZIENNIK_GET,
        symbol=symbol,
        host=host,
        schoolid=school_id,
        ssl=ssl,
    )
    students_response = session.post(url)
    for student in students_response.json()["data"]:
        semesters = []
        for semester in student["Okresy"]:
            semester = models.RegisterSemester(
                number=semester["NumerOkresu"],
                level=semester["Poziom"],
                start=datetime.fromisoformat(semester["DataOd"]),
                end=datetime.fromisoformat(semester["DataDo"]),
                class_id=semester["IdOddzial"],
                unit_id=semester["IdJednostkaSprawozdawcza"],
                current=semester["IsLastOkres"],
                id=semester["Id"],
            )
            semesters.append(semester)
        student = models.RegisterStudent(
            id=student["Id"],
            student_id=student["IdUczen"],
            student_name=student["UczenImie"],
            student_second_name=student["UczenImie2"],
            student_surname=student["UczenNazwisko"],
            is_register=student["IsDziennik"],
            register_id=student["IdDziennik"],
            kindergarten_register_id=student["IdPrzedszkoleDziennik"],
            level=student["Poziom"],
            symbol=student["Symbol"],
            name=student["Nazwa"],
            year=student["DziennikRokSzkolny"],
            start=datetime.fromisoformat(student["DziennikDataOd"]),
            end=datetime.fromisoformat(student["DziennikDataDo"]),
            full_name=student["UczenPelnaNazwa"],
            cookies={
                "idBiezacyDziennik": str(student["IdDziennik"]),
                "idBiezacyUczen": str(student["IdUczen"]),
                "idBiezacyDziennikPrzedszkole": str(student["IdPrzedszkoleDziennik"]),
                "biezacyRokSzkolny": str(student["DziennikRokSzkolny"]),
            },
            semesters=semesters,
        )
        students.append(student)
    return students


def get_script_param(text: str, param: str, default: str = None) -> str:
    m = re.search(f"{param}: '(.+?)'", text)
    return m.group(1) if m else default


def extract_symbols(wresult: str) -> list[str]:
    soup = BeautifulSoup(wresult.replace(":", ""), "lxml")
    symbol_tags = soup.select(
        'samlAttribute[AttributeName$="Instance"] samlAttributeValue'
    )
    symbols = [symbol_tag.text.strip() for symbol_tag in symbol_tags]
    symbols = [symbol for symbol in symbols if re.compile(
        r"[a-zA-Z0-9]*").fullmatch(symbol)]

    return symbols


def extract_school_ids(text: str) -> list[str]:
    soup = BeautifulSoup(text, "html.parser")
    school_tags = soup.select(
        '.panel.linkownia.pracownik.klient a[href*="uonetplus-uczen"]')
    school_ids = [school_tag["href"].split("/")[4] for school_tag in school_tags]
    return school_ids