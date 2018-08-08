#Script for exporting JSON and surveys to dataBase


import json
import pymysql.cursors
import pandas as pd



# Gets the location of the sattic content
# (Surely there Django does this but I could not figure it out)
def get_static_location():

	#loc = ""
	loc = "location_uploads/static/location_uploads/"
	return loc

def get_config_file():

	file =  open(get_static_location() + "config/db_config.json", "r")
	conf = json.load(file)

	return(conf)


def activity_mapper():

	file =  open(get_static_location() + "config/activity_mapper.json", "r")
	act = json.load(file)

	return(act)



# Gets the table name
def get_table(name):


	conf = get_config_file();

	if(name in conf['table_names'].keys()):
		return conf['table_names'][name]
	else:
		raise ValueError('Table: ' + name + ' not supported in table schemes')


# Gets the databse
def get_data_base():

	conf = get_config_file();

	connection = pymysql.connect(host=conf['host'],
	                     user=conf['user'],
	                     password= conf['password'],
	                     db=conf['db'],
	                     charset='utf8mb4',
	                     cursorclass=pymysql.cursors.DictCursor)

	return(connection)


#Exceute quety on database
def excecute_query(sql):

	connection = get_data_base()

	try:
		with connection.cursor() as cursor:
			# Create a new record	        
			cursor.execute(sql)

		#COmmits changes
		connection.commit()

	finally:
		connection.close()

	return(True)





# Process the survey
# and inserts it into the database
# Assumes the dictionary has the value to insert
# or None, otherwise
def export_survey(responses):

	scheme = pd.read_csv(get_static_location() + 'config/table_survey_scheme.csv')

	line_1 = 'INSERT INTO ' + get_table('surveys') + ' ('
	line_2 = 'VALUES ('




	for ind in scheme.index:

		row = scheme.iloc[ind]

		line_1 = line_1 + row['name'] + ','

		val = responses[row['name']]
		insert_val = val

		if(val is None):
			insert_val = 'NULL'

		elif('VARCHAR' in row['type']):
			insert_val = "'" + val + "'"

		elif('INT' in row['type']):
			insert_val = val

		else:
			raise ValueError("Columna: " + row['name'] + " no es numerica ni cadena de caracteres.")

		line_2 = line_2 + str(insert_val) + ','

	#Adjust the comas
	line_1 = line_1[0:-1] + ')'
	line_2 = line_2[0:-1] + ')'

	sql = line_1 + '\n' + line_2

	return(excecute_query(sql))



def save_json(json_obj, name):
	outfile = open(get_static_location() + 'jsons/' + name + '.json', 'w')
	json.dump(json_obj, outfile)


#inserts the json file into the database by batches
def export_json(student_id, interview_id, data, verbose = False):

	shift_seconds = 946684800

	conf = get_config_file();
	max_insert = conf['max_insert_batch']

	act_mapper = activity_mapper()


	scheme = pd.read_csv(get_static_location() + 'config/table_locations_scheme.csv')

	header = 'INSERT INTO ' + get_table('locations') + ' ('
	

	#Sets up the header
	for ind in scheme.index:

		row = scheme.iloc[ind]
		header = header + row['name'] + ','

	header = header[0:-1] + ') VALUES'	


	sql = header
	counter = 0
	global_counter = 0
	for location in data['locations'][0:-1]:

		temp_loc = {}
		temp_loc['carnet'] = student_id
		temp_loc['id_entrevistado'] = interview_id

		#sends it to seconds from 200/01/01
		temp_loc['timestamp'] = int(int(location['timestampMs'])/1000 - shift_seconds)

		temp_loc['latitude']  = location['latitudeE7']
		temp_loc['longitude'] = location['longitudeE7']

		temp_loc['accuracy'] = None
		if 'accuracy' in location:
			temp_loc['accuracy'] = location['accuracy']

		temp_loc['velocity'] = None
		if 'velocity' in location:
			temp_loc['velocity'] = location['velocity']

		temp_loc['altitude'] = None
		if 'altitude' in location:
			temp_loc['altitude'] = location['altitude']

		temp_loc['vertical_accuracy'] =  None
		if 'verticalAccuracy' in location:
			temp_loc['vertical_accuracy'] = location['verticalAccuracy']


		temp_loc['activity_timestamp'] = None
		temp_loc['activity'] = None
		temp_loc['activity_confidence'] = None

		if('activity' in location):
			act = location['activity'][0]
			temp_loc['activity_timestamp'] = int(int(act['timestampMs'])/1000 - shift_seconds)

			act_type = act['activity'][0]['type']
			if not act_type in act_mapper.keys():
				temp_loc['activity'] = act_mapper['UNKNOWN']
			else:
				temp_loc['activity'] = act_mapper[act_type]
		
			temp_loc['activity_confidence'] = act['activity'][0]['confidence']

		line = '('
		for ind in scheme.index:

			row = scheme.iloc[ind]

			val = temp_loc[row['name']]

			insert_val = val

			if(val is None):
				insert_val = 'NULL'

			elif('VARCHAR' in row['type']):
				insert_val = "'" + val + "'"

			elif('INT' in row['type']):
				insert_val = val

			else:
				raise ValueError("Columna: " + row['name'] + " no es numerica ni cadena de caracteres.")

			line = line + str(insert_val) + ','

		#Adjust the comas

		line = line[0:-1] + ')'

		counter = counter + 1
		global_counter = global_counter +1

		if(counter < max_insert):
			sql = sql +  '\n' + line + ','
		else:
			counter = 0	
			sql = sql + '\n' + line + ';'
			if(verbose):
				print('Batch Inserted')
			excecute_query(sql)
			sql = header

	#last batch
	if(counter > 0):
		sql = sql[0:-1] + ';'
		if(verbose):
			print('Batch Inserted')
		excecute_query(sql)

	if(verbose):
		print('JSON Exported')
	return(global_counter)



def export_json_csv(student_id, interview_id, survey_dict):

	file =  open("data/sample.json", "r")
	file_out = open("data/sample.csv", "w")

	data = json.load(file)

	file_out.write("'timestampMs','latitudeE7','longitudeE7', 'accuracy','velocity','altitude','verticalAccuracy','activity_timestampMs','activity','activity_confidence' \n")

	for location in data['locations']:

		timestampMs = location['timestampMs']
		latitudeE7 = location['latitudeE7']
		longitudeE7 = location['longitudeE7']
		accuracy = ''
		if 'accuracy' in location:
			accuracy = location['accuracy']

		velocity = ''
		if 'velocity' in location:
			velocity = location['velocity']

		altitude = ''
		if 'altitude' in location:
			altitude = location['altitude']

		verticalAccuracy = ''
		if 'verticalAccuracy' in location:
			verticalAccuracy = location['verticalAccuracy']


		activity_timestampMs = ''
		activity = ''
		activity_confidence = ''

		if('activity' in location):
			act = location['activity'][0]
			activity_timestampMs = act['timestampMs']
			activity = act['activity'][0]['type']
			activity_confidence = act['activity'][0]['confidence']

		file_out.write(str(timestampMs) + ',')
		file_out.write(str(latitudeE7) + ',')
		file_out.write(str(longitudeE7) + ',')
		file_out.write(str(accuracy) + ',')
		file_out.write(str(velocity) + ',')
		file_out.write(str(altitude) + ',')
		file_out.write(str(verticalAccuracy) + ',')
		file_out.write(str(activity_timestampMs) + ',')
		file_out.write(str(activity) + ',')
		file_out.write(str(activity_confidence) + '\n')

	file.close()
	file_out.close()
	print('File OK')


	



	
