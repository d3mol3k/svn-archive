<html>
<head>
    <title>OpenStreetMap</title>
    <script src="http://openlayers.org/api/OpenLayers.js"></script> 
    <script src="http://openstreetmap.org/openlayers/OpenStreetMap.js"></script>

    <script type="text/javascript">
        <?php
        $z = floor($_GET['zoom'] + 0);
        $lat = $_GET['lat'] + 0;
        $lon = $_GET['lon'] + 0;
        print " var lat = $lat;\n var lon = $lon;\n var zoom = $z;\n";
        
        $Base = '';
        $Tiles = 'tile.php?';
        if(array_key_exists('gpx', $_GET))
        {
          $gpx = $_GET['gpx'];
          $Base = sprintf("?gpx=%d", $gpx);
          $Tiles .= sprintf("gpx=%d&t=", $gpx);
        }
        else
        {
          $Tiles .= sprintf("t=", $gpx);
        }
        
        print "var routeServer = '$Tiles'\n";
        print "var extraUrlParams = '$Base';\n";
        ?>
        
	if (zoom==0)
	{
	 zoom = 2;
	 lon = 1.0996;
	 lat = 35.5862;
	}

	lat=parseFloat(lat)
	lon=parseFloat(lon)
	zoom=parseInt(zoom)
	        
        var map; //complex object of type OpenLayers.Map 

        //Initialise the 'map' object
        function init() {
          
            map = new OpenLayers.Map ("map", {
                controls:[
                    new OpenLayers.Control.Navigation(),
                    new OpenLayers.Control.Permalink('',extraUrlParams,''),
                     new OpenLayers.Control.LayerSwitcher(),
                    new OpenLayers.Control.PanZoomBar()],
                maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
                maxResolution: 156543.0399,
                numZoomLevels: 19,
                units: 'meters',
                projection: new OpenLayers.Projection("EPSG:900913"),
                displayProjection: new OpenLayers.Projection("EPSG:4326")
            } );
                

            // Define the map layer
            // Note that we use a predefined layer that will be
            // kept up to date with URL changes
            // Here we define just one layer, but providing a choice
            // of several layers is also quite simple
            // Other defined layers are OpenLayers.Layer.OSM.Mapnik and OpenLayers.Layer.OSM.Maplint
            layerTilesAtHome = new OpenLayers.Layer.OSM.Osmarender("Osmarender");


            route = new OpenLayers.Layer.OSM("Route",
              routeServer, //"tile.php?gpx=blibble&t=",
              {
                isBaseLayer: false, 
                type:'png', 
                /*opacity: 0.3*/
              },
              {'buffer':1});


            map.addLayer(layerTilesAtHome);
            map.addLayer(route);

            var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));

            map.setCenter (lonLat, zoom);
        }
        
    </script>
</head>

<!-- body.onload is called once the page is loaded (call the 'init' function) -->
<body onload="init();">

    <!-- define a DIV into which the map will appear. Make it take up the whole window -->
    <div style="width:100%; height:100%" id="map"></div>
    
</body>

</html>