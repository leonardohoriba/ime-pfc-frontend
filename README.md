# ime-pfc-frontend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

project_id = pfcime

app = ime_pfc_frontend

tag = gcr.io/pfcime/ime_pfc_frontend

## Comandos para subir a instancia no gcloud
gcloud builds submit --tag gcr.io/pfcime/ime-pfc-frontend  

 gcloud run deploy ime-pfc-frontend --image gcr.io/pfcime/ime-pfc-frontend --platform managed --region southamerica-east1 --allow-unauthenticated --port 8000   