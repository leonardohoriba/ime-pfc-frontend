from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Selecione um arquivo CSV')

import pandas as pd
from .models import Detection
from django.template import loader
from .forms import CSVUploadForm
from django.http import HttpResponse

def render_upload_form(request):
    context = {}
    form = CSVUploadForm(request.POST or None, request.FILES or None)
    html_template = loader.get_template('home/forms.html')
    if request.method == 'POST':
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            try:
                keys = ('Time', 'State', 'Longitude', 'Latitude')  # colunas do CSV que vamos extrair informações
                data = []  # JSON que vai armazenar os dados das linhas
                df = pd.read_csv(csv_file, delimiter=';', usecols=keys, decimal='.')
                for index, row in df.iterrows():
                    # Caso queira criar um objeto Detection na database para cada linha
                    if pd.notna(row['Latitude']) and pd.notna(row['Longitude']):
                        Detection.objects.create(
                            time=row['Time'],
                            state=row['State'],
                            latitude=float(row['Latitude']),
                            longitude=float(row['Longitude']),
                            danger=float(row['Danger']),
                            sensor=row['Sensor'],
                            sensortype=row['Sensor Type']
                        )
                    # Caso queira armazenar as linhas no JSON
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

                HttpResponse(html_template.render(context, request))
            except Exception as e:
                context['error_message'] = f"Ocorreu um erro no processamento do arquivo CSV: {str(e)}"
    context['form'] = form
    return HttpResponse(html_template.render(context, request))