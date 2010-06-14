# -*- coding: utf-8 -*-
# by kay - basic functions

### config for Trunk
DSN = 'dbname=gis'

import sys
import psycopg2
import csv
from numpy import *

highwaytypes = {
    'secondary':['<1,0.9,0.9>',1.0],
    'residential':['<0.9,0.9,0.9>',0.8],
    'living_street':['<0.8,0.8,0.9>',0.8],
    'unclassified':['<0.8,0.8,0.8>',0.8],
    'service':['<0.8,0.8,0.8>',0.6],
    'pedestrian':['<0.8,0.9,0.8>',0.8],
    'footway':['<0.8,0.9,0.8>',0.3],
    'cycleway':['<0.8,0.8,0.9>',0.3],
    'path':['<0.8,0.9,0.8>',0.5]
    }

def avg(a,b): return (a+b)/2.0

def shift_by_meters(lat, lon, brng, d):
    R = 6371000.0 # earth's radius in m
    lat=math.radians(lat)
    lon=math.radians(lon)
    lat2 = math.asin( math.sin(lat)*math.cos(d/R) + 
                      math.cos(lat)*math.sin(d/R)*math.cos(brng))
    lon2 = lon + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat), 
                             math.cos(d/R)-math.sin(lat)*math.sin(lat2))
    lat2=math.degrees(lat2)
    lon2=math.degrees(lon2)
    return [lat2,lon2]

def calc_bearing(x1,y1,x2,y2,side):
    Q = complex(x1,y1)
    R = complex(x2,y2)
    v = R-Q
    if side=='left':
        v=v*complex(0,1);
    elif side=='right':
        v=v*complex(0,-1);
    else:
        raise TypeError('side must be left or right')
    #v=v*(1/abs(v)) # normalize
    angl = angle(v) # angle (radians) (0°=right, and counterclockwise)
    bearing = math.pi/2.0-angl # (0°=up, and clockwise)
    return bearing

def pov_highway(f,highway):
    highwaytype = highway[1]
    #highwaytype = 'secondary'
    highwayparams = highwaytypes.get(highwaytype)
    linestring = highway[2]
    linestring = linestring[11:] # cut off the "LINESTRING("
    linestring = linestring[:-1] # cut off the ")"
    points = linestring.split(',')

    numpoints = len(points)
    f.write("sphere_sweep {{ cubic_spline, {0},\n".format(numpoints+2))
    f.write("/* osm_id={0} */\n".format(highway[0]))

    for i,point in enumerate(points):
        latlon = point.split(' ')
        if (i==0):
            f.write("  <{0}, 0, {1}>,5*{2}\n".format(latlon[0],latlon[1],highwayparams[1]))
        f.write("  <{0}, 0, {1}>,5*{2}\n".format(latlon[0],latlon[1],highwayparams[1]))
        if (i==numpoints-1):
           f.write("  <{0}, 0, {1}>,5*{2}\n".format(latlon[0],latlon[1],highwayparams[1]))

    print highwayparams[0],highwayparams[1]
    f.write("""  tolerance 1000
   
   pigment {{
      color rgb {0}
   }}
   scale <1, 0.1, 1>
}}
\n""".format(highwayparams[0]))

def pov_camera(f,bbox):
    polygonstring = bbox[0][0]
    polygonstring = polygonstring[9:] # cut off the "POLYGON(("
    polygonstring = polygonstring[:-2] # cut off the "))"
    print polygonstring
    points = polygonstring.split(',')

    numpoints = len(points)

    for i,point in enumerate(points):
        latlon = point.split(' ')
        if (i==0):
            left=float(latlon[0])
            bottom=float(latlon[1])
        if (i==2):
            right=float(latlon[0])
            top=float(latlon[1])

    print bottom,left,top,right
    zoom = 1.0
    zoom = 2500.0/zoom
    f.write("""
camera {{
   orthographic
   location <{0}, 10000, {1}-500>
   sky <0, 1, 0>
   direction <0, 0, 1>
   right <1.3333*{2}, 0, 0>
   up <0, 1*{2}, 0>
   look_at <{0}, 0, {1}>
}}
\n""".format(avg(left,right),avg(bottom,top),zoom))
    f.write("""
box {{
   <{0}, -0.5, {1}>, <{2}, -0.0, {3}>
   
   pigment {{
      color rgb <1, 1, 0.901961>
   }}
}}
\n""".format(left,bottom,right,top))
    f.write("""
light_source {{
   <{0}, 50000, {1}>, rgb <1, 1, 1>
}}
\n""".format(avg(left,right),avg(bottom,top)))


