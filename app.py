# imports
from flask_cors import CORS, cross_origin
from flask import Flask, flash, redirect, render_template, jsonify, request, send_from_directory, url_for, flash
import json
import os
import urllib.request as urlbreq
from werkzeug.utils import secure_filename
import string
import random

# local imports
from libs import Auths
from libs import DIP
from libs import IOT
from libs import miscs
from libs import models
from libs import webhook_fulfilment
# from libs import IOT
# from libs import IOT

# global variables
app = Flask(__name__)
cors = CORS(app)
app.config['UPLOAD_FOLDER'] = 'res/up/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['CORS_HEADERS'] = 'Content-Type'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])  
app.secret_key = 'the rndom string'

# local functions
allowed_file = lambda filename: '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
randStr	= lambda N=7 : ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))

def temp_redirect(): return render_template('Broken_htmls/broken.html')
def broken(): return render_template('Broken_htmls/broken.html')
def fileDeleted(): return render_template('Broken_htmls/Filedeleted.html')
def Virus(): return render_template('Broken_htmls/Gremlin.html')
def brokenLink(): return render_template('Broken_htmls/LinkNotFound.html')
def WorkingOnIT(): return render_template('Broken_htmls/notComplete.html')
def internal(): return render_template('Broken_htmls/OSerr.html')
def AttackOnBugs(): return render_template('Broken_htmls/somethingwentwrong.html')
def angryAI(): return render_template('Broken_htmls/UglyAIerr.html')
def uiui(): return render_template('tems/feedback.html') 

# page rendering

@app.route('/')
def landing_page():
	return redirect('/home', code=302)

@cross_origin(headers=['Content-Type'])
@app.route('/helloworld')
def hello_world():
	a = 3/0
	return "Hello World!"

@app.route('/home')
def welcome():
	return render_template('welcome.html')
	
@app.route('/upload-file', methods=['GET', 'POST'])
@cross_origin(headers=['Content-Type'])#
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = randStr() + secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		return jsonify({"awsurl": 'up/' + filename})
	return jsonify({"awsurl": 'up/'})

# routes
app.add_url_rule('/auth_redirect', view_func=Auths.validation, methods=['POST'])
app.add_url_rule('/authentication-gateway', view_func=Auths.auth_gateway, methods=['GET'])
app.add_url_rule('/Gwebhook', view_func=webhook_fulfilment.fulfill, methods=['GET','POST'])

app.add_url_rule('/AI/Chatbot', view_func=temp_redirect, methods=['GET'])

app.add_url_rule('/AI/Image', view_func=DIP.imageMenu, methods=['GET'])
app.add_url_rule('/AI/Image/Image-Captioning', view_func=temp_redirect, methods=['GET']) 
app.add_url_rule('/AI/Image/Image-Cartoonify', view_func=temp_redirect, methods=['GET', 'POST'])
app.add_url_rule('/AI/Image/Image-Classify', view_func=temp_redirect, methods=['GET', 'POST'])
app.add_url_rule('/AI/Image/Image-Style-Transfer', view_func=DIP.style_transfer_front, methods=['GET', 'POST'])
app.add_url_rule('/AI/Image/GANs/Upscaling', view_func=DIP.upscaling, methods=['GET'])
app.add_url_rule('/AI/Image/YOLO', view_func=temp_redirect, methods=['GET', 'POST'])
#AIs
app.add_url_rule('/AI/Process/neural-style-image', view_func=DIP.neuralStyleTransfer, methods=['POST'])

app.add_url_rule('/AI/Text', view_func=temp_redirect, methods=['GET']) #DIP.upscaling)

app.add_url_rule('/misc', view_func=miscs.misc, methods=['GET'])
app.add_url_rule('/misc/api/whatsapp-redirect', view_func=miscs.whatsappapi, methods=['GET'])

app.add_url_rule('/IOT/DarkSourceOfCode', view_func=IOT.home_control, methods=['GET', 'POST'])
app.add_url_rule('/IOT/EvilKing', view_func=IOT.home_control2, methods=['GET', 'POST'])
app.add_url_rule('/IOT/wallLED', view_func=IOT.HexLED, methods=['GET', 'POST'])
app.add_url_rule('/IOT/switches', view_func=IOT.setflags, methods=['POST'])
app.add_url_rule('/IOT/DarkSourceOfCode/status', view_func=IOT.getStatus, methods=['GET'])
app.add_url_rule('/IOT/DarkSourceOfCode/getDHT', view_func=IOT.getSensorData, methods=['GET'])
app.add_url_rule('/IOT/hex/DarkSourceOfCode/getWallLEDStatus', view_func=IOT.showwallstatus, methods=['GET'])
app.add_url_rule('/IOT/hex/DarkSourceOfCode/setWallLEDStatus', view_func=IOT.changewallstatus, methods=['POST'])

# app.add_url_rule('/IOT/EvilKing', view_func=IOT.home_control, methods=['GET', 'POST'])

app.add_url_rule('/error/broken', view_func=broken, methods=['GET'])
app.add_url_rule('/error/fileDeleted', view_func=fileDeleted , methods=['GET'])
app.add_url_rule('/error/Virus', view_func=Virus, methods=['GET']) 
app.add_url_rule('/error/brokenLink', view_func=brokenLink, methods=['GET']) 
app.add_url_rule('/error/WorkingOnIT', view_func=WorkingOnIT, methods=['GET'])
app.add_url_rule('/error/internal', view_func=internal, methods=['GET']) 
app.add_url_rule('/error/AttackOnBugs', view_func=AttackOnBugs, methods=['GET']) 
app.add_url_rule('/error/angryAI', view_func=angryAI, methods=['GET']) 

# log url
app.add_url_rule('/feedback', view_func=uiui, methods=['GET']) 
@app.route('/logDarkSourceOfCode', methods=["POST"])
def logg_details():
	req = request.get_json(force=True)
	key = req['secret_key']
	# if key == 'I Solemnly Swear That I Am Up To No Good':
	# 	pass
	s = req['data']
	with open("ledger.log", "a") as file:
		file.write(str(s))
	# else:
	return "Ok"

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

# def upload_file():
# 	if request.method == 'POST':
# 		# check if the post request has the file part
# 		# if 'file' not in request.files:
# 		# 	flash('No file part')
# 		# 	return redirect(request.url)
# 		file = request.files['file']
# 		# # if user does not select file, browser also
# 		# # submit an empty part without filename
# 		# if file.filename == '':
# 		# 	flash('No selected file')
# 		# 	return redirect(request.url)
# 		if file and allowed_file(file.filename):
# 			filename = secure_filename(file.filename)
# 			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# 			# with open(filename, "rb") as myfile:
# 			# s3.Bucket('mlbotsimagegansdump').put_object(Key=filename, ContentDisposition='inline;filename=%s'%filename, ContentType='mimetype', Body=file)
# 			# print("done uploading")
# 			# object = s3.Object('mlbotsimagegansdump',filename)
# 			# object.Acl().put(ACL='public-read')

# 			return {"awsurl": "dfos"}
# 	return '''
# 	Some error Encountered: No File selected or such.
# 	'''