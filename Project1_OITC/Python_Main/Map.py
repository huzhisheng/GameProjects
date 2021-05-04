'''
Map文件说明：

    PointMap类
        变量说明：
        1.point：点
        2.position：点的坐标
    yMap类
        变量说明：
        1.y：y值
        2.sets：y值对应的所有点的PointMap对象
          
    Map类
        变量说明：
        1.map：地图精灵Group对象
        2.platform_set：平台集合，每一个平台对象是精灵Group对象
        3.shortest_path_record：最短路径集合
        4.y_map_table：y值映射表，存储YMap对象
        5.point_map_table：点映射表，存储PointMap对象
        可见方法说明：
        1.generateMapOne：生成地图1，无参数，无返回值
        2.generateMapTwo：生成地图2，无参数，无返回值
    调用方法：
        map = Map()
        map.generateMapOne()
        platform_set = map.platform_set
        shortest_path_record = map.shortest_path_record
        y_map_table = map.y_map_table
        point_map_table = map.point_map_table

        #shortest_path_record获取最短路径方法
        #以获取从i到j的最短路径为例
        path = shortest_path_record[i][j]
        for point in path:
            print(point)
        
        #y_map_table获取第i个元素的y值及映射的方法
        y = y_map_table[i].y
        sets = y_map_table[i].sets
        #获取sets中的点
        point = sets[0].point
        position = sets[0].position

        #point_map_table获取对应点的方法
        #以第i个点为例
        point = point_map_table[i].point
        position = point_map_table[i].position

        while True:
            scene = pygame.display.set_mode((1200,900))
            ...
            map.map.draw(scene)
'''
#from PIL import Image
import operator
import pygame
import math
import cmath
import time
import sys
import random
from Test import Test
from ctypes import windll
#import sys

MAX = 100000
#点值映射对象
root = '.'

class PointMap(object):
    def __init__(self,point):
        self.point = point
        self.position = ()

    def setPosition(self,position):
        self.position = position
        return True
#Y值映射对象
class YMap(object):
    def __init__(self,y):
        self.y = y
        self.sets = []

    def setSets(self,point_map_sets):
        self.sets = point_map_sets
        return True

