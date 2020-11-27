# from googleapiclient import errors
from googleapiclient.http import MediaFileUpload
# from googleapiclient.discovery import build
from httplib2 import Http
# from oauth2client import file, client, tools
import os


def file_update_(service, pathtofile, file_id):
    file = service.files().get(fileId=file_id).execute()
    media = MediaFileUpload(pathtofile, resumable=True)
    result = service.files().update(fileId=file_id, media_body=media).execute()
    return result

def file_upload(service, pathtofile, folder_id):
    name = os.path.basename(pathtofile)
    file_metadata = {'name': name,'parents': [folder_id]}
    media = MediaFileUpload(pathtofile, resumable=True)
    result = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return result

def folder_create(service, folder_name, folder_id):
	file_metadata = {
    'name': folder_name,
    'mimeType': 'application/vnd.google-apps.folder',
    'parents': [folder_id]
	}
	result = service.files().create(body=file_metadata, fields='id').execute()
	return result.get('id')

def  get_listoffiles(service, folder_id):
	payload = "'" + folder_id + "'" + " in parents"
	result = service.files().list(q = payload, pageSize=10, spaces='drive', fields="nextPageToken, files(id, name)").execute()
	return result