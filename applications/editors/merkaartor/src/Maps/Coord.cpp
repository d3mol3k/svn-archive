#include "Coord.h"
#include "Utils/LineF.h"

#include <stdio.h>

/*
double angle(Coord & vertex, Coord p1, Coord p2)
{
	p1=p1-vertex;
	p2=p2-vertex;
	return angle(p2)-angle(p1);
}
*/
double angle(Coord p1)
{
	if (p1.length() == 0)
		return 0;
	double adjacent = (double)p1.lon() / p1.length();
	if (p1.lat() > 0)
		return acos(adjacent);
	return -acos(adjacent);
}

void rotate(Coord & p1,double angle)
{
	Coord p1p(int(sin(angle)*p1.lon()+cos(angle)*p1.lat()),int(cos(angle)*p1.lon()-sin(angle)*p1.lat()));
	p1=p1p;
}

CoordBox::CoordBox(const CoordBox &cb)
: BottomLeft(cb.bottomLeft()), TopRight(cb.topRight())
{
}

CoordBox::CoordBox(const Coord &C1, const Coord &C2)
: BottomLeft(C1.lat()<C2.lat()?C1.lat():C2.lat() , C1.lon()<C2.lon()?C1.lon():C2.lon()),
TopRight(C1.lat()>C2.lat()?C1.lat():C2.lat() , C1.lon()>C2.lon()?C1.lon():C2.lon())
{
}

CoordBox CoordBox::zoomed(double f) const
{
	Coord C(center());
	int DLat = int(latDiff()/2*f);
	int DLon = int(lonDiff()/2*f);
	return CoordBox(Coord(C.lat()-DLat,C.lon()-DLon), Coord(C.lat()+DLat,C.lon()+DLon) );
}

bool CoordBox::toXML(QString elName, QDomElement& xParent) const
{
	bool OK = true;

	QDomElement e = xParent.ownerDocument().createElement(elName);
	xParent.appendChild(e);

	TopRight.toXML("topright", e);
	BottomLeft.toXML("bottomleft", e);

	return OK;
}

CoordBox CoordBox::fromXML(QDomElement e)
{
	Coord tr = Coord::fromXML(e.firstChildElement("topright"));
	Coord bl = Coord::fromXML(e.firstChildElement("bottomleft"));

	return CoordBox(tr, bl);
}

double Coord::distanceFrom(const Coord& other) const
{
	int dlon = other.lon() - lon();

	const double slat1 = sin(coordToRad(lat()));
	const double clat1 = cos(coordToRad(lat()));

	const double slat2 = sin(coordToRad(other.lat()));
	const double clat2 = cos(coordToRad(other.lat()));

	const double sdlon = sin(coordToRad(dlon));
	const double cdlon = cos(coordToRad(dlon));

	const double t1 = clat2 * sdlon;
	const double t2 = clat1 * slat2 - slat1 * clat2 * cdlon;
	const double t3 = slat1 * slat2 + clat1 * clat2 * cdlon;
	const double dist = atan2(sqrt(t1*t1 + t2*t2), t3);

	const double earthRadius = 6372.795;
	return dist * earthRadius;
}

bool Coord::toXML(QString elName, QDomElement& xParent) const
{
	bool OK = true;

	QDomElement e = xParent.ownerDocument().createElement(elName);
	xParent.appendChild(e);

	e.setAttribute("lon",QString::number(coordToAng(Lon),'f',8));
	e.setAttribute("lat", QString::number(coordToAng(Lat),'f',8));

	return OK;
}

Coord Coord::fromXML(QDomElement e)
{
	int lat = angToCoord(e.attribute("lat").toDouble());
	int lon = angToCoord(e.attribute("lon").toDouble());

	return Coord(lat, lon);
}

void CoordBox::resize(double d)
{
	int dlat = int((TopRight.lat()-BottomLeft.lat())*(d-1)/2);
	int dlon = int((TopRight.lon()-BottomLeft.lon())*(d-1)/2);
	BottomLeft.setLat(BottomLeft.lat()-dlat);
	BottomLeft.setLon(BottomLeft.lon()-dlon);
	TopRight.setLat(TopRight.lat()+dlat);
	TopRight.setLon(TopRight.lon()+dlon);
}

bool CoordBox::visibleLine(const CoordBox & viewport, Coord & last, Coord & here)
{
	if (viewport.contains(last) && viewport.contains(here))
		return true;

	Coord A, B;
	LineF(last, here).intersectionWith(viewport, &A, &B);
	if (A.isNull() && B.isNull())
		return false;

	if (!A.isNull() && !B.isNull()) {
		last = A;
		here = B;
		return true;
	}

	if (viewport.contains(here))
		last = A;
	else
		here = A;

	return true;
//	return viewport.intersects( CoordBox(last, here) );
}

uint qHash(const Coord &c)
{
    return (uint)(c.lat() + 65537 * c.lon());
}