#砖块对象，组建平台
class Brick(pygame.sprite.Sprite):
    def __init__(self, brick_picture_path, centerPos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(brick_picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = centerPos
        self.topRect=pygame.Rect(self.rect.left,self.rect.top,self.rect.width,10)

#平台对象，组建场景
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.bricks = pygame.sprite.Group()
        self.width = None
        self.height = None
        self.x = None
        self.y = None
        self.start_point = (None,None)
        self.end_point = (None,None)
        self.middle_point = (None,None)


    def generateNormalPlatform(self,sequnce, center_pos,brick_picture_path, num = 6, dir = [1,1]):
        
        is_list = 0
        if isinstance(brick_picture_path, list):
            brick_picture = pygame.image.load(brick_picture_path[0])
            is_list = 1
        else:
            brick_picture = pygame.image.load(brick_picture_path)

        brick_rect = brick_picture.get_rect()
        width = brick_rect.width
        height = brick_rect.height
        x = center_pos[0]
        y = center_pos[1]

        #横拼平台
        if sequnce == 0:           
            
            self.width = width * num
            self.height = height
            self.x = x - dir[0] * width/2
            self.y = y - dir[1] * height/2
            self.start_point = (self.x, self.y)
            self.middle_point = (self.x + dir[0] * self.width/2, self.y)
            self.end_point = (self.x + dir[0] * self.width, self.y)

            for i in range(0,num):
                if i == 0:
                    pass
                else:
                    x += dir[0] * width  
                #print(x)
                if not is_list:
                    brick = Brick(brick_picture_path, (x,y))
                else:
                    if i == 0:
                        brick = Brick(brick_picture_path[0], (x,y))
                    elif i == num - 1:
                        brick = Brick(brick_picture_path[2], (x,y))
                    else:
                        brick = Brick(brick_picture_path[1], (x,y))
                self.bricks.add(brick)
        #竖拼平台
        if sequnce == 1:
            
            self.width = width
            self.height = height * num
            self.x = x - dir[0] * width/2
            self.y = y - dir[1] * height/2
            self.start_point = (self.x, self.y)
            self.middle_point = (self.x + dir[0] * self.width/2, self.y)
            self.end_point = (self.x + dir[0] * self.width, self.y)

            for i in range(0, num):
                if i == 0:
                    pass
                else:
                    y += dir[1] * height
                if not is_list:
                    brick = Brick(brick_picture_path,(x,y))
                else:
                    brick = Brick(brick_picture_path[1],(x,y))
                self.bricks.add(brick)
        #阶梯
        if sequnce == 2:

            self.width = width * num
            self.height = height * num
            self.x = x - dir[0] * width/2
            self.y = y - dir[1] * height/2
            self.start_point = (self.x, self.y)
            self.middle_point = (self.x + dir[0] * self.width/2, self.y + dir[1] * self.height/2)
            self.end_point = (self.x + dir[0] * self.width, self.y + dir[1] * self.height)

            for i in range(0, num):
                if i == 0:
                    pass
                else:
                    y += dir[1] * height
                    x += dir[0] * width
                brick = Brick(brick_picture_path, (x,y))
                self.bricks.add(brick)
#游戏环境创建
class Env(object):
    def __init__(self):
        self.platforms = pygame.sprite.Group()
        self.lines = []

    def dropPlatform(self, sequence, center_pos, brick_picture_path,num = 6,dir = [1,1]):
        platform = Platform()
        platform.generateNormalPlatform(sequence ,center_pos,brick_picture_path,num, dir)
        self.platforms.add(platform.bricks)
        if num >= 3:
            self.lines.append((platform.start_point,platform.middle_point,platform.end_point))
        else:
            self.lines.append(platform.middle_point)
            print(self.lines)
        return platform


class Map(object):
    def __init__(self, max_leap = 460):
        self.map = None #地图精灵对象
        self.max_leap = max_leap
        self.platform_set = [] #集合
        self.shortest_path_record = None #最短路径记录表
        #self.shortest_path_table = None #最短路径值表
        self.y_map_table = None #y值映射 y -> set
        self.point_map_table = None #点映射 A -> (x, y)
        self.background = [root+'/TestPic/skyBg.png',root+'/TestPic/soilBg.png',root+'/TestPic/grassBg.png',root+'/TestPic/stone.png',root+'/TestPic/desertBg.png',
						   root+'/TestPic/caveBg.jpg',root+'/TestPic/cliffBg.jpg',root+'/TestPic/forestBg.png',root+'/TestPic/oldBg.jpg',root+'/TestPic/universeBg.png']

    def loadBricks(self,brick_names):
        brick_name_list = []
        for brick_name in brick_names:
            brick_list = [root+'/MapComposer/'+brick_name+'Left.png',root+'/MapComposer/'+brick_name+'Mid.png',root+'/MapComposer/'+brick_name+'Right.png']
            brick_name_list.append(brick_list)
        return brick_name_list
        
    def generateMapOne(self):
        ##############################搭建场景1###################################
        env = Env()
        snow_list = self.loadBricks(['snow','snow2'])
        self.dropPlatform(env,0,(60, 720),random.choice(snow_list), 15)
        self.dropPlatform(env,0,(720, 720),random.choice(snow_list), 15)
        self.dropPlatform(env,0,(60, 480),random.choice(snow_list), 15)
        self.dropPlatform(env,0,(720, 480),random.choice(snow_list), 15)
        self.dropPlatform(env,0,(120, 360),random.choice(snow_list), 30)
        self.dropPlatform(env,0,(60, 240),random.choice(snow_list), 15)
        self.dropPlatform(env,0,(720, 240),random.choice(snow_list), 15)
        self.dropPlatform(env,0,(120, 600),random.choice(snow_list), 30)
        self.mapConvert(env)

        background = self.background[0]
        return background

    def generateMapTwo(self):
        ##############################搭建场景2###################################
        env = Env()
        dirt_list = self.loadBricks(['dirt','dirt2'])
        self.dropPlatform(env,0,(375, 600),random.choice(dirt_list), 15)
        self.dropPlatform(env,0,(120, 420),random.choice(dirt_list), 30)
        self.dropPlatform(env,0,(90, 240),random.choice(dirt_list), 15)
        self.dropPlatform(env,0,(630, 240),random.choice(dirt_list), 15)
        self.mapConvert(env)
        background = self.background[1]
        return background

    def generateMapThree(self):
        ##############################搭建场景3###################################
        env = Env()
        grass_list = self.loadBricks(['grass','grass2'])
        self.dropPlatform(env,0,(60, 480),random.choice(grass_list), 15)
        self.dropPlatform(env,0,(660, 480),random.choice(grass_list), 15)
        self.dropPlatform(env,0,(120, 360),random.choice(grass_list), 30)
        self.dropPlatform(env,0,(60, 240),random.choice(grass_list), 15)
        self.dropPlatform(env,0,(660, 240),random.choice(grass_list), 15)
        self.dropPlatform(env,0,(120, 600),random.choice(grass_list), 30)
        self.dropPlatform(env,0,(60, 720),random.choice(grass_list), 15)
        self.dropPlatform(env,0,(660, 720),random.choice(grass_list), 15)
        self.mapConvert(env)
        background = self.background[2]
        return background
    def generateMapFour(self):
        ##############################搭建场景4###################################
        env = Env()
        stone_list = self.loadBricks(['stone','stone2'])
        self.dropPlatform(env,0,(60, 480),random.choice(stone_list), 15)
        self.dropPlatform(env,0,(660, 480),random.choice(stone_list), 15)
        self.dropPlatform(env,0,(60, 360),random.choice(stone_list), 15)
        self.dropPlatform(env,0,(660, 360),random.choice(stone_list), 15)
        self.dropPlatform(env,0,(60, 240),random.choice(stone_list), 15)
        self.dropPlatform(env,0,(660, 240),random.choice(stone_list), 15)
        self.dropPlatform(env,0,(60, 600),random.choice(stone_list), 15)
        self.dropPlatform(env,0,(660, 600),random.choice(stone_list), 15)
        self.dropPlatform(env,0,(120, 720),random.choice(stone_list), 30)
        self.mapConvert(env)
        background = self.background[3]
        return background
    def generateMapFive(self):
        ##############################搭建场景5##################################
        env = Env()
        sand_list = self.loadBricks(['sand','sand2'])
        self.dropPlatform(env,0,(30, 480),random.choice(sand_list), 15)
        self.dropPlatform(env,0,(690, 480),random.choice(sand_list), 15)
        self.mapConvert(env)
        background = self.background[4]
        return background

    def generateMapSix(self):
        ##############################搭建场景6###################################
        env = Env()
        cave_list = self.loadBricks(['cave','cave2'])
        self.dropPlatform(env,0,(60, 720),random.choice(cave_list), 15)
        self.dropPlatform(env,0,(720, 720),random.choice(cave_list), 15)
        self.dropPlatform(env,0,(60, 480),random.choice(cave_list), 15)
        self.dropPlatform(env,0,(720, 480),random.choice(cave_list), 15)
        self.dropPlatform(env,0,(120, 360),random.choice(cave_list), 30)
        self.dropPlatform(env,0,(60, 240),random.choice(cave_list), 15)
        self.dropPlatform(env,0,(720, 240),random.choice(cave_list), 15)
        self.dropPlatform(env,0,(120, 600),random.choice(cave_list), 30)
        self.mapConvert(env)
        background = self.background[5]
        return background

    def generateMapSeven(self):
        ##############################搭建场景7###################################
        env = Env()
        cliff_list = self.loadBricks(['cliff','cliff2'])
        self.dropPlatform(env,0,(60, 720),random.choice(cliff_list), 15)
        self.dropPlatform(env,0,(720, 720),random.choice(cliff_list), 15)
        self.dropPlatform(env,0,(60, 480),random.choice(cliff_list), 15)
        self.dropPlatform(env,0,(720, 480),random.choice(cliff_list), 15)
        self.dropPlatform(env,0,(540, 360),random.choice(cliff_list), 4)
        self.dropPlatform(env,0,(60, 240),random.choice(cliff_list), 15)
        self.dropPlatform(env,0,(720, 240),random.choice(cliff_list), 15)
        self.dropPlatform(env,0,(540, 600),random.choice(cliff_list), 4)
        self.mapConvert(env)
        background = self.background[6]
        return background
    def generateMapEight(self):
        ##############################搭建场景8###################################
        env = Env()
        forest_list = self.loadBricks(['forest','forest2'])
        self.dropPlatform(env,0,(60, 720),random.choice(forest_list), 15)
        self.dropPlatform(env,0,(720, 720),random.choice(forest_list), 15)
        self.dropPlatform(env,0,(60, 480),random.choice(forest_list), 15)
        self.dropPlatform(env,0,(720, 480),random.choice(forest_list), 15)
        self.dropPlatform(env,0,(120, 360),random.choice(forest_list), 30)
        self.dropPlatform(env,0,(60, 240),random.choice(forest_list), 15)
        self.dropPlatform(env,0,(720, 240),random.choice(forest_list), 15)
        self.dropPlatform(env,0,(120, 600),random.choice(forest_list), 30)
        self.mapConvert(env)
        background = self.background[7]
        return background
    def generateMapNine(self):
        ##############################搭建场景9###################################
        env = Env()
        old_list = self.loadBricks(['old','old2'])
        n = 14
        for i in range(n):
            if i == 0:
                self.dropPlatform(env,0,(615,240),random.choice([old_list[0][1],old_list[1][1]]),1)
            else:
                start = (1200 - (2 * i - 1) * 30) / 2
                self.dropPlatform(env,0,(start,240 + i * 30),random.choice([old_list[0][1],old_list[1][1]]),1)
                self.dropPlatform(env,0,(start + 2 * i * 30, 240 + i * 30),random.choice([old_list[0][1],old_list[1][1]]),1)
        self.dropPlatform(env,0,(start, 240 + (n+2) * 30 ),random.choice(old_list),2*n - 1 )
        self.mapConvert(env)
        background = self.background[8]
        return background

    def generateMapTen(self):
        ##############################搭建场景10###################################
        env = Env()
        universe_list = self.loadBricks(['universe','universe2'])
        self.dropPlatform(env,0,(330, 240),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(30, 210),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(630, 240),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(930, 270),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(330, 360),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(30, 330),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(630, 360),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(930, 390),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(330, 480),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(30, 450),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(630, 480),random.choice(universe_list),8)
        self.dropPlatform(env,0,(930, 510),random.choice(universe_list),8)
        self.dropPlatform(env,0,(330, 600),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(30, 570),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(630, 600),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(930, 630),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(330, 720),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(30, 690),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(630, 720),random.choice(universe_list), 8)
        self.dropPlatform(env,0,(930, 750),random.choice(universe_list), 8)
        self.mapConvert(env)
        background = self.background[9]
        return background

    def mapConvert(self,env):
        ##############################获取矩阵###################################
        map_matrix,points, self.point_map_table = self.matriculated(env.lines)
        ##############################最短路径###################################
        self.shortest_path_record, shortest_path_table = self.floyd(map_matrix)
        ##############################y值映射表##################################
        self.y_map_table = self.getYMap(points, shortest_path_table)
        ###############################获取精灵##################################
        #if(self.map == None):
        self.map = env.platforms
        #else:
        #    raise Exception("map对象已经有了一个地图，请重新声明一个map对象")
        ###############################测试区#####################################
        #print(map_matrix)
        #printMatrix(map_matrix)
        #matrix = [
        #    [0,5,16,2],
        #    [5,0,10,3],
        #    [16,10,0,1],
        #    [2,3,1,0]
        #    ]
        #for i in range(0,len( self.shortest_path_record)):
        #    for j in range(0,len( self.shortest_path_record)):               
        #        print("From" +str(i)+ "to " +str(j))
        #        print(self.shortest_path_record[i][j])
    def dropPlatform(self, env, seqence, center_pos, brick_picture_path, num = 6,dir = [1,1]):
        platform = env.dropPlatform(seqence,center_pos,brick_picture_path,num,dir )
        self.platform_set.append(platform)
        return

    def matriculated(self, lines):
        matrix = []
        points = []
        point_map_table = []
        print(lines)
        for line in lines:
            if len(line) != len((1,1)):
                for point in line:
                    points.append(point)
            else:
                points.append(line)
        print(points)
        for point, position in enumerate(points):
            point_map = PointMap(point)
            point_map.setPosition(position)
            point_map_table.append(point_map)
        for point_map in point_map_table:
            printObject(point_map)
        #print(points)
        length = len(points)
        for i in range(0, length):
            matrix.append([])
            for j in range(0, length):
                matrix[i].append([])

        for i in range(0, length):
            for j in range(0, length):
                if i!= j:
                    #print(math.pow(abs(points[i][0] - points[j][0]), 2) + math.pow(abs(points[i][1] - points[j][1]), 2))
                    #print(points[i])
                    distance = int(math.sqrt(int(math.pow(points[i][0] - points[j][0], 2) + math.pow(points[i][1] - points[j][1], 2))))
                    if i%2 == 0 and j%2 == 1:
                        if i + 1 == j:
                            matrix[i][j] = distance
                        else:
                            if distance < self.max_leap:
                                matrix[i][j] = distance
                            else:
                                matrix[i][j] = MAX
                    elif i%2 == 1 and j%2 == 0:
                        if j + 1 == i:
                            matrix[i][j] = distance
                        else:
                            if distance < self.max_leap:
                                matrix[i][j] = distance
                            else:
                                matrix[i][j] = MAX
                    else:
                        if distance < self.max_leap:
                            matrix[i][j] = distance
                        else:
                            matrix[i][j] = MAX
                else:
                    matrix[i][j] = 0
        return matrix, points, point_map_table

    def floyd(self,matrix):
        v_num = len(matrix)
        copy = []
        distance = []
        path = []
        for i in range(v_num):
            copy.append([])
            distance.append([])
            path.append([])
            for j in range(v_num):
                copy[i].append([])
                distance[i].append(-1)
                path[i].append([])

        for i in range(v_num):
            for j in range(v_num):
                copy[i][j] = matrix[i][j]
       # printMatrix(copy)
       
        for k in range(v_num):
            for i in range(v_num):
                for j in range(v_num):
                   #Test.getCpu()
                   if(distance[i][j] == -1):
                       distance[i][j] = i
                   if copy[i][j] > copy[i][k] + copy[k][j]:
                       copy[i][j] = copy[i][k] + copy[k][j]                       
                       distance[i][j] = k
        Test.getCpu()            
        printMatrix(copy)
        #printMatrix(distance)
        #shortpath: v->w
        for v in range(v_num):
            for w in range(v_num):
                sequnce = []
                stack = []
                j = w
                if v <= w:
                    while True:
                        stack.append(distance[v][j])
                        if distance[v][j] != v:
                            j = distance[v][j]
                        else: break
                    while len(stack):
                        sequnce.append(stack.pop())
                    sequnce.append(w)
                path[v][w] = sequnce
        
        for v in range(v_num):
            for w in range(v_num):
                if v > w:
                    #print(path[w][v])
                    #print(path[w][v])
                    path[v][w] = path[w][v].copy()
                    path[v][w].reverse()
        Test.getCpu()
        return path, copy

    def getYMap(self, points, shortest_path_table):
        #for i in range(len(points)):
        #    print("点" + str(i))
        #    print(points[i])
        y_value = []
        y_map_table = []
        for i in range(len(points)):
            if points[i][1] not in y_value:
                y_value.append(points[i][1])
        for y in y_value:
            y_map = YMap(y)
            sets = []
            for i in range(len(points)):
                if points[i][1] == y_map.y:
                    point_map = PointMap(i)
                    point_map.setPosition(points[i])
                    sets.append(point_map)
            y_map.setSets(sets)
            y_map_table.append(y_map)
        for map in y_map_table:
            printObject(map)
        return y_map_table
                    
def printObject(object):
    for name, value in vars(object).items():
        #try:
            #x = vars(value).items()
        if isinstance(value, list):
            for elem in value:
                printObject(elem)
        #except:
        else:
            print('%s=%s'%(name,value))

def printMatrix(matrix):
    for i in range(0,len(matrix)):
            for j in range(0,len(matrix)):
                print(matrix[i][j], end = ' ')
            print('\n')

def test(is_window):
    pygame.init()
    #1200 1920
    if is_window:
        scene = pygame.display.set_mode([1200,900],flags=pygame.RESIZABLE)
    else:
        scene = pygame.display.set_mode([1200,900],flags=pygame.FULLSCREEN,depth = 32)
    #置于最上层 from ctypes import windll http://www.itkeyword.com/doc/5239207061455695x393/how-to-make-python-window-run-as-always-on-top
   # SetWindowPos = windll.user32.SetWindowPos
    #SetWindowPos(pygame.display.get_wm_info()['window'], -1, 0, 0, 0, 0, 0x0001)

    pygame.display.set_caption("输出全靠吼——测试")
    bg_image = pygame.image.load("MapComposer/bgImage.png")
    clock = pygame.time.Clock()
    myfont = pygame.font.Font(None,30) 
    
    map = Map()
    map.generateMapFive()
    return
    #map2 = map.generateMapTwo()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
                 #sys.exit()

        clock.tick(90)
        scene.blit(bg_image,(0,0))
        map.map.draw(scene)       
        for point in map.point_map_table:
            textImage = myfont.render(str(point.point),True,(255,255,255))
            scene.blit(textImage,point.position)
        pygame.display.update()

#test(1)