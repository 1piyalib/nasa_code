#https://www.youtube.com/watch?v=kZ9EhWI8veU&list=PLZU5hLL_713x0_AV_rVbay0pWmED7992G&index=9

import numpy as np
from angle_calculations import closest_point

# """
# Functions
# """
# #distance between two (x,y) points
# def distance(x1,y1,x2,y2):
#     return(math.sqrt((x2-x1) * (x2-x1) + (y2 -y1) * (y2 -y1)))
#
# # given a x list and y list finds the point (x,y) that is closest to the point x1,y1
# def closest_point(x1,y1, x_list, y_list):
#     closest_distance= 10000 #some big value
#     closest_x_y_index = None
#
#     for index in range(len(x_list)-1):
#         dist = distance(x1,y1,x_list[index],y_list[index])  #find distance between two points
#         if(dist < closest_distance):
#             closest_distance = dist  #keep on updating closest distance
#             closest_x_y_index = (x_list[index],y_list[index],index)
#
#     return(closest_x_y_index)
#

landing_site_x_y = [-89.1, 55]
destination_site_x_y = [-89.2, 120]

def create_matrix_and_maze(maze_output_file, matrix_output_file, slope_cutoff, zoom_data_area, matrix_size):
    """
    Initial values used
    """
    lunar_data_file = 'lunar_data.csv'
    maze_output_filename = maze_output_file
    matrix_output_filename = matrix_output_file
    SLOPE_CUTOFF = slope_cutoff
    MATRIX_N = matrix_size  # n x n matrix

    zoom_data = zoom_data_area # zooms the data around  Latitude(-88.7 - -89.3) long (50, 125) that covers the landing site

    """
    Read data from csv (x is longitude, y is lattitude, z is height
    """
    x_csv_list,y_csv_list,z_csv_list,slope_csv_list = np.loadtxt(lunar_data_file, unpack=True,  delimiter = ",")
    # index_list = np.array(range(1,len(x_list)+1))
    print(lunar_data_file , "file data ======>")
    print("num of rows ", len(x_csv_list))
    print("x_min = ", min(x_csv_list), " x_max = ", max(x_csv_list))
    print("y_min = ", min(y_csv_list), " y_max = ", max(y_csv_list))
    print("height_min = ", min(z_csv_list), " height_max = ", max(z_csv_list))

    """
    Data zoomed around landing and destination site
    """
    x_zoom_list = []
    y_zoom_list = []
    z_zoom_list = []
    slope_zoom_list = []

    if  zoom_data == True:
        y_zoom_min = 50
        y_zoom_max = 125
        x_zoom_max = -88.7
        x_zoom_min = -89.3

        for index in range(len(x_csv_list) -1):
            x = x_csv_list[index]
            y = y_csv_list[index]
            if( y> y_zoom_min and y< y_zoom_max and  x > x_zoom_min and x < x_zoom_max):
                x_zoom_list.append(x_csv_list[index])
                y_zoom_list.append(y_csv_list[index])
                z_zoom_list.append(z_csv_list[index])
                slope_zoom_list.append(slope_csv_list[index])

        print("zoom data ======>")
    else:
        x_zoom_list = x_csv_list
        y_zoom_list = y_csv_list
        z_zoom_list = z_csv_list
        slope_zoom_list = slope_csv_list

    print("num of rows ", len(x_zoom_list))
    print("x_min = ", min(x_zoom_list), " x_max = ", max(x_zoom_list))
    print("y_min = ", min(y_zoom_list), " y_max = ", max(y_zoom_list))
    print("height_min = ", min(z_zoom_list), " height_max = ", max(z_zoom_list))


    """
    create a n x n equally spaced matrix of x and y from the zoom list
    """
    x_min =  min(x_zoom_list)
    x_max =  max(x_zoom_list)
    y_min =  min(y_zoom_list)
    y_max =  max(y_zoom_list)

    x_list =[]
    y_list =[]
    step_x = (x_max - x_min)/(MATRIX_N-1) # equal n number of x steps
    step_y =(y_max - y_min) / (MATRIX_N-1) # equal n number of y steps
    for index in range(MATRIX_N):
        x_list.append(x_min + index *  step_x)
        y_list.append(y_min + index * step_y)

    print(MATRIX_N, "x", MATRIX_N, " data ======>")
    print("num of rows ", len(x_list))
    print("x_min = ", min(x_list), " x_max = ", max(x_list))
    print("y_min = ", min(y_list), " y_max = ", max(y_list))
    print("x_list ", x_list)
    print("y_list ", y_list)

    """
    Find the closest points
    """
    #find closest point in matrix that's close to landing site and destination site
    (landing_x, landing_y,landing_index) = closest_point(landing_site_x_y[0],landing_site_x_y[1], x_list, y_list)
    (destination_x, destination_y,destination_index) = closest_point(destination_site_x_y[0],destination_site_x_y[1], x_list, y_list)
    print("landing_x_y", landing_x," ", landing_y)
    print("destination_x_y", destination_x," ", destination_y)

    matrix_list_list =[]
    all_lines = ""  # all lines of maze file
    for index_x in range(len(x_list)):

        for index_y in range(len(y_list)):

            (closest_x, closet_y,closest_index) = closest_point(x_list[index_x],y_list[index_y], x_zoom_list, y_zoom_list)
            print("[" ,index_x , "," , index_y , "] " ,  x_list[index_x], ":",y_list[index_y], "-->", "x=", closest_x, "y=",closet_y, "zoom_index=" , closest_index, "slope =", slope_zoom_list[closest_index])
            if(x_list[index_x] == landing_x and y_list[index_y] == landing_y):
                all_lines = all_lines + "A"  #start point
            elif (x_list[index_x] == destination_x and y_list[index_y] == destination_y):
                all_lines = all_lines + "B"  # end point
            elif(slope_zoom_list[closest_index] < SLOPE_CUTOFF):
                all_lines = all_lines + " "
            else:
                all_lines = all_lines + "#"
            matrix_list = [x_list[index_x],y_list[index_y], z_zoom_list[closest_index],slope_zoom_list[closest_index]]
            matrix_list_list.append(matrix_list)
        all_lines = all_lines + "\n"

    """
    create maze file
    """
    maze_file = open(maze_output_filename, 'w')
    maze_file.write(all_lines + '\n')
    maze_file.close()

    """
    save nxn matrix file
    """

    np.savetxt(matrix_output_filename, matrix_list_list,delimiter = ",")

