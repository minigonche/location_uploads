from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'location_uploads/index.html', None)


def upload_info(request):

	data = {}

	if "GET" == request.method:
		raise Http404("Method is set to GET")

    # if not GET, then proceed
	try:
		json_file = request.FILES["json_file"]
		if not json_file.name.endswith('.json'):
			#NOt a JSON FILE
			raise Http404("Not a JSON File")
        #if file is too large, return
		#if json_file.multiple_chunks():
		#	raise Http404("Uploaded file is too big (%.2f MB)." % (json_file.size/(1000*1000),))

		json_text = json_file.read().decode("utf-8")	

		data['text'] = json_text
		data['sexo'] = request.POST.get('sexo')
		data['estrato'] = request.POST.get('estrato')

		return render(request, 'location_uploads/result.html', data)
		

	except Exception as e:
		raise Http404("Unable to load file")


	


