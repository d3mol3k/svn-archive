#include "Segment.h"
#include "RouteMetaDataHandler.h"

/*
Copyright (C) 2005 Nick Whitelegg, Hogweed Software, nick@hogweed.org

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111 USA

 */
namespace OpenStreetMap
{

void Segment::toOSM(QTextStream& outfile)
{
    nodes[0]->toOSM(outfile);
    nodes[1]->toOSM(outfile);
    segToOSM(outfile);
}
// 180306 updated to 0.3
void Segment::segToOSM(QTextStream &outfile, bool allUid)
{
    outfile << "<segment from='"
                << nodes[0]->getOSMID() <<
                   "' to='"
                << nodes[1]->getOSMID() << "' ";
    int sent_id = (osm_id>0 || (allUid&&osm_id)) ? osm_id : 0;
    
    outfile << " id='" << sent_id   << "'>" << endl;

    QString tags = "";

    //  avoid dumping the name too many times
    if(name!="")
        outfile << "<tag k='name' v='" << name << "' />" << endl;

	// Only write out the type if the segment does not belong to a way;
	// if it does, the segment will be assumed to have the same type as the way
	if(!wayStatus)
	{
		// 130506 change to use the new styles of tag (highway etc)
    	RouteMetaDataHandler mdh;
    	RouteMetaData metaData = mdh.getMetaData(type);
    	if(metaData.foot!="no")
       		outfile << "<tag k='foot' v='" << metaData.foot << "' />" << endl;
   		if(metaData.horse!="no")
       		outfile << "<tag k='horse' v='" << metaData.horse << "' />" << endl;
   		if(metaData.bike!="no")
       		outfile << "<tag k='bicycle' v='" << metaData.bike << "' />" 
					<< endl;
   		if(metaData.car!="no")
       		outfile << "<tag k='motorcar' v='" << metaData.car 
					<< "' />" << endl;
   		if(metaData.routeClass!="")
       		outfile << "<tag k='highway' v='" << metaData.routeClass << 
					"' />" << endl;
   		if(metaData.railway!="")
       		outfile << "<tag k='railway' v='" << metaData.railway << 
					"' />" << endl;
	}


   outfile << "</segment>" <<endl;


}
// 180306 updated to 0.3
QByteArray Segment::toOSM()
{
    QByteArray xml;
    QTextStream str(xml, IO_WriteOnly);
    str<<"<osm version='0.3'>"<<endl;
    segToOSM(str);
    str<<"</osm>"<<endl;
    str<<'\0';
    return xml;
}

// Upload an existing (or new) segment to OSM
// 130506 removed this old curl way of doing it

}
