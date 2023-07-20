import csv, os
from django.conf import settings
from django.core.management.base import BaseCommand
from apps.home.models import Detection
import pandas as pd
import random
import requests

class Command(BaseCommand):
    help = 'Load data from Detector file'

    def handle(self, *args, **kwargs):
        # data_file = os.path.join(settings.BASE_DIR, 'data/Detections.csv')
        # keys = ('Time','State','Longitude','Latitude')  # colunas do CSV que vamos extrair informações
        # df = pd.read_csv(data_file, delimiter=';', usecols=keys, decimal='.')
        # # Filtrar as linhas com valores "--" ou vazios para latitude e longitude
        # df = df[(df['Latitude'] != "") & (df['Longitude'] != "") & (df['Latitude'] != "--") & (df['Longitude'] != "--")]
        # # Cria uma nova coluna "Danger" com valores aleatórios de 0 ou 1
        # df['Danger'] = df.apply(lambda _: random.randint(0, 1), axis=1)
        # # Acrescenta as colunas do tipo de sensor e nome do sensor
        # df['Sensor Type'] = 'Radiológico'
        # df['Sensor'] = 'SPIR-ID'
        # records = df.to_dict('records')
        url = "https://backend-pr5m6uxofa-rj.a.run.app/table/spirid"  # URL da API que retorna os dados JSON
        response = requests.get(url)
        records = response.json()
        for record in records:
            # Acrescenta os dados na base de dados
            latitude = record['Latitude']
            longitude = record['Longitude']
            if latitude is not None and longitude is not None:
                Detection.objects.get_or_create(
                    time=record['Time'],
                    state=record['State'],
                    latitude=latitude,
                    longitude=longitude,
                    danger=record['Danger'],
                    sensortype=record['TipoLeitor'],
                    sensor=record['Leitor']
                )