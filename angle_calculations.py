#latitude longitude
#https://www.britannica.com/science/latitude

#azimuth calculator:
#https://www.omnicalculator.com/other/azimuth
#https://www.omnicalculator.com/other/azimuth#how-to-calculate-the-azimuth-from-latitude-and-longitude
#https://ttu-ir.tdl.org/bitstream/handle/2346/59629/ICES-2014-093.pdf?sequence=1

#cartesian to spherical


import math

LUNAR_RADIUS = 1737.4 * 1000 #meter
EARTH_RADIUS = 6371.0072 * 1000 #meter
# Earth Cartesian Position with respect to Lunar Fixed Frame at a single time instant is
# [X, Y, Z] = [361000, 0, –42100] km.
EARTH_CARTESIAN_FIXED = (361000000, 0, -42100000) #meter


# ***  x is longtide y is lattitude  ****

"""
Following routines has trig functions that accepts degree as input (Python math trig functions take radian)
"""
def rad_to_degree(rad):
    deg = rad * 180 / math.pi
    return(deg)
def degree_to_radian(deg):
    rad = deg * math.pi / 180
    return(rad)
def cos(degree):
    return(math.cos(degree_to_radian(degree)))
def sin(degree):
    return(math.sin(degree_to_radian(degree)))
def tan(degree):
    return(math.tan(degree_to_radian(degree)))
def asin_deg(val):  #takes value returns degree
    return(rad_to_degree(math.asin(val)))
def asin_rad(val):  #takes value returns radian
    return(math.asin(val))
def atan2_deg(val1, val2):  #takes value returns degree
    return(rad_to_degree(math.atan2(val1,val2)))
def atan2_rad(val1, val2):  #takes value returns radian
    return(math.atan2(val1,val2))


"""
Azimuth between point A (long,lat) and B(long,lat) in degree.  Azimoth does not need radius
"""
def azimuth_between_two_points(pointA,pointB):
    #https://www.omnicalculator.com/other/azimuth

    LatA,LongA,heightA = pointA
    LatB,LongB, heightB = pointB

    azimuth_A_B= atan2_deg((sin(LongB-LongA)*cos(LatB)), ((cos(LatA)*sin(LatB))-(sin(LatA)*cos(LatB)* cos(LongB-LongA))))
    return(azimuth_A_B)

#azimuth between Point A and earth
def azimuth_between_one_point_and_earth(pointA):
    earth_cartesian = (361000000, 0, -42100000)
    (x,y,z) = earth_cartesian;
    earth_spherical = cartesion_to_spherical(x, y, z)
    azimuth_A_Earth = azimuth_between_two_points(pointA,earth_spherical)
    return(azimuth_A_Earth)

def earth_fixed_azimuth():
    earth_cartesian = (361000000, 0, -42100000)
    (x,y,z) = earth_cartesian;
    (lat,long, radius) = cartesion_to_spherical(x, y, z)
    return(long) # long is azimuth

"""
Distance between point A (long,lat) and B(long,lat) in spherical coordinate in meters with a common radiuos
"""
def calculate_spherical_distance(pointA,pointB,radius):
    #https://www.omnicalculator.com/other/azimuth
    R = radius
    LatA,LongA,HeightA = pointA
    LatB,LongB,heightB = pointB
    a = math.pow (sin( (LatB - LatA) / 2),2) + cos(LatA) * cos(LatB) * pow (sin( (LongB -LongA) / 2), 2)
    c = 2 * atan2_rad(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return(d)

def calculate_linear_distance(pointA,pointB):
    LatA,LongA,HieghtA = pointA
    LatB,LongB,  HieghtB = pointB
    distance = math.sqrt( math.pow((LongB - LongA), 2) +  math.pow((LatB - LatA),2))
    return(distance)

"""
Converts from spherical to cartesian coordinate 
"""
def spherical_to_cartesion(lat,long, radius):  #radius = LUNAR_RADIUS + height
    x = radius* (cos(lat) * cos(long))
    y = radius * (cos(lat) * sin(long))
    z = radius * (sin(lat))
    return(x,y,z)

def spherical_to_cartesion_list(lat_list,long_list, radius):  #radius = LUNAR_RADIUS + height
    x_list = []
    y_list = []

    for index in range(len(lat_list)):
        (x,y,z) = spherical_to_cartesion(lat_list[index], long_list[index], radius)
        x_list.append(x)
        y_list.append(y)

    return(x_list,y_list)

def spherical_to_cartesion_list2(lat_list,long_list, height_list):
    x_list = []
    y_list = []
    z_list = []

    for index in range(len(lat_list)):
        (x,y,z) = spherical_to_cartesion(lat_list[index], long_list[index], height_list[index] + LUNAR_RADIUS)
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)

    return(x_list,y_list,z_list)


