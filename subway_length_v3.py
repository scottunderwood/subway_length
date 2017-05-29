import numpy as np
import pandas as pd
import datetime
import urllib
import geopy
from geopy.distance import vincenty

# source data: https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49
# query removes all of the rows where a school did not report scores, enables later code to change score column datatypes from str to int
query_1 = ("https://data.cityofnewyork.us/resource/kk4q-3rt2.json?")
subway_station_data = pd.read_json(query_1)

# unpacks 'the_geom' dictionary to separate columns
subway_station_data_expanded = pd.concat([subway_station_data.drop(['the_geom'], axis=1), subway_station_data['the_geom'].apply(pd.Series)], axis=1)

# Subway isolation formula
def line_isolator(li_name):
    active_line_frame = subway_station_data_expanded[subway_station_data_expanded['line'].str.contains(li_name)]
    return active_line_frame

station_1 = subway_station_data_expanded.loc[subway_station_data_expanded.name == 'Astor Pl', 'coordinates']
station_2 = subway_station_data_expanded.loc[subway_station_data_expanded.name == 'Bedford Ave', 'coordinates']
print(vincenty(station_1, station_2).miles)



line_name = raw_input("What line do you want to check? ")
  
isolated_line = line_isolator(line_name)
coordinates_array_prep = isolated_line['coordinates']  
coordinates_array = []
for x in coordinates_array_prep:
    coordinates_array.append(x)


def closest(points, x):
    current_low = vincenty(x,points[1]).miles
    for y in points:
        if vincenty(x,y) < current_low and vincenty(x, y) > 0:
            current_low = vincenty(x,y).miles
            return current_low
        else:
            current_low = current_low
            return current_low

points = coordinates_array
x = coordinates_array[0]
print(closest(points, x))


def check_for_closest(too_close_f, closest_f, current_index_item_f,ca_f):
    for y in ca_f:
        if (vincenty(current_index_item_f,y)) > too_close_f and (vincenty(current_index_item_f,y)) <= closest_f:
            closest_coord_f = y
            closest_f = vincenty(current_index_item_f,y)
        else:
            pass
    
    return closest_coord_f

# Line iterator runs through a specific line and returns the closest station to  each station on that line 
# Want to break the layers of this out into multiple distinct functions when I have it working
def line_iterator_test(ca):
    list_index = 0
    while list_index < len(ca) - 1:   
        for x in ca:
            current_index_item=ca[list_index]
            too_close = vincenty(current_index_item,current_index_item)
            if list_index == len(ca) -1:
                closest = vincenty(current_index_item,ca[list_index - 1])  
            else:
                closest = vincenty(current_index_item,ca[list_index + 1])
            closest_coord = check_for_closest(too_close, closest, current_index_item, ca)
            #for y in ca:
                #if (vincenty(current_index_item,y)) > too_close and (vincenty(current_index_item,y)) <= closest:
                    #closest_coord = y
                #else:
                    #closest_coord = closest
                #else:
                    #if list_index == len(ca) -1:
                        #closest_coord = ca[list_index - 1]
                    #else:
                        #closest_coord = ca[list_index + 1]
            #next three lines are attempt at coordinate to station name conversion
            #need to figure out how to make the name lookup work
            station_name_1 = isolated_line.loc[isolated_line['coordinates'].str[0] == current_index_item[0], 'name'].iloc[0]
            station_name_2 = isolated_line.loc[isolated_line['coordinates'].str[0] == closest_coord[0], 'name'].iloc[0]
            #station_name_1 = isolated_line.loc[isolated_line['coordinates'] == current_index_item, 'name'].iloc[0]
            #station_name_2 = isolated_line.loc[isolated_line['coordinates'] == closest_coord, 'name'].iloc[0]
            print(station_name_1, current_index_item, station_name_2, closest_coord, vincenty(current_index_item, closest_coord))
            #print(current_index_item, closest_coord, vincenty(current_index_item, closest_coord))
            list_index += 1

line_iterator_test(coordinates_array)

#Older versions of line iterator 

#  def line_iterator_test(ca):
#    for x in ca:
#        list_index = 0
#        current_index_item=ca[list_index]
#        too_close = (vincenty(current_index_item,current_index_item))
#        closest = (vincenty(current_index_item,ca[list_index + 1]))
#        for y in ca:
#            if (vincenty(current_index_item,y)) > too_close and (vincenty(current_index_item,y)) < closest:
#                closest_coord = y
#                print(current_index_item, closest_coord, vincenty(current_index_item, closest_coord))
#            else:
#                closest_coord = ca[list_index + 1]
#        list_index += 1
#      
#line_iterator_test(coordinates_array)

#def line_iterator_test(ca):
#    for x in ca:
#        list_index = 0
#        current_index_item=ca[list_index]
#        for y in ca:
#            print(vincenty(current_index_item,y))
#        list_index += 1
    
