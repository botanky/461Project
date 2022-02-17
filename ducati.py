import numpy as np
import time
class ducati:
    '''
    This is the random player used in the colab example.
    Edit this file properly to turn it into your submission or generate a similar file that has the same minimal class structure.
    You have to replace the name of the class (ME461Group) with one of the following (exactly as given below) to match your group name
        atlas
        backspacex
        ducati
        hepsi1
        mechrix
        meturoam
        nebula
        ohmygroup
        tulumba
    After you edit this class, save it as groupname.py where groupname again is exactly one of the above
    '''
    def __init__(self, userName, clrDictionary, maxStepSize, maxTime):
        self.name = userName # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize # maximum length of the returned path from run()
        self.maxTime = maxTime # run() is supposed to return before maxTime

  
    def run(self, img, info):
        myinfo = info[self.name]
        print(info[self.name])
        loc, game_point = info[self.name]
        rows = 15 #compressed size of rows
        cols = 15 #compressed size of collums
        grid=[]
        matrix = np.zeros((rows,cols), int) #compressed matrix
        lines = matrix.tolist()
        
        
        point = [[[1,1,1],0],[[225,1,1],100],[[1,255,1],50],[[1,1,255],30],[[200,200,1],20],
                 [[255,1,255],10],[[1,255,255],9],[[1,1,150],8],[[120,120,40],7],[[150,1,150],6],
                 [[1,150,150],5],[[222,55,222],4],[[1,99,55],3],[[200,100,10],2],[[100,10,200],1],
                 [[255,255,255],0]]
        
        #in this loop the points transform as a class objext(Node class)
        for i in range(rows):
            row = lines[i]
            row_nodes = []
            for j in range(len(row)):
                node = Node(grid, j, i)
                row_nodes.append(node)
            grid.append(row_nodes)

        #these variables are for our artificial matrix instead of real one 
        startx = round((loc[0]-25)/50)
        starty = round((loc[1]-25)/50)
        
        #the points are added to our matrix
        for i in range(rows):
            for j in range(cols):
                for z in point:
                    if np.array_equal((img[50*i+25,50*j+25,:]).astype(int),z[0]):
                        grid[i][j].color = z[1]
                        break


        start=grid[startx][starty] #the start point as the Node class object
        stepsize=5 #the step size the code search for one run
        close = [] #this is used in pathfind function to follow path
        print(start.y,start.x) 
        print(start.color)
        maxi, pat = pathfind(start,stepsize,close,game_point)
        ppath=[]
        print(maxi)
        if maxi == 0:
            maxi, pat = pathfind(start,9,close,game_point)
        realpat = []
        realpat.append([loc[0],loc[1]])
        ppath = []
        ppath.append([pat[0].y*50+25,pat[0].x*50+25])
        for i in pat[1:]:
            print([i.y*50+25,i.x*50+25])
            realpat.append([i.y*50+25,i.x*50+25])
            ppath.append([i.y*50+25,i.x*50+25])
        for i in range(len(ppath)-1):
            print(realpat[i])
            if not realpat[i][0] == ppath[i+1][0] or realpat[i][1] == ppath[i+1][1]:
                cor0 = realpat[i][0] - ppath[i][0]
                cor1 = realpat[i][1] - ppath[i][1]
                realpat[i+1][0] = realpat[i+1][0] + cor0
                realpat[i+1][1] = realpat[i+1][1] + cor1
            
                    
        return realpat[1:]
    
class Node:
    def __init__(self, grid, x, y):
        self.x = x
        self.y = y
        self.grid = grid
        self.color = None
        self.g_score = float('inf')
        self.f_score = float('inf')

    def get_neighbors(self):
        # Collection of arrays representing the x and y displacement
        rows = len(self.grid)
        cols = len(self.grid[0])
        directions = [[1, 0], [0, 1], [0, -1], [-1, 0]]
        neighbors = []
        for direction in directions:
            neighbor_x = self.x  + direction[0]
            neighbor_y = self.y + direction[1]
            if neighbor_x >= 0 and neighbor_y >= 0 and neighbor_x < cols and neighbor_y < rows:
                neighbors.append(self.grid[neighbor_y][neighbor_x])
        return neighbors
  

            
            
def pathfind (start,step,path,best,score=0,maxi=0,pathmax=[],t=0,):
    path.append(start)
    for i in start.get_neighbors():
        sco_re = score #to save the real score
        if not i in path:
            score=i.color+score #this is the collected score if this route is followed
            if (score > maxi or (score==maxi and len(path)+1 < len(pathmax))) and best>=score:
                pathmax = path+[i]
                maxi=score
            if t<step:
                maxi, pathmax = pathfind(i,step,path,best,score,maxi,pathmax,t+1)
        score=sco_re
    path.pop(-1)
    return maxi,pathmax

