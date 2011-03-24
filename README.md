cctv.py
=======

This is a python script that reads all CCTV cameras from a local OpenStreetMap PostGIS database and spits them out as KML. It takes the standard BBOX=minlon,minlat,maxlon,maxlat as querystring so you can just plug it into Google Earth as a network link.

installation
------------
You will need a local OSM database created with osm2pgsql. See [here](http://wiki.openstreetmap.org/wiki/Osm2pgsql) for more info.

You will also need a web server with WSGI, instructions for Apache are [here](http://webpy.org/cookbook/mod_wsgi-apache). These instructions are for Apache 1.x it looks like. Adapt for 2.x if you use that. You can also adapt the script to work with another python interface. The web.py documentation will tell you how.

Add something like this to your Apache config:
    WSGIScriptAlias /sqftenvy /home/mvexel/www/sqftenvy/sqftenvy.py/
    Alias /sqftenvy/static /home/mvexel/www/sqftenvy/static/
    AddType text/html .py

    <Directory /home/mvexel/www/sqftenvy/>
        Order deny,allow
        Allow from all 
    </Directory>

Put cctv.py somewhere in your web tree and navigate to yourserver/pathtocctv/?BBOX=4.9,52.35,4.95,52.40. The result should be a KML file with some cameras - if the example bounding box is in your database.

usage
-----
Ad a 'Network Link' in Google Earth pointing to http://yourserver/pathtocctv/

adapting for other tags
-----------------------
You can change the script easily to extract other features from the database. The only change necessary would be to adapt the first WHERE clause (man_made = 'surveillance') to a different key/value pair, and the name / description in the Placemark output. 
