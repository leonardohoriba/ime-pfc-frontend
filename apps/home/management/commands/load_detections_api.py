from django.core.management.base import BaseCommand
from apps.home.models import Detection
import requests

class Command(BaseCommand):
    help = 'Load data from API'

    def handle(self, *args, **kwargs):
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