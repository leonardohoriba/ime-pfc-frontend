from datetime import datetime
import requests


def format_number(number):
    return round(float(number), 2)

def get_statistic_data_from_api():
    # URL da API externa que você deseja acessar
    api_url = 'https://backend-pr5m6uxofa-rj.a.run.app/statiticslast_100'
    response = requests.get(api_url)
    data = response.json()[0]
    data['data_ultima_afericao'] = datetime.fromisoformat(data['data_ultima_afericao']).strftime('%d/%m/%Y %H:%M:%S')
    data['media'] = format_number(data['media'])
    data['valor_maximo'] = format_number(data['valor_maximo'])
    data['valor_minimo'] = format_number(data['valor_minimo'])
    return data