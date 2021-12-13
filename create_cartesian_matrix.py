import numpy as np
from angle_calculations import spherical_to_cartesion
from angle_calculations import closest_point

LUNAR_RADIUS = 1737.4 *1000
lunar_data_file = 'lunar_data.csv'

"""
Convert lunar file (spherical) to cartesian
"""
def create_cartesian_lunar_file(lunar_cartesian_file = "lunar_data_cartesian.csv"):
    lat_list, long_list, height_list, slope_list = np.loadtxt(lunar_data_file, unpack=True, delimiter=",")
    xyz_list_list = []
    for index,val in enumerate(lat_list):
        row = []
        (x,y,z) = spherical_to_cartesion(lat_list[index], long_list[index], height_list[index]+LUNAR_RADIUS)
        (x1, y1, z1) = spherical_to_cartesion(lat_list[index], long_list[index], LUNAR_RADIUS)
        row.append(x)
        row.append(y)
        row.append(z-z1)
        row.append(slope_list[index])
        xyz_list_list.append(row)

    np.savetxt(lunar_cartesian_file, xyz_list_list,delimiter = ",")
"""
Create 300x300 cartesian matrix
"""
def create_cartesian_matrix(matrix_output_file,matrix_size,lunar_cartesian_file = "lunar_data_cartesian.csv"):
    """
    Initial values used
    """
    lunar_data_file =lunar_cartesian_file
    matrix_output_filename = matrix_output_file
    MATRIX_N = matrix_size  # n x n matrix

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
    create a n x n equally spaced matrix of x and y from the zoom list
    """
    x_min =  min(x_csv_list)
    x_max =  max(x_csv_list)
    y_min =  min(y_csv_list)
    y_max =  max(y_csv_list)

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
    matrix_list_list =[]
    for index_x in range(len(x_list[100:200])):
        for index_y in range(len(y_list)):
            (closest_x, closet_y,closest_index) = closest_point(x_list[index_x],y_list[index_y], x_csv_list, y_csv_list)
            print("[" ,index_x , "," , index_y , "] " ,  x_list[index_x], ":",y_list[index_y], "-->", "x=", closest_x, "y=",closet_y, "closest_index=" , closest_index, "slope =", slope_csv_list[closest_index])
            matrix_list = [x_list[index_x],y_list[index_y], z_csv_list[closest_index],slope_csv_list[closest_index]]
            matrix_list_list.append(matrix_list)

    """
    save nxn matrix file
    """
    np.savetxt(matrix_output_filename, matrix_list_list,delimiter = ",")

if __name__ == "__main__":
    create_cartesian_lunar_file()
    create_cartesian_matrix(matrix_output_file = 'matrix_300_300_cartesian_temp.csv', matrix_size=300)