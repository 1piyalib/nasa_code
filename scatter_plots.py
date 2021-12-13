import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import csv
import math
from angle_calculations import spherical_to_cartesion, spherical_to_cartesion_list, closest_point, spherical_to_cartesion_list2


landing_site = [-89.1,55] #[-89.15,56] #[-89.232,54.794]
dest_site = [-89.200,120]
MAX_ROVER_SLOPE = 15
MAX_LANDING_SLOPE = 5
RELAXED_LANDING_SLOPE = 20
LUNAR_RADIUS = 1737.4 * 1000 #meter

"""
Gets polar coordinates for the polar scatter graph
"""
def get_polar_coordinate(lattitude, longitude):
    # convert longitude to theta (0-360) in radian
    # also polar scatter plot starts 0 theta at right hand side, it should be at the bottom for moon. So subtract 90 from theta
    if (longitude < 0):
        # theta is from 0-360.  -180W long =>  theta = 180, -90W long =>  theta = 270 also convert to radian deg * math.pi / 180
        theta = (((360 + longitude) * math.pi / 180) - math.pi / 2)
    else:
        # convert to radian
        theta= (((longitude) * math.pi / 180) - math.pi / 2)

    # radius is from zero scale (0 - max lattitude) by adding 90.  Latitude is -88S to -90S,
    r =(lattitude + 90)
    return(theta,r)
"""
Scatter slope plot in polar coordinate
Advantage: you can see as if it's on moon
"""
def scatter_slope_polar(filename):

    lat_list = []
    long_list = []
    r_list = []
    theta_list = []
    color = []

    f = open(filename, 'r')
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:

        # Read lattitude longitude slope from file
        lattitude = float(row[0])
        longitude = float(row[1])
        slope = float(row[3])
        #append to list
        lat_list.append(lattitude)
        long_list.append(longitude)

        theta, r = get_polar_coordinate(lattitude, longitude)
        theta_list.append(theta)
        r_list.append(r)

        if (slope <= MAX_ROVER_SLOPE):
            color.append("yellow")
        else:
            color.append("blue")

    """
    Print min/max values
    """
    print("lat min max: ",  min(lat_list), max(lat_list))
    print("long min max: ",  min(long_list), max(long_list))
    print("r min max: ",  min(r_list), max(r_list))
    print("theta min max: ",  min(theta_list), max(theta_list))

    """
    draw with landing and destination
    """
    ld_theta = []
    ld_r = []
    landing_theta, landing_r = get_polar_coordinate(landing_site[0], landing_site[1])
    ld_theta.append(landing_theta)
    ld_r.append(landing_r)
    dest_theta, dest_r = get_polar_coordinate(dest_site[0], dest_site[1])
    dest_theta_list = []
    dest_r_list = []
    dest_theta_list.append(dest_theta)
    dest_r_list.append(dest_r)

    """
    plot 
    """
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='polar')
    # r goes from 0 to one decimal above max r_list
    ax.set_ylim(0,math.ceil(max(r_list)*10)/10)
    ax.scatter(theta_list,r_list, color = color)
    ax.scatter(ld_theta, ld_r, color="red",s = 150, marker = "o")
    ax.scatter(dest_theta_list, dest_r_list, color="red",s = 200, marker = "*")
    #maximize plot
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    #show
    plt.show()
"""
Scatter slope with lattitude/long in cartesian coordinate
Disadvantage: the axis does not show lattitude/longitude actual values
"""
def scatter_slope_polar_val_cartesian_coordinate(filename):
    lat_list = []
    long_list = []
    landing_dest_Lat_list = []
    landing_dest_Long_list = []

    color = []
    f = open(filename, 'r')
    csv_reader = csv.reader(f, delimiter=',')
    for row in csv_reader:
        lattitude = float(row[0])
        longitude = float(row[1])
        slope = float(row[3])

        lat_list.append(lattitude)
        long_list.append(longitude)

        if (slope <= MAX_ROVER_SLOPE):
            color.append("yellow")
        else:
            color.append("blue")

    landing_dest_Lat_list.append(landing_site[0])
    landing_dest_Long_list.append(landing_site[1])
    landing_dest_Lat_list.append(dest_site[0])
    landing_dest_Long_list.append( dest_site[1])

    """
    Plot most significant data portion index 
    """
    plt.xlabel("latitude")
    plt.ylabel("longitude");
    plt.scatter(np.array(lat_list), np.array(long_list), color=color)
    # Put  landing and destination site as red star in the plot
    plt.scatter(np.array(landing_dest_Lat_list), np.array(landing_dest_Long_list), color="red", s=200, marker="*")
    plt.show()


