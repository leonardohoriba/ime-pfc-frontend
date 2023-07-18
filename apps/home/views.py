# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from apps.home.models import Detection
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
import json
from jinja2 import Template
import folium
from folium import Marker,Popup
from folium.plugins import MarkerCluster

############################################ Colocar esse trecho em outro arquivo .py ou em um módulo e importar na views ########################################################

# Constantes
colors = {
    0:'green',    # danger = 0
    1:'red',      # danger = 1
}

icons = {
    0:'info',        # danger = 0
    1:'exclamation'  # danger = 1
}

# Funcao para criar os icones que representam os clusters 
icon_create_function = '''
    function(cluster) {
        var markers = cluster.getAllChildMarkers();
        var hasDanger = false;

        for (var i = 0; i < markers.length; i++) {
            if (markers[i].options.props.danger) {
                hasDanger = true;
                break;
            }
        }

        var className = hasDanger ? 'marker-cluster marker-cluster-large' : 'marker-cluster marker-cluster-small';
       
        return L.divIcon({
            html: '<div style="display:flex;justify-content:center;align-items:center;font-size:9pt;">'+ markers.length +'</div>',         
            className: className,
            iconSize: new L.Point(40, 40)
        });
    }
'''
# Classe que extende a classe Marker original
class MarkerWithProps(Marker):
    _template = Template(u"""
      {% macro script(this, kwargs) %}
      var {{this.get_name()}} = L.marker(
          [{{this.location[0]}}, {{this.location[1]}}], 
          {
                icon: new L.Icon.Default(),
                {%- if this.draggable %}
                draggable: true,
                autoPan: true,
                {%- endif %}
                {%- if this.props %}
                props : {{ this.props }}
                {%- endif %}
            }
      ).addTo({{this._parent.get_name()}});
  {% endmacro %}
  """)
    def __init__(self, location, popup=None, tooltip=None, icon=None,draggable=False, props = None ):
        super(MarkerWithProps, self).__init__(location=location,popup=popup,tooltip=tooltip,icon=icon,draggable=draggable)
        self.props = json.loads(json.dumps(props))
        
######################################################################################################################################################

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

        # Acrescentando caminho para o mapa
        if load_template == 'map_test.html':
            detections = Detection.objects.all()
            m = folium.Map(location=[-22.870974,-43.42801], zoom_start=16)
            marker_cluster = MarkerCluster(icon_create_function=icon_create_function, showCoverageOnHover=False)
            for detection in detections:
                MarkerWithProps(
                    props={'danger': detection.danger},
                    location=[detection.latitude,detection.longitude],
                    popup=Popup('Data: {}\nCoordenadas: {}'.format(detection.time, [detection.latitude, detection.longitude]),max_width=200),
                    tooltip='Clique para mais informações',
                    icon = (folium.Icon(color=colors[detection.danger], icon=icons[detection.danger], prefix='fa')),  
                ).add_to(marker_cluster)    
            marker_cluster.add_to(m)     
            context['map'] = m._repr_html_()
            html_template = loader.get_template('home/' + load_template)
            return HttpResponse(html_template.render(context, request))

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
