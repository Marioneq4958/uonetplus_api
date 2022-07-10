from turtle import circle
from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.requests import Request
from app import models, paths, resources
import requests
from datetime import datetime
from cryptography.fernet import Fernet
import ast

router = APIRouter()

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

def get_response(data: dict, path: str, session_cookies: dict) -> requests.models.Response:
    session = requests.Session()
    session_cookies.update(data.register_cookies)
    url = build_url(
        subd="uonetplus-uczen",
        path=path,
        symbol=data.symbol,
        host=data.host,
        schoolid=data.school_id,
        ssl=data.ssl,
    )
    response = session.post(
        url=url,
        headers=data.headers,
        json=data.payload,
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
        session_data = ast.literal_eval(fernet.decrypt(session_data.encode("utf-8")).decode("utf-8"))
        if session_data['expire'] != None and session_data['session_cookies'] != None:
            if datetime.timestamp(datetime.utcnow())*1000 > float(session_data['expire']):
                raise credentials_exception
        else:
            raise credentials_exception
        return dict(session_data['session_cookies'])
    except:
        raise credentials_exception

@router.post("/notes", response_model=models.NotesAndAchievements)
def get_notes(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UCZEN.UWAGIIOSIAGNIECIA_GET
    response = get_response(data, path, session_cookies)
    notes = []
    for note in response.json()["data"]["Uwagi"]:
        note = models.Note(
            date=datetime.fromisoformat(note["DataWpisu"]).strftime("%d.%m.%Y %H:%M"),
            teacher=note["Nauczyciel"],
            category=note["Kategoria"],
            content=note["TrescUwagi"],
            points=note["Punkty"],
            show_points=int(note["PokazPunkty"]),
            category_type=bool(note["KategoriaTyp"]),
        )
        notes.append(note)
    notes_and_achievements = models.NotesAndAchievements(
        notes=notes, achievements=response.json()["data"]["Osiagniecia"]
    )
    return notes_and_achievements

@router.post("/school-info", response_model=models.SchoolInfo)
def get_school_info(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UCZEN.SZKOLAINAUCZYCIELE_GET
    response = get_response(data, path, session_cookies)
    teachers = []
    school = models.School(
        name=response.json()["data"]["Szkola"]["Nazwa"],
        address=response.json()["data"]["Szkola"]["Adres"],
        contact=response.json()["data"]["Szkola"]["Kontakt"],
        headmaster=response.json()["data"]["Szkola"]["Dyrektor"],
        pedagogue=response.json()["data"]["Szkola"]["Pedagog"],
    )
    for teacher in response.json()["data"]["Nauczyciele"]:
        teacher = models.Teacher(name=teacher["Nauczyciel"], subject=teacher["Nazwa"])
        teachers.append(teacher)
    school_info = models.SchoolInfo(school=school, teachers=teachers)
    return school_info

@router.post("/conferences", response_model=list[models.Conference])
def get_conferences(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UCZEN.ZEBRANIA_GET
    response = get_response(data, path, session_cookies)
    conferences = []
    for conference in response.json()["data"]:
        split = conference["Tytul"].split(", ")
        try:
            place = split[2]
        except:
            place = None
        try:
            date = datetime.fromisoformat(conference["DataSpotkania"]).strftime("%d.%m.%Y %H:%M")
        except:
            date = None
        conference = models.Conference(
            id=conference["Id"],
            subject=conference["TematZebrania"],
            agenda=conference["Agenda"],
            present_at_conference=conference["ObecniNaZebraniu"],
            online=conference["ZebranieOnline"],
            date=date,
            place=place
        )
        conferences.append(conference)
    return conferences

@router.post("/grades", response_model=models.Grades)
def get_grades(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UCZEN.OCENY_GET
    response = get_response(data, path, session_cookies)
    subjects = []
    descriptive_grades = []
    for subject in response.json()["data"]["Oceny"]:
        subject_grades = []
        for grade in subject["OcenyCzastkowe"]:
            if "(" in grade["Wpis"]:
                comment = grade["Wpis"].split("(")[1].replace(")", "")
                entry = grade["Wpis"].split("(")[0]
            else:
                comment = None
                entry = grade["Wpis"]
            color = str(grade["KolorOceny"]).replace("0", "black").replace("7261447", "green").replace(
                "11627761", "purple").replace("15748172", "red").replace("2139383", "blue")
            if "/" in entry:
                comment = grade["Wpis"]
                entry = str(int(int(entry.split("/")[0]) * 100 / int(entry.split("/")[1]))) + "%"
            weight = grade["Waga"]
            weight = f"{weight:.2f}"
            grade = models.Grade(
                entry=entry,
                comment=comment,
                color=color,
                symbol=grade["KodKolumny"],
                description=grade["NazwaKolumny"],
                weight_value=weight,
                date=grade["DataOceny"],
                teacher=grade["Nauczyciel"],
            )
            subject_grades.append(grade)
            subject_grades.sort(key=lambda t: datetime.strptime(t.date, "%d.%m.%Y"), reverse=True)
        subject = models.Subject(
            name=subject["Przedmiot"],
            visible_subject=subject["WidocznyPrzedmiot"],
            position=subject["Pozycja"],
            average=subject["Srednia"],
            proposed_grade=subject["ProponowanaOcenaRoczna"],
            points=subject["SumaPunktow"],
            final_grade=subject["OcenaRoczna"],
            proposed_points=subject["ProponowanaOcenaRocznaPunkty"],
            final_points=subject["OcenaRocznaPunkty"],
            grades=subject_grades,
        )
        subjects.append(subject)
    for descriptive_grade in response.json()["data"]["OcenyOpisowe"]:
        descriptive_grade = models.DescriptiveGrade(
            subject=descriptive_grade["NazwaPrzedmiotu"],
            description=descriptive_grade["Opis"],
            is_religion_or_ethics=descriptive_grade["IsReligiaEtyka"],
        )
        descriptive_grades.append(descriptive_grade)
    grades = models.Grades(
        is_average=response.json()["data"]["IsSrednia"],
        is_points=response.json()["data"]["IsPunkty"],
        subjects=subjects,
        descriptive_grades=descriptive_grades,
    )
    return grades

@router.post("/mobile-access/get-registered-devices", response_model=list[models.Device])
def get_registered_devices(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UCZEN.ZAREJESTROWANEURZADZENIA_GET
    response = get_response(data, path, session_cookies)
    registered_devices = []
    for device in response.json()["data"]:
        device = models.Device(
            id=device["Id"],
            name=device["NazwaUrzadzenia"],
            create_date=datetime.fromisoformat(device["DataUtworzenia"]).strftime("%d.%m.%Y %H:%M"),
        )
        registered_devices.append(device)
    return registered_devices

@router.post("/mobile-access/register-device", response_model=models.TokenResponse)
def get_register_device_token(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UCZEN.REJESTRACJAURZADZENIATOKEN_GET
    response = get_response(data, path, session_cookies)
    token_response = models.TokenResponse(
        token=response.json()["data"]["TokenKey"],
        symbol=response.json()["data"]["CustomerGroup"],
        pin=response.json()["data"]["PIN"],
        qr_code_image=response.json()["data"]["QrCodeImage"],
    )
    return token_response

@router.post("/mobile-access/delete-registered-device")
def delete_registered_device(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UCZEN.ZAREJESTROWANEURZADZENIA_DELETE
    response = get_response(data, path, session_cookies)
    return response.json()

@router.post("/mobile-access/register-device-check")
def register_device_check(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path = paths.UCZEN.REJESTRACJAURZADZENIATOKENCERTYFIKAT_GET
    response = get_response(data, path, session_cookies)
    return response.json()

class Test:
    def __init__(self, IsAuthorized, IsPrzedszkola, IsStudentParent, IsWychowankowie):
        self.IsAuthorized = IsAuthorized
        self.IsPrzedszkola = IsPrzedszkola
        self.IsStudentParent = IsStudentParent
        self.IsWychowankowie = IsWychowankowie 
        self.Test()


    def Test(self):
        global Oceny, Frekwencja, EwidencjaObecności, PlanLekcji, Sprawdzany, EgzaminySemestralne, EgzaminyZewnetrzne, ZadaniaDomowe, Uwagi, Zebrania, Jadłospis, Ogłoszenia, Podręczniki, SzkołaiNauczyciele, InfoUczen, DostępMobilny, Formularze, DostępOffice, Wiadomości
        if self.IsAuthorized == False:
            Oceny = False
            Frekwencja = False
            EwidencjaObecności = False
            PlanLekcji = False
            Sprawdzany = False
            EgzaminyZewnetrzne = False
            EgzaminySemestralne = False
            ZadaniaDomowe = False
            Uwagi = False
            Zebrania = False
            Jadłospis = False
            Ogłoszenia = False
            Podręczniki = False
            SzkołaiNauczyciele = False
            InfoUczen = False
            DostępMobilny = False
            Formularze = False
            DostępOffice = False 
            Wiadomości = False
        else:
            if self.IsPrzedszkola == True and not self.IsStudentParent == False:
                    Oceny = False
                    Frekwencja = False
                    EwidencjaObecności = True
                    PlanLekcji = False
                    Sprawdzany = False
                    EgzaminyZewnetrzne = False
                    EgzaminySemestralne = False
                    ZadaniaDomowe = False
                    Uwagi = False
                    Zebrania = False
                    Jadłospis = False
                    Ogłoszenia = False
                    Podręczniki = False
                    SzkołaiNauczyciele = False
                    InfoUczen = True
                    DostępMobilny = True
                    Formularze = False
                    DostępOffice = False 
                    Wiadomości = True
            else:
                if self.IsWychowankowie == True and not self.IsStudentParent == False:
                        Oceny = False
                        Frekwencja = False
                        EwidencjaObecności = True
                        PlanLekcji = False
                        Sprawdzany = False
                        EgzaminyZewnetrzne = False
                        EgzaminySemestralne = False
                        ZadaniaDomowe = False
                        Uwagi = False
                        Zebrania = True
                        Jadłospis = True
                        Ogłoszenia = False
                        Podręczniki = False
                        SzkołaiNauczyciele = True
                        InfoUczen = True
                        DostępMobilny = False
                        Formularze = False
                        DostępOffice = False 
                        Wiadomości = True
                else:
                    if self.IsWychowankowie == True and not self.IsStudentParent == True:
                            Oceny = False
                            Frekwencja = False
                            EwidencjaObecności = True
                            PlanLekcji = False
                            Sprawdzany = False
                            EgzaminyZewnetrzne = False
                            EgzaminySemestralne = False
                            ZadaniaDomowe = False
                            Uwagi = False
                            Zebrania = False
                            Jadłospis = True
                            Ogłoszenia = False
                            Podręczniki = False
                            SzkołaiNauczyciele = True
                            InfoUczen = True
                            DostępMobilny = False
                            Formularze = False
                            DostępOffice = False 
                            Wiadomości = True
                    else:
                        if not self.IsWychowankowie == True and not self.IsStudentParent == True and not self.IsPrzedszkola == True and not self.IsAuthorized:
                                Oceny = True
                                Frekwencja = True
                                EwidencjaObecności = True
                                PlanLekcji = True
                                Sprawdzany = True
                                EgzaminyZewnetrzne = True
                                EgzaminySemestralne = False
                                ZadaniaDomowe = True
                                Uwagi = True
                                Zebrania = True
                                Jadłospis = False
                                Ogłoszenia = True
                                Podręczniki = True
                                SzkołaiNauczyciele = True
                                InfoUczen = True
                                DostępMobilny = True
                                Formularze = True
                                DostępOffice = False 
                                Wiadomości = True
@router.post("/get-block-info")
def get_blocks_info(data: models.UonetPlusUczen, request: Request):
    session_cookies = decrypt_session_data(request, data.session_data)
    path1 = paths.UCZEN.UCZENCACHE_GET
    path2 = paths.UCZEN.UCZENDZIENNIK_GET
    response1 = get_response(data, path1, session_cookies)
    response2 = get_response(data, path2, session_cookies)
    for i in response2.json()["data"]:
        if i["IdDziennik"] == int(data.register_cookies["idBiezacyDziennik"]):
            global RokSzkolny, IdDziennik, IsArtystyczna, IsArtystyczna13, IsSpecjalny, IsPrzedszkola, IsArchiwalny, IsOplaty, IsPayButton, IsWychowankowie, IsPlatnosci, IsDorosli, IsPolicealna, Is13, IsAuthorized, IsAdult, IsStudentParent
            RokSzkolny = i['DziennikRokSzkolny']
            IdDziennik = i["IdDziennik"]
            IsArtystyczna = i["IsArtystyczna"]
            IsArtystyczna13 = i["IsArtystyczna13"]
            IsSpecjalny = i["IsSpecjalny"]
            IsPrzedszkola = i["IsPrzedszkola"]
            IsArchiwalny = i["IsArchiwalny"]
            IsOplaty = i["IsOplaty"]
            IsPayButton = i["IsPayButtonOn"]
            IsWychowankowie = i["IsWychowankowie"]
            IsPlatnosci = i["IsPlatnosci"]
            IsDorosli = i["IsDorosli"]
            IsPolicealna = i["IsPolicealna"]
            Is13 = i["Is13"]
            IsAuthorized = i["IsAuthorized"]
            IsAdult = i["IsAdult"]
            IsStudentParent = i["IsStudentParent"]
            break
        else:
            raise Exception("Nie znaleziono dziennika")
    Test(IsAuthorized, IsPrzedszkola, IsStudentParent, IsWychowankowie)
    block_inf = {
        "datefromtheserver": response1.json()["data"]["serverDate"],
        "authorised": IsAuthorized,
        "register_id": IdDziennik,
        "schoolyear": RokSzkolny,
        "Blockages": {
            "TypeSchool":{
                "Special": IsSpecjalny,
                "Kindergarten": IsPrzedszkola,
                "Artistic": IsArtystyczna,
                "Artistic13": IsArtystyczna13,
                "Post-secondary": IsPolicealna,
                "Reformatory": IsWychowankowie
            },
            "TypeStudent":{
                "Student18yearsold": IsAdult,
                "StudentParent": IsStudentParent,
                "StudentAdult": IsDorosli,
                "StudentArchive": IsArchiwalny,
                "Parent": response1.json()["data"]["isParentUser"],
                "KidParent": response1.json()["data"]["isPupilUser"],
                "Is13": Is13
            },
            "FrontendBlockages":{
                "AccessMenu": response1.json()["data"]["isMenuOn"],
                "AccessFees": IsOplaty,
                "AccessPayment": IsPayButton,
                "AccesstotheRealisedLessons": response1.json()["data"]["pokazLekcjeZrealizowane"],
                "AccesstothePlannedLessons": response1.json()["data"]["pokazLekcjeZaplanowane"], 
                "AccessBooks": response1.json()["data"]["isPodrecznikiOn"],
                "AccessOffice": response1.json()["data"]["isDostepOffice"],
                "LoginO365Hidden": response1.json()["data"]["isO365LoginOff"],
                "PasswordO365Hidden": response1.json()["data"]["isO365PassOff"], 
                "PaymentsOff": response1.json()["data"]["isPayButtonOn"], 
                "AccesstothePayments": IsPlatnosci,
                "AttachmentsOnedrive": response1.json()["data"]["isHomeworksOneDriveAttachmentsOn"],
                "AttachmentsGoogleDrive": response1.json()["data"]["isHomeworksGoogleDriveAttachmentsOn"]
            },
            "BlockadesList":{
                "Oceny": Oceny,
                "Frekwencja": Frekwencja,
                "EwidencjaObecnosci": EwidencjaObecności,
                "PlanLekcji": PlanLekcji,
                "Sprawdzany": Sprawdzany,
                "EgzaminyZewnetrzne": EgzaminyZewnetrzne,
                "EgzaminySemestralne": EgzaminySemestralne,
                "ZadaniaDomowe": ZadaniaDomowe,
                "Uwagi": Uwagi,
                "Zebrania": Zebrania,
                "Jadlospis": Jadłospis,
                "Ogłoszenia": Ogłoszenia,
                "Podreczniki": Podręczniki,
                "SzkołaINauczyciele": SzkołaiNauczyciele,
                "DaneUcznia": InfoUczen,
                "DostepMobilny": DostępMobilny,
                "Formularze": Formularze,
                "DostepOffice": DostępOffice,
                "Wiadomosci": Wiadomości,

            }
        }
    }
    return block_inf