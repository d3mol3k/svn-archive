create table data (uid integer primary key, tags text, time timestamp, reference text, minlat float not null, minlon float not null, maxlat float not null, maxlon float not null);
create index data_bbox on data (minlat,minlon,maxlat,maxlon);
create index data_id on data (uid);