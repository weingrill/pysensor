'''
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04
'''

from flask import Flask
from flask import request
from flask_sslify import SSLify
import sqlite3
import datetime
import logging
import _config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

application = Flask(__name__)
sslify = SSLify(application)

@application.route("/hello")
def hello():
    '''a hello world demo for testing'''
    logger.debug('hello')
    return "<h1 style='color:blue'>Hello There!</h1>"

@application.route("/createdb")
def createdb():
    '''creates the database table'''
    logger.debug('createdb()')
    try:
        conn = sqlite3.connect('pysensor.db')
        c = conn.cursor()
        # Create table
        c.execute("CREATE TABLE sensordata (device text, value real, timestamp text)")
        conn.commit()
        conn.close()
    except e:
        return str(e)
    return "Database created"


'''
https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
'''

def savedata(data):
    '''if the authtoken in the JSON is correct, data will be stored to the DB'''
    logger.debug('savedata()')
    if not u'authtoken' in data or data[u'authtoken'] != _config.authtoken:
        logger.warn('invalid token')
        return "invalid authtoken"

    try:
        conn = sqlite3.connect('pysensor.db')
        c = conn.cursor()
    except e:
        logger.exception('cannot connect to db')
        return str(e)

    data[u'value'] = float(data[u'value'])
    # Insert data
    if not u'timestamp' in data or data[u'timestamp']=='':
        data[u'timetamp'] = datetime.datetime.utcnow().isoformat()
    try:
        logger.debug(str(data))
        c.execute("INSERT INTO sensordata VALUES ('%(device)s',%(value)f,'%(timestamp)s')" % data)
        conn.commit()
    except e:
        logger.exception('cannot commit')
        conn.close()
        return str(e)
    conn.close()

def getdata():
    '''fetches the data from the database and returns it as a string'''
    logger.debug('getdata()')
    try:
        conn = sqlite3.connect('pysensor.db')
        c = conn.cursor()
    except e:
        logger.exception('cannot connect to db')
        return str(e)

    c.execute("SELECT device, value, timestamp from sensordata LIMIT 10")
    data = c.fetchall()
    conn.close()
    return str(data)

@application.route('/',methods=['GET', 'POST'])
def base():
    '''root directory accepts both GET and POST methods'''
    logger.debug('base')
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
