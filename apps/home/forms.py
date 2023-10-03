from django import forms
import pandas as pd
from .models import Detection
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
import requests
import json
from unidecode import unidecode

def render_upload_form(request):
    context = {}
    html_template = loader.get_template('home/forms.html')

    if request.method == 'POST':
        data_file = request.FILES.get('inputCSV', None)
        # CSV Upload
        if data_file:  
            df = pd.read_csv(data_file, delimiter=';', decimal='.')
            data = df.to_dict(orient='records')
            json_data = json.dumps(data, indent=4)
            
            try:
                url = "https://backend-pr5m6uxofa-rj.a.run.app/uploadSpirId"
                response = requests.post(url,data=json_data)
                
                if response.status_code == 200:
                    if response.text == '"Sucesso"':
                        messages.success(request, "Leituras adicionadas à base de dados.")
                    else:
                        messages.error(request, response.text)
                elif response.status_code == 413:
                        messages.error(request, "Não foi possível adicionar, tamanho de arquivo muito grande.")
                else:
                    messages.error(request, "Não foi possível adicionar o arquivo. Código de status: {}".format(response.status_code))
            except Exception as e:
                messages.error(request, "Ocorreu um erro durante a solicitação: {}".format(str(e)))
    
        # Single detection upload
        else:
            date = request.POST.get('inputDate', False)
            time = request.POST.get('inputTime', False)
            state = request.POST.get('inputState', False)
            latitude = request.POST.get('inputLatitude', False)
            longitude = request.POST.get('inputLongitude', False)
            reading = request.POST.get('inputReading', False)
            sensor = request.POST.get('inputSensor', False)
            sensortype = request.POST.get('inputType', False)

            # Handling special characters and uppercase letters
            sensor = sensor.replace('-','').lower()
            sensortype = sensortype.replace('-','').lower()
            state = unidecode(state).lower()

            # Handling date format
            day, month, year = map(int, date.split('-'))
            new_date = f"{year:04d}-{month:02d}-{day:02d}"
            datetime = str(new_date) + " " + str(time)

            try:
                url = "https://backend-pr5m6uxofa-rj.a.run.app/uploadIndividualRegister"
                data = {
                    "data":datetime,
                    "estado":state,
                    "longitude":str(longitude),
                    "latitude":str(latitude),
                    "leitura":reading,
                    "tipoleitor":sensortype,
                    "leitor":sensor
                }
                response = requests.post(url,data=json.dumps(data))
                if response.status_code == 200:
                    if response.text == 'true':
                        messages.success(request, "Leitura adicionada à base de dados")
                    else:
                        messages.error(request,response.text)
                else:
                    messages.error(request, "Não foi possível adicionar a leitura. Código de status: {}".format(response.status_code))
            except Exception as e:
                messages.error(request, "Ocorreu um erro durante a solicitação: {}".format(str(e)))

    return HttpResponse(html_template.render(context, request))