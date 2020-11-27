import json
class Course():
	def __init__(self):
		self.id
		self.fullname
		self.shortname
		self.idnumber
		self.summary
		self.summaryformat
		self.startdate
		self.enddate
		self.visible
		self.fullnamedisplay
		self.viewurl
		self.courseimage
		self.progress
		self.hasprogress
		self.isfavourite
		self.hidden
		self.timeaccess
		self.showshortname
		self.coursecategory

	def toclassdata(self,dictionary):
		self.id = dictionary['id']
		self.fullname = dictionary['fullname']
		self.shortname = dictionary['shortname']
		self.idnumber = dictionary['idnumber']
		self.summary = dictionary['summary']
		self.summaryformat = dictionary['summaryformat']
		self.startdate = dictionary['startdate']
		self.enddate = dictionary['enddate']
		self.visible = dictionary['visible']
		self.fullnamedisplay = dictionary['fullnamedisplay']
		self.viewurl = dictionary['viewurl']
		self.courseimage = dictionary['courseimage']
		self.progress = dictionary['progress']
		self.hasprogress = dictionary['hasprogress']
		self.isfavourite = dictionary['isfavourite']
		self.hidden = dictionary['hidden']
		self.timeaccess = dictionary['timeaccess']
		self.showshortname = dictionary['showshortname']
		self.coursecategory = dictionary['coursecategory']

	def todictdata(self):
		dic = {
			'id': self.id,
			'fullname' :self.fullname,
			'shortname': self.shortname, 
			'idnumber': self.idnumber,
			'summary': self.summary,
			'summaryformat': self.summaryformat,
			'startdate' :self.startdate,
			'enddate' :self.enddate,
			'visible': self.visible,
			'fullnamedisplay': self.fullnamedisplay,
			'viewurl': self.viewurl,
			'courseimage': self.courseimage,
			'progress': self.progress,
			'hasprogress' :self.hasprogress,
			'isfavourite' :self.isfavourite,
			'hidden': self.hidden,
			'timeaccess': self.timeaccess,
			'showshortname' :self.showshortname,
			'coursecategory' :self.coursecategory
		}

	def dumpjson(self, dictionary, pathtosavefile):
		lines = json.dumps(dictionary)
		with open(pathtosavefile,'w') as file:
			file.write(lines)