if len(sys.argv) == 2:
    DSN = sys.argv[1]
else:
    print "using default: DSN=", DSN

print "Opening connection using dns:", DSN
conn = psycopg2.connect(DSN)
print "Encoding for this connection is", conn.encoding
curs = conn.cursor()

f = open('/home/kayd/workspace/Parking/osray/pov_highways.pov', 'w')

"""
SELECT ST_AsText(transform("way",4326)) AS geom
FROM planet_osm_line
WHERE "way" && transform(SetSRID('BOX3D(9.92498 49.78816,9.93955 49.8002)'::box3d,4326),900913)
LIMIT 10;

SELECT highway,ST_AsText(transform("way",4326)) AS geom
FROM planet_osm_line
WHERE "way" && transform(SetSRID('BOX3D(9.92498 49.78816,9.93955 49.8002)'::box3d,4326),900913)
and highway='secondary' LIMIT 50;
"""

latlon= 'ST_Y(ST_Transform(ST_line_interpolate_point(way,0.5),4326)),ST_X(ST_Transform(ST_line_interpolate_point(way,0.5),4326))'
coords= "ST_Y(ST_line_interpolate_point(way,0.5)) as py,ST_X(ST_line_interpolate_point(way,0.5)) as px,ST_Y(ST_line_interpolate_point(way,0.49)) as qy,ST_X(ST_line_interpolate_point(way,0.49)) as qx,ST_Y(ST_line_interpolate_point(way,0.51)) as ry,ST_X(ST_line_interpolate_point(way,0.51)) as rx"
FW = "FROM planet_osm_line WHERE"

### display disc - maxstay

curs.execute("SELECT ST_AsText(transform(SetSRID('BOX3D(9.92498 49.78816,9.93955 49.8002)'::box3d,4326),900913)) AS geom")
bbox = curs.fetchall()
pov_camera(f,bbox)

highways = []
for highwaytype in highwaytypes.iterkeys():
    curs.execute("SELECT osm_id,highway,ST_AsText(\"way\") AS geom "+FW+" \"way\" && transform(SetSRID('BOX3D(9.92498 49.78816,9.93955 49.8002)'::box3d,4326),900913) and highway='"+highwaytype+"' LIMIT 2000;")
    highways += curs.fetchall()

#print highways

for highway in highways:
    pov_highway(f,highway)

f.close()

conn.rollback()

sys.exit(0)

                             
"""
SELECT
   ST_Y(way) AS lat_wgs84,
   ST_X(way) AS lon_wgs84,
   ST_X(transform(way, 31466)) AS KOORD_X,
   ST_Y(transform(way, 31466)) AS KOORD_Y,
   skeys(tags) AS key,
   svals(tags) AS value,
   osm_id
FROM
   dortmund_point
WHERE
   exist(tags, 'amenity')
LIMIT 10;

SELECT
   ST_Y(way) AS lat_wgs84,
   ST_X(way) AS lon_wgs84,
   ST_X(transform(way, 31466)) AS KOORD_X,
   ST_Y(transform(way, 31466)) AS KOORD_Y,
   key,
   value,
   tags->'name' as name,
   osm_id
FROM
   (SELECT
       osm_id, way, tags,
       (each(tags)).key,
       (each(tags)).value
    FROM
       dortmund_point
    WHERE
       exist(tags, 'amenity') /*AND exist(tags, 'name')*/
   ) AS sq
WHERE
   key = 'amenity'
LIMIT 10;

SELECT
   ST_Y(way) AS lat_wgs84,
   ST_X(way) AS lon_wgs84,
   ST_X(transform(way, 31466)) AS KOORD_X,
   ST_Y(transform(way, 31466)) AS KOORD_Y,
   key,
   value,
   tags->'name' as name,
   tags->'sport' as sport,
   osm_id
FROM
   (SELECT
       osm_id, tags,
       ST_Centroid(way) as way,
       (each(tags)).key,
       (each(tags)).value
    FROM
       dortmund_polygon
    WHERE
       tags->'natural' = 'water'
       AND
       tags->'sport' = 'swimming'
   ) AS sq
WHERE
   key = 'natural'
LIMIT 10;
"""

