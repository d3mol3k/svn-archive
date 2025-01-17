#! /usr/bin/python3
# vim: fileencoding=utf-8 encoding=utf-8 et sw=4

from xml.sax import make_parser
from xml.sax.handler import ContentHandler
import sys

lng = "en"
if len(sys.argv) >= 2:
    lng = sys.argv[1]

abbrevs = [
    # D. Feature Name Directionals
    ( "N",              "North",                                0, 1, 1 ),
    ( "S",              "South",                                0, 1, 1 ),
    ( "W",              "West",                                 0, 1, 1 ),
    ( "E",              "East",                                 0, 1, 1 ),
    ( "NE",             "Northeast",                            0, 1, 1 ),
    ( "NW",             "Northwest",                            0, 1, 1 ),
    ( "SE",             "Southeast",                            0, 1, 1 ),
    ( "SW",             "Southwest",                            0, 1, 1 ),
    ( "N",              "Norte",                                1, 1, 1 ),
    ( "S",              "Sur",                                  1, 1, 1 ),
    ( "E",              "Este",                                 1, 1, 1 ),
    ( "O",              "Oeste",                                1, 1, 1 ),
    ( "NE",             "Noreste",                              1, 1, 1 ),
    ( "NO",             "Noroeste",                             1, 1, 1 ),
    ( "SE",             "Sudeste",                              1, 1, 1 ),
    ( "SO",             "Sudoeste",                             1, 1, 1 ),

    # D. Feature Name Qualifiers
    ( "Acc",            "Access",                               0, 0, 1 ),
    ( "Alt",            "Alternate",                            0, 1, 1 ),
    #( "Bus",            "Business",                             0, 1, 1 ),
    ( "Byp",            "Bypass",                               0, 1, 1 ),
    ( "Con",            "Connector",                            0, 0, 1 ),
    ( "Exd",            "Extended",                             0, 1, 1 ),
    ( "Exn",            "Extension",                            0, 0, 1 ),
    ( "Hst",            "Historic",                             0, 1, 0 ),
    ( "Lp",             "Loop",                                 0, 1, 1 ),
    ( "Old",            "Old",                                  0, 1, 0 ),
    ( "Pvt",            "Private",                              0, 1, 1 ),
    #( "Pub",            "Public",                               0, 1, 1 ),
    ( "Scn",            "Scenic",                               0, 0, 1 ),
    ( "Spr",            "Spur",                                 0, 1, 1 ),
    ( "Rmp",            "Ramp",                                 0, 0, 1 ),
    ( "Unp",            "Underpass",                            0, 0, 1 ),
    ( "Ovp",            "Overpass",                             0, 0, 1 ),

    # E. Feature Name Types
    ( "Acmdy",          "Academy",                              0, 1, 1 ),
    ( "Acdmy",          "Academy",                              0, 1, 1 ),
    ( "Acueducto",      "Acueducto",                            1, 1, 0 ),
    ( "Aero",           "Aeropuerto",                           1, 1, 0 ),
    ( "AFB",            "Air Force Base",                       0, 0, 1 ),
    ( "Airfield",       "Airfield",                             0, 0, 1 ),
    ( "Airpark",        "Airpark",                              0, 0, 1 ),
    ( "Arprt",          "Airport",                              0, 0, 1 ),
    ( "Airstrip",       "Airstrip",                             0, 0, 1 ),
    ( "Aly",            "Alley",                                0, 0, 1 ),
    ( "Alleyway",       "Alleyway",                             0, 0, 1 ),
    ( "Apt Bldg",       "Apartment Building",                   0, 0, 1 ),
    ( "Apt Complex",    "Apartment Complex",                    0, 0, 1 ),
    ( "Apts",           "Apartments",                           0, 0, 1 ),
    ( "Aqueduct",       "Aqueduct",                             0, 0, 1 ),
    ( "Arc",            "Arcade",                               0, 1, 1 ),
    ( "Arroyo",         "Arroyo",                               1, 1, 0 ),
    ( "Asstd Liv Ctr",  "Assisted Living Center",               0, 0, 1 ),
    ( "Asstd Liv Fac",  "Assisted Living Facility",             0, 0, 1 ),
    ( "Autopista",      "Autopista",                            1, 1, 0 ),
    ( "Ave",            "Avenida",                              1, 1, 0 ),
    ( "Ave",            "Avenue",                               0, 1, 1 ),
    ( "Bahia",          "Bahia",                                1, 1, 0 ),
    ( "Bk",             "Bank",                                 0, 1, 1 ),
    ( "Base",           "Base",                                 0, 0, 1 ),
    ( "Basin",          "Basin",                                0, 0, 1 ),
    ( "Bay",            "Bay",                                  0, 1, 1 ),
    ( "Byu",            "Bayou",                                0, 1, 1 ),
    ( "Bch",            "Beach",                                0, 0, 1 ),
    ( "B and B",        "Bed and Breakfast",                    0, 0, 1 ),
    ( "Beltway",        "Beltway",                              0, 0, 1 ),
    ( "Bnd",            "Bend",                                 0, 0, 1 ),
    ( "Blf",            "Bluff",                                0, 0, 1 ),
    ( "Brdng Hse",      "Boarding House",                       0, 0, 1 ),
    ( "Bog",            "Bog",                                  0, 0, 1 ),
    ( "Bosque",         "Bosque",                               1, 1, 0 ),
    ( "Blvd",           "Boulevard",                            0, 1, 1 ),
    ( "Boundary",       "Boundary",                             0, 0, 1 ),
    ( "Br",             "Branch",                               0, 1, 1 ),
    ( "Brg",            "Bridge",                               0, 0, 1 ),
    ( "Brk",            "Brook",                                0, 0, 1 ),
    ( "Bldg",           "Building",                             0, 1, 1 ),
    ( "Bulevar",        "Bulevar",                              1, 1, 0 ),
    ( "BIA Highway",    "Bureau of Indian Affairs Highway",     0, 1, 1 ),
    ( "BIA Highway",    "Bureau of Indian Affairs Highway",     1, 1, 0 ),
    ( "BIA Hwy",        "Bureau of Indian Affairs Highway",     0, 1, 1 ),
    ( "BIA Hwy",        "Bureau of Indian Affairs Highway",     1, 1, 0 ),
    ( "BIA Road",       "Bureau of Indian Affairs Road",        0, 1, 1 ),
    ( "BIA Road",       "Bureau of Indian Affairs Road",        1, 1, 0 ),
    ( "BIA Rd",         "Bureau of Indian Affairs Road",        0, 1, 1 ),
    ( "BIA Rd",         "Bureau of Indian Affairs Road",        1, 1, 0 ),
    ( "BIA Route",      "Bureau of Indian Affairs Route",       0, 1, 1 ),
    ( "BIA Route",      "Bureau of Indian Affairs Route",       1, 1, 0 ),
    ( "BIA Rte",        "Bureau of Indian Affairs Route",       0, 1, 1 ),
    ( "BIA Rte",        "Bureau of Indian Affairs Route",       1, 1, 0 ),
    ( "BLM Rd",         "Bureau of Land Management Road",       0, 1, 1 ),
    ( "BLM Rd",         "Bureau of Land Management Road",       1, 1, 0 ),
    ( "BLM Road",       "Bureau of Land Management Road",       0, 1, 1 ),
    ( "BLM Road",       "Bureau of Land Management Road",       1, 1, 0 ),
    ( "Byp",            "Bypass",                               0, 1, 1 ),
    ( "Cll",            "Calle",                                1, 1, 0 ),
    ( "Calleja",        "Calleja",                              1, 1, 0 ),
    ( "Callejón",       "Callejón",                             1, 1, 0 ),
    ( "Cmt",            "Caminito",                             1, 1, 0 ),
    ( "Cam",            "Camino",                               1, 1, 0 ),
    ( "Cp",             "Camp",                                 0, 1, 1 ),
    ( "Cmpgrnd",        "Campground",                           0, 0, 1 ),
    ( "Cmps",           "Campus",                               0, 0, 1 ),
    ( "Cnl",            "Canal",                                0, 1, 1 ),
    ( "Caño",           "Caño",                                 1, 1, 0 ),
    ( "Cantera",        "Cantera",                              1, 1, 0 ),
    ( "Cyn",            "Canyon",                               0, 1, 1 ),
    ( "Capilla",        "Capilla",                              1, 1, 0 ),
    ( "Ctra",           "Carretera",                            1, 1, 0 ),
    ( "Carr",           "Carretera",                            1, 1, 0 ),
    ( "Cswy",           "Causeway",                             0, 0, 1 ),
    ( "Cayo",           "Cayo",                                 1, 1, 0 ),
    ( "Cem",            "Cementerio",                           1, 1, 0 ),
    ( "Cem",            "Cemetery",                             0, 0, 1 ),
    ( "Cementery",      "Cemetery",                             0, 0, 1 ),
    ( "Cemetary",       "Cemetery",                             0, 0, 1 ),
    ( "Cmtry",          "Cemetery",                             0, 0, 1 ),
    ( "Ctr",            "Center",                               0, 1, 1 ),
    ( "Centro",         "Centro",                               1, 1, 0 ),
    ( "Cer",            "Cerrada",                              1, 1, 0 ),
    ( "Cham of Com",    "Chamber of Commerce",                  0, 0, 1 ),
    ( "Chnnl",          "Channel",                              0, 0, 1 ),
    ( "Cpl",            "Chapel",                               0, 1, 1 ),
    ( "Childrens Home", "Childrens Home",                       0, 1, 1 ),
    ( "Church",         "Church",                               0, 1, 1 ),
    ( "Cir",            "Circle",                               0, 0, 1 ),
    ( "Cir",            "Circulo",                              1, 1, 0 ),
    ( "City Hall",      "City Hall",                            0, 0, 1 ),
    ( "City Park",      "City Park",                            0, 0, 1 ),
    ( "Clf",            "Cliff",                                0, 0, 1 ),
    ( "Clb",            "Club",                                 0, 1, 1 ),
    ( "Colegio",        "Colegio",                              1, 1, 0 ),
    ( "Colg",           "College",                              0, 1, 1 ),
    ( "Cmn",            "Common",                               0, 0, 1 ),
    ( "Cmns",           "Commons",                              0, 1, 1 ),
    ( "Community Ctr",  "Community Center",                     0, 0, 1 ),
    ( "Community Clg",  "Community College",                    0, 1, 1 ),
    ( "Community Park", "Community Park",                       0, 1, 1 ),
    ( "Complx",         "Complex",                              0, 1, 1 ),
    ( "Condios",        "Condominios",                          1, 1, 0 ),
    ( "Condo",          "Condiminium",                          0, 1, 1 ),
    ( "Condos",         "Condiminiums",                         0, 0, 1 ),
    ( "Cnvnt",          "Convent",                              0, 1, 1 ),
    ( "Convention Ctr", "Convention Center",                    0, 1, 1 ),
    ( "Cors",           "Corners",                              0, 0, 1 ),
    ( "Corr Faclty",    "Correctional Facility",                0, 0, 1 ),
    ( "Corr Inst",      "Correctional Institute",               0, 0, 1 ),
    ( "Corte",          "Corte",                                1, 1, 0 ),
    ( "Cottage",        "Cottage",                              0, 0, 1 ),
    ( "Coulee",         "Coulee",                               0, 0, 1 ),
    ( "Country Club",   "Country Club",                         0, 1, 1 ),
    ( "Co Hwy",         "County Highway",                       0, 1, 1 ),
    ( "Co Hwy",         "County Highway",                       1, 1, 0 ),
    ( "Co Home",        "County Home",                          0, 1, 1 ),
    ( "Co Ln",          "County Lane",                          0, 1, 0 ),
    ( "Co Park",        "County Park",                          0, 0, 1 ),
    ( "Co Rd",          "County Road",                          0, 1, 0 ),
    ( "Co Rte",         "County Route",                         0, 1, 0 ),
    ( "Co St Aid Hwy",  "County State Aid Highway",             0, 1, 1 ),
    ( "Co St Aid Hwy",  "County State Aid Highway",             1, 1, 0 ),
    ( "Co Trunk Hwy",   "County Trunk Highway",                 0, 1, 1 ),
    ( "Co Trunk Hwy",   "County Trunk Highway",                 1, 1, 0 ),
    ( "Co Trunk Rd",    "County Trunk Road",                    0, 1, 1 ),
    ( "Co Trunk Rd",    "County Trunk Road",                    1, 1, 0 ),
    ( "Crs",            "Course",                               0, 0, 1 ),
    ( "Ct",             "Court",                                0, 1, 1 ),
    ( "Courthouse",     "Courthouse",                           0, 0, 1 ),
    ( "Cts",            "Courts",                               0, 0, 1 ),
    ( "Cv",             "Cove",                                 0, 0, 1 ),
    ( "Cr",             "Creek",                                0, 0, 1 ),
    ( "Crk",            "Creek",                                0, 0, 1 ),
    ( "Cres",           "Crescent",                             0, 0, 1 ),
    ( "Crst",           "Crest",                                0, 0, 1 ),
    ( "Xing",           "Crossing",                             0, 0, 1 ),
    ( "Xroad",          "Crossroads",                           0, 1, 1 ),
    ( "Cutoff",         "Cutoff",                               0, 0, 1 ),
    ( "Dm",             "Dam",                                  0, 0, 1 ),
    ( "Delta Rd",       "Delta Road",                           0, 1, 0 ),
    ( "Dept",           "Department",                           0, 1, 1 ),
    ( "Dep",            "Depot",                                0, 0, 1 ),
    ( "Detention Ctr",  "Detention Center",                     0, 0, 1 ),
    ( "DC Hwy",         "District of Columbia Highway",         0, 1, 1 ),
    ( "DC Hwy",         "District of Columbia Highway",         1, 1, 0 ),
    ( "Ditch",          "Ditch",                                0, 1, 1 ),
    ( "Dv",             "Divide",                               0, 0, 1 ),
    ( "Dock",           "Dock",                                 0, 0, 1 ),
    ( "Dormitory",      "Dormitory",                            0, 0, 1 ),
    ( "Drn",            "Drain",                                0, 0, 1 ),
    ( "Draw",           "Draw",                                 0, 0, 1 ),
    ( "Dr",             "Drive",                                0, 0, 1 ),
    ( "Driveway",       "Driveway",                             0, 1, 1 ),
    ( "Drwy",           "Driveway",                             0, 1, 1 ),
    ( "Dump",           "Dump",                                 0, 0, 1 ),
    ( "Edif",           "Edificio",                             1, 1, 0 ),
    ( "Elem School",    "Elementary School",                    0, 0, 1 ),
    ( "Ensenada",       "Ensenada",                             1, 1, 0 ),
    ( "Ent",            "Entrada",                              1, 1, 0 ),
    ( "Escuela",        "Escuela",                              1, 1, 0 ),
    ( "Esplanade",      "Esplanade",                            0, 1, 1 ),
    ( "Esplanade",      "Esplanade",                            1, 1, 1 ),
    ( "Ests",           "Estates",                              0, 0, 1 ),
    ( "Estuary",        "Estuary",                              0, 0, 1 ),
    ( "Expreso",        "Expreso",                              1, 1, 0 ),
    ( "Expy",           "Expressway",                           0, 1, 1 ),
    ( "Exp-Way",        "Expressway",                           0, 1, 1 ),
    ( "Ext",            "Extension",                            0, 1, 1 ),
    ( "Faclty",         "Facility",                             0, 0, 1 ),
    ( "Fairgrounds",    "Fairgrounds",                          0, 0, 1 ),
    ( "Fls",            "Falls",                                0, 1, 1 ),
    ( "Frm",            "Farm",                                 0, 0, 1 ),
    ( "Farm Rd",        "Farm Road",                            0, 1, 0 ),
    ( "FM",             "Farm-to-Market",                       0, 1, 0 ),
    ( "Fence Line",     "Fence Line",                           0, 0, 1 ),
    ( "Ferry Crossing", "Ferry Crossing",                       0, 1, 1 ),
    ( "Fld",            "Field",                                0, 0, 1 ),
    ( "Fire Cntrl Rd",  "Fire Control Road",                    0, 1, 1 ),
    ( "Fire Dept",      "Fire Department",                      0, 0, 1 ),
    ( "Fire Dist Rd",   "Fire District Road",                   0, 1, 1 ),
    ( "Fire Ln",        "Fire Lane",                            0, 1, 0 ),
    ( "Fire Rd",        "Fire Road",                            0, 1, 0 ),
    ( "Fire Rte",       "Fire Route",                           0, 1, 0 ),
    ( "Fire Sta",       "Fire Station",                         0, 1, 1 ),
    ( "Fire Trl",       "Fire Trail",                           0, 1, 0 ),
    ( "Flowage",        "Flowage",                              0, 0, 1 ),
    ( "Flume",          "Flume",                                0, 0, 1 ),
    ( "Frst",           "Forest",                               0, 0, 1 ),
    ( "Forest Hwy",     "Forest Highway",                       1, 1, 1 ),
    ( "Forest Rd",      "Forest Road",                          0, 1, 1 ),
    ( "Forest Rd",      "Forest Road",                          1, 1, 0 ),
    ( "Forest Rte",     "Forest Route",                         0, 1, 1 ),
    ( "Forest Rte",     "Forest Route",                         1, 1, 0 ),
    ( "FS Rd",          "Forest Service Road",                  0, 1, 1 ),
    ( "FS Rd",          "Forest Service Road",                  1, 1, 0 ),
    ( "F S",            "Forest Service",                       0, 1, 1 ),
    ( "N F S",          "National Forest Service",              0, 1, 1 ),
    ( "North F S",      "National Forest Service",              0, 1, 1 ),
    ( "North F South",  "National Forest Service",              0, 1, 1 ),
    ( "Frk",            "Fork",                                 0, 0, 1 ),
    ( "Ft",             "Fort",                                 0, 1, 0 ),
    ( "4WD Trl",        "Four-Wheel Drive Trail",               0, 1, 1 ),
    ( "Frtrnty",        "Fraternity",                           0, 0, 1 ),
    ( "Fwy",            "Freeway",                              0, 0, 1 ),
    ( "Grge",           "Garage",                               0, 0, 1 ),
    ( "Gdns",           "Gardens",                              0, 0, 1 ),
    ( "Gtwy",           "Gateway",                              0, 0, 1 ),
    ( "Gen",            "General",                              0, 1, 0 ),
    ( "Glacier",        "Glacier",                              0, 0, 1 ),
    ( "Gln",            "Glen",                                 0, 0, 1 ),
    ( "Golf Club",      "Golf Club",                            0, 1, 1 ),
    ( "Golf Course",    "Golf Course",                          0, 1, 1 ),
    ( "Grade",          "Grade",                                0, 0, 1 ),
    ( "Grn",            "Green",                                0, 0, 1 ),
    ( "Group Home",     "Group Home",                           0, 0, 1 ),
    ( "Gulch",          "Gulch",                                0, 0, 1 ),
    ( "Gulf",           "Gulf",                                 0, 1, 1 ),
    ( "Gully",          "Gully",                                0, 0, 1 ),
    ( "Halfway House",  "Halfway House",                        0, 0, 1 ),
    ( "Hall",           "Hall",                                 0, 0, 1 ),
    ( "Hbr",            "Harbor",                               0, 0, 1 ),
    ( "Hts",            "Heights",                              0, 0, 1 ),
    ( "High School",    "High School",                          0, 0, 1 ),
    ( "Hwy",            "Highway",                              0, 1, 1 ),
    ( "Hl",             "Hill",                                 0, 0, 1 ),
    ( "Holw",           "Hollow",                               0, 0, 1 ),
    ( "Home",           "Home",                                 0, 1, 1 ),
    ( "Hosp",           "Hospital",                             0, 1, 1 ),
    ( "Hostel",         "Hostel",                               0, 0, 1 ),
    ( "Hotel",          "Hotel",                                0, 1, 1 ),
    ( "Hse",            "House",                                0, 1, 1 ),
    ( "Hsng",           "Housing",                              0, 1, 1 ),
    ( "Iglesia",        "Iglesia",                              1, 1, 0 ),
    ( "Indian Rte",     "Indian Route",                         0, 1, 1 ),
    ( "Indian Svc Rte", "Indian Service Route",                 0, 1, 1 ),
    ( "Ind St Rte",     "Indian State Route",                   0, 1, 1 ),
    ( "Ind St Rt",      "Indian State Route",                   0, 1, 1 ),
    ( "Indl Park",      "Industrial Park",                      0, 0, 1 ),
    ( "Inlt",           "Inlet",                                0, 0, 1 ),
    ( "Inn",            "Inn",                                  0, 1, 1 ),
    ( "Inst",           "Institute",                            0, 1, 1 ),
    ( "Instn",          "Institution",                          0, 0, 1 ),
    ( "Instituto",      "Instituto",                            1, 1, 0 ),
    ( "Inter School",   "Intermediate School",                  0, 0, 1 ),
    ( "I-",             "Interstate Highway ",                  0, 1, 0 ),
    ( "Isla",           "Isla",                                 1, 1, 0 ),
    ( "Is",             "Island",                               0, 0, 1 ),
    ( "Iss",            "Islands",                              0, 1, 1 ),
    ( "Isle",           "Isle",                                 0, 1, 1 ),
    ( "Jail",           "Jail",                                 0, 0, 1 ),
    ( "Jeep Trl",       "Jeep Trail",                           0, 1, 1 ),
    ( "Junction",       "Junction",                             0, 0, 1 ),
    ( "Jr HS",          "Junior High School",                   0, 0, 1 ),
    ( "Kill",           "Kill",                                 0, 1, 1 ),
    ( "Lago",           "Lago",                                 1, 1, 0 ),
    ( "Lagoon",         "Lagoon",                               0, 0, 1 ),
    ( "Laguna",         "Laguna",                               1, 1, 0 ),
    ( "Lk",             "Lake",                                 0, 1, 1 ),
    ( "Lks",            "Lakes",                                0, 0, 1 ),
    ( "Lndfll",         "Landfill",                             0, 0, 1 ),
    ( "Lndg",           "Landing",                              0, 1, 1 ),
    ( "Landing Area",   "Landing Area",                         0, 1, 1 ),
    ( "Landing Fld",    "Landing Field",                        0, 1, 1 ),
    ( "Landing Strp",   "Landing Strip",                        0, 1, 1 ),
    ( "Ln",             "Lane",                                 0, 1, 1 ),
    ( "Lateral",        "Lateral",                              0, 1, 1 ),
    ( "Levee",          "Levee",                                0, 1, 1 ),
    ( "Lbry",           "Library",                              0, 1, 1 ),
    ( "Lift",           "Lift",                                 0, 1, 1 ),
    ( "Lighthouse",     "Lighthouse",                           0, 0, 1 ),
    ( "Line",           "Line",                                 0, 1, 1 ),
    ( "Ldg",            "Lodge",                                0, 0, 1 ),
    ( "Logging Rd",     "Logging Road",                         0, 1, 1 ),
    ( "Loop",           "Loop",                                 0, 1, 1 ),
    ( "Mall",           "Mall",                                 0, 1, 1 ),
    ( "Mnr",            "Manor",                                0, 0, 1 ),
    ( "Mar",            "Mar",                                  1, 1, 0 ),
    ( "Marginal",       "Marginal",                             1, 1, 0 ),
    ( "Marina",         "Marina",                               0, 0, 1 ),
    ( "Marsh",          "Marsh",                                0, 0, 1 ),
    ( "Mdws",           "Meadows",                              0, 0, 1 ),
    ( "Medical Bldg",   "Medical Building",                     0, 0, 1 ),
    ( "Medical Ctr",    "Medical Center",                       0, 1, 1 ),
    ( "Meml",           "Memorial",                             0, 0, 1 ),
    ( "Memorial Gnds",  "Memorial Gardens",                     0, 0, 1 ),
    ( "Memorial Pk",    "Memorial Park",                        0, 0, 1 ),
    ( "Mesa",           "Mesa",                                 0, 1, 1 ),
    ( "Mgmt",           "Management",                           0, 1, 1 ),
    ( "Mid Schl",       "Middle School",                        0, 0, 1 ),
    ( "Mil Res",        "Military Reservation",                 0, 0, 1 ),
    ( "Millpond",       "Millpond",                             0, 0, 1 ),
    ( "Mine",           "Mine",                                 0, 0, 1 ),
    ( "Mssn",           "Mission",                              0, 1, 1 ),
    ( "Mobile Hm Cmty", "Mobile Home Community",                0, 1, 1 ),
    ( "Mobile Hm Est",  "Mobile Home Estates",                  0, 1, 1 ),
    ( "Mobile Hm Pk",   "Mobile Home Park",                     0, 1, 1 ),
    ( "Monstry",        "Monastery",                            0, 1, 1 ),
    ( "Mnmt",           "Monument",                             0, 0, 1 ),
    ( "Mosque",         "Mosque",                               0, 1, 1 ),
    ( "Mtl",            "Motel",                                0, 1, 1 ),
    ( "Motor Lodge",    "Motor Lodge",                          0, 0, 1 ),
    ( "Mtwy",           "Motorway",                             0, 0, 1 ),
    ( "Mt",             "Mount",                                0, 1, 1 ),
    ( "Mtn",            "Mountain",                             0, 0, 1 ),
    ( "Mus",            "Museum",                               0, 1, 1 ),
    ( "Natl Bfld",      "National Battlefield",                 0, 0, 1 ),
    ( "Natl Bfld Pk",   "National Battlefield Park",            0, 0, 1 ),
    ( "Natl Bfld Site", "National Battlefield Site",            0, 0, 1 ),
    ( "Natl Cnsv Area", "National Conservation Area",           0, 0, 1 ),
    ( "Natl Forest",    "National Forest",                      0, 1, 1 ),
    ( "Nf Rd",          "National Forest Road",                 0, 0, 1 ),
    ( "Nat For Dev Rd", "National Forest Development Road",     0, 1, 1 ),
    ( "NFD",            "National Forest Development",          0, 1, 1 ),
    ( "N F D",          "National Forest Development",          0, 1, 1 ),
    ( "North F D",      "National Forest Development",          0, 1, 1 ),
    ( "Nat For Development", "National Forest Development",     0, 1, 1 ),
    ( "Natl Forest Develop", "National Forest Development",     0, 1, 1 ),
    ( "F Dev Rd",       "Forest Development Road",              0, 1, 1 ),
    ( "F Dev",          "Forest Development",                   0, 1, 1 ),
    ( "N F Dev Rd",     "National Forest Development Road",     0, 1, 1 ),
    ( "N F Dev",        "National Forest Development",          0, 1, 1 ),
    ( "North F Dev Rd", "National Forest Development Road",     0, 1, 1 ),
    ( "North F Dev",    "National Forest Development",          0, 1, 1 ),
    ( "Natl Grsslands", "National Grasslands",                  0, 1, 1 ),
    ( "Natl Hist Site", "National Historic Site",               0, 0, 1 ),
    ( "Natl Hist Pk",   "National Historical Park",             0, 0, 1 ),
    ( "Natl Lkshr",     "National Lakeshore",                   0, 0, 1 ),
    ( "Natl Meml",      "National Memorial",                    0, 0, 1 ),
    ( "Natl Mil Pk",    "National Military Park",               0, 0, 1 ),
    ( "Natl Mnmt",      "National Monument",                    0, 0, 1 ),
    ( "Natl Pk",        "National Park",                        0, 0, 1 ),
    ( "Natl Prsv",      "National Preserve",                    0, 0, 1 ),
    ( "Natl Rec Area",  "National Recreation Area",             0, 0, 1 ),
    ( "Natl Rec Riv",   "National Recreational River",          0, 0, 1 ),
    ( "Natl Resv",      "National Reserve",                     0, 0, 1 ),
    ( "Natl Riv",       "National River",                       0, 0, 1 ),
    ( "Natl Sc Area",   "National Scenic Area",                 0, 0, 1 ),
    ( "Natl Sc Riv",    "National Scenic River",                0, 0, 1 ),
    ( "Natl Sc Rvrwys", "National Scenic Riverways",            0, 0, 1 ),
    ( "Natl Sc Trl",    "National Scenic Trail",                0, 0, 1 ),
    ( "Natl Shr",       "National Seashore",                    0, 0, 1 ),
    ( "Natl Wld Rfg",   "National Wildlife Refuge",             0, 0, 1 ),
    ( "Natl",           "National",                             0, 0, 1 ),
    ( "Navajo Svc Rte", "Navajo Service Route",                 0, 1, 0 ),
    ( "Naval Air Sta",  "Naval Air Station",                    0, 0, 1 ),
    ( "Nurse Home",     "Nursing Home",                         0, 0, 1 ),
    ( "Ocean",          "Ocean",                                0, 0, 1 ),
    ( "Océano",         "Océano",                               1, 1, 0 ),
    ( "Ofc",            "Office",                               0, 1, 1 ),
    ( "Office Bldg",    "Office Building",                      0, 0, 1 ),
    ( "Office Park",    "Office Park",                          0, 0, 1 ),
    ( "Orchard",        "Orchard",                              0, 0, 1 ),
    ( "Orchrds",        "Orchards",                             0, 0, 1 ),
    ( "Orphanage",      "Orphanage",                            0, 0, 1 ),
    ( "Outlet",         "Outlet",                               0, 0, 1 ),
    ( "Oval",           "Oval",                                 0, 0, 1 ),
    ( "Opas",           "Overpass",                             0, 0, 1 ),
    ( "Parish Rd",      "Parish Road",                          0, 1, 0 ),
    ( "Park",           "Park",                                 0, 0, 1 ),
    ( "Park and Ride",  "Park and Ride",                        0, 0, 1 ),
    ( "Pkwy",           "Parkway",                              0, 0, 1 ),
    ( "Pky",            "Parkway",                              0, 0, 1 ),
    ( "Parque",         "Parque",                               1, 1, 0 ),
    ( "Pasaje",         "Pasaje",                               1, 1, 0 ),
    ( "Pso",            "Paseo",                                1, 1, 0 ),
    ( "Pass",           "Pass",                                 0, 1, 1 ),
    ( "Psge",           "Passage",                              0, 1, 1 ),
    ( "Path",           "Path",                                 0, 0, 1 ),
    ( "Pavilion",       "Pavilion",                             0, 0, 1 ),
    ( "Peak",           "Peak",                                 0, 0, 1 ),
    ( "Penitentiary",   "Penitentiary",                         0, 0, 1 ),
    ( "Pier",           "Pier",                                 0, 1, 1 ),
    ( "Pike",           "Pike",                                 0, 0, 1 ),
    ( "Pipeline",       "Pipeline",                             0, 0, 1 ),
    ( "Pl",             "Place",                                0, 0, 1 ),
    ( "Pla",            "Placita",                              1, 1, 0 ),
    ( "Plnt",           "Plant",                                0, 0, 1 ),
    ( "Plantation",     "Plantation",                           0, 0, 1 ),
    ( "Playa",          "Playa",                                1, 1, 0 ),
    ( "Playground",     "Playground",                           0, 0, 1 ),
    ( "Plz",            "Plaza",                                0, 1, 1 ),
    ( "Pt",             "Point",                                0, 1, 1 ),
    ( "Pointe",         "Pointe",                               0, 0, 1 ),
    ( "Police Dept",    "Police Department",                    0, 1, 1 ),
    ( "Police Station", "Police Station",                       0, 1, 1 ),
    ( "Pond",           "Pond",                                 0, 1, 1 ),
    ( "Ponds",          "Ponds",                                0, 0, 1 ),
    ( "Prt",            "Port",                                 0, 1, 1 ),
    ( "Post Office",    "Post Office",                          0, 0, 1 ),
    ( "Power Line",     "Power Line",                           0, 0, 1 ),
    ( "Power Plant",    "Power Plant",                          0, 0, 1 ),
    ( "Prairie",        "Prairie",                              0, 0, 1 ),
    ( "Preserve",       "Preserve",                             0, 0, 1 ),
    ( "Prison",         "Prison",                               0, 0, 1 ),
    ( "Prison Farm",    "Prison Farm",                          0, 0, 1 ),
    ( "Promenade",      "Promenade",                            0, 0, 1 ),
    ( "Prong",          "Prong",                                0, 0, 1 ),
    ( "Puente",         "Puente",                               1, 1, 0 ),
    ( "Quandrangle",    "Quadrangle",                           0, 0, 1 ),
    ( "Quar",           "Quarry",                               0, 0, 1 ),
    ( "Quarters",       "Quarters",                             0, 0, 1 ),
    ( "Qbda",           "Quebrada",                             1, 1, 0 ),
    ( "Race",           "Race",                                 0, 0, 1 ),
    ( "Rail",           "Rail",                                 0, 0, 1 ),
    ( "Rail Link",      "Rail Link",                            0, 1, 1 ),
    ( "Railnet",        "Railnet",                              0, 0, 1 ),
    ( "RR",             "Railroad",                             0, 0, 1 ),
    ( "Rlwy",           "Railway",                              0, 0, 1 ),
    ( "Ry",             "Railway",                              0, 0, 1 ),
    ( "Ramal",          "Ramal",                                1, 1, 0 ),
    ( "Ramp",           "Ramp",                                 0, 0, 1 ),
    ( "Ranch Rd",       "Ranch Road",                           0, 1, 0 ),
    ( "RM",             "Ranch to Market Road",                 0, 1, 0 ),
    ( "Rch",            "Rancho",                               1, 1, 0 ),
    ( "Ravine",         "Ravine",                               0, 0, 1 ),
    ( "Rec Area",       "Recreation Area",                      0, 0, 1 ),
    ( "Reformatory",    "Reformatory",                          0, 0, 1 ),
    ( "Refuge",         "Refuge",                               0, 0, 1 ),
    ( "Regional Pk",    "Regional Park",                        0, 0, 1 ),
    ( "Reservation",    "Reservation",                          0, 0, 1 ),
    ( "Resvn Hwy",      "Reservation Highway",                  0, 1, 1 ),
    ( "Resvn Hwy",      "Reservation Highway",                  1, 1, 0 ),
    ( "Resv",           "Reserve",                              0, 0, 1 ),
    ( "Reservoir",      "Reservoir",                            0, 1, 1 ),
    ( "Res Hall",       "Residence Hall",                       0, 0, 1 ),
    ( "Residencial",    "Residencial",                          1, 1, 0 ),
    ( "Resrt",          "Resort",                               0, 0, 1 ),
    ( "Rest Home",      "Rest Home",                            0, 0, 1 ),
    ( "Retirement Home","Retirement Home",                      0, 0, 1 ),
    ( "Retirement Vlg", "Retirement Village",                   0, 0, 1 ),
    ( "Rdg",            "Ridge",                                0, 0, 1 ),
    ( "Rio",            "Rio",                                  1, 1, 0 ),
    ( "Riv",            "River",                                0, 0, 1 ),
    ( "Rd",             "Road",                                 0, 1, 1 ),
    ( "Roadway",        "Roadway",                              0, 0, 1 ),
    ( "Rock",           "Rock",                                 0, 1, 1 ),
    ( "Romming Hse",    "Rooming House",                        0, 0, 1 ),
    ( "Rte",            "Route",                                0, 1, 1 ),
    ( "Row",            "Row",                                  0, 1, 1 ),
    ( "Rue",            "Rue",                                  0, 1, 1 ),
    ( "Run",            "Run",                                  0, 0, 1 ),
    ( "Runway",         "Runway",                               0, 1, 1 ),
    ( "Ruta",           "Ruta",                                 1, 1, 0 ),
    ( "RV Park",        "RV Park",                              0, 0, 1 ),
    ( "Sanitarium",     "Sanitarium",                           0, 0, 1 ),
    ( "Schl",           "School",                               0, 1, 1 ),
    ( "Sea",            "Sea",                                  0, 1, 1 ),
    ( "Seashore",       "Seashore",                             0, 0, 1 ),
    ( "Sec",            "Sector",                               1, 1, 0 ),
    ( "Smry",           "Semindary",                            0, 1, 1 ),
    ( "Sendero",        "Sendero",                              1, 1, 0 ),
    ( "Svc Rd",         "Service Road",                         0, 1, 1 ),
    ( "Shelter",        "Shelter",                              0, 0, 1 ),
    ( "Shop",           "Shop",                                 0, 0, 1 ),
    ( "Shopping Ctr",   "Shopping Center",                      0, 0, 1 ),
    ( "Shopping Mall",  "Shopping Mall",                        0, 0, 1 ),
    ( "Shopping Plz",   "Shopping Plaza",                       0, 0, 1 ),
    ( "Site",           "Site",                                 0, 0, 1 ),
    ( "Skwy",           "Skyway",                               0, 0, 1 ),
    ( "Slough",         "Slough",                               0, 1, 1 ),
    ( "Sonda",          "Sonda",                                1, 1, 0 ),
    ( "Sorority",       "Sorority",                             0, 1, 1 ),
    ( "Snd",            "Sound",                                0, 1, 0 ),
    ( "Spa",            "Spa",                                  0, 1, 1 ),
    ( "Speedway",       "Speedway",                             0, 1, 1 ),
    ( "Spg",            "Spring",                               0, 0, 1 ),
    ( "Spur",           "Spur",                                 0, 1, 1 ),
    ( "Sq",             "Square",                               0, 1, 1 ),
    ( "State Beach",    "State Beach",                          0, 0, 1 ),
    ( "State Forest",   "State Forest",                         0, 0, 1 ),
    ( "St Beach",       "State Beach",                          0, 0, 1 ),
    ( "St Forest",      "State Forest",                         0, 0, 1 ),
    ( "St FS Rd",       "State Forest Service Road",            0, 1, 1 ),
    ( "St FS Rd",       "State Forest Service Road",            1, 1, 0 ),
    ( "State Hwy",      "State Highway",                        0, 1, 1 ),
    ( "State Hwy",      "State Highway",                        1, 1, 0 ),
    ( "St Hwy",         "State Highway",                        0, 1, 1 ),
    ( "St Hwy",         "State Highway",                        1, 1, 0 ),
    ( "St Highway",     "State Highway",                        0, 1, 1 ),
    ( "St Highway",     "State Highway",                        1, 1, 0 ),
    ( "State Hospital", "State Hospital",                       0, 1, 1 ),
    ( "St Hospital",    "State Hospital",                       0, 1, 1 ),
    ( "State Loop",     "State Loop",                           0, 1, 0 ),
    ( "St Loop",        "State Loop",                           0, 1, 0 ),
    ( "State Park",     "State Park",                           0, 0, 1 ),
    ( "St Park",        "State Park",                           0, 0, 1 ),
    ( "State Prison",   "State Prison",                         0, 0, 1 ),
    ( "St Prison",      "State Prison",                         0, 0, 1 ),
    ( "State Rd",       "State Road",                           0, 1, 1 ),
    ( "State Rd",       "State Road",                           1, 1, 0 ),
    ( "St Road",        "State Road",                           0, 1, 0 ),
    ( "St Road",        "State Road",                           1, 1, 0 ),
    ( "St Rd",          "State Road",                           0, 1, 0 ),
    ( "St Rd",          "State Road",                           1, 1, 0 ),
    ( "State Rte",      "State Route",                          0, 1, 1 ),
    ( "State Rte",      "State Route",                          1, 1, 0 ),
    ( "St Rte",         "State Route",                          0, 1, 1 ),
    ( "St Rte",         "State Route",                          1, 1, 0 ),
    ( "State Rt",       "State Route",                          0, 1, 1 ),
    ( "State Rt",       "State Route",                          1, 1, 0 ),
    ( "St Rt",          "State Route",                          0, 1, 1 ),
    ( "St Rt",          "State Route",                          1, 1, 0 ),
    ( "St Route",       "State Route",                          0, 1, 1 ),
    ( "St Route",       "State Route",                          1, 1, 0 ),
    ( "State Spur",     "State Spur",                           0, 1, 0 ),
    ( "St Spur",        "State Spur",                           0, 1, 0 ),
    ( "St Spr",         "State Spur",                           0, 1, 1 ),
    ( "St Trunk Hwy",   "State Trunk Highway",                  0, 1, 1 ),
    ( "St Trunk Hwy",   "State Trunk Highway",                  1, 1, 0 ),
    ( "Sta",            "Station",                              0, 0, 1 ),
    ( "Strait",         "Strait",                               0, 1, 1 ),
    ( "Stra",           "Stravenue",                            0, 0, 1 ),
    ( "Strm",           "Stream",                               0, 0, 1 ),
    ( "St",             "Street",                               0, 0, 1 ),
    # NOTE: Enable these only if you know what you're doing -- all of these
    # need to be reviewed manually in the resulting .osc file
    #( "St Market",      "State Market",                         0, 1, 1 ),####
    #( "St Line",        "State Line",                           0, 1, 1 ),####
    #( "Saint Line",     "State Line",                           0, 1, 1 ),####
    #( "Street Line",    "State Line",                           0, 1, 1 ),####
    #( "St",             "Saint",                                0, 1, 0 ),####
    #( "St Andrews",     "Saint Andrew's",                       0, 1, 1 ),####
    #( "St Johns",       "Saint John's",                         0, 1, 1 ),####
    #( "St Marys",       "Saint Mary's",                         0, 1, 1 ),####
    #( "St Matthews",    "Saint Matthew's",                      0, 1, 1 ),####
    #( "St Josephs",     "Saint Joseph's",                       0, 1, 1 ),####
    #( "St Michaels",    "Saint Michael's",                      0, 1, 1 ),####
    #( "St Bernards",    "Saint Bernard's",                      0, 1, 1 ),####
    #( "St Helens",      "Saint Helen's",                        0, 1, 1 ),####
    #( "St Annes",       "Saint Anne's",                         0, 1, 1 ),####
    #( "St Albans",      "Saint Alban's",                        0, 1, 1 ),####
    #( "St Martins",     "Saint Martin's",                       0, 1, 1 ),####
    #( "St Pauls",       "Saint Paul's",                         0, 1, 1 ),####
    #( "Saint Andrews",  "Saint Andrew's",                       0, 1, 1 ),####
    #( "Saint Johns",    "Saint John's",                         0, 1, 1 ),####
    ( "St No",          "Street No",                            0, 1, 0 ),
    ( "St Of",          "Street Of",                            0, 1, 0 ),
    ( "St of",          "Street of",                            0, 1, 0 ),
    ( "Strip",          "Strip",                                0, 1, 1 ),
    ( "Swamp",          "Swamp",                                0, 0, 1 ),
    ( "Synagogue",      "Synagogue",                            0, 1, 1 ),
    ( "Tank",           "Tank",                                 0, 0, 1 ),
    ( "Tmpl",           "Temple",                               0, 1, 1 ),
    ( "Trmnl",          "Terminal",                             0, 0, 1 ),
    ( "Ter",            "Terrace",                              0, 1, 1 ),
    ( "Thoroughfare",   "Thoroughfare",                         0, 0, 1 ),
    ( "Toll Booth",     "Toll Booth",                           0, 1, 1 ),
    ( "Toll Rd",        "Toll Road",                            0, 0, 1 ),
    ( "Tollway",        "Tollway",                              0, 0, 1 ),
    ( "Twr",            "Tower",                                0, 1, 1 ),
    ( "Town Ctr",       "Town Center",                          0, 1, 1 ),
    ( "Town Hall",      "Town Hall",                            0, 0, 1 ),
    ( "Town Hwy",       "Town Highway",                         0, 1, 1 ),
    ( "Town Hwy",       "Town Highway",                         1, 1, 0 ),
    ( "Town Rd",        "Town Road",                            0, 1, 1 ),
    ( "Town Rd",        "Town Road",                            1, 1, 0 ),
    ( "Towne Ctr",      "Towne Center",                         0, 1, 1 ),
    ( "Twp Hwy",        "Township Highway",                     0, 1, 1 ),
    ( "Twp Hwy",        "Township Highway",                     1, 1, 0 ),
    ( "Twp Rd",         "Township Road",                        0, 1, 1 ),
    ( "Twp Rd",         "Township Road",                        1, 1, 0 ),
    ( "Trce",           "Trace",                                0, 0, 1 ),
    ( "Trak",           "Track",                                0, 1, 1 ),
    ( "Trfy",           "Trafficway",                           0, 0, 1 ),
    ( "Trl",            "Trail",                                0, 1, 1 ),
    ( "Tr",             "Trail",                                0, 0, 1 ),
    ( "Trailer Ct",     "Trailer Court",                        0, 0, 1 ),
    ( "Trailer Park",   "Trailer Park",                         0, 0, 1 ),
    ( "Trans Ln",       "Transmission Line",                    0, 0, 1 ),
    ( "Trmt Plant",     "Treatment Plant",                      0, 1, 1 ),
    ( "Tribal Rd",      "Tribal Road",                          0, 1, 1 ),
    ( "Trolley",        "Trolley",                              0, 1, 1 ),
    ( "Truck Trl",      "Truck Trail",                          0, 1, 1 ),
    ( "Túnel",          "Túnel",                                1, 1, 0 ),
    ( "Tunl",           "Tunnel",                               0, 1, 1 ),
    ( "Tpke",           "Turnpike",                             0, 0, 1 ),
    ( "Upas",           "Underpass",                            0, 1, 1 ),
    ( "Universidad",    "Universidad",                          1, 1, 0 ),
    ( "Univ",           "University",                           0, 1, 1 ),
    ( "USFS Hwy",       "US Forest Service Highway",            0, 1, 1 ),
    ( "USFS Hwy",       "US Forest Service Highway",            1, 1, 0 ),
    ( "USFS Rd",        "US Forest Service Road",               0, 1, 1 ),
    ( "USFS Rd",        "US Forest Service Road",               1, 1, 0 ),
    ( "US Hwy",         "US Highway",                           0, 1, 1 ),
    ( "US Hwy",         "US Highway",                           1, 1, 1 ),
    ( "USFS Rte",       "US Forest Service Route",              0, 1, 1 ),
    ( "USFS Rte",       "US Forest Service Route",              1, 1, 1 ),
    ( "US Rte",         "US Route",                             1, 1, 1 ),
    ( "Vly",            "Valley",                               0, 0, 1 ),
    ( "Ver",            "Vereda",                               1, 1, 0 ),
    ( "Via",            "Via",                                  1, 1, 0 ),
    ( "Viaduct",        "Viaduct",                              0, 0, 1 ),
    ( "Vw",             "View",                                 0, 0, 1 ),
    ( "Villa",          "Villa",                                0, 1, 1 ),
    ( "Vlg",            "Village",                              0, 1, 1 ),
    ( "Village Ctr",    "Village Center",                       0, 1, 1 ),
    ( "Vineyard",       "Vineyard",                             0, 0, 1 ),
    ( "Vineyards",      "Vineyards",                            0, 0, 1 ),
    ( "Vis",            "Vista",                                0, 1, 1 ),
    ( "Walk",           "Walk",                                 0, 0, 1 ),
    ( "Walkway",        "Walkway",                              0, 0, 1 ),
    ( "Wash",           "Wash",                                 0, 0, 1 ),
    ( "Waterway",       "Waterway",                             0, 0, 1 ),
    ( "Way",            "Way",                                  0, 0, 1 ),
    ( "Wharf",          "Wharf",                                0, 0, 1 ),
    ( "Wld 0 Snc Riv",  "Wild and Scenic River",                0, 0, 1 ),
    ( "Wld 0 Scn Riv",  "Wild and Scenic River",                0, 0, 1 ),
    ( "Wld & Snc Riv",  "Wild and Scenic River",                0, 0, 1 ),
    ( "Wld & Scn Riv",  "Wild and Scenic River",                0, 0, 1 ),
    ( "Wild River",     "Wild River",                           0, 0, 1 ),
    ( "Wilderness",     "Wilderness",                           0, 0, 1 ),
    ( "Wilderness Pk",  "Wilderness Park",                      0, 0, 1 ),
    ( "Wldlf Mgt Area", "Wildlife Management Area",             0, 0, 1 ),
    ( "Winery",         "Winery",                               0, 1, 1 ),
    ( "Yard",           "Yard",                                 0, 0, 1 ),
    ( "Yards",          "Yards",                                0, 1, 1 ),
    ( "YMCA",           "YMCA",                                 0, 1, 1 ),
    ( "YWCA",           "YWCA",                                 0, 1, 1 ),
    ( "Zanja",          "Zanja",                                1, 1, 0 ),
    ( "Zoo",            "Zoo",                                  0, 1, 1 ),
]

