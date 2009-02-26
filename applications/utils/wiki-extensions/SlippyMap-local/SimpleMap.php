<?php
# OpenStreetMap Simple Map - MediaWiki extension
# 
# This defines what happens when <map> tag is placed in the wikitext
# 
# We show a map based on the lat/lon/zoom data passed in. This extension brings in
# image generated by the static map image service called 'GetMap' maintained by OJW.  
#
# Usage example:
# <map lat=51.485 lon=-0.15 z=11 w=300 h=200 format=jpeg /> 
#
# Images are not cached local to the wiki.
# To acheive this (remove the OSM dependency) you might set up a squid proxy,
# and modify the requests URLs here accordingly.
#
##################################################################################
#
# Copyright 2008 Harry Wood, Jens Frank, Grant Slater, Raymond Spekking and others
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# @addtogroup Extensions
#


if( defined( 'MEDIAWIKI' ) ) {
	$wgExtensionFunctions[] = 'wfsimplemap';

	$wgExtensionCredits['parserhook'][] = array(
		'name'           => 'OpenStreetMap Simple Map',
		'author'         => '[http://harrywood.co.uk Harry Wood], Jens Frank',
		'svn-date'       => '$LastChangedDate: 2008-07-23 22:20:05 +0100 (Wed, 23 Jul 2008) $',
		'svn-revision'   => '$LastChangedRevision: 37977 $',
		'url'            => 'http://wiki.openstreetmap.org/wiki/Simple_image_MediaWiki_Extension',
		'description'    => 'Allows the use of the <tt><nowiki>&lt;map&gt;</nowiki></tt> tag to display a static map image. Maps are from [http://openstreetmap.org openstreetmap.org]',
		'descriptionmsg' => 'simplemap_desc',
	);

	$wgAutoloadClasses['SimpleMap'] = dirname( __FILE__ ) . '/SimpleMap.class.php';
	$wgExtensionMessagesFiles['SimpleMap'] = dirname( __FILE__ ) . "/SimpleMap.i18n.php";
	
	function wfsimplemap() {
		global $wgParser, $wgMapOfServiceUrl;
		# register the extension with the WikiText parser
		# the first parameter is the name of the new tag.
		# In this case it defines the tag <map> ... </map>
		# the second parameter is the callback function for
		# processing the text between the tags
		$wgParser->setHook( 'map', array( 'SimpleMap', 'parse' ) );
		$wgMapOfServiceUrl = "http://osm-tah-cache.firefishy.com/~ojw/MapOf/?";
	}

}
