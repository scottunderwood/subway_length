import numpy as np
import pandas as pd
import datetime
import urllib
import geopy
from geopy.distance import vincenty


# FUNCTIONS THAT PULL SOURCE DATA AND PREPARE FOR USE
#####################################################

# source data: https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49
query_1 = ("https://data.cityofnewyork.us/resource/kk4q-3rt2.json?")
subway_station_data = pd.read_json(query_1)

# unpacks 'the_geom' dictionary to separate columns
subway_station_data_expanded = pd.concat([subway_station_data.drop(['the_geom'], axis=1), subway_station_data['the_geom'].apply(pd.Series)], axis=1)

# Removes all instances of "Express" from the line names
subway_station_data_expanded['line'] = subway_station_data_expanded['line'].str.replace(' Express', '')



# FUNCTIONS USED IN ISOLATING SINGLE LINES FOR ANALYSIS
#######################################################

def line_isolator(li_name):
    active_line_frame = subway_station_data_expanded[subway_station_data_expanded['line'].str.contains(li_name)]
    return active_line_frame

def coord_array_isolator(iso_line):
    coordinates_array_prep = isolated_line['coordinates']  
    active_coordinates_array = []
    for x in coordinates_array_prep:
        active_coordinates_array.append(x)
    return active_coordinates_array


    
# FUNCTIONS THAT MEASURE THE DISTANCE BETWEEN STATIONS ALONG A LINE
###################################################################
          
# SETS THE CURRENT INDEX ITEM FOR A DISTANCE CALCULATION AND SETS THE VALUES FOR "TOO CLOSE" AND "CLOSEST"    
def range_set(ca_f2, list_index_f2):
    current_index_item_int = ca_f2[list_index_f2]
    too_close_int = vincenty(current_index_item_int, current_index_item_int)
    if list_index_f2 == len(ca_f2) -1:
        closest_int = vincenty(current_index_item_int, ca_f2[list_index_f2 - 1])
    else:
        closest_int = vincenty(current_index_item_int,ca_f2[list_index_f2 +1])
    range_output = [current_index_item_int, too_close_int, closest_int]
    return range_output
  
          
def check_for_closest(too_close_f, closest_f, current_index_item_f,ca_f):
    for y in ca_f:
        if (vincenty(current_index_item_f,y)) > too_close_f and (vincenty(current_index_item_f,y)) <= closest_f:
            closest_coord_f = y
            closest_f = vincenty(current_index_item_f,y)
        else:
            pass
    return closest_coord_f
  

# Line iterator runs through a specific line and returns the closest station to  each station on that line 
# TODO: Want to break the layers of this out into multiple distinct functions when I have it working
def line_iterator_v1(ca):
    list_index = 0
    while list_index < len(ca) - 1:   
        for x in ca:
            range_list = range_set(ca, list_index)
            
            current_index_item = range_list[0]
            too_close = range_list[1]
            closest = range_list[2]
            
            closest_coord = check_for_closest(too_close, closest, current_index_item, ca)
            station_name_1 = isolated_line.loc[isolated_line['coordinates'].str[0] == current_index_item[0], 'name'].iloc[0]
            station_name_2 = isolated_line.loc[isolated_line['coordinates'].str[0] == closest_coord[0], 'name'].iloc[0]
            print(station_name_1, current_index_item, station_name_2, closest_coord, vincenty(current_index_item, closest_coord))
            list_index += 1
            
            

# TODO: need to create a system that stores a line and its two closest stations in a dictionary of the stations coordinates, distances, and names
def line_iterator_v2(ca):
    list_index = 0
    station_dict = {}
    while list_index < len(ca) - 1:   
        for x in ca:
            range_list = range_set(ca, list_index)
            
            current_index_item = range_list[0]
            too_close = range_list[1]
            closest = range_list[2]
            
            closest_coord = check_for_closest(too_close, closest, current_index_item, ca)
            station_name_1 = isolated_line.loc[isolated_line['coordinates'].str[0] == current_index_item[0], 'name'].iloc[0]
            station_name_2 = isolated_line.loc[isolated_line['coordinates'].str[0] == closest_coord[0], 'name'].iloc[0]
            # TODO: append all station outputs to dictionary where the key is the station name and the values are the station name, coord, closest station name, and closest station coord
            # TODO may ultimately want to spin this out as a separate function? 
            station_dict[station_name_1] = {'s1': station_name_1, 'c1': current_index_item, 's2': station_name_2, 'c2': closest_coord, 'd2': vincenty(current_index_item, closest_coord) }
            list_index += 1
    print(station_dict)
            
            
            
# RUN THE FUNCTION
###################

line_name = raw_input("What line do you want to check? ")  

isolated_line = line_isolator(line_name)

coordinates_array = coord_array_isolator(isolated_line)

#line_iterator_v1(coordinates_array)
line_iterator_v2(coordinates_array)