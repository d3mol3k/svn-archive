#ifndef WAY_H
#define WAY_H

/*
 Copyright (C) 2006 Nick Whitelegg, Hogweed Software, nick@hogweed.org

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

#include "Node.h"
#include "Object.h"

#include <vector>


namespace OSM
{

class Way: public Object
{
public:
	Way(int id = 0) : Object(id)
	{
	}

	void addNode(int n)
	{
		nodes.push_back(n);
	}

	int removeNode(int);

	bool addNodeAt(int index, int n);

	int getNode(int i) const;

	int nNodes() const
	{
		return nodes.size();
	}

	void toXML(std::ostream &strm);

private:
	std::vector<int> nodes;
};

}

#endif
