class CUFS:
    START: str = "/{SYMBOL}/Account/LogOn?ReturnUrl=%2F{SYMBOL}%2FFS%2FLS%3Fwa%3Dwsignin1.0%26wtrealm%3D{REALM}"
    LOGOUT: str = "/{SYMBOL}/FS/LS?wa=wsignout1.0"


class UONETPLUS:
    START: str = "/{SYMBOL}/LoginEndpoint.aspx"
    GETKIDSLUCKYNUMBERS: str = "/{SYMBOL}/Start.mvc/GetKidsLuckyNumbers"
    GETSTUDENTDIRECTORINFORMATIONS: str = (
        "/{SYMBOL}/Start.mvc/GetStudentDirectorInformations"
    )


class UZYTKOWNIK:
    NOWAWIADOMOSC_GETJEDNOSTKIUZYTKOWNIKA: str = (
        "/{SYMBOL}/NowaWiadomosc.mvc/GetJednostkiUzytkownika"
    )


class UCZEN:
    START: str = "/{SYMBOL}/{SCHOOLID}/Start"
    UCZENDZIENNIK_GET: str = "/{SYMBOL}/{SCHOOLID}/UczenDziennik.mvc/Get"
    OCENY_GET: str = "/{SYMBOL}/{SCHOOLID}/Oceny.mvc/Get"
    STATYSTYKI_GETOCENYCZASTKOWE: str = (
        "/{SYMBOL}/{SCHOOLID}/Statystyki.mvc/GetOcenyCzastkowe"
    )
    UWAGIIOSIAGNIECIA_GET: str = "/{SYMBOL}/{SCHOOLID}/UwagiIOsiagniecia.mvc/Get"
    ZEBRANIA_GET: str = "/{SYMBOL}/{SCHOOLID}/Zebrania.mvc/Get"
    SZKOLAINAUCZYCIELE_GET: str = "/{SYMBOL}/{SCHOOLID}/SzkolaINauczyciele.mvc/Get"
    ZAREJESTROWANEURZADZENIA_GET: str = (
        "/{SYMBOL}/{SCHOOLID}/ZarejestrowaneUrzadzenia.mvc/Get"
    )
    ZAREJESTROWANEURZADZENIA_DELETE: str = (
        "/{SYMBOL}/{SCHOOLID}/ZarejestrowaneUrzadzenia.mvc/Delete"
    )
    REJESTRACJAURZADZENIATOKEN_GET: str = (
        "/{SYMBOL}/{SCHOOLID}/RejestracjaUrzadzeniaToken.mvc/Get"
    )
    UCZEN_GET: str = "/{SYMBOL}/{SCHOOLID}/Uczen.mvc/Get"
    REJESTRACJAURZADZENIATOKENCERTYFIKAT_GET: str = (
        "/{SYMBOL}/{SCHOOLID}/RejestracjaUrzadzeniaTokenCertyfikat.mvc/Get"
    )
