import urllib.parse
import urllib.request
import datetime
import dateutil.parser
import json

class BaseSoidGridsModel(object):

    def __init__(self, agls_api_key=None):
        self.agls_api_key = agls_api_key


    def get_soilgrids_classification_query(self, lat=None, lon=None, wrb_number_classes=None):
        float_lat = float(lat)
        float_lon = float(lon)
        int_classes = int(wrb_number_classes)
        
        if not -90 <= float_lat <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        if not -180 <= float_lon <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        
        query_params_dict = {
            'lat': lat,
            'lon': lon,
            'number_classes': int_classes
        }
        query_params = urllib.parse.urlencode(query_params_dict)
        https://rest.soilgrids.org/soilgrids/v2.0/classification/query?
        url = 'https://rest.soilgrids.org/soilgrids/v2.0/classification/query?%s' % (query_params)
        req = urllib.request.Request(url)
        response_raw = urllib.request.urlopen(req).read().decode('utf-8')
        response_json = json.loads(response_raw)
        
        return response_json
    
    def get_soilgrids_layers():
        url = 'https://rest.soilgrids.org/soilgrids/v2.0/properties/layers'
        req = urllib.request.Request(url)
        response_raw = urllib.request.urlopen(req).read().decode('utf-8')
        response_json = json.loads(response_raw)
        
        return response_json
    
    def get_soilgrids_properties_query(lat=None, lon=None):
    float_lat = float(lat)
    float_lon = float(lon)

    if not -90 <= float_lat <= 90:
        raise ValueError('Latitude must be between -90 and 90')
    if not -180 <= float_lon <= 180:
        raise ValueError('Longitude must be between -180 and 180')

    query_params_str =\
        'lon='+str(lon)+\
        '&lat='+str(lat)+\
        '&property=bdod'+\
        '&property=cec'+\
        '&property=cfvo'+\
        '&property=clay'+\
        '&property=nitrogen'+\
        '&property=ocd'+\
        '&property=ocs'+\
        '&property=phh2o'+\
        '&property=sand'+\
        '&property=silt'+\
        '&property=soc'+\
        '&depth=0-5cm'+\
        '&depth=0-30cm'+\
        '&depth=5-15cm'+\
        '&depth=15-30cm'+\
        '&depth=30-60cm'+\
        '&depth=60-100cm'+\
        '&depth=100-200cm'+\
        '&value=Q0.05'+\
        '&value=Q0.5'+\
        '&value=Q0.95'+\
        '&value=mean'+\
        '&value=uncertainty'

    #query_params = urllib.parse.urlencode(query_params_dict)
    url = 'https://rest.soilgrids.org/soilgrids/v2.0/properties/query?%s' % (query_params_str)
    req = urllib.request.Request(url)
    response_raw = urllib.request.urlopen(req).read().decode('utf-8')
    response_json = json.loads(response_raw)


    return response_json

    """
    def register(self, agls_api_key):
        self.agls_api_key = agls_api_key


    def convert_to_fahrenheit(self, air_temperature):
        return air_temperature * 1.8 + 32


    def get_hourly_data(self, lat=None, lon=None, start_dt=None, end_dt=None, res='hourly', include=None, system=None):
        if not self.agls_api_key:
            raise AssertionError('An Agralogics API Key is required to retrieve data from the Agralogics API')

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

        query_params_dict = {
            'lat': lat,
            'lon': lon,
            'start_dt': start_dt.isoformat(),
            'end_dt': end_dt.isoformat()
        }

        if system is not None:
            if system in ['cimis', 'noaa']:
                query_params_dict['system'] = system
            else:
                raise ValueError('Weather system must be either \'cimis\' or \'noaa\'')

        if include:
            if not isinstance(include, list):
                raise TypeError('Included fields must be passed as a list')
            include_str = ','.join(include)
            query_params_dict['include'] = include_str

        query_params = urllib.parse.urlencode(query_params_dict)
        url = 'https://api.agralogics.com/weather/%s/?%s' % (res, query_params)
        headers = { 'Agls-Api-Key': self.agls_api_key }
        req = urllib.request.Request(url, headers=headers)
        response_raw = urllib.request.urlopen(req).read().decode('utf-8')
        response_json = json.loads(response_raw)

        return response_json
    """
