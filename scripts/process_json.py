#Script for exporting JSON and surveys to dataBase
#anal_geografico_2018
import json



def export_json(student_id, interview_id, survey_dict):

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


	
# Process the survey
def export_survey(dict):

	