directionals = [ "N", "S", "E", "W", "O" ]

en = { "suffixes": {}, "prefixes": {} }
es = { "suffixes": {}, "prefixes": {} }
for abbrev, full, is_es, pref, suff in abbrevs:
    if pref:
        [ en, es ][is_es]["prefixes"][abbrev] = full
    if suff:
        [ en, es ][is_es]["suffixes"][abbrev] = full
for abbrev, full, is_es, pref, suff in abbrevs:
    if pref and full not in [ en, es ][is_es]["prefixes"]:
        [ en, es ][is_es]["prefixes"][full] = full
    if suff and full not in [ en, es ][is_es]["suffixes"]:
        [ en, es ][is_es]["suffixes"][full] = full

def is_num(strng):
    d = 0
    l = 0
    for i in strng:
        if i.isupper():
            l += 1
        elif i.isdigit():
            d += 1
        else:
            return 0
    return l < 2 and d > l

def expand_name(name, lingo, avoid=[]):
    # Try matching the longest suffix / prefix first
    if name in lingo["suffixes"]:
        return lingo["suffixes"][name]
    if name in lingo["prefixes"]:
        return lingo["prefixes"][name]
    l = len(name) - 1
    if l > 40:
        l = 40
    while l > 1:
        l -= 1
        if name[- l - 1] == " " and name[- l:] in lingo["suffixes"]:
            return expand_name(name[:- l - 1], lingo) + " " + \
                    lingo["suffixes"][name[- l:]]
        if name[- l - 1] == " " and is_num(name[- l:]):
            return expand_name(name[:- l - 1], lingo) + " " + name[- l:]
    l = len(name) - 1
    if l > 40:
        l = 40
    while l > 1:
        l -= 1
        if name[l] == " " and name[:l] in lingo["prefixes"]:
            return lingo["prefixes"][name[:l]] + " " + \
                    expand_name(name[l + 1:], lingo)
    return name

