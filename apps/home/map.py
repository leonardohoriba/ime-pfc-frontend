import folium
from folium import Marker, Popup
from folium.plugins import MarkerCluster
from jinja2 import Template
import json
from .models import Detection
from django.template import loader
from django.http import HttpResponse

# Constantes
colors = {
    0: 'green',  # danger = 0
    1: 'red',    # danger = 1
}

icons = {
    0: 'info',         # danger = 0
    1: 'exclamation',  # danger = 1
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

def get_map():
    detections = Detection.objects.all()
    initial_location = [-22.870974, -43.42801]
    m = folium.Map(location=initial_location, zoom_start=16, min_zoom=1.5, max_bounds=True)
    marker_cluster = MarkerCluster(icon_create_function=icon_create_function, showCoverageOnHover=False)
    for detection in detections:
        MarkerWithProps(
            props={'danger': detection.danger},
            location=[detection.latitude, detection.longitude],
            popup=Popup('Data: {}\nCoordenadas: {}'.format(detection.time, [detection.latitude, detection.longitude]), max_width=200),
            tooltip='Clique para mais informações',
            icon=(folium.Icon(color=colors[detection.danger], icon=icons[detection.danger], prefix='fa')),
        ).add_to(marker_cluster)
    marker_cluster.add_to(m)
    return m._repr_html_()

def render_map(request):
    context = {}
    context['map'] = get_map()
    html_template = loader.get_template('home/map.html')
    return HttpResponse(html_template.render(context, request))