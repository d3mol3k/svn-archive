#!/usr/bin/env ruby

=begin Copyright (C) 2006 Ben Gimpert (ben@somethingmodern.com)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston,
MA  02111-1307, USA.

=end

module Ns1togpx

	class Converter

		def initialize
			@ns1_version = nil
		end

		def read_uint8(io)
			ar = io.getc
			ar.pack("I")
		end

		def read_uint32(io)
			ar = []
			4.times { ar << io.getc }
			ar.pack("I")
		end

		def read_int32(io)
			ar = []
			4.times { ar << io.getc }
			ar.pack("i")
		end

		def read_double(io)
			ar = []
			8.times { ar << io.getc }
			ar.pack("E")
		end

		def read_time_t(io)
			read_int32(io)
		end

		def read_filetime(io)
			ar = []
			8.times { ar << io.getc }
			ar.pack("I")
		end

		def filetime_to_time(filetime)
			epoch = Time.utc(1601, 1, 1, 0, 0, 0, 0)
			nanos = filetime * 100
			seconds = nanos / 1000000000
			epoch + seconds
		end

		def time_t_to_time(time_t)
			epoch = Time.utc(1970, 1, 1, 0, 0, 0, 0)
			epoch + time_t
		end

		def convert(ns1, gpx)
			write_header(gpx)
			ns1_sig = ns1.read(4)
			throw "Does not seem to be an NS1 file" unless ns1_sig == "NetS"
			@ns1_version = read_uint32(ns1)
			ns1_num_apinfo = read_uint32(ns1)
			ns1_num_apinfo.times do
				convert_apinfo(ns1, gpx)
			end
			ns1.close
			write_footer(gpx)
			gpx.close
		end

		def convert_apinfo(ns1, gpx)
			case @ns1_version
			when 1
				# no real GPS data in version 1 of the NS1 format
			when 6
				ns1_ssid_length = read_uint8(ns1)
				ns1_ssid = ns1.read(ns1_ssid_length)
				ns1.read(38)  # skip ahead to the LastSeen FILETIME
				ns1_lastseen = read_filetime(ns1)
				ns1_time = filetime_to_time(ns1_lastseen)
				ns1_lat = read_double(ns1)
				ns1_long = read_double(ns1)
				write_point(gpx, ns1_lat, ns1_long, ns1_time)
				ns1_num_apdata = read_uint32(ns1)
				ns1_num_apdata.times do
					convert_apdata(ns1, gpx)
				end
			else  # when 11 or 12
				ns1_ssid_length = read_uint8(ns1)
				ns1_ssid = ns1.read(ns1_ssid_length)
				ns1.read(34)  # skip ahead to the LastSeen FILETIME
				ns1_lastseen = read_filetime(ns1)
				ns1_time = filetime_to_time(ns1_lastseen)
				ns1_lat = read_double(ns1)
				ns1_long = read_double(ns1)
				write_point(gpx, ns1_lat, ns1_long, ns1_time)
				ns1_num_apdata = read_uint32(ns1)
				ns1_num_apdata.times do
					convert_apdata(ns1, gpx)
				end
			end
			ns1.read  # skip the rest
		end

		def convert_apdata(ns1, gpx)
			ns1_time = nil
			if (3..4).member?(@ns1_version)
				ns1_timefield = read_time_t(ns1)
				ns1_time = time_t_to_time(ns1_timefield)
			else
				ns1_timefield = read_filetime(ns1)
				ns1_time = filetime_to_time(ns1_timefield)
			end
			read(8)  # skip ahead to the Location Source
			ns1_location_source = read_int32(ns1)
			if ns1_location_source == 1
				convert_gpsdata(ns1, gpx, ns1_time)
			end
		end

		def convert_gpsdata(ns1, gpx, time)
			ns1_lat = read_double(ns1)
			ns1_long = read_double(ns1)
			write_point(gpx, ns1_lat, ns_long, time)
			read(44)  # skip the rest
		end

		def time_to_gpxtime(time)
			time.utc.strftime("%Y-%m-%dT%H:%M:%SZ")
		end

		def write_header(io)
			io.print <<EOF
<?xml version="1.0"?>
<gpx version="1.0" creator="ns1togpx" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">
<time>#{time_to_gpxtime(Time.now)}</time>
<trk>
<name>ns1togpx Converted GPX Track</name>
<trkseg>
EOF
		end

		def write_point(io, lat, long, time)
			io.print <<"EOF"
<trkpt lat="#{lat}" lon="#{long}">
<time>#{time_to_gpxtime(time)}</time>
</trkpt>
EOF
		end

		def write_footer(io)
			io.print <<EOF
</trkseg>
</trk>
</gpx>
EOF
		end

	end

end  # of module

if __FILE__ == $0

	require 'ns1togpx'

	if (ARGV.length >= 1) && (ARGV.first =~ /(-h)|(--help)/i)
		$stderr.print <<EOF
ns1togpx Converter

Usage:
	$ ./ns1togpx <some_file.ns1 >another_file.gpx

EOF
		exit(1)
	end

	source = $stdin
	if (ARGV.length >= 1) && (ARGV.first != "-") && File.exists?(ARGV.first)
		source = File.open(ARGV.first)
	end

	begin
		source.binmode
		Ns1togpx::Converter.new.convert(source, $stdout)
	ensure
		source.close
	end

end

