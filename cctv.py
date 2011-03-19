import simplekml
import psycopg2
import web
from shapely.wkt import loads
 
DEBUG=False

urls = (
	'/', 'getcctvs',
)

if DEBUG:
	app = web.application(urls, globals())
else:
	app = web.application(urls, globals()).wsgifunc()	

class getcctvs:
	def GET(self):
		global DEBUG
		qs=web.ctx.query.split('=')
		(minlon,minlat,maxlon,maxlat)=qs[1].split(',')
		#print (minlon,minlat,maxlon,maxlat)
		web.header('Content-Type', 'application/vnd.google-earth.kml+xml')
		kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Folder><name>Camera\'s</name>'
		minlon=float(minlon)
		minlat=float(minlat)
		maxlon=float(maxlon)
		maxlat=float(maxlat)
		sql = """SELECT ST_AsText(way), (planet_osm_point.name) , planet_osm_nodes.tags FROM planet_osm_point
		INNER JOIN planet_osm_nodes
		ON planet_osm_point.osm_id = planet_osm_nodes.id
		WHERE 
			man_made = 'surveillance' AND
			ST_Within(
				way,
				transform(
					transform(ST_GeomFromText('POLYGON((%.6f %.6f,%.6f %.6f,%.6f %.6f,%.6f %.6f,%.6f %.6f))',4326)
					,28992)
				, 4326)
			);""" % (minlon,minlat,maxlon,minlat,maxlon,maxlat,minlon,maxlat,minlon,minlat)
		if DEBUG:
			print sql
		conn = psycopg2.connect("host=10.0.0.6 dbname=osm user=osm password=osm")
		c = conn.cursor()
		c.execute(sql)
		conn.commit()
		for row in c:
			#print row[0]
			point = loads(row[0])
			if DEBUG:
				print row[2]
			#adres="lalala"
			pm = "<Placemark><name>%s</name><description>%s</description><Point><coordinates>%.6f,%.6f</coordinates></Point></Placemark>" % ("camera","camera",point.x,point.y)
			kml += pm
			#print point.x
		return kml

if __name__ == "__main__": app.run()