def strf(val):
    return(str(round(val,1)))

"""
Scatter slope plot in cartesian coordinate
Disadvantage: the axis does not show lattitude/longitude actual values
"""
def scatter_slope_cartesian(filename, max_slope, rover_file_path = None,com_checkpoint_file = None):

    color_list = []

    """
    Get polar coordinates from file
    """
    landing_dest_x_list = []
    landing_dest_y_list = []
    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    """
    Convert to cartesian coordinates
    """
    (x_list, y_list) = spherical_to_cartesion_list(lat_list,long_list,LUNAR_RADIUS)

    """
    Convert to two lists, more_x_list > MAX_ROVER_SLOPE
    """
    more_x_list =[]
    more_y_list = []
    less_x_list = []
    less_y_list = []

    index =0
    for slope in slope_list:
        if (slope <= max_slope):
            less_x_list.append(x_list[index])
            less_y_list.append(y_list[index])
        else:
            more_x_list.append(x_list[index])
            more_y_list.append(y_list[index])
        index = index + 1

    color_less = "yellow"
    color_more = "blue"
    label_less = "slope below " + str(max_slope)
    label_more = "slope above " + str(max_slope)

    """
    Print min/max values
    """
    print("lat min max: ", min(lat_list), max(lat_list))
    print("long min max: ", min(long_list), max(long_list))

    """
    Convert destination and landing to cartesian
    """
    (x,y,z) =spherical_to_cartesion(landing_site[0], landing_site[1],LUNAR_RADIUS)
    landing_dest_x_list.append(x)
    landing_dest_y_list.append(y)
    (x, y, z) = spherical_to_cartesion(dest_site[0], dest_site[1], LUNAR_RADIUS)
    landing_dest_x_list.append(x)
    landing_dest_y_list.append(y)

    if rover_file_path != None:
        pts_rov = np.loadtxt(np.DataSource().open(rover_file_path), delimiter=",")
        rlat_list, rlong_list,rheight_list,rslope_list = pts_rov.T
        (rx_list, ry_list) = spherical_to_cartesion_list(rlat_list, rlong_list, LUNAR_RADIUS)


    if com_checkpoint_file != None:
        pts_com = np.loadtxt(np.DataSource().open(com_checkpoint_file), delimiter=",")
        clat_list, clong_list,cheight_list = pts_com.T
        (cx_list, cy_list) = spherical_to_cartesion_list(clat_list, clong_list, LUNAR_RADIUS)

    """
    Plot 
    """
    plt.title("Slope between latitude " + strf(min(lat_list)) + "-" + strf(max(lat_list)) + " longitude " + strf(min(long_list)) + "-" + strf(max(long_list)))
    plt.xlabel("latitude in cartesian coordinate")
    plt.ylabel("longitude in cartesian coordinate");
    #plt.grid(color='green', linestyle='--', linewidth=0.2)

    plt.scatter(np.array(more_x_list), np.array(more_y_list), color=color_more,s= 1, label=label_more)
    plt.scatter(np.array(less_x_list), np.array(less_y_list), color = color_less, s=1, label = label_less)

    if rover_file_path != None:
        plt.scatter(np.array(rx_list), np.array(ry_list), color= "green", s= 30,label="rover path")

    if com_checkpoint_file != None:
        plt.scatter(np.array(cx_list), np.array(cy_list), color= "red", s= 200,label="communication checkpoints")

    # Put  landing and destination site as red star in the plot
    plt.scatter(np.array(landing_dest_x_list), np.array(landing_dest_y_list), color="red", s=200, marker="*", label="landing and dest")

    plt.legend(loc = "upper left")
    # maximize plot
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

