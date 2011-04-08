import psycopg2
import web
from shapely.wkt import loads
 
DEBUG=False
db = {
	"host"		: "hades",
	"dbname"	: "osm_cctv",
	"user"		: "osm",
	"password"	: "osm"
	}

urls = (
	'/', 'getcctvs',
)

if DEBUG:
	app = web.application(urls, globals())
else:
	app = web.application(urls, globals()).wsgifunc()	
	application = app.wsgifunc()

class getcctvs:
	def GET(self):
		global DEBUG,db
		qs=web.ctx.query.lstrip('?').lower().split('=')
		print len(qs)
		print qs
		if not 'bbox' in qs:
			return "usage: cctv?bbox=minlon,minlat,maxlon,maxlat"
		else:
			(minlon,minlat,maxlon,maxlat)=qs[1].split(',')
			web.header('Content-Type', 'application/vnd.google-earth.kml+xml')
			kml = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2"><Folder><name>Camera\'s</name>'
			kml += """<Style id="cctvicon">
      <IconStyle>
         <Icon>
         	<color>ffffff00</color>
         	<href>https://www.securitycamera2000.com/CCTV/camera-icon.png</href>
         </Icon>
      </IconStyle>
   </Style>"""

			minlon=float(minlon)
			minlat=float(minlat)
			maxlon=float(maxlon)
			maxlat=float(maxlat)
			sql = """select ST_AsText(n.geom),n.tags,n.tstamp,u.name from nodes as n INNER JOIN users as u ON n.user_id = u.id where tags->'man_made'='surveillance' AND ST_Within(geom, ST_GeomFromText('POLYGON((%.6f %.6f,%.6f %.6f,%.6f %.6f,%.6f %.6f,%.6f %.6f))',4326));""" % (minlon,minlat,maxlon,minlat,maxlon,maxlat,minlon,maxlat,minlon,minlat)
			if DEBUG:
				print sql
				print " ".join(["%s=%s" % (k,v) for k,v in db.iteritems()])
			conn = psycopg2.connect(" ".join(["%s=%s" % (k,v) for k,v in db.iteritems()]))
			c = conn.cursor()
			c.execute(sql)
			conn.commit()
			for row in c:
				point = loads(row[0])
				if DEBUG:
					print row[2]
				descr = " <![CDATA[datum: %s\ngebruiker: <a href=""http://www.openstreetmap.org/user/%s"">%s</a>]]>" % (row[2],row[3],row[3])
				pm = """<Placemark>
				<styleUrl>#cctvicon</styleUrl>
				<name>%s</name>
				<description>%s</description>
				<Point>
				<coordinates>%.6f,%.6f</coordinates>
				</Point>
				</Placemark>""" % ("camera",descr,point.x,point.y)
				kml += pm
				del pm
			kml += "</Folder>\n</kml>"
			return kml
		
if __name__ == "__main__": app.run()