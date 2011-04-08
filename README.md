cctv.py
=======

This is a python script that reads all CCTV cameras from a local OpenStreetMap PostGIS database and spits them out as KML. It takes the standard BBOX=minlon,minlat,maxlon,maxlat as querystring so you can just plug it into Google Earth as a network link.

installation
------------
You will need a local database with all CCTV cameras from OSM in the osmosis DB schema. There's a step-by-step on how to accomplish that  [here](https://docs.google.com/document/pub?id=1paaYsOakgJEYP380R70s4SGYq8ME3ASl-mweVi1DlQ4).

You will also need a web server with WSGI, instructions for Apache are [here](http://webpy.org/cookbook/mod_wsgi-apache). These instructions are for Apache 1.x it looks like. Adapt for 2.x if you use that. You can also adapt the script to work with another python interface. The web.py documentation will tell you how.

Add something like this to your Apache config:
    WSGIScriptAlias /cctv /home/mvexel/www/cctv/cctv.py/
    Alias /cctv/static /home/mvexel/www/cctv/static/
    AddType text/html .py

    <Directory /home/mvexel/www/cctv/>
        Order deny,allow
        Allow from all 
    </Directory>

Put cctv.py somewhere in your web tree and navigate to yourserver/cctv/?BBOX=4.9,52.35,4.95,52.40. The result should be a KML file with some cameras - if the example bounding box is in your database.

usage
-----
Ad a 'Network Link' in Google Earth pointing to http://yourserver/pathtocctv/

adapting for other tags
-----------------------
You can change the script easily to extract other features from the database. The only change necessary would be to adapt the first WHERE clause (man_made = 'surveillance') to a different key/value pair, and the name / description in the Placemark output. You would of course need to make sure that the features you want are in your local database as well. This requires adapting the how-to for the database setup to your particular needs.
