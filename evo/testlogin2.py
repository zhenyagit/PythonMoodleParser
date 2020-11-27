import sys
import requests
import json
from bs4 import BeautifulSoup


def mprint(x):
    sys.stdout.write(x)
    print()
    return


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}

mprint('[-] Initialization...')
s = requests.session()
s.headers.update(headers)
print('done')


mprint('[-] Gathering JSESSIONID..')

# This  should redirect us to the login page 
# On looking at the page source we can find that 
# in the submit form 6 values are submitted (at least at the time of this script)
# try to take those values out using beautiful soup 
# and then do a post request. On doing post https://login.oracle.com/mysso/signon.jsp 
# we will be given message we have the data which is more than necessary
# then it will take us to the form where we have to submit data here 
# https://login.oracle.com/oam/server/sso/auth_cred_submit
# once done we are signed in and doing and requests.get(url) will get you the page you want.
# https://stud.lms.tpu.ru/
r = s.get('https://stud.lms.tpu.ru/login/index.php?authSSO=OSSO')
if r.status_code != requests.codes.ok:
  print('error')
  exit(1)
print('done')

c = r.content
soup = BeautifulSoup(c,'lxml')
svars = {}

for var in soup.findAll('input',type="hidden"):
    svars[var['name']] = var['value']
s = requests.session()
r = s.post('https://login.oracle.com/mysso/signon.jsp', data=svars)

mprint('[-] Trying to submit credentials...')
# inputRaw = open('credentials.json','r')
# login = json.load(inputRaw)


data =  {
        'v': svars['v'],
        'site2pstoretoken':svars['site2pstoretoken'],
        'locale': svars['locale'], 
        'appctx': svars['appctx'],
        'ssousername': 'sdp3',
        'password': 'qC6CloL1',
        'domen':'main'
}

# r = s.post('https://login.oracle.com/oam/server/sso/auth_cred_submit', data=data)

r = s.post('https://aid.main.tpu.ru/sso/auth',data=data)
print(r.text)
# dumping the html page to html file
r = s.get('https://stud.lms.tpu.ru/my/')
print('\n'*10)
soup = BeautifulSoup(r.content,"lxml")
name = soup.find('div', {'class': 'page-header-headings'}).find('h1').text
print(name)

with open('gets.html','wb') as f:
    f.write(r.content)