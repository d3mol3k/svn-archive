######################################################################
# Automatically generated by qmake (2.01a) Sun May 24 14:52:14 2009
######################################################################

TEMPLATE = app
TARGET = 
DEPENDPATH += .
INCLUDEPATH += .
LIBS += `curl-config --libs`

# Input
HEADERS += osm-parse.h srtm.h main.h relations.h
SOURCES += osm-parse.cpp srtm.cpp main.cpp relations.cpp
QT           += network
CONFIG += console debug