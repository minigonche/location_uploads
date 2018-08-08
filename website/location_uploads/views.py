from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas as pd
import json

from location_uploads import process_survey as ps


# Create your views here.

def index(request):
    return render(request, 'location_uploads/index.html', None)


def upload_info(request):

	anonimize = True

	data = {}

	if "GET" == request.method:
		data['mensaje_error'] = "Se produjo el siguiente error en el servidor: \n" + "Method is set to GET." + "\n\n" + "Por favor comuníquese con el monitor."
		return render(request, 'location_uploads/error.html', data)

    # if not GET, then proceed
	try:

		#Survey case
		if(request.POST.get('tipo_encuesta') == 'informacion'):

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


			if(anonimize):
				responses['id_entrevistado'] = ps.anonimize(responses['id_entrevistado'])

			ps.export_survey(responses)

			data['envio'] = 'encuesta'
			data['por_enviar'] = 'el archivo .json'




		elif(request.POST.get('tipo_encuesta') == 'json'):

			student_id = request.POST.get('carnet')
			interview_id = request.POST.get('id_entrevistado')

			if(anonimize):
				interview_id = ps.anonimize(interview_id)

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



			data['student_id'] = student_id
			data['interview_id'] = interview_id

			ps.save_json(json_obj = data, name = student_id + '_' + interview_id)

			data['envio'] = 'archivo json'
			data['por_enviar'] = 'la encuesta'

			

		else:
			data['mensaje_error'] = "Tipo encuesta: "  + request.POST.get('tipo_encuesta') + ' no soportado.' + '\n' + 'Favor comuniquese con el monitor del curso.'
			return render(request, 'location_uploads/error.html', data)
			


		return render(request, 'location_uploads/result.html', data)

	except Exception as e:
		data['mensaje_error'] = "Se produjo el siguiente error en el servidor: \n" + str(e) + "\n\n" + "Por favor comuníquese con el monitor."
		return render(request, 'location_uploads/error.html', data)



