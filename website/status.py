# Script for testing status and configuration of the Djanfo server
import json

try:
	file =  open("location_uploads/static/location_uploads/config/db_config.json", "r")
	conf = json.load(file)
	file.close()
	print('')
	print('')
	print('-'*60)
	print('-'*60)
	print('Running Status Check:')
	print('')
	print('Configuration Filed Located')
	print('')
	print('')
	print('Current Configuration:')
	print('')
	print('--- Data Base ---')

	try:
		tables = conf['table_names']

			#Check Surveys
		try:
			tab_surv = tables['surveys']			
			div = tab_surv.split('_')
			if(len(div) == 1):
				print('Survey allocation Unknown: ' + tab_surv)
			elif(div[1] == 'dev'):
				print('Surveys: Development')
			elif(div[1] == 'prod'):
				print('Surveys: Production')
			else:
				print('Survey allocation Unknown: ' + tab_surv)

		except KeyError:
			print('Surveys not allocated')


		#Check locations
		try:
			tab_surv = tables['locations']
			div = tab_surv.split('_')
			if(len(div) == 1):
				print('Locations allocation Unknown: ' + tab_surv)
			elif(div[1] == 'dev'):
				print('Locations: Development')
			elif(div[1] == 'prod'):
				print('Locations: Production')
			else:
				print('Locations allocation Unknown: ' + tab_surv)

		except KeyError:
			print('Locations not allocated')


		#Check summary
		try:
			tab_surv = tables['summary']
			div = tab_surv.split('_')
			if(len(div) == 1):
				print('Summary allocation Unknown: ' + tab_surv)
			elif(div[1] == 'dev'):
				print('Summary: Development')
			elif(div[1] == 'prod'):
				print('Summary: Production')
			else:
				print('Summary allocation Unknown: ' + tab_surv)

		except KeyError:
			print('Summary not allocated')

	except KeyError:
		print('Table Names not allocated')


	print('')
	print('--- Interval ---')

	try:
		sleep_time = conf['sleep_time']

		try:
			sleep_time = int(sleep_time)
			print('Interval Check time: ' + str(sleep_time) + ' Seconds')
		except ValueError:
			print('Interval time not numeric: ' + str(sleep_time))

	except KeyError:
		print('Interval Check time not allocated')


	#Survey machines
	print('')
	print('--- Survey URLs ---')
	try:
		survey_urls = conf['survey_urls']
		if(len(survey_urls) == 0):
			print('No Survey URLs found')
		else:
			for ur in survey_urls:
				if(ur  == "survey"):
					print("survey (local)")
				else:
					print(ur)

	except KeyError:
		print('Survey URLs time not allocated')

	#Jsons machines
	print('')
	print('--- Survey URLs ---')
	try:
		json_urls = conf['json_urls']
		if(len(json_urls) == 0):
			print('No Json URLs found')
		else:
			for ur in json_urls:
				if(ur  == "jsons"):
					print("jsons (local)")
				else:
					print(ur)

	except KeyError:
		print('Json URLs time not allocated')

except FileNotFoundError:
	print('Configuration File no Found')

print('')
print('--- General State ---')

try:
	file =  open("website/settings.py", "r")
	debug = False
	for line in file.readlines():
		if("DEBUG" in line):
			if("True" in line):
				debug = True
			break

	file.close()

	if(debug):
		print('Development (Debug On)')
	else:
		print('Production (Debug Off)')


	print('')
	print('')
	print('Status Check Finished')		
	print('')
	print('-'*60)
	print('-'*60)

except:
	print('Settings File no Found')





