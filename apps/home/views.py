from .aux_functions import *
from .map import render_map, get_map
from .forms import render_upload_form
from .datatable import render_datatable
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'
    context['map'] = get_map()
    context['data'] = get_statistic_data_from_api()
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
        
        if load_template == 'forms.html':
            return render_upload_form(request)
        
        if load_template == 'datatable.html':
            return render_datatable(request)

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        html_template = loader.get_template('home/page-500.html')
        print(e)
        return HttpResponse(html_template.render(context, request))
