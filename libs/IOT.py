from flask import Flask, flash, redirect, render_template, jsonify, request, send_from_directory, url_for, flash
from libs import datatable

def home_control():
	if request.method == 'POST':
		return render_template('home_control.html')
	return redirect("/authentication-gateway?fwdid=IOT")

def home_control2():
	if request.method == 'POST':
		return render_template('home_control_EK.html')
	return redirect("/authentication-gateway?fwdid=IOT")

def HexLED():
        return "jinga lala uu uu"

def setflags():
	req = request.get_json(force=True) 
	req = req['setStatus']

	_st = datatable.get_table('flags')
	
	for k,v in req.items():
		_st[k] = v
	
	datatable.set_table('flags', _st)
	
	return jsonify({"code":1})

def getStatus():
	flags = request.args.get('flags', default=[], type=list)
	f = request.args.get('format', default='', type=str)

	_st = datatable.get_table('flags')
	flags = eval("".join(flags)) 

	print(flags,type(flags))
	
	d = {k:v for k,v in _st.items() if k in flags}
	if f == 'arduino':	
		return ''.join([str(d[key])[1] for key in d.keys()])
	return jsonify(d)

def getSensorData():
	s = datatable.get_table('sensordata')
	return jsonify({
			"temp": s['Temperature'],
			"humidity": s['Humidity'],
			"FeelsLike": s['HeatIndex']
		})
def setSensorData():
    req = request.get_json(force=True)

    s = datatable.get_table('sensordata')

    s['Temperature'] = req['Temp']
    s['Humidity'] = req['Hum']
    s['HeatIndex'] = req['TempFL']

    datatable.set_table('sensordata', s)
    
    return "ok"

def getSensorData_EK():
	s = datatable.get_table('sensordata_EK')
	return jsonify({
			"temp": s['Temperature'],
			"humidity": s['Humidity'],
			"FeelsLike": s['HeatIndex']
		})
def setSensorData_EK():
    req = request.get_json(force=True)

    s = datatable.get_table('sensordata_EK')

    s['Temperature'] = req['Temp']
    s['Humidity'] = req['Hum']
    s['HeatIndex'] = req['TempFL']

    datatable.set_table('sensordata', s)
    
    return "ok"

def showwallstatus():
	s = datatable.get_table('hexStatus')
	return jsonify(s)

def changewallstatus():
	req = request.get_json(force=True)
	with open('res/hexStatus.txt') as file:
		s = eval(file.read())
	s['brightness_lvl'] = req['Blvl']
	s['effect'] = req['eData']
	s['color'] = req['color']
	with open('res/hexStatus.txt', 'w') as file:
		file.write(str(s))
	return "ok"
