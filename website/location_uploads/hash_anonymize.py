import json
import hashlib
from datetime import datetime
import pytz
import re


# Gets the hex from the json
def get_hex_from_json(json_object):

	string_json = json.dumps(json_object, sort_keys=True).encode()
	return(hashlib.md5(string_json).hexdigest())	


def anonymize(entry_string, max_len = 18):

	if(entry_string == ""):
		return('0')
	
	#Eliminates unsupported charachters
	entry_string = re.sub('[^0-9a-zA-Z]+', '0', entry_string)
	entry_string = entry_string[(-1*min(max_len, len(entry_string))):]


	entry_string = entry_string.lower()
	out_string = ''

	switch = 1

	for i in range(len(entry_string)):
		new_char = ""
		if(entry_string[i].isalpha()):
			new_number = string.ascii_lowercase.index(entry_string[i])
			new_number = (new_number + switch*(i+1))%26
			new_char = string.ascii_lowercase[new_number]
		else:
			new_number = int(entry_string[i])
			new_number = (new_number + switch*(i+1))%10
			new_char = str(new_number)

		out_string = out_string + new_char
		switch = switch*(-1)
			

	return(out_string)


def get_timestamp(location = "America/Bogota"):
	server_timezone = pytz.timezone(location)
	server_time = datetime.now(server_timezone)
	return(int(server_time.timestamp()))

