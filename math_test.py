import math



def angle_round(cx,cy,d):
    angle_round_list=[]
    angle_unit_number=36
    #print("Warning: A circle is divided into ",angle_unit_number," parts, each part of ",round(180/angle_unit_number,1)," degrees")
    for i in range(1,angle_unit_number*2+1):
        x1= round(math.cos(i / angle_unit_number * math.pi), 3) * d + cx
        y1 = round(math.sin(i / angle_unit_number * math.pi), 3) * d + cy
        angle_round_list.append([x1,y1])
    return angle_round_list

def un_angle_round(cx,cy,round_list):

    angle_round_list=[]
    angle_unit_number=36 
    for i in range(1,angle_unit_number*2+1):
        d=round_list[i-1]
        x1= round(round(math.cos(i / angle_unit_number * math.pi), 3) * d + cx)

        y1 = round(round(math.sin(i / angle_unit_number * math.pi), 3) * d + cy)
        angle_round_list.append([x1,y1])
    return angle_round_list




def cell_wall_ray_lenth(cx,cy,x1,y1):
    distance=round(((x1-cx)**2+(y1-cy)**2)**0.5,3)
    return distance

a=cell_wall_ray_lenth(0,0,2,0)


def distance(x1,y1,x2,y2):
    result=((x1-x2)**2+(y1-y2)**2)**0.5

    return round(result,2)



def quantile_p(data,p):
    pos = (len(data) + 1)*p
    pos_integer = int(math.modf(pos)[1])
    pos_decimal = pos - pos_integer
    Q = data[pos_integer - 1] + (data[pos_integer] - data[pos_integer - 1])*pos_decimal
    return Q

def ourliers_clean(list):
    list.sort()
    Q1=quantile_p(list,0.25)
    Q2=quantile_p(list,0.5)
    Q3=quantile_p(list,0.75)
    IQR=Q3-Q1
    Min_limit=Q1-1.5*IQR
    Max_limit=Q3+1.5*IQR
    for i in range(0,len(list)):
        if list[i]<=Min_limit and list[i]>=Max_limit:
            list.remove(list[i])
    return list



def combine_two_2d_list(a,b):
    for i in range(0, len(a)):
    
        a[i].append(b[i][0])

    return a

def find_min_length_list(dataset):
    m=999
    for i in dataset:
        if len(i)<=m:
            m=len(i)
            position=dataset.index(i)

    return position,dataset[position]

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
def GetAreaOfPolyGonbyVector(points):
    area = 0
    if(len(points)<3):

         raise Exception("error")

    for i in range(0,len(points)-1):
        p1 = points[i]
        p2 = points[i + 1]

        triArea = (p1.x*p2.y - p2.x*p1.y)/2
        area += triArea
    return abs(area)
def area_calculate_from_points(points_list):
    points = []
    x=[]
    y=[]
    for i in range(0,len(points_list)):
        x.append(points_list[i][0])
        y.append(points_list[i][1])
    for index in range(len(x)):
        points.append(Point(x[index],y[index]))

    area = GetAreaOfPolyGonbyVector(points)
    return math.ceil(area)


def holo_area_calculate_from_points(points_list,img,threshold):
    white_count=0

    for i in range(0,len(points_list)):
        x=points_list[i][0]
        y = points_list[i][1]
        print(img[x,y])

        if img[x,y]>=threshold:
            white_count+=1

    print("The Holo of this cell is: ",white_count)
    return white_count

def find_longest_element_index(list):
    word_len_list = [len(word) for word in list]
    max_word_len = max(word_len_list)
    for word in list:
        if len(word) == max_word_len:
            output=list.index(word)
           

    return output


def relocate_start_point(units_number, start_point):
    i1 = [tt for tt in range(0, start_point+1)]

    i2 = [t for t in range(start_point+1, units_number)]

    i2.extend(i1)

    return i2