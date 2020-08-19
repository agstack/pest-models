from models.base.BaseModel import BaseModel


class ChillDictModel(BaseModel):
    def __init__(self, dict_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dict_model = dict_model


    def get_chill_increment(self, air_temperature):
        for temp_range in self.dict_model.keys():
            temp_value = self.dict_model[temp_range]
            left, right = temp_range.split('_')
            if left == 'lt' and air_temperature <= int(right):
                return temp_value
            elif left == 'gt' and air_temperature > int(right):
                return temp_value
            elif left != 'gt' and left != 'lt' and int(left) < air_temperature <= int(right):
                return temp_value


    def calculate(self, lat=None, lon=None, start_dt=None, end_dt=None):
        data = self.get_data(lat=lat, lon=lon, start_dt=start_dt, end_dt=end_dt, include=['air_temperature'])
        hourly_data = data['hourly']
        chill_hours = 0
        for data in hourly_data:
            air_temperature = data['air_temperature']
            increment = self.get_chill_increment(air_temperature)
            chill_hours += increment

        return chill_hours


class ChillModelUtah(ChillDictModel):
    def __init__(self, *args, **kwargs):
        model = {
            "lt_34": 0,
            "34_36": 0.5,
            "36_48": 1,
            "48_54": 0.5,
            "54_60": 0,
            "60_65": -0.5,
            "gt_65": -1.0
        }

        super().__init__(model, *args, **kwargs)
