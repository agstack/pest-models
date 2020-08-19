import math

from agralogics.models.base import BaseModel


class CART_SLD(BaseModel):
    """
    From https://apsjournals.apsnet.org/doi/pdfplus/10.1094/PDIS.2002.86.2.179
    """
    def classify(self, data):
        air_temperature = data['air_temperature']
        dew_point = data['dew_point']
        relative_humidity = data['relative_humidity']
        wind_speed = data['wind_speed'] * 1000 / 3600 # this is km/h, need m/s

        dew_point_depression = air_temperature - dew_point
        if dew_point_depression >= 3.7:
            return 0

        if wind_speed < 2.5:
            inequality_1 = (
                1.6064 * math.sqrt(air_temperature) +
                0.0036 * air_temperature ** 2 + 0.1531 * relative_humidity -
                0.4599 * wind_speed * dew_point_depression -
                0.0035 * air_temperature * relative_humidity
            ) > 14.4674
            return 1 if inequality_1 else 0

        if relative_humidity >= 87.8:
            inequality_2 = (
                0.7921 * math.sqrt(air_temperature) +
                0.0046 * relative_humidity -
                2.3889 * wind_speed -
                0.039 * air_temperature * wind_speed +
                1.0613 * wind_speed * dew_point_depression
            ) > 37
            return 1 if inequality_2 else 0

        return 0


    def calculate(self, lat=None, lon=None, start_dt=None, end_dt=None):
        data = self.get_data(lat=lat, lon=lon, start_dt=start_dt, end_dt=end_dt, include=[
            'air_temperature',
            'dew_point',
            'relative_humidity',
            'wind_speed'
        ], units='metric')

        hourly_data = data['hourly']
        lwd = 0
        for data in hourly_data:
            lwd += self.classify(data)

        return lwd
