import requests
from django.template import loader
from django.http import HttpResponse
from datetime import datetime

def get_datatable():
    try:
        url = "https://backend-pr5m6uxofa-rj.a.run.app/last_100"
        response = requests.get(url)
        response.raise_for_status() 
        detections = response.json()

        # Handling datetime format
        for detection in detections:
            try:
                original = detection["data"]
                new_date = datetime.strptime(original, "%Y-%m-%d %H:%M")
                detection["data"] = new_date
            except ValueError:
                 print(f"A data {original} não está no formato desejado.")
                
        
        # Handling sensor name format
        mapping = {
            "spirid": "SPIR-ID",
            "gdax": "GDA-X",
            "lsid": "LS-ID",
            "prdradeye": "PRD-RadEye"
        }
        for detection in detections:
                if "leitor" in detection:
                    original = detection["leitor"].lower()
                    leitor = mapping.get(original)
                    if leitor:
                        detection["leitor"] = leitor

    except requests.exceptions.RequestException as e:
        # Handle API request errors here
        print(f"API Request Error: {e}")
        detections = [] 
    return detections

def render_datatable(request):
    context = {}
    context['detections'] = get_datatable()
    html_template = loader.get_template('home/datatable.html')
    return HttpResponse(html_template.render(context, request))