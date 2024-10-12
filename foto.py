import os
from flask import Flask
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)
Ftoken = "Ftoken.json"
SCOPES = ['https://www.googleapis.com/auth/drive.file']
def upload_to_drive(file_path):
    creds = None

    if os.path.exists(Ftoken):
        creds = Credentials.from_authorized_user_file(Ftoken, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_console()

        with open(Ftoken, 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Defina o FOLDER_ID aqui
    FOLDER_ID = '1KYUWJvS2adgo8bJzzmwfCBLY7Fa9qPD2'  # Substitua pelo seu ID de pasta

    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [FOLDER_ID]  # Adicione o folder ID aqui
    }
    
    media = MediaFileUpload(file_path, mimetype='image/jpeg')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    file_id = file.get('id')
    service.permissions().create(
        fileId=file_id,
        body={'type': 'anyone', 'role': 'reader'}
    ).execute()

    link_foto = f"https://drive.google.com/thumbnail?sz=w500&id={file_id}"
    return link_foto
