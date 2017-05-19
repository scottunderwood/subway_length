import numpy as np
import pandas as pd
import datetime
import urllib

# source data: https://data.cityofnewyork.us/Transportation/Subway-Stations/arq3-7z49
# query removes all of the rows where a school did not report scores, enables later code to change score column datatypes from str to int
query_1 = ("https://data.cityofnewyork.us/resource/kk4q-3rt2.json?")
subway_station_data = pd.read_json(query_1)

# unpacks 'the_geom' dictionary to separate columns
subway_station_data_expanded = pd.concat([subway_station_data.drop(['the_geom'], axis=1), subway_station_data['the_geom'].apply(pd.Series)], axis=1)

# moves each list value in 'coordinates' to its own column
coordinate_dataframe_holder = subway_station_data_expanded['coordinates'].apply(pd.Series)
coordinate_dataframe_holder = coordinate_dataframe_holder.rename(columns = lambda x : 'coordinate_' + str(x))
subway_station_data_expanded_2 = pd.concat([subway_station_data_expanded[:], coordinate_dataframe_holder[:]], axis = 1)

#Normalize the names of all lines so that it is just the major ones

#creating a line isolator
def line_isolator(li_name):
    active_line_frame = subway_station_data_expanded_2[subway_station_data_expanded_2['line'] == li_name]
    return active_line_frame

line_name = '4-6-6 Express'
#print(line_isolator(line_name))  
 
  
#function that calculates the distance between any two subway stations  
def distance_finder(stat_1, stat_2, lin_1, lin_2):    
    subway_station_data_expanded_2_search_1 = subway_station_data_expanded_2[subway_station_data_expanded_2['line'] == lin_1]
    stat_1_coord_1 = subway_station_data_expanded_2_search_1.loc[subway_station_data_expanded_2_search_1.name == stat_1, 'coordinate_0']
    stat_1_coord_2 = subway_station_data_expanded_2_search_1.loc[subway_station_data_expanded_2_search_1.name == stat_1, 'coordinate_1']
    stat_1_coord_2 = float(stat_1_coord_2)
    stat_1_coord_1 = float(stat_1_coord_1)

    
    subway_station_data_expanded_2_search_2 = subway_station_data_expanded_2[subway_station_data_expanded_2['line'] == lin_2]
    stat_2_coord_1 = subway_station_data_expanded_2_search_2.loc[subway_station_data_expanded_2_search_2.name == stat_2, 'coordinate_0']
    stat_2_coord_2 = subway_station_data_expanded_2_search_2.loc[subway_station_data_expanded_2_search_2.name == stat_2, 'coordinate_1']    
    stat_2_coord_2 = float(stat_2_coord_2)
    stat_2_coord_1 = float(stat_2_coord_1)
    
    #https://docs.scipy.org/doc/numpy/reference/routines.math.html
    #http://www.mathwarehouse.com/algebra/distance_formula/index.php
    distance_result = np.sqrt((np.square(stat_2_coord_1 - stat_1_coord_1) + np.square(stat_2_coord_2 - stat_1_coord_2)))
    
    print(distance_result)

distance_finder('Canal St', 'Astor Pl', '4-6-6 Express', '4-6-6 Express')
                         




# change points to ints
# create column for point distance from two closest stations
