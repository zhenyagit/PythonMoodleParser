import requests 
from bs4 import BeautifulSoup

def login():
	rsess = requests.Session()
	# r = rsess.get('https://stud.lms.tpu.ru/login/index.php?authSSO=NOOSSO')
	# r = rsess.get('https://stud.lms.tpu.ru/login/index.php')
	r = rsess.get('https://aid.main.tpu.ru/sso/jsp/login.jsp')
	c = r.content
	soup = BeautifulSoup(c,'lxml')
	svars = {}

	for var in soup.findAll('input',type="hidden"):
		svars[var['name']] = var['value']
	print("*&"*20)
	print(svars)
	print("*&"*20)
	
	print(c)
	print(soup)
	print(rsess.cookies)
	s = requests.session()
	r = s.post('https://login.oracle.com/mysso/signon.jsp', data=svars)


	data =  {
			'logintoken':svars['logintoken'],
			'ssousername': 'edd7',
			'password': 'RayCytQ6',
	}

	r = s.post('https://login.oracle.com/oam/server/sso/auth_cred_submit', data=data)
	r = s.get('https://aid.main.tpu.ru/sso/jsp/login.jsp',data=data)
	with open('test.html','w') as f:
   		f.write(r.content)
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'ru',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Content-Length': '83',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Cookie': 'MoodleSession=421ea110b36c7ed838b973dfaf5d0019',
		'Host': 'stud.lms.tpu.ru',
		'Origin': 'https://stud.lms.tpu.ru',
		'Referer': 'https://stud.lms.tpu.ru/login/index.php?authSSO=NOOSSO',
		'Sec-Fetch-Dest': 'document',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-Site': 'same-origin',
		'Sec-Fetch-User': '?1',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
	data = {
			'anchor':'',
			'logintoken': 'z6isayC4uAsAttDLhil1vbC7lcyEKy0C',
			'username': 'edd7',
			'password': 'RayCytQ6'}
	rheaders = {
		'Cache-Control': 'no-store, no-cache, must-revalidate',
		'Connection': 'keep-alive',
		'Content-Language': 'ru',
		'Content-Type': 'text/html; charset=utf-8',
		'Date': 'Sat, 19 Sep 2020 11:26:48 GMT',
		'Expires': 'Thu, 19 Nov 1981 08:52:00 GMT',
		'Location': 'https://stud.lms.tpu.ru/login/index.php',
		'Pragma': 'no-cache',
		'Server': 'nginx/1.16.1',
		'Transfer-Encoding': 'chunked',
		'X-Powered-By': 'PHP/7.3.9'}
	req = rsess.post('https://aid.main.tpu.ru/sso/auth',data=data)
	print(req.text)
	print(req)
	return(0)
t = login()
print(t)