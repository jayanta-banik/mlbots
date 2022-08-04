def get_table(table_name):
	with open('/home/pi/mlbots/dict_tables/'+table_name+'.table') as file:
		_st = eval(file.read())
	return _st

def set_table(table_name, dd):
	with open('/home/pi/mlbots/dict_tables/'+table_name+'.table', 'w') as file:
		file.write(str(dd))