"""
Compare terrain height differences of adjacent points to slope data of current points
"""
def line_slope_vs_height(filename):

    #read file
    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    index_list = [] #x axis is index
    slope_plot_list = [] #two less than slope_list
    height_diff_list = []

    for index in range(1,300): # start @1 end @len-2 to accommodate the height before and after
        height_diff = height_list[index + 1] - height_list[index - 1]
        if (math.fabs(height_diff) < 100):  # ignore transition points
            index_list.append(index)
            slope_plot_list.append(slope_list[index])
            height_diff_list.append(height_diff)

    """
    Plot two Y axis, slope and height difference vs X axis is index
    """
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(index_list, slope_plot_list, color="green",linewidth=3.0)
    ax2.plot(index_list, height_diff_list, color = 'blue',linewidth=3.0)

    plt.title("terrain height differences of adjacent points to slope data of current points")
    ax1.set_xlabel('Data Index')
    ax1.set_ylabel('Slope', color='g')
    ax2.set_ylabel('Height Difference', color='b')
    plt.legend(loc="upper left")
    # maximize plot
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

"""
smallest maximum degree of slope that must be allowed from the path of normal starting point to
the top of the rim of large crater southwest of it
"""
def max_slope_top_of_rim(filename):

    #read file
    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    lat_res_list = []
    slope_res_list = []
    height_res_list = []
    index_list = []

    res_index = 0
    for index, val in enumerate(slope_list):
        if ( lat_list[index] > -89.2  and lat_list[index] < -88  and long_list[index] > 54.3 and long_list[index] <  55.2): #-89.2
            lat_res_list.append(lat_list[index])
            index_list.append(res_index)
            slope_res_list.append(slope_list[index])
            height_res_list.append(height_list[index])
            res_index = res_index + 1

    """
    Plot two Y axis, slope and height difference vs X axis is index
    """
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.scatter(lat_res_list, slope_res_list, color="green")
    ax2.scatter(lat_res_list, height_res_list, color = 'blue')

    plt.title("height vs slope for normal starting point to the top of the rim of Shoemaker Crater")
    ax1.set_xlabel('lattitude')
    ax1.set_ylabel('Slope', color='g')
    ax2.set_ylabel('Height', color='b')
    plt.legend(loc="upper left")
    # maximize plot
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()

"""
Scatter color plot of height
"""
def scatter_hieght_cartesian(filename):

    # min_height = -2872.0
    # max_height = 1958.0

    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    x_list=[]
    y_list=[]
    z_list =[]
    color =[]

    """
       Convert to cartesian coordinates
       """
    (x_list, y_list,z_list) = spherical_to_cartesion_list2(lat_list, long_list, height_list)

    for height in height_list:
        #matplotlib colors
        #https://matplotlib.org/stable/gallery/color/named_colors.html

        if (height < -2500):
            color.append("darkgrey")
        elif (height >= -2500 and height < -2000):
            color.append("gray")
        elif (height >= -2000 and height <-1500):
            color.append("navy")
        elif (height >= -1500 and height < -1000):
            color.append("green")
        elif (height >= -1000 and height < -800):
            color.append("orange")
        elif (height >= -800 and height < -650):
            color.append("salmon")
        elif (height >= -650 and height < -500):
            color.append("lightcoral")
        elif (height >= -500 and height <0):
            color.append("cyan")
        elif (height >= 0 and height < 500):
            color.append("gold")
        elif (height >= 500 and height < 1000):
            color.append("chocolate")
        elif (height >= 1000 and height < 1500):
            color.append("lightcoral")
        else:
            color.append("firebrick")

    #check points
    plt.title("Height in colors")
    plt.xlabel("latitude in cartesian")
    plt.ylabel("longitude in cartesian");
    plt.scatter(np.array(x_list), np.array(y_list), color=color)
    plt.legend(loc="upper left")
    # maximize plot
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()


