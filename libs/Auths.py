from flask import Flask, flash, redirect, render_template, jsonify, request, send_from_directory, url_for, flash
from libs import datatable

def auth_gateway():
	fwdid = request.args.get('fwdid', default='none', type=str)
	trytimes = request.args.get('trytimes', default='1', type=int)
	with open('templates/auth.html') as file:
		page = file.read()
	data = {'fwdid': fwdid,'trytimes': trytimes}
	
	for k,v in data.items():
		page = page.replace('{%s}'%k, str(v))

	if int(trytimes) > 1:
		page = page.replace('''<!-- <div class="card-title text-danger">
						Invalid credentials. Try agian.
					</div> -->''',
					'''<div class="card-title text-danger">
						Invalid credentials. Try agian.
					</div>''')
	return page
	
def validation():
	fwdid = request.form.get('fwdid')
	trytimes = request.form.get('trytimes')
	username = request.form.get('username')
	password = request.form.get('password')
	
	profiles = datatable.get_table('passwd')
		
	if username in profiles:
		if profiles[username] == password:
			return redirect('/%s/%s'%(fwdid,username), code=307)
	return redirect('/authentication-gateway?fwdid=%s&trytimes=%s'%(fwdid,int(trytimes)+1))
