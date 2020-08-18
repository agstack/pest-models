from weathermodels.base import BaseModel

class ChillModelUtah(BaseModel):
    def calculate_chill_hours(self, lat, lon, start_dt, end_dt):
        data = self.get_data(lat, lon, start_dt, end_dt)
        print(data)