"""
Scatter hieght plot in cartesian coordinate showing different colors - did not work
"""
def scatter_hieght(filename):
    #https://towardsdatascience.com/plotting-regional-topographic-maps-from-scratch-in-python-8452fd770d9d
    #https://kanoki.org/2020/08/30/matplotlib-scatter-plot-color-by-category-in-python/

    from scipy.interpolate import griddata

    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T
    x_list, y_list, z_list = spherical_to_cartesion_list2(lat_list, long_list, height_list)


    pts = 5000;  # Input the desired number of points here
    [x, y] = np.meshgrid(np.linspace(np.min(y_list), np.max(y_list), np.sqrt(pts)),
                         np.linspace(np.min(x_list), np.max(x_list), np.sqrt(pts)));
    z = griddata((y_list, x_list), z_list, (x, y), method='linear');
    x = np.matrix.flatten(x);  # Gridded longitude
    y = np.matrix.flatten(y);  # Gridded latitude
    z = np.matrix.flatten(z);  # Gridded elevation


    fig, ax = plt.subplots()
    cmap = plt.cm.viridis
    norm = colors.Normalize(vmin=min(z), vmax=max(z))
    ax.scatter(x, y, color=cmap(norm(z)),cmap='viridis')
    ax.set_xticks(x)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    fig.colorbar(sm)
    plt.show()

"""
Use colormap to do height chart - did not work
"""
def scatter_hieght_colormap(filename):

    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T
    x_list, y_list, z_list = spherical_to_cartesion_list2(lat_list, long_list, height_list)

    plt.title("Height Colormap")
    plt.xlabel("latitude in cartesian coordinate")
    plt.ylabel("longitude in cartesian coordinate");

    plt.scatter(np.array(x_list), np.array(y_list), c=height_list, cmap= 'rainbow_r') #use c for colormap
    plt.colorbar()
    plt.legend(loc = "upper left")
    # maximize plot
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.show()


if __name__ == "__main__":

    lunar_data_cartesian = 'lunar_data_cartesian.csv'
    lunar_data_file = 'lunar_data.csv'  # the complete file provided by NASA
    matrix_300_zoom_file = 'matrix_300_300_spherical_zoom.csv'  # 300x300 matrix file witin specific coordinates (zoomed)
    matrix_300_all_file = 'matrix_300_300_spherical_all.csv'
    matrix_300_all_cartesian_file = "matrix_300_300_cartesian.csv"
    filename = matrix_300_all_file

    scatter_slope_cartesian(matrix_300_all_cartesian_file, MAX_ROVER_SLOPE, "rover_path.csv")

    scatter_hieght_cartesian(matrix_300_all_file)

    line_slope_vs_height(lunar_data_file)
    #scatter_slope_cartesian(matrix_300_all_file, MAX_ROVER_SLOPE)
    max_slope_top_of_rim(lunar_data_file)

    scatter_hieght_colormap(lunar_data_file)


    line_slope_vs_height(lunar_data_file)

    #scatter_hieght_cartesian("matrix_100_100.csv")
    scatter_slope_cartesian(filename, 5, rover_file_path=None,com_checkpoint_file=None)


    #test()

    scatter_hieght_cartesian()

    # In polar coordinate
    scatter_slope_polar(filename)

    # in cartesian coordinate
    scatter_slope_polar_val_cartesian_coordinate(filename)

    #plot in cartesian coordinate with values converted from polar to cartesian
    scatter_slope_cartesian(filename, MAX_ROVER_SLOPE)

    # plot the slope graph for rover with the path
    scatter_slope_cartesian(filename,MAX_ROVER_SLOPE, "rover_path.csv")

    """
    Landing needs
    1. Flat surce slope < 5
    2. No craters or mountain (height between - -100 to 100?)
    3. Close to Craters where water can be explored
    """
    scatter_slope_cartesian(filename,MAX_LANDING_SLOPE)

    # Graph with relaxed slope of 20
    scatter_slope_cartesian(filename, RELAXED_LANDING_SLOPE, "rover_path_slope20.csv")
