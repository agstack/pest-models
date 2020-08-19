from agralogics.models.base import BaseModel


class GrowingDegreeDaysModel(BaseModel):
    def calculate(self, lat=None, lon=None, start_dt=None, end_dt=None, upper_threshold=None, lower_threshold=None):
        data = self.get_data(lat=lat, lon=lon, start_dt=start_dt, end_dt=end_dt, include=['air_temperature'])
        hourly_data = data['hourly']

        gdd = 0
        for data in hourly_data:
            air_temperature = data['air_temperature']
            if lower_threshold < air_temperature < upper_threshold:
                gdd += air_temperature - lower_threshold

        return gdd