"""
From the matrix file gets nxn dim list of (lat,long) tuples
matrix_n = dimention (300) of matrix
"""
def get_matrix_nxn_list(matrix_filename, matrix_n):

    pts = np.loadtxt(np.DataSource().open(matrix_filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    one_row = []
    rows = []

    all_line_lat_long = ""
    for index in range(len(lat_list)):
            cell = (lat_list[index], long_list[index])
            all_line_lat_long = all_line_lat_long + " " + str((round(lat_list[index], 2), round(long_list[index], 2)))
            one_row.append(cell)
            if ((index + 1) % matrix_n == 0):
                rows.append(one_row)
                one_row = []
                all_line_lat_long = all_line_lat_long + "\n"

    print(all_line_lat_long)

    return(rows)

if __name__ == "__main__":

    """
    Create matrix
    """
    maze_output_file = "rover_maze_temp.txt"
    matrix_output_file = "matrix_300_300_temp.csv"
    slope_cutoff = 15
    zoom_data = False
    matrix_size = 300

    create_matrix_and_maze(maze_output_file, matrix_output_file, slope_cutoff, zoom_data, matrix_size)

    """
    Get the 300x300 list
    """
    #matrix_nxn_list = get_matrix_nxn_list("matrix_300_300_spherical_zoom.csv", 300)
