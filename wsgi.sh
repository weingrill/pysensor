#!/bin/bash
#su - jwe -s /bin/bash -c '/home/jwe/src/pysensor/wsgi.sh'
cd /home/jwe/src/pysensor
. pysensorenv/bin/activate
uwsgi --ini pysensor.ini
