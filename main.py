#!/opt/local/bin/python3.7
#from flask import Flask, url_for
# from flask import request
from pprint import pprint
#import fillicspdf
import re

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
#app = Flask(__name__)


def fillpdf(request):
    print("Fillpdf")
    try:
        payload = request.json
        # filename = "IAP-"+payload['200_incident_name'] \
            #            + '-op' + payload['200_operational_period'] \
            #            + '-' + re.sub(r'/', '_', payload['200_op_start_date']) \
            #            + '.pdf'
        filename = 'test'
        print("Filename: ", filename)

        # fillicspdf.fill_pdf(payload, filename)
        url = request.url_root+'IAPs/'+filename
        print("URL: ", url)
    except Exception as e:
        print("Failure:", e)
    return url

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/0.12/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'

def hello(request):
    print(request.headers, file=open("server.log", "a"))
    return 'Hello World! ('+request.json['name']+')'


# if __name__ == '__main__':
#     # This is used when running locally only. When deploying to Google App
#     # Engine, a webserver process such as Gunicorn will serve the app. This
#     # can be configured by adding an `entrypoint` to app.yaml.
#     app.run(host='127.0.0.1', port=8080, debug=True)
