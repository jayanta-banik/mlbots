from flask import Flask, flash, redirect, render_template, jsonify, request, send_from_directory, url_for, flash

def misc(): return render_template('misc.html')
def whatsappapi(): return render_template('whatsappapi.html')