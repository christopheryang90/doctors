from flask import Flask
from flask import request
import datetime
import json
from collections import defaultdict
app = Flask(__name__)
# class hospital():
# 	def __init__(self, name):
# 		self.hospital_name = name
# 		self.personel = defaultdict()
# 	def get_doctors(self):
# 		return self.personel.values()
# 	def add_doctor(self,doctor):
# 		self.personel[doctor.name]=doctor
Doctor_dict = {}
class Appointment():
	def __init__(self,name, kind, notes, date, time):
		self.name = name
		self.kind = kind
		self.notes = notes
		self.date = date
		self.time = time
	def update(self,kind,notes):
		self.kind = kind
		self.notes = notes

class Day():
	def __init__(self):
		self.slots = defaultdict(set)
	def add_appointment(self,time,appointment):
		if len(self.slots[time])>=3:
			return False
		else:
			self.slots[time].add(appointment)
			return True
	def get_appointments(self,time=''):
		if time!='':
			return list(self.slots[time])
		else:
			list_of_sets = self.slots.values()
			appointment_list = [x for app_set in list_of_sets for x in app_set]
			return appointment_list
	def delete_appointment(self,time,patient):
		appointments = self.slots[time]
		target = [app for app in appointments if app.name==patient]
		self.slots[time].remove(target)
		return True

class Doctor():
	def __init__(self,name):
		self.name=name
		self.calendar = defaultdict(lambda: Day())
	def add_appointment(self,date_string,time,appointment):
		'''input format: 2019-7-30,  16:20'''
		return self.calendar[date_string].add_appointment(time,appointment)
	def delete_appointment(self,date_string,time,patient):
		return self.calendar[date_string].delete_appointment(time,patient)
	def get_appointments(self,date_string):
		return self.calendar[date_string].get_appointments()
@app.route('/')
def hello_world():
	return 'mellow world'

@app.route('/get_doctors',methods=['GET'])
def get_doctors():
	data = [ {'name': name} for name in Doctor_dict.keys()]
	return json.dumps(data)

@app.route('/get_appointments', methods=['GET'])
def get_appointments():
	doc_name, date_str = request.args.get('doctor'), request.args.get('date')
	appointment_list = Doctor_dict[doc_name].get_appointments(date_str)
	data = [{'name':a.name,'kind':a.kind,'notes':a.notes,'date':a.date,'time':a.time} for a in appointment_list]
	return json.dumps(data)

@app.route('/delete_appointment/<string:doctor>/<string:date>/<string:time>/<string:patient>', methods=['DELETE'])
def delete_appointment(doctor,date,time,patient):
	# items = request.get_json(force=True)
	# print items
	# print request.args
	# doctor, date, time, patient = request.args.get('doctor'),\
	# 		request.args.get('date'),request.args.get('time'),request.args.get('patient')
	print input
	doctor = Doctor_dict[doctor]
	doctor.delete_appointment(date,time,patient)
	return "",200

@app.route('/add_appointment', methods=['POST'])
def add_appointment():
	date,time,patient,doctor,kind,notes = request.form['date'],\
	    request.form['time'],request.form['patient'],request.form['doctor'],\
	    request.form['kind'],request.form['notes']
	appointment = Appointment(name=patient,kind=kind,notes=notes,date=date,time=time)
	doctor = Doctor_dict[doctor]
	doctor.add_appointment(date_string=date,time=time,appointment=appointment)
	return "",200

if __name__ == '__main__':
	#generate some test data
	for x in range(1,5):
		doc_name = 'doc-'+ str(x)
		doc = Doctor(name=doc_name)
		Doctor_dict[doc_name]=doc
		time_obj = datetime.datetime.strptime('10:00','%H:%M')
		for y in range(1,5):
			date_str ='2019-8-2'+str(y)
			for z in range(1,5):
				time_delt = datetime.timedelta(minutes=15)
				new_time_obj = time_obj + (z * time_delt)
				time_str = new_time_obj.strftime('%H:%M')
				appoint = Appointment(name='patient-'+str(z),kind='kind-'+str(z),
				                      notes='',date=date_str,time=time_str)
				doc.add_appointment(date_string=date_str,time=time_str,appointment=appoint)
	#end test data generation
	app_list = Doctor_dict.values()[1].get_appointments('2019-8-24')
	for appoint in app_list:
		print appoint.name, appoint.time

	app.run(debug=True,host='0.0.0.0')