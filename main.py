#!/opt/local/bin/python3.7
from flask import Flask, request, url_for
from pprint import pprint
import fillicspdf
import re

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/fillpdf', methods = ['PUT', 'POST'])
def fillpdf():
    payload = request.json
    filename = "IAP-"+payload['200_incident_name'] \
               + '-op' + payload['200_operational_period'] \
               + '-' + re.sub(r'/', '_', payload['200_op_start_date']) \
               + '.pdf'

    fillicspdf.fill_pdf(payload, filename)

    url = request.url_root+'IAPs/'+filename
    return url

@app.route('/', methods = ['PUT', 'POST'])
def hello():
    print(request.headers, file=open("server.log", "a"))
    return 'Hello World! ('+request.json['name']+')'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)