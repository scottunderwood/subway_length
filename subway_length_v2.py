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


# Subway isolation formula
def line_isolator(li_name):
    active_line_frame = subway_station_data_expanded_2[subway_station_data_expanded_2['line'].str.contains(li_name)]
    return active_line_frame

  
# Closest pair of points in python algo
# https://www.ics.uci.edu/~eppstein/161/python/closestpair.py
def closestpair(L):
    def square(x): return x*x
    def sqdist(p,q): return square(p[0]-q[0])+square(p[1]-q[1])

    # Work around ridiculous Python inability to change variables in outer scopes
    # by storing a list "best", where best[0] = smallest sqdist found so far and
    # best[1] = pair of points giving that value of sqdist.  Then best itself is never
    # changed, but its elements best[0] and best[1] can be.

    # We use the pair L[0],L[1] as our initial guess at a small distance.
    best = [sqdist(L[0],L[1]), (L[0],L[1])]
    # check whether pair (p,q) forms a closer pair than one seen already
    
    def testpair(p,q):
        d = sqdist(p,q)
        if d < best[0]:
            best[0] = d
            best[1] = p,q

    # merge two sorted lists by y-coordinate
    def merge(A,B):
        i = 0
        j = 0
        while i < len(A) or j < len(B):
            if j >= len(B) or (i < len(A) and A[i][1] <= B[j][1]):
                yield A[i]
                i += 1
            else:
                yield B[j]
                j += 1

    # Find closest pair recursively; returns all points sorted by y coordinate
    def recur(L):
        if len(L) < 2:
            return L
        split = len(L)/2
        splitx = L[split][0]
        L = list(merge(recur(L[:split]), recur(L[split:])))

        # Find possible closest pair across split line
        # Note: this is not quite the same as the algorithm described in class, because
        # we use the global minimum distance found so far (best[0]), instead of
        # the best distance found within the recursive calls made by this call to recur().
        # This change reduces the size of E, speeding up the algorithm a little.

        E = [p for p in L if abs(p[0]-splitx) < best[0]]
        for i in range(len(E)):
            for j in range(1,8):
                if i+j < len(E):
                    testpair(E[i],E[i+j])
        return L

    L.sort()
    recur(L)
    return best[1]
                         
# create column for point distance from two closest stations
# add this here

# run the program

line_name = raw_input("What line do you want to check? ")
  
isolated_line = line_isolator(line_name)  
coordinates_array_prep = isolated_line['coordinates']  
coordinates_array = []
for x in coordinates_array_prep:
    coordinates_array.append(x)

close_pair = (closestpair(coordinates_array))     
a_coord_1 = (close_pair[0][0])
a_coord_2 = (close_pair[1][0])

station_name_1 = subway_station_data_expanded_2.loc[subway_station_data_expanded_2.coordinate_0 == a_coord_1, 'name']
station_name_2 = subway_station_data_expanded_2.loc[subway_station_data_expanded_2.coordinate_0 == a_coord_2, 'name']

print(closestpair(coordinates_array))
print(station_name_1)
print(close_pair[0])
print(station_name_2)
print(close_pair[1])

#attempt at finding the closest coordinate for all coordinates in list


#print(isolated_line)

