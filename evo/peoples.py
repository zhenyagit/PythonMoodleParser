import json
# from main import *
class  Person():
	def __init__(self):	
		pass

	# def toclassdata(self,dictionary):
	# 	self.fullname = dictionary['fullname']
	# 	self.familia = dictionary['familia']
	# 	self.name = dictionary['name']
	# 	self.otchestvo = dictionary['otchestvo']
	# 	self.userid = dictionary['userid']
	# 	self.groupname = dictionary['groupname']

	# def todictdata(self):
	# 	dic = {
 #            'fullname': self.fullname ,
 #            'familia': self.familia ,
 #            'name': self.name,
 #            'otchestvo': self.otchestvo,
 #            'userid': self.userid,
 #            'groupname': self.groupname}
 #        return(dic)
	def update_data(self,dictionary):
		self.person_dat.update(dictionary)
	def dumpjson(self, dictionary,pathtosavefile):
		lines = json.dumps(dictionary)
		with open(pathtosavefile,'w') as file:
			file.write(lines)
	def ChAL_data(self,pathtosavefile):
		try:
			f = open(pathtosavefile,'r')
			self.person_data = json.load(f)
			f.close()
		except IOError:
			with open(pathtosavefile,'w') as f:
				self.person_data = {
					'name': "DefaultName"
				}
				self.dumpjson(self.person_data,pathtosavefile)
			return 0
