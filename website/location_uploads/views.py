from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas as pd
import json

from location_uploads import process_survey as ps
from location_uploads import hash_anonymize as ha


# Create your views here.

def index(request):
    return render(request, 'location_uploads/index.html', None)


def upload_info(request):

	anonymize = True

	data = {}

	if "GET" == request.method:
		data['mensaje_error'] = "Se produjo el siguiente error en el servidor: \n" + "Method is set to GET." + "\n\n" + "Por favor comuníquese con el monitor."
		return render(request, 'location_uploads/error.html', data)

    # if not GET, then proceed
	#try:

	student_id = request.POST.get('carnet')
	interview_id = request.POST.get('id_entrevistado')
		
	if(anonymize):
			interview_id = ha.anonymize(interview_id)


	#gets the status
	upload_status = ps.check_interview_status(interview_id = interview_id, student_id = student_id)
	interview_id_status = ps.check_interview_id_status(student_id = student_id, interview_id = interview_id)

	#If already finished the process
	if(upload_status == "FOUND_BOTH"):
		data['mensaje_error'] = "Lo sentimos, pero el estudiante: " + student_id + " ya subió la información de la encuesta y el archivo.json para la persona con identificación: " + request.POST.get('id_entrevistado') +  "."
		return render(request, 'location_uploads/error.html', data)


	#Survey case
	if(request.POST.get('tipo_encuesta') == 'informacion'):

		#IF already uploaded the survey
		if(upload_status == "FOUND_SURVEY"):
			data['mensaje_error'] = "Lo sentimos, pero el estudiante: " + student_id +  " ya subió la información de la encuesta para la persona con identificación: " + request.POST.get('id_entrevistado') +  "."
			return render(request, 'location_uploads/error.html', data)

		#If other student uploaded that info
		if(interview_id_status == "UPLOADED"):
			data['mensaje_error'] = "Lo sentimos, pero la persona con identificación: " + request.POST.get('id_entrevistado') +  " ya se encuentra en proceso de entrevista con otro estudiante."
			return render(request, 'location_uploads/error.html', data)


		#Loads the survey scheme
		scheme = pd.read_csv('location_uploads/static/location_uploads/config/table_survey_scheme.csv')

		#Creates the dictionary that the insert method will process
		responses = {}

		#Fills the dictionary
		for ind in scheme.index:

			row = scheme.iloc[ind]

			#Sets to None if no value is set
			responses[row['name']] = None

			if(request.POST.get(row['name']) is not None and request.POST.get(row['name']) != ""):

				if('VARCHAR' in row['type']):
					responses[row['name']] = request.POST.get(row['name'])

				elif('INT' in row['type']):
					responses[row['name']] = int(request.POST.get(row['name']))

				else:
					raise Http404("Columna: " + row['name'] + " no es numerica ni cadena de caracteres.")


		#Special Cases (Times)
		#hora_levantar
		if(request.POST.get('horas_levantar') != "" and request.POST.get('minutos_levantar') != ""):
			responses['hora_levantar'] = int(request.POST.get('horas_levantar'))*60 + int(request.POST.get('minutos_levantar'))

		#hora_llegar_destino
		if(request.POST.get('horas_llegar_destino') != "" and request.POST.get('minutos_llegar_destino') != ""):
			responses['hora_llegar_destino'] = int(request.POST.get('horas_llegar_destino'))*60 + int(request.POST.get('minutos_llegar_destino'))


		#hora_salir_hogar
		if(request.POST.get('horas_salir_hogar') != "" and request.POST.get('minutos_salir_hogar') != ""):
			responses['hora_salir_hogar'] = int(request.POST.get('horas_salir_hogar'))*60 + int(request.POST.get('minutos_salir_hogar'))

		#hora_volver_hogar
		if(request.POST.get('horas_volver_hogar') != "" and request.POST.get('minutos_volver_hogar') != ""):
			responses['hora_volver_hogar'] = int(request.POST.get('horas_volver_hogar'))*60 + int(request.POST.get('minutos_volver_hogar'))


		if(anonymize):
			responses['id_entrevistado'] = ha.anonymize(responses['id_entrevistado'])

		ps.export_survey(responses)
		ps.survey_received(interview_id, student_id)

		data['envio'] = 'encuesta'
		data['por_enviar'] = 'el archivo .json'



		#json case
	elif(request.POST.get('tipo_encuesta') == 'json'):

		#IF already uploaded the json
		if(upload_status == "FOUND_JSON"):
			data['mensaje_error'] = "Lo sentimos, pero el estudiante: " + student_id + " ya subió el archivo .json de la persona con identificación: " + request.POST.get('id_entrevistado') +  "."
			return render(request, 'location_uploads/error.html', data)			

		#If other student uploaded that info
		if(interview_id_status == "UPLOADED"):
			data['mensaje_error'] = "Lo sentimos, pero la persona con identificación: " + request.POST.get('id_entrevistado') +  " ya se encuentra en proceso de entrevista con otro estudiante."
			return render(request, 'location_uploads/error.html', data)

		json_file = request.FILES["json_file"]
		if not json_file.name.upper().endswith('.JSON'):
			#NOt a JSON FILE
			data['mensaje_error'] = 'El archivo sumistrado no tiene una extensión .json. Asegurse de subir el archivo apropiado.'
			return render(request, 'location_uploads/error.html', data)
        
		print(json_file.name + ' received succesfully')	
		json_text = json_file.read().decode("utf-8")	


		try:
			data = json.loads(json_text)
		except:
			data['mensaje_error'] = 'El archivo suministrado está corrupto y no puede ser procesado, verifique que se encuentre en formato JSON.'
			return render(request, 'location_uploads/error.html', data)

		#checks status of json
		json_hash = ha.get_hex_from_json(data)
		status_json = ps.check_json_status(student_id, json_hash)

		#If student uploaded that info for someother interview
		if(status_json == "USER_UPLOADED"):
			data['mensaje_error'] = "Lo sentimos, pero el estudiante: " + student_id + " ya subió el archivo .json suministrado para otra entrevista."
			return render(request, 'location_uploads/error.html', data)

		#If json uploaded by other user
		if(status_json == "UPLOADED"):
			data['mensaje_error'] = "Lo sentimos, pero el archivo .json suministrado ya se encuentra en la base de datos."
			return render(request, 'location_uploads/error.html', data)

		grupo = request.POST.get('grupo_rad')
		if(grupo == "OTRO"):
			grupo = request.POST.get('grupo_text')

		if(grupo == ""):
			grupo = "NINGUNO"

		
		data['student_id'] = student_id
		data['interview_id'] = interview_id
		data['json_hash'] = json_hash
		

		ps.save_json(json_obj = data, name = interview_id)
		ps.json_received(interview_id, student_id, json_hash, grupo)

		data['envio'] = 'archivo json'
		data['por_enviar'] = 'la encuesta'

		

	else:
		data['mensaje_error'] = "Tipo encuesta: "  + request.POST.get('tipo_encuesta') + ' no soportado.' + '\n' + 'Favor comuniquese con el monitor del curso.'
		return render(request, 'location_uploads/error.html', data)
		


	return render(request, 'location_uploads/result.html', data)

	#except Exception as e:

		#data['mensaje_error'] = "Se produjo el siguiente error en el servidor: \n" + str(e) + "\n\n." + "Por favor comuníquese con el monitor."
		#return render(request, 'location_uploads/error.html', data)



