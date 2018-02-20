'''
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04
'''

from flask import Flask
from flask import request
from flask_sslify import SSLify
import sqlite3

application = Flask(__name__)
sslify = SSLify(application)

@application.route("/hello")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@application.route("/createdb")
def createdb():
    conn = sqlite3.connect('pysensor.db')
    c = conn.cursor()
    # Create table
    c.execute("CREATE TABLE sensordata (device text, value real, timestamp text)")
    conn.commit()
    conn.close()
    return "Database created"


'''
https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
'''

def savedata(data):
    conn = sqlite3.connect('pysensor.db')
    c = conn.cursor()
    
    data[u'value'] = float(data[u'value'])
    # Insert data
    c.execute("INSERT INTO sensordata VALUES ('%(device)s',%(value)f,'%(timestamp)s')" % data)
    conn.commit()
    conn.close()

@application.route('/postjson', methods = ['POST'])
def postJsonHandler():
    if not request.is_json:
        return 'invalid JSON object'
    content = request.get_json()
    print (content)
    savedata(content)
    return 'JSON posted'

if __name__ == "__main__":
    application.run()
