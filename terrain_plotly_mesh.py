#https://plotly.com/python/3d-mesh/

import plotly.graph_objects as go
import numpy as np
from angle_calculations import spherical_to_cartesion_list2, azimuth_between_one_point_and_earth, calculate_earth_elevation_angle
import plotly.express as px
import plotly.offline as go_offline

LUNAR_RADIUS = 1737.4 * 1000 #meter
"""
Plotly mesh diagram for slope 
"""
def mesh_slope(filename, convert_to_cartesian):

    """
    Read File
    """
    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    """
    Convert x,y,z to cartesian
    """
    if(convert_to_cartesian == True):
        x_list, y_list, z_list = spherical_to_cartesion_list2(lat_list, long_list, height_list)
    else:
        x_list, y_list, z_list = lat_list, long_list, height_list

    """
    Plot
    """
    fig = go.Figure(
        data=[go.Mesh3d(x=np.array(x_list), y=np.array(y_list), z=np.array(slope_list), colorscale= "viridis", intensity =slope_list, opacity=0.90)])
    fig.update_layout(
        title='lattitude (x) longitude (y) and Slope (z) in cartesian coordinate',
        width=1400,
        height=1200,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=0,
                    y=1.0707,
                    z=1,
                )
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual',
        ),
        xaxis=dict(range=[min(x_list), max(x_list)], ),
        yaxis=dict(range=[min(y_list), max(y_list)])
    )
    fig.show()

"""
Plotly mesh diagram for azimuth with respect to earth fixed coordinate 
"""
def mesh_azimuth(filename):

    """
    Read File
    """
    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    """
    Convert x,y,z to cartesian
    """
    x_list, y_list, z_list = spherical_to_cartesion_list2(lat_list, long_list, height_list)

    azimuth_list = []
    for index,lat in enumerate(lat_list):
        pointA = (lat_list[index], long_list[index], height_list[index])
        azimuth = azimuth_between_one_point_and_earth(pointA)
        azimuth_list.append(azimuth)


    """
    Plot
    """
    fig = go.Figure(
        data=[go.Mesh3d(x=np.array(x_list), y=np.array(y_list), z=np.array(azimuth_list), colorscale= "rainbow", intensity =azimuth_list, opacity=0.90)])
    fig.update_layout(
        title='lattitude (x) longitude (y) and Azimuth between point and earth (z) in cartesian coordinate',
        width=1200,
        height=800,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=0,
                    y=1.0707,
                    z=1,
                )
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual',
        ),
        xaxis=dict(range=[min(x_list), max(x_list)], ),
        yaxis=dict(range=[min(y_list), max(y_list)])
    )
    fig.show()


"""
Plotly mesh diagram for elevation with respect to earth fixed coordinate 
"""
def mesh_elevation(filename):

    """
    Read File
    """
    pts = np.loadtxt(np.DataSource().open(filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    """
    Convert x,y,z to cartesian
    """
    x_list, y_list, z_list = spherical_to_cartesion_list2(lat_list, long_list, height_list)

    elevation_list = []
    for index,lat in enumerate(lat_list):
        pointA = (lat_list[index], long_list[index], height_list[index])
        elevation = calculate_earth_elevation_angle(pointA)
        elevation_list.append(elevation)


    """
    Plot
    """
    fig = go.Figure(
        data=[go.Mesh3d(x=np.array(x_list), y=np.array(y_list), z=np.array(elevation_list), colorscale= "twilight", intensity =elevation_list, opacity=0.90)])
    fig.update_layout(
        title='lattitude (x) longitude (y) and elevation angle between point and earth (z) in cartesian coordinate',
        width=1100,
        height=700,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=0,
                    y=1.0707,
                    z=1,
                )
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual',
        ),
        xaxis=dict(range=[min(x_list), max(x_list)], ),
        yaxis=dict(range=[min(y_list), max(y_list)])
    )
    fig.show()
"""
Plotly mesh plot of lat, long and hiegt with rover path and communication links
"""
def mesh_plot_height(data_filename, convert_to_cartesian, rover_filename = 'rover_path.csv', com_link_filename = "communication_posts.csv"):

    """
    Read File Convert x,y,z to cartesian
    """
    pts = np.loadtxt(np.DataSource().open(data_filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    if (convert_to_cartesian == True):
        x_list, y_list, z_list = spherical_to_cartesion_list2(lat_list, long_list, height_list)
    else:
        x_list = lat_list
        y_list = long_list
        z_list = height_list

    """
    Read rover path file
    """
    #https://plotly.com/python/3d-line-plots/
    pts = np.loadtxt(np.DataSource().open(rover_filename), delimiter=",")
    r_lat_list, r_long_list, r_height_list, r_slope_list = pts.T
    r_x_list, r_y_list, r_height_list = spherical_to_cartesion_list2(r_lat_list, r_long_list, r_height_list)
    """
    Read com link file
    """
    pts = np.loadtxt(np.DataSource().open(com_link_filename), delimiter=",")
    c_lat_list, c_long_list, c_height_list = pts.T
    c_x_list, c_y_list, c_z_list = spherical_to_cartesion_list2(c_lat_list, c_long_list, c_height_list)

    """
    Plot
    """
    fig = go.Figure(
        data=[
            go.Mesh3d(x=np.array(x_list), y=np.array(y_list), z=np.array(height_list), colorscale= "rainbow", intensity =height_list, opacity=0.9),
            go.Scatter3d(x=np.array(r_x_list), y=np.array(r_y_list), z=np.array(r_height_list), marker=dict(size=4, line=dict(width=2,color='DarkSlateGrey')),line = dict(color='white',width=2)),
            #go.Scatter3d(x=np.array(c_x_list), y=np.array(c_y_list), z=np.array(c_height_list), marker=dict(size=4, line=dict(width=2,color='DarkSlateGrey')), line = dict(width=0))
             ])


    fig.update_layout(
        title='lattitude (x) longitude (y) and height (z) in cartesian coordinate with rover path and communication links',
        width=1400,
        height=1200,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(
                    x=0,
                    y=0,
                    z=1
                ),
                eye=dict(
                    x=0,
                    y=1.0707,
                    z=1,
                )
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual',
        ),
        xaxis=dict(range=[min(x_list), max(x_list)], ),
        yaxis=dict(range=[min(y_list), max(y_list)])
    )
    #go_offline.plot(fig,filename='lunar_3d_terrain_height.html',validate=True, auto_open=False)
    fig.show()


if __name__ == "__main__":
    filename = "matrix_300_300_spherical_all.csv"  # matrix_300_300_spherical_zoom.csv
    matrix_300_all_cartesian_file = "matrix_300_300_cartesian.csv"
    mesh_plot_height(matrix_300_all_cartesian_file,convert_to_cartesian=False, rover_filename='rover_path.csv', com_link_filename="communication_posts.csv")
    #mesh_slope(matrix_300_all_cartesian_file, convert_to_cartesian = False)
    #mesh_plot_height(filename)
    mesh_azimuth(filename)
    mesh_elevation(filename)





 #  Plotly colors:
 # ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
 # 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
 # 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
 # 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
 # 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
 # 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
 # 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
 # 'orrd', 'oryel', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
 # 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor',
 # 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy',
 # 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral',
 # 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose',
 # 'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'twilight',
 # 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd'].