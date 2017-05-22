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
    active_line_frame = subway_station_data_expanded_2[subway_station_data_expanded_2['line'].str.contains(li_name)]
    return active_line_frame

line_name = raw_input("What line do you want to check? ")
#print(line_isolator(line_name))  
 
#start of external distance calc test
def distance(pt_1, pt_2):
    pt_1 = np.array((pt_1[0], pt_1[1]))
    pt_2 = np.array((pt_2[0], pt_2[1]))
    return np.linalg.norm(pt_1-pt_2)

def closest_node(node, nodes):
    pt = []
    dist = 9999999
    for n in nodes:
        if distance(node, n) <= dist:
            dist = distance(node, n)
            pt = n
    return pt

a = []
for x in range(50000):
    a.append((np.random.randint(0,1000),np.random.randint(0,1000)))

some_pt = (1, 2)


active_coord = closest_node(some_pt, subway_station_data_expanded_2['coordinates'])
print(active_coord)

station_name = subway_station_data_expanded_2.loc[subway_station_data_expanded_2.coordinate_0 == active_coord[0], 'name']

print(station_name)

#end of external distance calc test
  
# Closest pair of points in python
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


isolated_line = line_isolator(line_name)  
coordinates_array_prep = isolated_line['coordinates']  
coordinates_array = []
for x in coordinates_array_prep:
    coordinates_array.append(x)

a_coord_1 = (closestpair(coordinates_array)[0])
a_coord_2 = (closestpair(coordinates_array)[1])

station_name_1 = subway_station_data_expanded_2.loc[subway_station_data_expanded_2.coordinate_0 == a_coord_1[0], 'name']
station_name_2 = subway_station_data_expanded_2.loc[subway_station_data_expanded_2.coordinate_0 == a_coord_2[0], 'name']

print(station_name_1)
print(station_name_2)

print(isolated_line)

# End Closest pair of points in python
  
  
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
                         

#test note


# change points to ints
# create column for point distance from two closest stations
