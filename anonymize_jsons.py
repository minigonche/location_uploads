# Anonymize the json scripts
import os
import json
import pickle
import numpy as np

from website.location_uploads import hash_anonymize as ha
from website.location_uploads import process_survey as ps

old_directory = 'scripts/old_jsons/'
new_directory = 'scripts/old_jsons_anonymized/'

corrupt_files = 0
no_student_files = 0
total_files = 0

with open('scripts/json_map.pickle', 'rb') as file:
    json_map = pickle.load(file)

file_names = os.listdir(old_directory)
np.random.shuffle(file_names)

for file_name in file_names:


	json_file = open(old_directory + file_name, 'r')
	try:
		data = json.load(json_file)
	except:
		print('Corrupt File: ' + file_name)
		print('')
		corrupt_files = corrupt_files + 1
		continue
	finally:
		json_file.close()


	old_interview_id = file_name.split('.')[0]
	old_interview_id = old_interview_id.replace(' ','')


	interview_id = ha.anonymize(old_interview_id)


	data['json_hash'] = ha.get_hex_from_json(data)
	data['interview_id'] = interview_id
	if(interview_id in json_map.keys()):
		data['student_id'] = json_map[interview_id]
	else:
		data['student_id'] = 'NA'
		no_student_files = no_student_files +1
		print('No Student Uploaded')

	outfile = open(new_directory + interview_id + '.json', 'w')
	json.dump(data, outfile)
	outfile.close()
	os.remove(old_directory + file_name)

	ps.json_received(data['interview_id'], data['student_id'], data['json_hash'], grupo = 'NINGUNO')

	total_files = total_files + 1
	print(old_interview_id)
	print(interview_id)
	print('')

print('')
print('Finished')
print('Corrupt Files: ' + str(corrupt_files))
print('No Student Files: ' + str(no_student_files))
print('Total Files: ' + str(total_files))
