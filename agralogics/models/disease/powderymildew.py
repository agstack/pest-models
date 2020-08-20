import dateutil.parser
import datetime

from agralogics.models.base import BaseModel
from agralogics.models.weather.leafwetnessduration import CART_SLD

class PowderyMildewGrapes(BaseModel):
    """
    Model reference: http://ipm.ucanr.edu/DISEASE/DATABASE/grapepowderymildew.html
    Reference Image: http://ipm.ucanr.edu/PMG/IMAGES/U/D-GR-UNEC-FO.002.jpg
    """
    def print_formatted(self, calculation_res):
        ascospore_values, conidial_res = calculation_res

        print("Ascopore Infection Recommended Actions:")
        for date, treatment in ascospore_values:
            print("%s: %s" % (date, treatment))

        print('---------------------------------------')

        if conidial_res is None:
            print("Your fields are not at risk for Conidial Infection")
        elif len(conidial_res) == 1:
            print(conidial_res)
        else:
            recommendations, day_acc = conidial_res
            print("Conidial Infection Treatment Recommendation:")
            print("(Use ONE of the following to treat your fields)")
            for spray_material, spray_interval in recommendations:
                print("- Spray Material: %s, Spray Interval: %s" % (spray_material, spray_interval))

            print()

            print("Day-Over-Day Accumulated Conidial Infection Risk Index:")
            for date, acc_index in day_acc:
                print("%s: %s" % (date, acc_index))


    def calculate(self, lat=None, lon=None, start_dt=None, end_dt=None):
        # make sure that the start date is 1st hour of day
        if isinstance(start_dt, str):
            start_dt = dateutil.parser.parse(start_dt)
        start_dt = start_dt.replace(hour=1, minute=0, second=0, microsecond=0)

        # make sure end date is stripped of hour/minute/second info
        if isinstance(end_dt, str):
            end_dt = dateutil.parser.parse(end_dt)
        end_dt = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)

        data = self.get_hourly_data(lat=lat, lon=lon, start_dt=start_dt, end_dt=end_dt, include=['air_temperature'])
        hourly_data = data['hourly']

        ascospore_values = self.calculate_ascospore_stage(hourly_data, lat, lon)
        conidial_res = self.calculate_conidial_stage(hourly_data)

        return ascospore_values, conidial_res


    def calculate_ascospore_stage(self, hourly_data, lat, lon):
        def classify_ascospore(temp_avg, lwd):
            """
            Classify ascospore treatment for a day given the average temperature
            and hours of leaf wetness
            """
            SAFE = 'safe'
            TREAT = 'treat'

            if temp_avg < 42 or temp_avg > 79:
                return SAFE

            def determine_treatment(threshold):
                return SAFE if lwd < threshold else TREAT

            if temp_avg < 43: return determine_treatment(40)
            if temp_avg < 44: return determine_treatment(34)
            if temp_avg < 45: return determine_treatment(30)
            if temp_avg < 46: return determine_treatment(27.3)
            if temp_avg < 47: return determine_treatment(25.3)
            if temp_avg < 48: return determine_treatment(23.3)
            if temp_avg < 50: return determine_treatment(20)
            if temp_avg < 51: return determine_treatment(19.3)
            if temp_avg < 52: return determine_treatment(18)
            if temp_avg < 53: return determine_treatment(17.3)
            if temp_avg < 54: return determine_treatment(16.7)
            if temp_avg < 56: return determine_treatment(16)
            if temp_avg < 58: return determine_treatment(14.7)
            if temp_avg < 60: return determine_treatment(14)
            if temp_avg < 62: return determine_treatment(13.3)
            if temp_avg < 63: return determine_treatment(12.7)
            if temp_avg < 76: return determine_treatment(12)
            if temp_avg < 77: return determine_treatment(12.7)
            if temp_avg < 78: return determine_treatment(14)

            # temp_avg >= 78
            return determine_treatment(17.3)

        # ascospore stage
        ascospore_values = []
        # use cart sld model to classify leaf wetness hours every day
        leafwetnessmodel = CART_SLD(agls_api_key=self.agls_api_key)
        # take sections of returned data in groups of 24
        i = 0
        temp_sum = 0
        while i < len(hourly_data):
            temp_sum += hourly_data[i]['air_temperature']

            if (i + 1) % 24 == 0:
                temp_avg = temp_sum / 24
                lwd = leafwetnessmodel.calculate(
                    lat=lat,
                    lon=lon,
                    start_dt=hourly_data[i - 23]['timestamp'],
                    end_dt=hourly_data[i]['timestamp']
                )
                ascospore_value = classify_ascospore(temp_avg, lwd)
                date = hourly_data[i - 1]['timestamp'].split('T')[0]
                ascospore_values.append((date, ascospore_value))

                temp_sum = 0

            i += 1

        return ascospore_values


    def calculate_conidial_stage(self, hourly_data):
        if len(hourly_data) < 72:
            return "Could not compute Conidial Stage -- requires at least 3 days of data"

        def has_6_consecutive_hours(day_data):
            # see if there are 6 consecutive hours of temp between 70 and 85
            for i in range(len(day_data) - 6):
                for j in range(0, 6):
                    temp = day_data[i + j]['air_temperature']
                    if temp < 70 or temp > 85:
                        break
                return True
            return False

        def has_gt_95(day_data):
            for d in day_data:
                if d['air_temperature'] >= 95:
                    return True
            return False

        # conidial stage
        day_acc = []
        conidial_index = 0
        conidial_start = False
        for i in range(int(len(hourly_data) / 24 - 3)):
            hourly_data_base_i = 24 * i

            if not conidial_start:
                # see if there are 6 consecutive hours on this day
                current_day_check = has_6_consecutive_hours(hourly_data[hourly_data_base_i:hourly_data_base_i + 24])
                if current_day_check:
                    next_day_check = has_6_consecutive_hours(hourly_data[hourly_data_base_i + 24:hourly_data_base_i + 48])
                    if next_day_check:
                        final_day_check = has_6_consecutive_hours(hourly_data[hourly_data_base_i + 48:hourly_data_base_i + 72])
                        if final_day_check:
                            conidial_start = True

                            conidial_start_date = hourly_data[hourly_data_base_i]['timestamp'].split('T')[0]
                            conidial_next_date = hourly_data[hourly_data_base_i + 24]['timestamp'].split('T')[0]
                            conidial_final_date = hourly_data[hourly_data_base_i + 48]['timestamp'].split('T')[0]

                            day_acc.extend([
                                (conidial_start_date, 20),
                                (conidial_next_date, 40),
                                (conidial_final_date, 60)
                            ])

                            conidial_index += 60
                            i += 2
            else:
                # check conditions 2 - 7
                date = hourly_data[hourly_data_base_i]['timestamp'].split('T')[0]
                day_hours = hourly_data[hourly_data_base_i:hourly_data_base_i + 24]
                current_day_check = has_6_consecutive_hours(day_hours)
                if current_day_check:
                    conidial_index += 20
                    if has_gt_95(day_hours):
                        conidial_index -= 10
                else:
                    conidial_index -= 10

                if conidial_index < 0:
                    conidial_index = 0

                if conidial_index > 100:
                    conidial_index = 100

                day_acc.append((date, conidial_index))

            i += 1

        if not conidial_start:
            return None

        recommendations = {
            'low': [
                ('sulfur dust', '14 days'),
                ('micronized sulfur', '18 days'),
                ('DMI fungicides', '21 days')
            ],
            'med': [
                ('sulfur dust', '10 days'),
                ('micronized sulfur', '14 days'),
                ('DMI fungicides', '17 days')
            ],
            'high': [
                ('sulfur dust', '7 days'),
                ('micronized sulfur', '10 days'),
                ('DMI fungicides', '14 days')
            ]
        }

        if conidial_index < 45:
            recommendation = recommendations['low']
        elif 45 <= conidial_index < 55:
            recommendation = recommendations['med']
        else:
            recommendation = recommendations['high']

        return recommendation, day_acc
