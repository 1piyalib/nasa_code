import numpy as np
from angle_calculations import *
import math

# Latitude: −89.232° N
# Longitude: 54.794° E
NUM_CHECKPOINTS = 10

"""
Reads the rover path file and gets 10 communication checkpoint that are equal distance from each other
returns a list of tuple (lat, long) for these 10 points
"""
def get_communication_checkpoint_locations(rover_path_file= 'rover_path.csv'):
    pts_rov = np.loadtxt(np.DataSource().open(rover_path_file), delimiter=",")
    rlat_list, rlong_list,rheight_list,rslope_list = pts_rov.T

    print("rover list len = ", len(rlat_list))
    com_checkpoints = []
    com_spacing = int(len(rlat_list)/(NUM_CHECKPOINTS-1))# spacing between posts
    #loop throug rover path and
    for index, lat in enumerate(rlat_list):
        if index%com_spacing == 0:
            com_checkpoints.append((rlat_list[index],rlong_list[index],rheight_list[index]))
            print("checkpoint index = "  ,index, "  ", rlat_list[index],rlong_list[index] )
    # the last one is the end point
    com_checkpoints.append((rlat_list[len(rlat_list)-1],rlong_list[len(rlat_list)-1],rheight_list[len(rlat_list)-1]))
    return(com_checkpoints)
"""
reads the nxn flat matrix file converts it to a n row and n column array
"""
def create_matrix(flat_matrix_file = "matrix_300_300_spherical_zoom.csv", matrix_n = 300):
    pts = np.loadtxt(np.DataSource().open(flat_matrix_file), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T
    table = []
    row = []
    for index,lat in enumerate(lat_list):
        row.append((lat_list[index],long_list[index],height_list[index]))
        if (index+1)%matrix_n == 0: # every 300 lines
            table.append(row)
            row = []

    print(len(table))
    print(len(table[0]))
    print(len(table[matrix_n-1]))
    return(table)
"""
From the table matrix finds the indexes of a pointA(lat,long,height)
"""
def find_point_index(PointA,table_matrix):
    indexes = (-1,-1)
    for i,row in enumerate(table_matrix):
        for j,point in enumerate(row):
            if (point == PointA):
                indexes = (i,j)
                return(indexes)
    return(indexes)

def load_lunar_data_file(data_file = 'lunar_data.csv'):
    pts = np.loadtxt(np.DataSource().open(data_file), delimiter=",");
    return(pts)

"""
For a com checkpoint PointA, Find Azimuth between PointA and Earth Fixed coordinate in pts
Find the azimuth of all points within 5 degree.  Returns True if elevation between PointA and Eart is
greater than the elevation between PointA and any points with same relative azimuth
"""
def is_good_elevation(pts, pointA,azimuth_delta = 2):

    (lat_list, long_list, height_list, slope_list) = pts.T

    #earth_fixed_azimuth = earth_fixed_azimuth()
    azimuth_between_pointA_earth = azimuth_between_one_point_and_earth(pointA)
    elevation_between_pointA_earth = calculate_earth_elevation_angle(pointA)
    isElevationSatisfied = True;
    for index, value in enumerate(lat_list):
        pointB = (lat_list[index], long_list[index], height_list[index])
        azimuth_between_two_pnts = azimuth_between_two_points(pointA, pointB)
        if (math.fabs(azimuth_between_pointA_earth - azimuth_between_two_pnts) < azimuth_delta):
            elevation_between_two_points = calculate_elevation_angle(pointA, pointB)
            print(index,"(",lat_list[index], long_list[index],")", azimuth_between_two_pnts, ",", elevation_between_two_points, ",", azimuth_between_pointA_earth, ",",elevation_between_pointA_earth)
            if(elevation_between_two_points >  elevation_between_pointA_earth):
                isElevationSatisfied = False
                break;


    return(isElevationSatisfied)


if __name__ == "__main__":
    rover_checkpoints = get_communication_checkpoint_locations()
    matrix_table = create_matrix(flat_matrix_file="matrix_300_300_spherical_zoom.csv", matrix_n=300)
    all_points = load_lunar_data_file(data_file='lunar_data.csv')

    all_checkpoints = []

    for rover_point in rover_checkpoints:
        indexes = find_point_index(rover_point, matrix_table)
        i,j = indexes
        #print("point ", point, " matrix_point ", matrix_table[i][j])
        #start with one left to the rover path, if not satisfied move one more left
        comm_point = matrix_table[i][j-1]
        is_good_point = is_good_elevation(all_points, comm_point, azimuth_delta=2)
        if (is_good_point):
            all_checkpoints.append(list(comm_point))


    print(all_checkpoints)
    np.savetxt("communication_posts.csv", all_checkpoints, delimiter=",")