# Takes lat,long, and **height** data and coverts to (x,y,z)
def moon_sperical_to_cartesian(long, lat, height):
    return(spherical_to_cartesion(lat, long, height + LUNAR_RADIUS))

def cartesion_to_spherical(x, y, z):
    radius = math.sqrt(x*x + y*y + z*z)
    lat = asin_deg(z/radius)
    long = atan2_deg(y,x)
    return(lat,long, radius)


"""
Elevation angle (degree) from PointA(lat,long, height) (spherical) to PointB  in Moon
"""
def calculate_elevation_angle(pointA, pointB):
    (LatA,LongA,HeightA) = pointA
    (LatB,LongB, HeightB) = pointB

    (xA,yA,zA) = moon_sperical_to_cartesian(LongA,LatA,HeightA) #m
    (xB, yB, zB) = moon_sperical_to_cartesian(LongB, LatB, HeightB)
    xAB = xB - xA
    yAB = yB - yA
    zAB = zB - zA
    rangeAB = math.sqrt(math.pow(xAB,2) +math.pow(yAB,2) +math.pow(zAB,2) )
    #𝑟𝑧 = 𝑥𝐴𝐵cos(𝐿𝑎𝑡𝐴)cos(𝐿𝑜𝑛𝑔𝐴) + 𝑦𝐴𝐵cos(𝐿𝑎𝑡𝐴)sin(𝐿𝑜𝑛𝑔𝐴) + 𝑧𝐴𝐵sin(𝐿𝑎𝑡𝐴)
    rz = xAB * cos(LatA)*cos(LongA) + yAB * cos(LatA)*sin(LongA) + zAB * sin(LatA)
    elevationAB_deg = asin_deg(rz/rangeAB)

    return(elevationAB_deg)

"""
Elevation angle (degree) from PointA(lat,long, height) (spherical) to earth fixed cartesian from moon
"""
def calculate_earth_elevation_angle(pointA):
    (LatA,LongA, HeightA) = pointA

    (xA, yA, zA) = moon_sperical_to_cartesian(LongA, LatA, HeightA)  # m
    (xB, yB, zB) = EARTH_CARTESIAN_FIXED
    xAB = xB - xA
    yAB = yB - yA
    zAB = zB - zA
    rangeAB = math.sqrt(math.pow(xAB, 2) + math.pow(yAB, 2) + math.pow(zAB, 2))
    # 𝑟𝑧 = 𝑥𝐴𝐵cos(𝐿𝑎𝑡𝐴)cos(𝐿𝑜𝑛𝑔𝐴) + 𝑦𝐴𝐵cos(𝐿𝑎𝑡𝐴)sin(𝐿𝑜𝑛𝑔𝐴) + 𝑧𝐴𝐵sin(𝐿𝑎𝑡𝐴)
    rz = xAB * cos(LatA) * cos(LongA) + yAB * cos(LatA) * sin(LongA) + zAB * sin(LatA)
    elevationAB_deg = asin_deg(rz / rangeAB)

    return (elevationAB_deg)

# given a x list and y list finds the point (x,y) that is closest to the point x1,y1
def closest_point(x1,y1, x_list, y_list):
    closest_distance= 10000 #some big value
    closest_x_y_index = None

    for index in range(len(x_list)-1):
        dist = distance(x1,y1,x_list[index],y_list[index])  #find distance between two points
        if(dist < closest_distance):
            closest_distance = dist  #keep on updating closest distance
            closest_x_y_index = (x_list[index],y_list[index],index)

    return(closest_x_y_index)

#distance between two (x,y) points
def distance(x1,y1,x2,y2):
    return(math.sqrt((x2-x1) * (x2-x1) + (y2 -y1) * (y2 -y1)))

"""
calculate
"""

