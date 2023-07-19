# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from .models import Detection
from .map import render_map
from .forms import render_upload_form
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import pandas as pd

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # Todos os paths terminam em .html.
    # Pega o arquivo html pelo nome da url e carrega o template associado.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        if load_template == 'map.html':
            return render_map(request)
        
        if load_template == 'datatable.html':
            detections = Detection.objects.all()
            context['detections'] = detections
            html_template = loader.get_template('home/' + load_template)
            return HttpResponse(html_template.render(context, request))
        
        # if load_template == 'forms.html':
        #     return render_upload_form(request)

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
