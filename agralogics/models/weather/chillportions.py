from agralogics.models.base import BaseModel


class ChillPortions(BaseModel):
	def calculate(self, lat=None, lon=None, start_dt=None, end_dt=None):
		data = self.get_hourly_data(lat=lat, lon=lon, start_dt=start_dt, end_dt=end_dt, include=['air_temperature'])
		hourly_data = data['hourly']

		#Create the constants
		slp = 1.6
		tetmlt = 277
		a0 = 139500
		a1 = 2.567 * 10**18
		e0 = 4153.5
		e1 = 12888.8
		aa = a0/a1
		ee = e1-e0

		portions = 0
		inter_s = 0
		delt = 0

		for data in hourly_data:
			t = data['air_temperature']
			t_kelvin = t+273
			ftmprt = slp*tetmlt*(t_kelvin - tetmlt)/ t_kelvin
			s_r = np.exp(ftmprt)
			x_i = s_r/(1+s_r)
			x_s = aa *np.exp(ee/t_kelvin)
			ak1 = a1 *np.exp(-e1/t_kelvin)
			inter_e = x_s - (x_s - inter_s)* np.exp(-ak1)

			if inter_e < 1:
				delt = 0
			else:
				delt = inter_e * x_i

			#acculumate the portions
			portions = portions + delt

			#set variables for the next iteration
			if inter_e < 1: 
				inter_s = inter_e
			else:
				inter_s = inter_e - inter_e*x_i

		return portions

