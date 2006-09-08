##################################################################
package Geo::Tracks::NMEA;
##################################################################

use Exporter;
@ISA = qw( Exporter );
use vars qw(@ISA @EXPORT @EXPORT_OK %EXPORT_TAGS $VERSION);
@EXPORT = qw( read_track_NMEA );

use strict;
use warnings;

use Data::Dumper;
use Date::Manip;
use Date::Parse;
use Date::Parse;
use Date::Parse;
use IO::File;
use Math::Trig;

use Geo::Geometry;
use Utils::Debug;
use Utils::File;
use Utils::Math;

# -----------------------------------------------------------------------------
# Read GPS Data from NMEA - File
sub read_track_NMEA($) { 
    my $filename = shift;

    my $start_time=time();

    my $new_tracks={ 
	filename => $filename,
	tracks => [],
	wpt => []
	};
    printf STDERR ("Reading $filename\n") if $VERBOSE || $DEBUG;
    printf STDERR "$filename:	".(-s $filename)." Bytes\n" if $DEBUG;

    my $fh = data_open($filename);
    return $new_tracks unless $fh;
    my $elem ={};
    my $last_date='';
    my $last_time=0;
    my $new_track=[];
    my ($sat,$pdop,$hdop,$vdop,$sat_count);
    my $sat_time = 0;
    my $dop_time = 0;
    while ( my $line = $fh->getline() ) {
	my ($dummy,$type,$time,$status,$lat,$lat_v,$lon,$lon_v,$speed,$alt);
	my ($date,$mag_variation,$checksumm,$quality,$alt_unit);
	$alt=0;
	chomp $line;
	$line =~ s/\*(\S+)\s*$//;
	$checksumm=$1;
	($type,$line) = split( /,/,$line,2);
	$type =~ s/^\s*\$GP//;
	printf STDERR "type $type, line: $line, checksumm:$checksumm\n"
	    if $DEBUG>4;
	if ( $type eq "GGA" ) {
	    # GGA - Global Positioning System Fix Data
	    # Time, Position and fix related data fora GPS receiver.
	    #        1         2       3 4        5 6 7  8   9  10 |  12 13  14   15
	    #        |         |       | |        | | |  |   |   | |   | |   |    |
	    # $--GGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh<CR><LF>
	    #  1) Universal Time Coordinated (UTC)
	    #  2) Latitude
	    #  3) N or S (North or South)
	    #  4) Longitude
	    #  5) E or W (East or West)
	    #  6) GPS Quality Indicator, 0 - fix not available, 1 - GPS fix, 2 - Differential GPS fix
	    #  7) Number of satellites in view, 00 - 12
	    #  8) Horizontal Dilution of precision
	    #  9) Antenna Altitude above/below mean-sea-level (geoid) 
	    # 10) Units of antenna altitude, meters
	    # 11) Geoidal separation, the difference between the WGS-84 earth
	    #     ellipsoid and mean-sea-level (geoid), "-" means mean-sea-level below ellipsoid
	    # 12) Units of geoidal separation, meters
	    # 13) Age of differential GPS data, time in seconds since last SC104
	    #     type 1 or 9 update, null field when DGPS is not used
	    # 14) Differential reference station ID, 0000-1023
	    # 15) Checksum
	    ($time,$lat,$lat_v,$lon,$lon_v,$quality,$dummy,$dummy,$alt,$alt_unit,
	     $dummy,$dummy,$dummy)
		= split(/,/,$line);	    
	    #printf STDERR "(,$time,$status, la: $lat,$lat_v, lo: $lon,$lon_v, Q: $quality,,, Alt: $alt,$alt_unit,,,,)\n";

	} elsif ( $type eq "RMC" ) {
	    # RMC - Recommended Minimum Navigation Information
	    #        1         2 3       4 5        6 7   8   9    10  11|
	    #        |         | |       | |        | |   |   |    |   | |
	    # $--RMC,hhmmss.ss,A,llll.ll,a,yyyyy.yy,a,x.x,x.x,xxxx,x.x,a*hh<CR><LF>
	    #  1) UTC Time
	    #  2) Status, V = Navigation receiver warning
	    #  3) Latitude
	    #  4) N or S
	    #  5) Longitude
	    #  6) E or W
	    #  7) Speed over ground, knots
	    #  8) Track made good, degrees true
	    #  9) Date, ddmmyy
	    # 10) Magnetic Variation, degrees
	    # 11) E or W
	    # 12) Checksum
	    ($time,$status,$lat,$lat_v,$lon,$lon_v,$speed,$dummy,$date,$mag_variation)
		= split(/,/,$line);    
	} elsif ( $type eq "GSA" ) {
	    # GSA - GPS DOP and active satellites
	    #        1 2 3                        14 15  16  17  18
	    #        | | |                         |  |   |   |   |
	    # $--GSA,a,a,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x.x,x.x,x.x*hh<CR><LF>
	    # Field Number: 
	    #  1) Selection mode
	    #  2) Mode
	    #  3) ID of 1st satellite used for fix
	    #  ...
	    #  14) ID of 12th satellite used for fix
	    #  15) PDOP in meters
	    #  16) HDOP in meters
	    #  17) VDOP in meters
	    #  18) checksum 
	    ($dummy,$dummy,$dummy,$dummy,$dummy,$dummy,$dummy,$dummy,$dummy,$dummy,
	     $dummy,$dummy,$dummy,$dummy,$pdop,$hdop,$vdop)
		= split(/,/,$line);
	    $hdop = undef unless $hdop =~ m/[\d\-\+]+/;
	    $vdop = undef unless $vdop =~ m/[\d\-\+]+/;
	    $pdop = undef unless $pdop =~ m/[\d\-\+]+/;
	    $dop_time=$last_time;
	    next;
	} elsif ( $type eq "GSV" ) {
	    # GSV - Satellites in view
	    #
	    #        1 2 3 4 5 6 7     n
	    #        | | | | | | |     |
	    # $--GSV,x,x,x,x,x,x,x,...*hh<CR><LF>
	    # Field Number: 
	    #  1) total number of messages
	    #  2) message number
	    #  3) satellites in view
	    #  4) satellite number
	    #  5) elevation in degrees
	    #  6) azimuth in degrees to true
	    #  7) SNR in dB
	    #  more satellite infos like 4)-7)
	    #  n) checksum
	    my ($msg_anz,$msg_no,$rest);
	    ($msg_anz,$msg_no,$sat_count,$rest) = split(/,/,$line,4);
	    $msg_anz = 20 if $msg_anz>20;
	    $sat={} if $msg_no == 1;
	    #printf STDERR "# of Messages: $msg_anz; rest: '$rest'\n";
	    while ( defined $rest && $rest =~ m/,/) {
		#printf STDERR "# $count: $rest\n";
		my ($sat_no,$sat_ele,$sat_azi,$sat_snr);
		($sat_no,$sat_ele,$sat_azi,$sat_snr,$rest) = split(/,/,$rest,5);
		#printf STDERR "($sat_no,$sat_ele,$sat_azi,$sat_snr)\n";
		last unless defined ($sat_no) && defined($sat_ele) && defined($sat_azi) && defined($sat_snr);
		$sat->{$sat_no}->{ele} = $sat_ele;
		$sat->{$sat_no}->{azi} = $sat_azi;
		$sat->{$sat_no}->{snr} = $sat_snr;
	    }
	    $sat_time = $last_time;
	    #printf STDERR Dumper(\$sat);
	    next;
	} else {
	    printf STDERR "Ignore Line $type: $line\n"
		if $DEBUG>6;
	    next;
	};

	next unless ($lat ne "" )&& ($lon ne "");
	next if  ($lat eq "0000.0000" ) && ($lon eq "00000.0000");
	if ( $lat =~ m/(\d\d)(\d\d.\d+)/) {
	    $lat = $1 + $2/60;
	} else {
	    printf STDERR "Error in lat: $lat\n$line\n";
	}
	if ($lon =~ m/(\d+)(\d\d\.\d+)/){
	    $lon = $1 + $2/60;
	} else {
	    printf STDERR "Error in lon: $lon\n$line\n";
	}
	$lat = -$lat if $lat_v eq "S";
	$lon = -$lon if $lon_v eq "W";
	printf STDERR "type $type (time:$time	lat:$lat	lon:$lon	alt:$alt	speed:$speed)\n" 
	    if $DEBUG>5;
	if ( ( abs($lat) < 0.001 ) && 
	     ( abs($lat) < 0.001 ) ) {
	    printf STDERR "too near to (0/0) : type $type (time:$time	lat:$lat	lon:$lon	alt:$alt	speed:$speed)\n";
	    next;
	};

	$time =~ s/^(..)(..)(..)/$1:$2:$3/;
	if ( defined($date)) {
	    $date =~ s/^(..)(..)(..)/20$3-$2-$1/;
	} else {
	    $date = $last_date;
	}
	$last_date=$date;
	$time = str2time("$date ${time}");
	$last_time = $time if $time;

    	if ( defined $elem->{time} &&
	     defined $elem->{lat} &&
	     defined $elem->{lon} &&
	     ($elem->{time} != ($time||0)) ) { # We have a new Timestamp
	    bless($elem,"NMEA::gps-point");
	    push(@{$new_track},$elem);
	    $elem ={};
	}

	$elem->{lat} = $lat;
	$elem->{lon} = $lon;
	$elem->{alt} = $alt if defined $alt;
	$elem->{time} = $time if defined $time;
	$time ||=0;

	my $dop_time_diff = $time - $dop_time;
	#printf STDERR "time diff: %f\n ", $dop_time_diff;
	if ( $dop_time_diff < 10
	     && defined($hdop) 
	     && defined($vdop)
	     && defined($pdop)
	     ) {
	    $elem->{pdop} = $pdop if $pdop;
	    $elem->{hdop} = $hdop if $hdop;
	    $elem->{vdop} = $vdop if $vdop;
	    if ( $hdop > 30 or 
		 $vdop > 30 or 
		 $pdop > 30  ) {
		#printf STDERR Dumper(\$elem);
		next;
	    }
	}
	
	if (0) { # Currently we don't need these values
	    # So we save on local memory consumption
	    my $sat_time_diff = $time - $sat_time;
	    #printf STDERR "time diff: %f\n ", $sat_time_diff;
	    if ( $sat_time_diff < 10 ) {
		$elem->{sat}  = $sat_count;
		for my $sat_no ( keys %{$sat} ) {
		    $elem->{"sat_${sat_no}_ele"} = $sat->{$sat_no}->{ele};
		    $elem->{"sat_${sat_no}_azi"} = $sat->{$sat_no}->{azi};
		    $elem->{"sat_${sat_no}_snr"} = $sat->{$sat_no}->{snr};
		}
	    }
	}
	# More interesting Info might be:
	# <course>52.000000</course>
	# <ele>0.000000</ele>
	# <fix>2d</fix>
	# <fix>3d</fix>
	# <sat>4</sat>
	# <speed>0.000000</speed>
	# <time>2035-12-03T05:42:23Z</time>
	# <trkpt lat="48.177040000" lon="11.759786667">
    }
    
    # Write last element
    if ( defined $elem->{lat} &&
	 defined $elem->{lon} ) {
	 bless($elem,"NMEA::gps-point");
	 push(@{$new_track},$elem);
	 $elem ={};
     };
    
    push(@{$new_tracks->{tracks}},$new_track);
    if ( $VERBOSE >1 ) {
	printf STDERR "Read and parsed $filename";
    print_time($start_time);
    }
    
    return $new_tracks;
}

1;
