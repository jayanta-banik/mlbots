from flask import Flask, jsonify, request
from libs import datatable

base_response = {
	'speech' : "completed",
	'source' : 'Manual'

}

fulfill_device_map = {
			'bulb'  :'GaneshLamp', 
			'lamp'  :'RedTableLamp', 
			'fans'  :'Fan', 
			'lights':'TubeLight'
			}
fulfill_action_map = {
						'on': 1101,
					  	'off': 1001
					}
def fulfill():
	if request.method == 'GET':
		return 'welcome to the fulfilment center'
	else:
		req = request.get_json()
		with open("fulfill.txt", 'w') as file:
			file.write(str(req))
		device = req['queryResult']['parameters']['devices']
		status = req['queryResult']['parameters']['onoff']
		with open("fulfill.txt", 'w') as file:
			file.write(str((device, status)))

		resp = base_response.copy()
		
		_st = datatable.get_table('flags')
		_st[fulfill_device_map[device]] = 1001 + int(not _st[fulfill_device_map[device]]//100%10)*100
		# _st[fulfill_device_map[device]] = fulfill_action_map[status]
		datatable.set_table('flags', _st)

		return jsonify(resp)