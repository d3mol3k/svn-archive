/*
    Copyright (C) 2005 Nick Whitelegg, Hogweed Software, nick@hogweed.org 

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111 USA

 */

#include "GPXParser.h"

#include <iostream>
#include <cstdlib>
using std::cout;
using std::endl;
using std::cerr;

namespace OpenStreetMap 
{

GPXParser::GPXParser(  )
{
	inDoc = inWpt = inTrk = inName = inTrkpt = inType = 
	inTrkseg = foundSegType = false;
	components = new Components;
	trkptCount = 0;
}

bool GPXParser::startDocument()
{
	cerr<<"startDocument()"<<endl;	
	inDoc = true;
	return true;
}

bool GPXParser::endDocument()
{
	cerr<<"endDocument()"<<endl;	
	inDoc = false;
	return true;
}

bool GPXParser::startElement(const QString&,const QString&,
						const QString& element,
						const QXmlAttributes& attributes)
{
	cerr<<"startElement(): element: "<<element<<endl;
	if(inDoc)
	{
		if(element=="wpt")
		{
			inWpt=true;
		}
		else if (element=="trk")
		{
			inTrk=true;
		}
		else if (element=="trkseg")
		{
			inTrkseg=true;
			segStart=trkptCount;
		}
		else if (element=="name" && (inWpt||inTrkpt||inTrk))
			inName=true;
		else if (element=="type" && (inWpt||inTrk||inTrkseg))
		{
			inType=true;
			if(inTrkseg) foundSegType=true;
		}
		else if (element=="time" && (inWpt||inTrkpt))
			inTime=true;
		else if (element=="trkpt" && inTrk)
		{
			inTrkpt = true;
			trkptCount++;
		}

		if(element=="wpt"||element=="trkpt"||element=="polypt")
		{
			for(int count=0; count<attributes.length(); count++)
			{
				if(attributes.qName(count)=="lat")
					curLat = atof (attributes.value(count).ascii());		
				else if(attributes.qName(count)=="lon")
					curLong = atof (attributes.value(count).ascii());
			}
		}
	}
	return true;
}

bool GPXParser::endElement(const QString&,const QString&,
						const QString&	element)
{
	cerr<<"endElement(): element: "<<element<<endl;
	if(inTrkpt && element=="trkpt")
	{
		components->addTrackpoint(curTimestamp,curLat,curLong);
		inTrkpt = false;
	}

	else if(inTrk && element=="trk")
	{
		cerr<<"setting track ID: " << curName << endl;
		components->setTrackID (curName);
		inTrk = false;
	}

	else if(inName && element=="name")
		inName=false;

	else if(inType && element=="type")
		inType=false;


	
	else if(inWpt && element=="wpt")
	{
		cerr<<"adding waypoint:" <<
				curName <<" " << curLat << " " << curLong << " "
				<< atoi(curType.ascii()) << endl;
		components->addWaypoint(Waypoint(curName,curLat,curLong,curType));
		inWpt = false;
	}

	// If the segment had a type, add the segment to the segment table.
	else if (inTrkseg && element=="trkseg")
	{
		if(foundSegType)
			components->addSegdef(segStart,trkptCount-1,curType);
		inTrkseg = foundSegType = false;
	}

	cerr<<"endElement done" << endl;
	return true;
}

bool GPXParser::characters(const QString& characters)
{
	cerr<<"characters(): " << characters << endl;
	if(characters=="\n") return true;
	cerr<<"inName: " << inName << endl;
	if(inName)
	{
		curName = characters;
		cerr << "curName set to " << curName << endl;
	}
	else if(inType)
		curType = characters; 
	else if(inTime)
		curTimestamp = characters; // 10/04/05 timestamp now string 
	return true;
}

}
////////////////////////////////////////////////////////////////////////////////



