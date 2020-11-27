from enum import Enum
from queue import Queue
import os
import time
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import argparse
flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'D:/Desing/group0v81-e066441ff3c2.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

def get_credentials():
    home_FOLDER = os.path.expanduser('~')
    credential_FOLDER = os.path.join(home_FOLDER, '.credentials')
    if not os.path.exists(credential_FOLDER):
        os.makedirs(credential_FOLDER)
    credential_path = os.path.join(credential_FOLDER,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials

#class for GoogleDrive item such as file/folder
class Node():
	class FileType(Enum):
		FILE = 0
		FOLDER = 1

	def __init__(self, path, depth, file_type, file_id):
		self.path = path
		self.depth = depth
		self.file_type = file_type
		self.file_id = file_id
		self.children = []
	
	def print_children(self):
		print('{0}{1}    (ID: {2}    file_type: {3})'.format('  '*self.depth, os.path.basename(self.path), self.file_id, self.file_type))
		for child in self.children:
			child.print_children()
	
	def count_children(self):
		num_files = 0; num_folders = 0
		for child in self.children:
			if child.file_type == Node.FileType.FILE:
				num_files += 1
			if child.file_type == Node.FileType.FOLDER:
				num_folders += 1
			a,b = child.count_children()
			num_files += a; num_folders += b
		return (num_files, num_folders)
	
	#search child items using combined method of BFS-serach and batch-processing
	@classmethod
	def search(cls, start_node, drive_service):
		MAX_API_CALLS_PER_BATCH = 100	#Google says this is the largest value we can use
		MAX_PAGE_SIZE_PER_REQUEST = 10

		#class for single request. We pack these requests, as many as possible (up to 100), into every batch.
		class SingleRequest():
			def __init__(self, node, page_token):
				self.node = node
				self.page_token = page_token

		#callback function for batch proessing.
		#In every batch process, the argument 'request_id' starts at 1 and increases by 1 for each callback.
		#When a batch is completed and another batch starts, 'request_id' returns to 1.
		def callback(request_id, response, exception):
			parent_node, page_token = req_id_vs_single_request_correspondence_table[request_id]	#specify parent node associated with this request, using correspondence table
			print('{0}in callback, request_id: {1}'.format('  '*parent_node.depth, request_id))
			print('{0}parent node: {1}'.format('  '*parent_node.depth, os.path.basename(parent_node.path)))
			if exception:
				if exception._get_reason() == 'User Rate Limit Exceeded' or exception._get_reason() == 'Rate Limit Exceeded':
					print('Rate Limit Exceeded !!!')
					queue.put(SingleRequest(node=parent_node, page_token=page_token))	#re-queue this failed request
					print('{0}re-queueing: {1}'.format('  '*parent_node.depth, os.path.basename(parent_node.path)))
					print('{0}->  queue size: {1}'.format('  '*parent_node.depth, queue.qsize()))
					nonlocal reached_rate_limit
					reached_rate_limit = True	#tell event to batch maker
				else:
					print(exception)
					raise Exception('Unknown Google Drive REST API Error !!!')
				return
			for file in response.get('files', []):
				print('{0}Found file: {1} ({2}), mimeType: {3}'.format('  '*(parent_node.depth+1), file['name'], file['id'], file['mimeType']))
				if file['mimeType'] == 'application/vnd.google-apps.folder':
					file_type = Node.FileType.FOLDER
				else:
					file_type = Node.FileType.FILE
				child = Node(path=parent_node.path+'/'+file['name'], depth=parent_node.depth+1, file_type=file_type, file_id=file['id'])
				parent_node.children.append(child)
				queue.put(SingleRequest(node=child, page_token=None))	#add child node to search queue
				print('{0}queueing: {1}'.format('  '*child.depth, file['name']))
			page_token = response.get('nextPageToken', None)
			if page_token is not None:	#When this response has next chunk, we must put the chunk to request so that it will be handled immediately after currently queued requests.
				print('{0}next page: {1}'.format('  '*parent_node.depth, page_token))
				queue.put(SingleRequest(node=parent_node, page_token=page_token))
				print('{0}queueing: {1}'.format('  '*parent_node.depth, os.path.basename(parent_node.path)))
			print('{0}->  queue size: {1}'.format('  '*(parent_node.depth+1), queue.qsize()))
		
		start_node.children.clear()
		#initialize request queue
		queue = Queue()
		queue.put(SingleRequest(node=start_node, page_token=None))
		reached_rate_limit = False
		print('{0}queueing: {1}'.format('  '*start_node.depth, os.path.basename(start_node.path)))

		while not queue.empty():
			#---------- make batch
			if reached_rate_limit == True:	#When we reached '(User) Rate Limit Exceeded', we have to wait for a seconds, otherwise next batch will fail.
				time.sleep(2)
				reached_rate_limit = False

			batch = drive_service.new_batch_http_request(callback=callback)
			batch_size = 0

			#correspondence table for 'request_id(str)'(an argument for callback function) and associated (node, page_token) pair.
			#This is a dict {request_id: (node,　page_token)}.
			#Sometimes we may encounter '(User) Rate Limit Exceeded' exception because there may be too many items to handle at once, and need to re-queue the failed request.
			#In this time we need (node, page_token) pair information.
			#Since it is difficult to specify, in the callback function, the (node, page_token) pair associated with the request, 
			#we make correspondence table, and refer it in callback function.
			req_id_vs_single_request_correspondence_table = {}

			while (not queue.empty()) and (batch_size < MAX_API_CALLS_PER_BATCH): #pack requests as many as possible
				single_request = queue.get()
				node = single_request.node
				print('{0}pop {1} from queue and adding to batch'.format('  '*node.depth, os.path.basename(node.path)))
				if node.file_type == Node.FileType.FILE:
					continue
				batch.add(
					drive_service.files().list(
						q="'%s' in parents and trashed=false" % node.file_id,
						corpus='user', includeTeamDriveItems=False, orderBy='name', pageSize=100, spaces='drive',
						fields='nextPageToken, files(id, name, mimeType)', supportsTeamDrives=False,
						pageToken=single_request.page_token
					)
				)
				batch_size += 1
				req_id_vs_single_request_correspondence_table[str(batch_size)] = (node, single_request.page_token)
			#----------
			print('{0}->  queue size: {1}'.format('  '*node.depth, queue.qsize()))
			print('executing batch')
			batch.execute()

		print('----------\n')

def main():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('drive', 'v3', http=http)

	start_time = time.time()

	root = Node(path='root', depth=0, file_type=Node.FileType.FOLDER, file_id='root')
	root.search(root, service)
	print('tree structure:\n')
	root.print_children()
	print('\nThere are {0} files and {1} folders.'.format(*root.count_children()))

	print('Search took {0} [sec].'.format(time.time()-start_time))
	
if __name__ == '__main__':
    main()