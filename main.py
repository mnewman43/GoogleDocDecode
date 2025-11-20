import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.auth import default
import requests
import io
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
API_KEY = "API_KEY"

doc_id = 'DOC_ID'

dataFileName = 'dataFile.txt'

def printData(doc_id):
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    # Set up Drive service
    drive_service = build('drive', 'v3', credentials=creds, developerKey=API_KEY)

    # Export and download as Text File
    request = drive_service.files().export_media(fileId=doc_id, mimeType='text/plain')

    try:
        if request:
            with open(dataFileName, 'wb') as file:
                file.write(request.execute())
    except IOError as e:
        print(f"ERROR: {e}")

    with open(dataFileName, 'r') as file:
        for line in file:
            if 'y-coordinate' in line:
                break
        lines = file.readlines()

    maxXCoord = 0
    maxYCoord = 0
    coordinates = []    #List of tuples, index 0 is x-coordinate, index 1 is character, index 2 is y coordinate
    for i in range(1, len(lines), 3):   #Appends data to tuples and finds maximum coords for mapping data
        xCoord = int(lines[i-1].strip())
        yCoord = int(lines[i + 1].strip())
        coordinates.append((xCoord, lines[i].strip(), yCoord))
        if xCoord > maxXCoord:
            maxXCoord = xCoord

        if yCoord > maxYCoord:
            maxYCoord = yCoord

    charMap = [[' ' for i in range(maxXCoord + 1)] for i in range(maxYCoord + 1)]

  
    for i in coordinates:
        charMap[i[2]][i[0]] = i[1]

    charMap.reverse()
    for i in charMap:
        print(*i, sep='')

printData(doc_id)

