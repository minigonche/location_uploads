
from location_uploads import process_survey as ps
import json
import os
import time
import datetime
import numpy as np





def write_to_log(message):

	conf = ps.get_config_file()
	log_location = conf['log_location']

	st = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	with open(log_location, "a") as log:
		log.write(str(st) + ": ")
		log.write(message)
		log.write('\n')


#continous loop
while(True):

	conf = ps.get_config_file()
	json_location = conf["json_location"]
	sleep_time = conf["sleep_time"]

	try:

		file_names = os.listdir(json_location)
		np.random.shuffle(file_names)

		if(len(file_names) == 0):
			write_to_log('Nothing found in folder. Sleeping for: ' + str(int(sleep_time/60)) + ' minutes')
			time.sleep(sleep_time)
		else:
			for file_name in file_names:

				if not file_name.endswith('.json'):
					write_to_log('Found: ' + file_name + ' which is not a JSON. Deleting file...')
					os.remove(location + file_name)
				else:
					json_file = open(location + file_name, 'r')
					data = json.load(json_file)

					write_to_log('Exporting: ' + file_name )
					rows = ps.export_json(data['interview_id'], data)
					write_to_log( 'Done. Added: ' + str(rows) + ' records to database. Deleting file...')
					os.remove(location + file_name)

	except Exception as e:
	    write_to_log('-----------------')
	    write_to_log('Error:')
	    write_to_log('-----------------')
	    write_to_log(str(e))
	    write_to_log(' ')
	    write_to_log(' ')












