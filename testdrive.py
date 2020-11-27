from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io
import json
from uploadfiletodrive import update_file

data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)

with open("data_file.json", "r") as read_file:
    data = json.load(read_file)
print(data["president"])
with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
pp = pprint.PrettyPrinter(indent=4)
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'D:/Desing/group0v81-e066441ff3c2.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

results = service.files().list(q = "'1KOytdjDcgpJqcVQEntSHARJPKUEt4QAX' in parents",pageSize=10,spaces='drive',fields="nextPageToken, files(id, name)").execute()
print(results)
update_file(service,'152xGDISi4m6fyRzuYOjVhaZgknNJQm2I','tree.json')