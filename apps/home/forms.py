from django import forms
import pandas as pd
from .models import Detection
from django.template import loader
from django.http import HttpResponse
import random

from django import forms

class LeituraForm(forms.Form):
    # Defina os campos do formulário Django correspondentes aos campos do seu formulário HTML
    input_type = forms.ChoiceField(choices=[('', 'Selecione o tipo de sensor'), ('quimico', 'Químico'), ('radiologico', 'Radiológico')])
    input_sensor = forms.ChoiceField(choices=[])
    input_latitude = forms.CharField(max_length=100)
    input_longitude = forms.CharField(max_length=100)
    input_state = forms.CharField(max_length=100)
    input_danger = forms.ChoiceField(choices=[('', ''), ('nao', 'Não'), ('sim', 'Sim')])
    input_date = forms.DateField(input_formats=['%d/%m/%Y'])
    input_time = forms.TimeField(input_formats=['%H:%M:%S.%f'], required=False)
    input_csv = forms.FileField(required=False)

# class CSVUploadForm(forms.Form):
#     csv_file = forms.FileField(label='Selecione um arquivo CSV')

# def render_upload_form(request):
#     context = {}
#     form = CSVUploadForm(request.POST or None, request.FILES or None)
#     html_template = loader.get_template('home/forms.html')
#     if request.method == 'POST':
#         if form.is_valid():
#             csv_file = form.cleaned_data['csv_file']
#             try:
#                 keys = ('Time', 'State', 'Longitude', 'Latitude')  # colunas do CSV que vamos extrair informações
#                 data = []  # JSON que vai armazenar os dados das linhas
#                 df = pd.read_csv(csv_file, delimiter=';', usecols=keys, decimal='.')
#                 df['Danger'] = df.apply(lambda _: random.randint(0, 1), axis=1)
#                 df['Sensor Type'] = 'Radiologico'
#                 df['Sensor'] = 'SpirId'     
#                 # Caso queira criar um objeto Detection na database para cada linha
#                 records = df.to_dict('records')
#                 for record in records:
#                     if pd.notna(record['Latitude']) and pd.notna(record['Longitude']):
#                         Detection.objects.get_or_create(
#                             time=record['Time'],
#                             state=record['State'],
#                             latitude=float(record['Latitude']),
#                             longitude=float(record['Longitude']),
#                             danger=float(record['Danger']),
#                             sensor=record['Sensor'],
#                             sensortype=records['Sensor Type']
#                         )
                # Caso queira armazenar as linhas no JSON
                # for index, row in df.iterrows():
                    # if str(row['Latitude']).isnumeric() and str(row['Longitude']).isnumeric():
                    #     json_data = {
                    #         'Time': row['Time'],
                    #         'State': row['State'],
                    #         'Latitude': float(row['Latitude']),
                    #         'Longitude': float(row['Longitude']),
                    #         'Danger': float(row['Danger']),
                    #         'Sensor Type': row['Sensor Type'],
                    #         'Sensor': row['Sensor']
                    #     }
                    #     data.append(json_data)

    #             HttpResponse(html_template.render(context, request))
    #         except Exception as e:
    #             context['error_message'] = f"Ocorreu um erro no processamento do arquivo CSV: {str(e)}"
    # context['form'] = form
    # return HttpResponse(html_template.render(context, request))