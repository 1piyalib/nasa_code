import collections
import numpy as np


"""
This runs a Breadth First Search on a maze
https://en.wikipedia.org/wiki/Breadth-first_search
https://stackoverflow.com/questions/47896461/get-shortest-path-to-a-cell-in-a-2d-array-in-python
"""
def bfs(grid):

    path = None;
    #definition, A is start point B is target
    wall, clear, goal, begin = "#", " ", "B", "A"

    # check grid size
    if(len(grid)< 1):
        print("Error: grid cannot be less than one element")
        return path;

    # find width and hieght of the grid
    width, height = len(grid[0]), len(grid)

    # find starting point
    i = 0
    j = -1
    for row in grid:
        if(begin in row):
            j = row.index(begin)
            break;
        i = i+ 1
    start = (j,i)
    if (j == -1):
        print("Error: Could not find starting point ", begin)
        return path;

    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        print(path)
        x, y = path[-1]
        if grid[y][x] == goal:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height:
                try:
                    if grid[y2][x2] != wall and (x2, y2) not in seen:
                        queue.append(path + [(x2, y2)])
                        seen.add((x2, y2))
                except:
                    print("Error: out of index ", x2,y2)

    return(path)

"""
Create maze file from the matrix file
"""
def create_maze_file(matrix_filename, matrix_n, maze_filename, slope_cutoff):

    from angle_calculations import closest_point
    landing_site_x_y = [-89.1, 55]
    destination_site_x_y = [-89.2, 120]

    pts = np.loadtxt(np.DataSource().open(matrix_filename), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    (landing_x, landing_y, landing_index) = closest_point(landing_site_x_y[0], landing_site_x_y[1], lat_list, long_list)
    (destination_x, destination_y, destination_index) = closest_point(destination_site_x_y[0], destination_site_x_y[1],lat_list, long_list)
    print("landing_x_y", landing_x, " ", landing_y)
    print("destination_x_y", destination_x, " ", destination_y)

    all_lines = ""
    for index in range(len(lat_list)):
            if (lat_list[index] == landing_x and long_list[index] == landing_y):
                all_lines = all_lines + "A"  # start point
            elif (lat_list[index] == destination_x and long_list[index] == destination_y):
                all_lines = all_lines + "B"  # end point
            elif (slope_list[index] < slope_cutoff):
                all_lines = all_lines + " "
            else:
                all_lines = all_lines + "#"

            if ((index + 1) % matrix_n == 0):
                all_lines = all_lines + "\n"

    #print(all_lines)
    maze_file = open(maze_filename, 'w')
    maze_file.write(all_lines + '\n')
    maze_file.close()
    print(maze_filename + " was created")


"""
takes the path from bfs() and reads the csv file, identifies 
corresponding indexes in the matrix_300_300_spherical_zoom.csv and writes the
coordinates into the rover_path.csv file
"""
def save_rover_path(path, matrix_file, matrix_n, rover_path_output_file):

    index_list = []
    for element in path:
        (a, b) = element
        index_list.append(matrix_n * b + a)  # 300 matrix_n

    pts = np.loadtxt(np.DataSource().open(matrix_file), delimiter=",")
    lat_list, long_list, height_list, slope_list = pts.T

    all_lines = ""
    for index in index_list:
        all_lines = all_lines + str(lat_list[index]) + "," + str(long_list[index]) + "," + str(height_list[index]) + "," + str(slope_list[index]) +"\n"

    maze_file = open(rover_path_output_file, 'w')
    maze_file.write(all_lines + '\n')
    maze_file.close()

def debug_grid():
    test_grid = ["          ",
                 "  ##   ## ",
                 "  ## A ## ",
                 "     ###  ",
                 "B         "]

    path = bfs(test_grid)
    print("----  Final Path --------")
    print("expected: [(5, 2), (4, 2), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3), (0, 4)]")
    print("received:", path)
    #path is [(5, 2), (4, 2), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3), (0, 4)]

if __name__ == "__main__":

    #debug_grid()


    matrix_file = "matrix_300_300_spherical_zoom.csv"
    matrix_n = 300
    maze_file = "deprecated/rover_maze_temp.txt"
    rover_path_output_file = "rover_path_temp.csv"
    slope_cutoff = 15

    # step 1: create maze from matrix
    create_maze_file(matrix_file, matrix_n, maze_file, slope_cutoff)
    # step 2: Find best path in maze
    f = open(maze_file)
    grid = f.readlines()
    path = bfs(grid)
    # step 3: save best path to a lat, long file
    save_rover_path(path, matrix_file, matrix_n, rover_path_output_file)


