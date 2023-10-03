import folium
from folium import Marker, Popup
from folium.plugins import MarkerCluster
from jinja2 import Template
import json
from django.template import loader
from django.http import HttpResponse
import requests
from dateutil import parser
# from .models import Detection


# Constantes
colors = {
    False: 'green',  # danger = False
    True: 'red',    # danger = True
}

icons = {
    False: 'info',         # danger = False
    True: 'exclamation',  # danger = True
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
    try:
        url = "https://backend-pr5m6uxofa-rj.a.run.app/last_100"
        response = requests.get(url)
        response.raise_for_status() 
        detections = response.json()
    except requests.exceptions.RequestException as e:
        # Handle API request errors here
        print(f"API Request Error: {e}")
        detections = [] 

    initial_location = [-22.870974, -43.42801]
    m = folium.Map(location=initial_location, zoom_start=16, min_zoom=1.5, max_bounds=True)
    marker_cluster = MarkerCluster(icon_create_function=icon_create_function, showCoverageOnHover=False)

    for detection in detections:
        try:
            # Parse the ISO 8601 timestamp to a more readable format
            datetime = parser.parse(detection['data']).strftime('%Y-%m-%d %H:%M:%S')

            # Handling sensor name format
            mapping = {
                "spirid": "SPIR-ID",
                "gdax": "GDA-X",
                "lsid": "LS-ID",
                "prdradeye": "PRD-RadEye"
            }
            if "leitor" in detection:
                original = detection["leitor"].lower()
                leitor = mapping.get(original)
                if leitor:
                    detection["leitor"] = leitor

            #html that will appear in popup
            html = folium.Html(f"""
                <!DOCTYPE html>
                <html>
                <div style="font-family: Arial, sans-serif; max-width: 200px;">
                    <p><strong>Aparelho:</strong> {detection['leitor']}</p>
                    <p><strong>Data:</strong> {datetime}</p>
                    <p><strong>Coordenadas:</strong> [{detection['latitude']}, {detection['longitude']}]</p>
                    <p><strong>Leitura:</strong> {detection['leitura']}</p>
                </div>
                </html>
            """, script=True)
            MarkerWithProps(
                props={'danger': str(detection['perigo'])},
                location=[float(detection['latitude']), float(detection['longitude'])],
                popup=Popup(html, max_width=200),
                tooltip='Clique para mais informações',
                icon=(folium.Icon(color=colors[detection['perigo']], icon=icons[detection['perigo']], prefix='fa')),
            ).add_to(marker_cluster)
        except Exception as e:
            # Handle marker creation errors here
            print(f"Marker Creation Error: {e}")
    
    marker_cluster.add_to(m)
    return m._repr_html_()

def render_map(request):
    context = {}
    context['map'] = get_map()
    html_template = loader.get_template('home/map.html')
    return HttpResponse(html_template.render(context, request))