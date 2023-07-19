import os
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.home.models import Detection
import pandas as pd
import random

class Command(BaseCommand):
    help = 'Load data from Detector file'

    def handle(self, *args, **kwargs):
        data_file = os.path.join(settings.BASE_DIR, 'data/Detections.csv')
        keys = ('Time','State','Longitude','Latitude')  # colunas do CSV que vamos extrair informações
        df = pd.read_csv(data_file, delimiter=';', usecols=keys, decimal='.')
        # Filtrar as linhas com valores "--" ou vazios para latitude e longitude
        df = df[(df['Latitude'] != "") & (df['Longitude'] != "") & (df['Latitude'] != "--") & (df['Longitude'] != "--")]
        # Cria uma nova coluna "Danger" com valores aleatórios de 0 ou 1
        df['Danger'] = df.apply(lambda _: random.randint(0, 1), axis=1)
        # Acrescenta as colunas do tipo de sensor e nome do sensor
        df['Sensor Type'] = 'Radiológico'
        df['Sensor'] = 'SPIR-ID'

        records = df.to_dict('records')
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
            