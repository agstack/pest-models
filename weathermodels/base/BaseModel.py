import urllib.parse
import urllib.request
import datetime
import dateutil.parser
import json

class BaseModel(object):
    def __init__(self, agls_api_key=None):
        self.agls_api_key = agls_api_key


    def register(self, agls_api_key):
        self.agls_api_key = agls_api_key


    def get_data(self, lat=None, lon=None, start_dt=None, end_dt=None, res='hourly'):
        float_lat = float(lat)
        float_lon = float(lon)

        if not -90 <= float_lat <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        if not -180 <= float_lon <= 180:
            raise ValueError('Longitude must be between -180 and 180')

        if isinstance(start_dt, str):
            start_dt = dateutil.parser.parse(start_dt)
        elif not isinstance(start_dt, datetime.date):
            raise TypeError('Start date must be of type datetime')

        if isinstance(end_dt, str):
            end_dt = dateutil.parser.parse(end_dt)
        elif not isinstance(end_dt, datetime.date):
            raise TypeError('End date must be of type datetime')

        if res not in ['hourly', 'daily']:
            raise ValueError('Data resolution must be either \'hourly\' or \'daily\'')

        if not self.agls_api_key:
            raise AssertionError('An Agralogics API Key is required to retrieve data from the Agralogics API')

        query_params = urllib.parse.urlencode({
            'lat': lat,
            'lon': lon,
            'start_dt': start_dt.isoformat(),
            'end_dt': end_dt.isoformat()
        })
        url = 'https://api.agralogics.com/weather/%s/?%s' % (res, query_params)
        headers = { 'Agls-Api-Key': self.agls_api_key }
        req = urllib.request.Request(url, headers=headers)
        response_raw = urllib.request.urlopen(req).read().decode('utf-8')
        response_json = json.loads(response_raw)

        return response_json
