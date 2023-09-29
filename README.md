# ime-pfc-frontend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

project_id = pfcime

app = ime_pfc_frontend

tag = gcr.io/pfcime/ime_pfc_frontend


FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# running migrations
RUN python manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]