#!/usr/bin/ruby -w

require 'cgi'
require 'time'
require 'date'
load 'osm/dao.rb'
load 'osm/ox.rb'
require 'rexml/document'

include Apache
include REXML

r = Apache.request

dao = OSM::Dao.instance

cgi = CGI.new
segment_ids = cgi['segmentids'].split(',')

segs = []

segment_ids.each do |n|
  segs << n.to_i
end

ox = OSM::Ox.new

dao.get_streets_from_segments(segs).each do |n|
  ox.add_street(n)
end

puts ox.to_s

