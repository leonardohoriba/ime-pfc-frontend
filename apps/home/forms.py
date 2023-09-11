from django import forms
import pandas as pd
import random
from .models import Detection
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages

# from django import forms

# class DetectionForm(forms.Form):
#     # Defina os campos do formulário Django correspondentes aos campos do seu formulário HTML
#     input_type = forms.ChoiceField(choices=[('', 'Selecione o tipo de sensor'), ('quimico', 'Químico'), ('radiologico', 'Radiológico')])
#     input_sensor = forms.ChoiceField(choices=[])
#     input_latitude = forms.CharField(max_length=100)
#     input_longitude = forms.CharField(max_length=100)
#     input_state = forms.CharField(max_length=100)
#     input_danger = forms.ChoiceField(choices=[('', ''), ('nao', 'Não'), ('sim', 'Sim')])
#     input_date = forms.DateField(input_formats=['%d/%m/%Y'])
#     input_time = forms.TimeField(input_formats=['%H:%M:%S.%f'], required=False)
#     input_csv = forms.FileField(required=False)

# class CSVUploadForm(forms.Form):
#     csv_file = forms.FileField(label='Selecione um arquivo CSV')

def render_upload_form(request):
    context = {}
    html_template = loader.get_template('home/forms.html')

    if request.method == 'POST':
        data_file = request.FILES.get('inputCSV', None)
        # CSV Upload
        if data_file:
            keys = ('Time','State','Longitude','Latitude')
            df = pd.read_csv(data_file, delimiter=';', usecols=keys, decimal='.')
            # Filtrar as linhas com valores "--" ou vazios para latitude e longitude
            df = df[(df['Latitude'] != "") & (df['Longitude'] != "") & (df['Latitude'] != "--") & (df['Longitude'] != "--")]
            # Cria uma nova coluna "Danger" com valores aleatórios de 0 ou 1
            df['Danger'] = df.apply(lambda _: random.randint(0, 1), axis=1)
            # Acrescenta as colunas do tipo de sensor e nome do sensor
            df['Sensor Type'] = 'Radiologico'
            df['Sensor'] = 'SpirId'
            records = df.to_dict('records')
            try:
                for record in records:
                # Acrescenta os dados na base de dados
                    Detection.objects.get_or_create(
                        time=record['Time'],
                        state=record['State'],
                        latitude=record['Latitude'],
                        longitude=record['Longitude'],
                        danger=record['Danger'],
                        sensortype=record['Sensor Type'],
                        sensor=record['Sensor']
                    )
                messages.success(request, "Arquivo adicionado à base de dados.")
            except:
                messages.error(request, "Não foi possível adicionar o arquivo.")
    
        # Single detection upload
        else:
            date = request.POST.get('inputDate', False)
            time = request.POST.get('inputTime', False)
            datetime = str(date) + " " + str(time)
            state = request.POST.get('inputState', False)
            latitude = request.POST.get('inputLatitude', False)
            longitude = request.POST.get('inputLongitude', False)
            danger = 1
            sensor = request.POST.get('inputSensor', False)
            sensortype = request.POST.get('inputType', False)
            try:
                new_detection = Detection(time=datetime, state=state, latitude=latitude, longitude=longitude, danger=danger, sensor=sensor, sensortype=sensortype)
                new_detection.save()
                messages.success(request, "Leitura adicionada à base de dados.")
            except:
                messages.error(request, "Não foi possível adicionar a leitura.")

    return HttpResponse(html_template.render(context, request))