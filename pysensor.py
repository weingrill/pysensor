'''
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04
'''

from flask import Flask
from flask import request
from flask_sslify import SSLify
import sqlite3
import datetime
import _config

application = Flask(__name__)
sslify = SSLify(application)

@application.route("/hello")
def hello():
    '''a hello world demo for testing'''
    return "<h1 style='color:blue'>Hello There!</h1>"

@application.route("/createdb")
def createdb():
    '''creates the database table'''
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
    '''if the authtoken in the JSON is correct, data will be stored to the DB'''
    if not u'authtoken' in data or data[u'authtoken'] != _config.authtoken:
        return "invalid authtoken"

    conn = sqlite3.connect('pysensor.db')
    c = conn.cursor()

    data[u'value'] = float(data[u'value'])
    # Insert data
    if not u'timestamp' in data or data[u'timestamp']=='':
        data[u'timetamp'] = datetime.datetime.utcnow().isoformat()
    c.execute("INSERT INTO sensordata VALUES ('%(device)s',%(value)f,'%(timestamp)s')" % data)
    conn.commit()
    conn.close()

def getdata():
    '''fetches the data from the database and returns it as a string'''
    conn = sqlite3.connect('pysensor.db')
    c = conn.cursor()

    c.execute("SELECT device, value, timestamp from sensordata LIMIT 10")
    data = c.fetchall()
    conn.close()
    return str(data)

@application.route('/',methods=['GET', 'POST'])
def base():
    '''root directory accepts both GET and POST methods'''
    if request.method == 'GET':
        return getdata()
    elif request.method == 'POST':
        if not request.is_json:
            return 'invalid JSON object\n%s' % str(request)
        content = request.get_json()
        print (content)
        savedata(content)
        return 'JSON posted'

if __name__ == "__main__":
    application.run()