def test():

    (x,y,z) = EARTH_CARTESIAN_FIXED
    earth_fixed_sperical = cartesion_to_spherical(x,y,z)

    """
    Verify azimuth and spherical distance
    """
    point_1 = (51.50,0, 0)  #london
    point_2 = (-22.97,-43.18,0) #Rio de genero lat 22.9S long 43.17W
    az = azimuth_between_two_points(point_1, point_2) # <-- should be -140.65
    print("azimuth between ", point_1, " ", point_2, " = ", az)

    pointA = (-89.59284887168748, 137.7575280440554, 2602.5)
    eath_azimuth = azimuth_between_one_point_and_earth(pointA)
    print("azimuth between ", point_1, " and earth = ",eath_azimuth, " deg")

    # the azimoth between london and Rio is -140.65 deg
    distance = calculate_spherical_distance(point_1, point_2, EARTH_RADIUS)
    print("spherical distance for ", point_1, " ", point_2, " = ", distance, " meter")
    #the distance between london and Rio is 9289 km

    """
    Verify linear distance
    """
    lin_dis = calculate_linear_distance((0,0,0), (3,4,0))  # in cartesian coordinate, should be 5
    print("linear distance for ", (0,0), " ", (3,4), " = ", lin_dis)

    """
    Verify spherical to cartesian conversion
    """
    long = 60 #pi/3
    lat = 30  #pi/6
    radius = 8
    (x,y,z) = spherical_to_cartesion(lat,long, radius) # answer should be (x,y,z) = (2,2√3,4√3) = (2,3.46,6.93)
    print("linear distance for long =", long,"lat=", lat, "radius=", radius, " = ", (x,y,z)) # x y swapped?

    """
    Elevation Angle
    """
    pointA =(-89.59284887168748, 137.7575280440554, 2602.5) # slope 26
    pointB = (-89.59187137092688, 137.8820225887941, 3000) #slope 28
    elevation = calculate_elevation_angle(pointA, pointB)
    print("In moon elevation between ", pointA, " ", pointB, " = ", elevation, " degree")
    earth_elevation = calculate_earth_elevation_angle(pointA)
    print("elevation between ", pointA, " in moon and earth = ", earth_elevation, " degree")

def test_azimuth_matrix():

    pointA = (-89, 90, 0)  # slope 26
    pointB = (-89, 90, 0)
    az = azimuth_between_two_points(pointA,pointB) # azimuth between same point =0

    pointA = (-90, 0, 0)  # slope 26
    pointB = (-90, 90, 0)
    az = azimuth_between_two_points(pointA, pointB)  # azimuth between same point =0

    MATRIX_N = 5
    lat_min = -90
    lat_max = -88.4
    long_min = -180
    long_max = 180
    step_lat = (lat_max - lat_min) / (MATRIX_N - 1)  # equal n number of x steps
    step_long = (long_max - long_min) / (MATRIX_N - 1)  # equal n number of y steps

    lat_list = []
    long_list = []
    step_x = (lat_max - lat_min) / (MATRIX_N - 1)  # equal n number of x steps
    step_y = (long_max - long_min) / (MATRIX_N - 1)  # equal n number of y steps
    for index in range(MATRIX_N):
        lat_list.append(lat_min + index * step_lat)
        long_list.append(long_min + index * step_long)
    mid_index = int(MATRIX_N / 2)
    mid_point = (lat_list[mid_index], long_list[mid_index], 0)
    print("mid point ", mid_point)
    one_row = []
    rows = []
    all_line_lat_long = ""
    all_line_azimoth = ""
    for index_lat in range(len(lat_list)):
        for index_long in range(len(long_list)):
            pointB = (lat_list[index_lat], long_list[index_long], 0)
            cell = (round(lat_list[index_lat], 2), round(long_list[index_long], 2))
            all_line_lat_long = all_line_lat_long + " " + str(cell)
            all_line_azimoth = all_line_azimoth + " " + str(round(azimuth_between_two_points(mid_point, pointB), 2))
            one_row.append(cell)
            if ((index_long + 1) % MATRIX_N == 0):
                rows.append(one_row)
                one_row = []
                all_line_lat_long = all_line_lat_long + "\n"
                all_line_azimoth = all_line_azimoth + "\n"

    print(all_line_lat_long)
    print(all_line_azimoth)


if __name__ == "__main__":
    #test()
    test_azimuth_matrix()