def to_xml(str):
    return str.replace("&", "&amp;").replace("\"", "&quot;")

def attr_str(attrs):
    str = ""
    for attr in attrs.keys():
        str += " " + attr + "=\"" + to_xml(attrs[attr]) + "\""
    return str

class WayHandler(ContentHandler):
    def __init__ (self, lingo):
        self.lingo = lingo
        self.is_tag, self.is_nd = 0, 0
    def startElement(self, name, attrs):
        if name == "way":
            self.attrs = attrs
            self.nodes = []
            self.tags = {}
        elif name == "nd":
            self.nodes.append(attrs)
        elif name == "tag":
            self.tags[attrs["k"]] = attrs["v"]
    def endElement(self, name):
        if name != "way":
            return
        modified = 0
        tag = "name"
        tiger_tags = [ 'tiger:name_base', 'tiger:name_type',
                'tiger:name_direction_prefix', 'tiger:name_direction_suffix' ]
        ttags = tiger_tags
        i = 1
        while tag in self.tags:
            # Check that the name has not been corrected after the
            # original import
            if ttags[0] not in self.tags:
                continue
            base = self.tags[ttags[0]]
            type = ""
            if ttags[1] not in self.tags:
                type = self.tags[ttags[1]]
            dir_prefix = ""
            if ttags[2] not in self.tags:
                dir_prefix = self.tags[ttags[2]]
            dir_suffix = ""
            if ttags[3] not in self.tags:
                dir_suffix = self.tags[ttags[3]]

            current_name = self.tags[tag].replace(" ", "")
            if current_name not in [
                    (dir_prefix + base + dir_suffix + type).replace(" ", ""),
                    (dir_prefix + base + type + dir_suffix).replace(" ", "") ]:
                continue

            # Special case: name_base contains one of the single letter
            # directionals, in this case it's likely just a letter used
            # for enumerations such as in arrayes of avenues from A to Z,
            # don't expand those..
            special = 0
            for word in base.split():
                if word in directionals and base.find("N F") == -1:
                    special = 1
                    break

            if not special:
                newname = expand_name(self.tags[tag], self.lingo)
            else:
                newname = ""
                pos = self.tags[tag].find(base)

                pref = self.tags[tag][:pos] + "XXX"
                newname += expand_name(pref, self.lingo)[:-3]

                newname += expand(base, self.lingo, directionals)

                suff = "XXX" + self.tags[tag][pos + len(base)]
                newname += expand_name(suff, self.lingo)[3:]

            if newname.find(" Road ") > -1 and newname[-5:] == " Road":
                newname = newname[:-5]
            if newname != self.tags[tag]:
                modified = 1
                self.tags[tag] = newname

            tag = "name_" + str(i)
            ttags = [ t + "_" + str(i) for t in tiger_tags ]
            i += 1

        if not modified:
            return

        if "tiger:upload_uuid" in self.tags:
            del self.tags["tiger:upload_uuid"]

        sys.stdout.write("  <way" + attr_str(self.attrs) + ">\n")
        for node in self.nodes:
            sys.stdout.write("   <nd" + attr_str(node) + " />\n")
        for tag in self.tags:
            sys.stdout.write("   <tag k=\"" + to_xml(tag) +
                    "\" v=\"" + to_xml(self.tags[tag]) + "\" />\n")
        sys.stdout.write("  </way>\n")

parser = make_parser()
parser.setContentHandler(WayHandler([ en, es ][[ "en", "es" ].index(lng)]))

sys.stdout.write("<osmChange version=\"0.3\" " +
        "generator=\"TIGER abbrev expander\">\n")
sys.stdout.write(" <modify generator=\"TIGER abbrev expander\">\n")

parser.parse(sys.stdin)

sys.stdout.write(" </modify>\n")
sys.stdout.write("</osmChange>")
