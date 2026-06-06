import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
load_dotenv()


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def obtener_credenciales():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return creds


def crear_evento_calendar(
    tarea: str,
    fecha: str,
    hora: str,
    recurrente: bool = False
) -> str:
    creds = obtener_credenciales()
    service = build("calendar", "v3", credentials=creds)

    inicio = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    fin = inicio + timedelta(hours=1)

    evento = {
        "summary": tarea,
        "start": {
            "dateTime": inicio.isoformat(),
            "timeZone": "America/Bogota"
        },
        "end": {
            "dateTime": fin.isoformat(),
            "timeZone": "America/Bogota"
        }
    }

    if recurrente:
        evento["recurrence"] = ["RRULE:FREQ=WEEKLY"]

    resultado = service.events().insert(
        calendarId="primary",
        body=evento
    ).execute()

    return resultado["id"]
