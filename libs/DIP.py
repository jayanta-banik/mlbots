from flask import render_template, request, jsonify
import os
from libs.ImageAI import Style_Transfer

def imageMenu(): return render_template('DIP.html')
def upscaling(): return render_template('upscaling.html')
def style_transfer_front(): return render_template('style_transfer.html')

def neuralStyleTransfer():
    req = request.get_json(force=True) 
    uri_conte = "res/" + req['content']
    uri_style = "res/" + req['style']
    uri_blend = 1 - float(req['blend_percentage'])/100
    return jsonify({"awsuri": Style_Transfer.applyTransfer(uri_conte, uri_style, uri_blend)})