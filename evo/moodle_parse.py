import sys
import requests
import json
from bs4 import BeautifulSoup

class MoodleParser():
	def __init__(self, login,password):
		self.login = login
		self.password = password
		self.session = None
		self.sesskey = None
	def auth(self):
		headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}
		s = requests.session()
		s.headers.update(headers)
		r = s.get('https://stud.lms.tpu.ru/login/index.php?authSSO=OSSO')
		if r.status_code != requests.codes.ok:
		  print('Lms error')
		  exit(1)

		c = r.content
		soup = BeautifulSoup(c,'lxml')
		svars = {}

		for var in soup.findAll('input',type="hidden"):
			svars[var['name']] = var['value']
		self.session = requests.session()
		r = self.session.post('https://login.oracle.com/mysso/signon.jsp', data=svars)
		data = {'v': svars['v'],
				'site2pstoretoken':svars['site2pstoretoken'],
				'locale': svars['locale'], 
				'appctx': svars['appctx'],
				'ssousername': self.login,
				'password': self.password,
				'domen':'main'}
		r = self.session.post('https://aid.main.tpu.ru/sso/auth',data=data)
		with open('sd.html', 'wb') as file:
			file.write(r.content)
		soup = BeautifulSoup(r.content,"lxml")
		# print(self.session.cookies)
		try:
			text1 = soup.find('font', {'class': 'OraErrorHeader'}).text
		except Exception:
			return 0 
		else:
			print(text1,end = '')
			text1 = soup.find('font', {'class': 'OraErrorText'}).text
			print(text1)
			return 1
	def get_sesskey(self):
		r = self.session.get('https://stud.lms.tpu.ru/my/')
		soup = BeautifulSoup(r.content,"lxml")
		self.sesskey = soup.find('input', {'name': 'sesskey'})['value']
	# def parse_name(self):
	#     r = self.session.get('https://stud.lms.tpu.ru/my/')
	#     soup = BeautifulSoup(r.content,"lxml")
	#     name = soup.find('div', {'class': 'page-header-headings'}).find('h1').text
		# return(name)
	def pase_userdata(self):
		r = self.session.get('https://stud.lms.tpu.ru/my/')
		soup = BeautifulSoup(r.content,"lxml")
		group = soup.find('div',{'class': 'page-context-header'}).find('img', {'class': 'userpicture defaultuserpic'})['alt']
		userid = soup.find('a', {'id': 'message-user-button'})['data-userid']
		fullname = soup.find('div', {'class': 'page-header-headings'}).find('h1').text
		fam,name,otch = fullname.split(' ') 
		dic = {
			'fullname':fullname,
			'familia':fam,
			'name':name,
			'otchestvo':otch,
			'userid':userid,
			'groupname':group
		}
		return(dic)

	def get_resentcources(self,userid):
		params = {
			'sesskey': self.sesskey,
			'info': 'core_course_get_recent_courses'}
		payload = {
			"index":0,
			"methodname":"core_course_get_recent_courses",
			"args":{"userid":userid,"limit":20} }
		headers={'Content-Type':'application/json'}
		r = self.session.post('https://stud.lms.tpu.ru/lib/ajax/service.php',data = '['+json.dumps(payload)+']',headers = headers, params = params)
		courcesjson = json.loads(r.content)
		if not(courcesjson[0]['error']):
			return(courcesjson[0]['data'])
		else: return()

	def get_listofquiz(self,idc):
		url = 'https://stud.lms.tpu.ru/mod/quiz/index.php'
		params = { 'id' : idc}
		r = self.session.get(url, params = params)
		soup = BeautifulSoup(r.content,'lxml')
		svars = {}
		listing = []
		allzad = soup.find('tbody')
		for var in allzad.findAll('tr'):
			href = var.find('td',{'class':'cell c1'}).find('a')['href']
			dic = {
				'week': var.find('td',{'class':'cell c0'}).text,
				'name': var.find('a').text,
				'id': href[href.find('id=')+3:]
				}
			listing.append(dic)
		return(listing)

	def get_listofpopitki(self,idc):
		url = 'https://stud.lms.tpu.ru/mod/quiz/view.php'
		params = { 'id' : idc}
		r = self.session.get(url, params = params)
		soup = BeautifulSoup(r.content,'lxml')
		svars = {}
		listing = []
		allzad = soup.find('tbody')
		for var in allzad.findAll('tr'):
			kogda = var.find('td',{'class':'cell c1'}).find('span',{'class':'statedetails'})
			href = var.find('td',{'class':'cell c3 lastcol'}).find('a')['href']
			dic = {
				'attempt': var.find('td',{'class':'cell c0'}).text,
				'kogdatext': kogda.text,
				'score': var.find('td',{'class':'cell c2'}).text,
				'attemptid': href[href.find("attempt=")+8:href.find("&cmid=")],
				'cmid':href[href.find("&cmid=")+6:]
				}
			listing.append(dic)
		return(listing)
	
	def get_attempt(self,idc,cmid,page=None):
		url = 'https://stud.lms.tpu.ru/mod/quiz/attempt.php'
		params = { 
				'attempt' : idc,
				'cmid' : cmid
				}
		if (page!=None):
			params.update({'page':page})
		r = self.session.get(url, params = params)
		soup = BeautifulSoup(r.content,'lxml')
		svars = {}
		listing = []
		allzad = soup.find('div',{'role':'main'}).find('form').find('div')
		for var in allzad.findAll('div'):
			print(var)
			try:
				var['id']
				idc,numq = var['id'].split('-')[1:]

				dic = {
						'id': idc,
						'numofq': numq,
						'state' : var.find('div',{'class':'state'}).text,
						'grade' : var.find('div',{'class':'grade'}).text
						}
				listing.append(dic)
			except Exception:
				pass
		return(listing)
	

def demo():
	newparcer = MoodleParser('edd7','RayCytQ6')
	if not(newparcer.auth()):
		newparcer.get_sesskey()
		print(newparcer.pase_userdata())
		print(newparcer.get_resentcources("26672")) #userid
		print(newparcer.get_listofquiz(2380)) #id of cource
		print(newparcer.get_listofpopitki(252190)) #id of zadanie idz
		print(newparcer.get_attempt(2248798,252204))
if __name__ == '__main__':
	demo()