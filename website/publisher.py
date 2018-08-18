
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
				write_to_log('Exporting: ' + file_name )
				if not file_name.endswith('.json'):
					write_to_log('Found: ' + file_name + ' which is not a JSON. Deleting file...')
					os.remove(json_location + file_name)
				else:
					json_file = open(json_location + file_name, 'r')
					data = json.load(json_file)
					json_file.close()
		
					interview_id = data['interview_id']
					json_hash = data['json_hash']
					student_id = data['student_id']

					rows = ps.export_json(interview_id, data)
					ps.json_exported(interview_id, student_id)

					write_to_log( 'Done. Added: ' + str(rows) + ' records to database. Deleting file...')					
					os.remove(json_location + file_name)

			write_to_log('Finished Round. Sleeping for: ' + str(int(sleep_time/60)) + ' minutes')
			time.sleep(sleep_time)

	except Exception as e:
	    write_to_log('-----------------')
	    write_to_log('Error:')
	    write_to_log('-----------------')
	    write_to_log(str(e))
	    write_to_log(' ')
	    write_to_log(' ')












