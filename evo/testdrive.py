from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth import exceptions
from httplib2 import Http
import httplib2
import os
import pprint
import io
import json

class MyGoogleDriveAPI():
	def __init__(self):
		self.rootfolder = "1KOytdjDcgpJqcVQEntSHARJPKUEt4QAX"
		self.errors = {
		-1 : 'Check internet connection',
		-2 : 'Check time settings'
		}
		# print(folder_create(self.google_service,"Accounts",testfolderid))
		return(None)

	def buildservice(self):
		SCOPES = ['https://www.googleapis.com/auth/drive']
		SERVICE_ACCOUNT_FILE = './accfile/group0v81-e066441ff3c2.json'
		credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
		try:
			self.google_service = build('drive', 'v3', credentials=credentials)
		except httplib2.ServerNotFoundError:
			return(-1)
		return(0)

	def file_update_(self, pathtofile, file_id):
		file = self.google_service.files().get(fileId=file_id).execute()
		media = MediaFileUpload(pathtofile, resumable=True)
		result = self.google_service.files().update(fileId=file_id, media_body=media).execute()
		return result

	def file_upload(self, pathtofile, folder_id):
		name = os.path.basename(pathtofile)
		file_metadata = {'name': name,'parents': [folder_id]}
		media = MediaFileUpload(pathtofile, resumable=True)
		result = self.google_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
		return result

	def folder_create(self, folder_name, folder_id):
		file_metadata = {
		'name': folder_name,
		'mimeType': 'application/vnd.google-apps.folder',
		'parents': [folder_id]
		}
		result = self.google_service.files().create(body=file_metadata, fields='id').execute()
		return result.get('id')

	def get_listoffiles(self, folder_id):
		payload = "'" + folder_id + "'" + " in parents"
		try:
			result = self.google_service.files().list(q = payload, pageSize=10, spaces='drive', fields="nextPageToken, files(id, name)").execute()
		except exceptions.RefreshError:
			return(-2)
		return result

def demo():
	googledriveapi = MyGoogleDriveAPI()
	if not(googledriveapi.buildservice()):
		print(googledriveapi.get_listoffiles(googledriveapi.rootfolder))
	else: print(googledriveapi.errors[googledriveapi.buildservice()])
if __name__ == '__main__':
	demo()

# results = service.files().list(q = "'1KOytdjDcgpJqcVQEntSHARJPKUEt4QAX' in parents",pageSize=10,spaces='drive',fields="nextPageToken, files(id, name)").execute()
# print(results)
# update_file(service,'152xGDISi4m6fyRzuYOjVhaZgknNJQm2I','tree.json')