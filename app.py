# ALL IMPORTS
from flask import Flask, render_template, request, make_response, jsonify
from flask.json import jsonify 
from werkzeug.debug import DebuggedApplication
import os

project_root = os.getcwd()
template_path = os.path.join(project_root, 'templates')

app = Flask(__name__,template_folder=template_path)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

# GLOBAL FUNCTIONS
def get_response(hostname, headers=None):
  import requests
  try:
    r = requests.get(hostname, headers=headers)
  except requests.exceptions.RequestException as e:
    return 
  return r

def parse_headers(text):
  if len(text) == 0:
    return
  dictionary = {}
  for t in text.strip().split(';'):
    try: #oh my god
      new = t.strip().split(':')
    except IndexError:
      return
    try: #why
      dictionary[new[0]] = new[1]
    except IndexError:
      return
  return dictionary

def parse_aka_headers(text):
  if len(text) == 0:
    return
  return text
  
def merge_headers(a,b):
	if a is not None:
	  try:
	    a["Pragma"] = b
	  except TypeError:
	    return a
	  return a
	else:
		return {"Pragma": b}
		
# for POST requests
def send_post(hostname,headers=None,data=None):
	import requests
	try: 
		r = requests.post(hostname,headers=headers,data=data)
	except requests.exceptions.RequestException as e:
		return
	return r

def parse_data(text):
	d = {}
	for t in text.strip().split('&'):
		try:
			new = t.strip().split('=')
			d[new[0]] = new[1]
		except IndexError:
			return
	return d

app.jinja_env.globals.update(get_response = get_response)
app.jinja_env.globals.update(parse_headers = parse_headers)
app.jinja_env.globals.update(parse_aka_headers = parse_aka_headers)
app.jinja_env.globals.update(merge_headers = merge_headers)
app.jinja_env.globals.update(send_post = send_post)
app.jinja_env.globals.update(parse_data = parse_data)

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
  	if request.form.get("method") == "GET":
  		return render_template("form_response.html")
  	else:
  		return render_template("form_response_post.html")
  return render_template("index.html")
  
@app.route('/api', methods=["GET","POST"])
def api():
	import json
	code = None
  #return render_template("api.html", req=request.headers)
	req = request.headers.get('Content-Type')
	# DEBUG
	''' 
	if req is not None:
		return req
	else:
		return "<h1>Blah</h1>"
	'''
	if req is not None:
		if req == 'application/json':
			resp = make_response(jsonify({k:v for k,v in request.headers.iteritems()}))
			resp.headers['Content-Type'] = "application/json"
			return resp
		elif req == 'text/html':
			return "<h1>You have requested for the text/html MIME type. Please request JSON.</h1>"
		else:
			return "<h1>Not sure what happened here.</h1>"
	else:	
		code = request.headers.items()
		#return render_template('api_response.html', code=code)
		return "<p>Content Type not set. Please send proper headers.</p>"

@app.route('/api/v1/lang', methods=["GET","POST"])
def api_lang():
	import re
	req = request.headers.get("Accept-Language")
	if req == None:
		return "<h1>No language set.</h1>"
	elif req.lower() in 'fr-fo':
		return render_template("lan/fr.html")
	elif req.lower() in 'ja-jp':
		return render_template("lan/ja.html")
	else:
		return render_template("lan/eng.html")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
