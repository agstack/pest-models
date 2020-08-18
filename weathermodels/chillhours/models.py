from weathermodels.base import BaseModel

class ChillModelUtah(BaseModel):
    def calculate_chill_hours(self, lat, lon, start_dt, end_dt):
        data = self.get_data(lat, lon, start_dt, end_dt)

        model = {
            "lt_34": 0,
            "34_36": 0.5,
            "36_48": 1,
            "48_54": 0.5,
            "54_60": 0,
            "60_65": -0.5,
            "gt_65": -1.0
        }
