from django.shortcuts import render
from django.contrib.staticfiles.storage import staticfiles_storage
import pandas as pd
import json

from location_uploads import process_survey as ps


# Create your views here.

def index(request):
    return render(request, 'location_uploads/index.html', None)


def upload_info(request):

	data = {}

	if "GET" == request.method:
		raise Http404("Method is set to GET")

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


			ps.export_survey(responses)

			data['envio'] = 'encuesta'
			data['por_enviar'] = 'el archivo .json'




		elif(request.POST.get('tipo_encuesta') == 'json'):

			student_id = request.POST.get('carnet')
			interview_id = request.POST.get('id_entrevistado')

			json_file = request.FILES["json_file"]
			if not json_file.name.endswith('.json'):
				#NOt a JSON FILE
				raise Http404("Not a JSON File")
	        
			print(json_file.name + ' received succesfully')	
			json_text = json_file.read().decode("utf-8")	


			data = json.loads(json_text)
			data['student_id'] = student_id
			data['interview_id'] = interview_id

			ps.save_json(json_obj = data, name = student_id + '_' + interview_id)

			#export_json_async.delay(student_id, interview_id, json_text)
			#export_json_async.apply_async(args=[student_id, interview_id,json_text ], kwargs={'kwarg1': 'student_id', 'kwarg2': 'interview_id', 'kwarg3': 'json_text'})

			data['envio'] = 'archivo json'
			data['por_enviar'] = 'la encuesta'

			

		else:
			raise Http404("Tipo encuesta: "  + request.POST.get('tipo_encuesta') + ' no soportado')

		#json_file = request.FILES["json_file"]
		#if not json_file.name.endswith('.json'):
			#NOt a JSON FILE
		#	raise Http404("Not a JSON File")
        #if file is too large, return
		#if json_file.multiple_chunks():
		#	raise Http404("Uploaded file is too big (%.2f MB)." % (json_file.size/(1000*1000),))

		#json_text = json_file.read().decode("utf-8")	

		#data['text'] = json_text


		return render(request, 'location_uploads/result.html', data)

	except Exception as e:
		raise Http404("Unable to load file")



