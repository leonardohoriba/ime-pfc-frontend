import csv, os
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.home.models import Detection

class Command(BaseCommand):
    help = 'Load data from Detector file'

    def handle(self, *args, **kwargs):
        data_file = os.path.join(settings.BASE_DIR, 'data/Detections.csv')
        keys = ('Time','State','Longitude','Latitude','Danger')  # colunas do CSV que vamos extrair informações.
        
        records = []
        with open(data_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                records.append({k: row[k] for k in keys})

        for record in records:
            longitude = record['Longitude'].replace(".","")
            latitude = record['Latitude'].replace(".","")
            # Considerando que todos os valores de latitude e longitude são negativos e deveriam ter a vírgula após o segundo algarismo
            # Isso é verdade para os valores armazenados no csv gerado pelo SPIR-ID na ESIE, mas depois devemos implementar uma logica melhor
            record['longitude'] = float("{}.{}".format(longitude[:3],longitude[3:]))
            record['latitude'] = float("{}.{}".format(latitude[:3],latitude[3:]))
            # Acrescenta os dados na base de dados
            Detection.objects.get_or_create(
                time=record['Time'],
                state=record['State'],
                latitude=record['latitude'],
                longitude=record['longitude'],
                danger=record['Danger']
            )
            