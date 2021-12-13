Python Files
-------------

angle_calculations.py -  functions for distance, spherical and cartesian coordinate conversions, and azimuth and elevation angles from the formula provided in the handbook

communication_checkpoints.py - Finds 10 communication checkpoints

create_cartesian_matrix.py -  Converts lunar data file to cartesian coordinates and creates a 300x330 equal distance cartesian matrix of x, y, z (height) and slope

create_sherical_matrix_and_maze.py - creates 300x300 matrix with lat,long,height, slope and the maze file

maze_bfs.py - takes the maze file and applies BFS algorithm to find the rover path

scatter_plots.py - all matplotlib scatter and line plots

terrain_plotly_meash.py - 3D mesh plots using plotly

csv files
----------

lunar_data.csv - original lunar data file with latitude, longitude, height and slope

lunar_data_cartesian.csv - Lunar data files converted to cartesian coordinates

matrix_300_300_cartesian.csv - 300x300 matrix in cartesian coordinates

matrix_300_300_spherical.csv - 300x300 matrix in spherical coordinates (lat, long,radius)

communication_posts.csv - 10 communication checkpoints calculated by communication_checkpoints.py 

rover_maze.txt - maze text file with go/no-go cells for input to BFS algorithm (slop cutoff = 15)

rover_maze_slope20.txt - maze text file with go/no-go cells for input to BFS algorithm (slop cutoff = 20)

rover_path.csv - rover path array in latitude, longitude (slope =15)

rover_path_slope20.csv - rover path array in latitude, longitude (slope = 20)
