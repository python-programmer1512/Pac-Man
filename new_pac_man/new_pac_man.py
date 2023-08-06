#https://stackoverflow.com/questions/57043905/how-can-we-use-pygame-on-google-colab

import sys
sys.setrecursionlimit(10**9)
from random import *
import pygame
import datetime
from collections import deque
import time
from math import *
from queue import PriorityQueue
from pygame.locals import QUIT,KEYDOWN,K_LEFT,K_RIGHT,K_UP,K_DOWN,Rect,MOUSEBUTTONDOWN,K_SPACE
from large_dataset import *
pygame.init()
FPSCLOCK = pygame.time.Clock()
size=(1500,800)
FPS=150
SCORE=0
SURFACE = pygame.display.set_mode((size[0],size[1]+50))
color={
    "black":[0,0,0],
    "white":[255,255,255],
    "red":[255,0,0],
    "blue":[0,0,255],
    "yellow":[255,255,0],
    "green":[0,255,0],
    "gray":[192,192,192]
    }
#angle : - 가 시계방향, + 가 반시계 방향
QE=["white","red","blue","yellow","green","gray"]
colorn=[QE[i%len(QE)]for i in range(100)]
SCORE=0

MAP=[]
class Item(pygame.sprite.Sprite):
    global MAP
    def __init__(self, tile_size=50):
        pygame.sprite.Sprite.__init__(self)
        self.tile_size=tile_size
        self.y_length=size[1]//tile_size
        self.x_length=size[0]//tile_size
        self.img_x_size=10
        self.img_y_size=10
        self.dy=[-1,1,0,0]
        self.dx=[0,0,-1,1]
        self.all_item_count=0

        self.item_map=[[-1 for i in range(self.x_length+5)]for g in range(self.y_length+5)]

        self.item_img=[pygame.image.load("pac_man_item_image/item_1.png").convert_alpha(),
                       pygame.image.load("pac_man_item_image/item_2.png").convert_alpha()]
        
        for i in range(len(self.item_img)):
            self.item_img[i]=pygame.transform.scale(self.item_img[i],(self.item_img[i].get_width()/10,self.item_img[i].get_height()/10))
        
        self.item_percentage=[50,1]

    
    def produce_item(self,map):
        for i in range(self.y_length):
            for g in range(self.x_length):
                if map[i][g]==0:
                    RANDOM=randint(1,sum(self.item_percentage))
                    last_v=0
                    for j in range(len(self.item_percentage)):
                        pt_v=sum(self.item_percentage[:j+1])
                        if last_v<RANDOM<=pt_v:
                            self.item_map[i][g]=j
                            if j==0:
                                self.all_item_count+=1
                            break


                        last_v=pt_v
        #print("all item",self.all_item_count)

    def draw(self):
        for i in range(self.y_length):
            for g in range(self.x_length):
                if self.item_map[i][g]!=-1:
                    RECT=self.item_img[self.item_map[i][g]].get_rect()
                    RECT.center=((2*g*self.tile_size+self.tile_size)/2,(2*i*self.tile_size+self.tile_size)/2)
                    SURFACE.blit(self.item_img[self.item_map[i][g]],RECT)


    def collect_item(self,Player_x,Player_y):
        global SCORE
        IDX_pos=self.idx_pos(Player_x,Player_y)
        if self.item_map[IDX_pos[1]][IDX_pos[0]]!=-1:
            A=self.item_map[IDX_pos[1]][IDX_pos[0]]
            self.item_map[IDX_pos[1]][IDX_pos[0]]=-1
            if A==0:
                SCORE+=1
                #print(SCORE)
                if self.all_item_count<=SCORE:
                    return 2
                return 0
            else:
                return 1
            #self.item_map[IDX_pos[1]][IDX_pos[0]]=-1
            #print("eat item")



    def idx_pos(self,x,y):
        return [int(x//self.tile_size),int(y//self.tile_size)]
    
    def real_pos(self,x,y):
        return [(2*x*self.tile_size+self.tile_size)/2,(2*y*self.tile_size+self.tile_size)/2]



class map(pygame.sprite.Sprite):
    global MAP
    def __init__(self,tile_size=50):
        pygame.sprite.Sprite.__init__(self)
        self.tile_size=tile_size
        self.y_length=size[1]//tile_size
        self.x_length=size[0]//tile_size
        self.img_x_size=50#self.img_rect.size[0]/10
        self.img_y_size=50#self.img_rect.size[1]/10
        self.dy=[-1,1,0,0]
        self.dx=[0,0,-1,1]
        self.root=[]
        self.max_number=(self.y_length+1)*(self.x_length+1)+2
        #print("max_number")
        #print(self.max_number)
        self.dp=[[inf for i in range(self.max_number+1)]for g in range(self.max_number+1)]
        #print("###",len(self.dp[0]),len(self.dp))
        self.path=[[-1 for i in range(self.max_number+1)]for g in range(self.max_number+1)]

        self.image_map=[[[0,0] for i in range(self.x_length+5)]for g in range(self.y_length+5)]

        self.tile_img=[pygame.image.load("pac_man_map_image/finish.png").convert_alpha(),
                       pygame.image.load("pac_man_map_image/wall_90.png").convert_alpha(),
                       pygame.image.load("pac_man_map_image/wall_180.png").convert_alpha(),
                       pygame.image.load("pac_man_map_image/wall_T.png").convert_alpha(),
                       pygame.image.load("pac_man_map_image/wall_+.png").convert_alpha(),
                       pygame.image.load("pac_man_map_image/wall_0.png").convert_alpha()]
        
        
        for i in range(len(self.tile_img)):
            self.tile_img[i]=pygame.transform.scale(self.tile_img[i],(self.img_x_size,self.img_y_size))




        #print("self length")
        #print(self.x_length,self.y_length)

    def dimensional_change(self,pos):
        return pos[1]*(self.x_length+1)+pos[0]+1
    
    def uploading_MapData(self,Map):

        #print("################")
        #print(*Map, sep=', \n')

        for i in range(self.y_length+1):
            for g in range(self.x_length+1):
                if Map[i][g]==0:
                    A=self.dimensional_change((g,i))
                    #print(A)
                    self.dp[A][A]=0
                    for j in range(4):
                        nx=g+self.dx[j]
                        ny=i+self.dy[j]
                        if nx<0 or nx>=self.x_length or ny<0 or ny>=self.y_length:
                            continue
                        if Map[ny][nx]==0:
                            B=self.dimensional_change((nx,ny))
                            self.dp[A][B]=1
                            self.dp[B][A]=1
                            self.dp[B][B]=0
        

        for i in range(self.y_length+5):
            for g in range(self.x_length+5):
                if Map[i][g]==1:
                    st=[0,0,0,0]
                    for j in range(4):
                        nx=g+self.dx[j]
                        ny=i+self.dy[j]
                        if nx<0 or nx>=self.x_length+5 or ny<0 or ny>=self.y_length+5:
                            continue
                        if Map[ny][nx]==1:
                            st[j]=1


                    SUM_st=sum(st)
                    if SUM_st==0:
                        self.image_map[i][g]=[5,0]
                    elif SUM_st==4:
                        self.image_map[i][g]=[4,0]
                    elif SUM_st==1:
                        if st[0]==1:self.image_map[i][g]=[0,0]
                        elif st[1]==1:self.image_map[i][g]=[0,2]
                        elif st[2]==1:self.image_map[i][g]=[0,3]
                        elif st[3]==1:self.image_map[i][g]=[0,1]
                    elif SUM_st==2:
                        if st[0]==1 and st[1]==1:self.image_map[i][g]=[2,0]
                        elif st[2]==1 and st[3]==1:self.image_map[i][g]=[2,1]
                        elif st[0]==1:
                            if st[2]==1:self.image_map[i][g]=[1,3]
                            elif st[3]==1:self.image_map[i][g]=[1,0]
                        elif st[1]==1:
                            if st[2]==1:self.image_map[i][g]=[1,2]
                            elif st[3]==1:self.image_map[i][g]=[1,1]
                    elif SUM_st==3:
                        if st[0]==0:self.image_map[i][g]=[3,1]
                        elif st[1]==0:self.image_map[i][g]=[3,3]
                        elif st[2]==0:self.image_map[i][g]=[3,0]
                        elif st[3]==0:self.image_map[i][g]=[3,2]

        #self.floyd_warshall_setting()
        #sys.exit()
        self.dp=dataset("dp")
        self.path=dataset("path")
        #print("VVVVVVVV",len(self.dp))       


    def floyd_warshall_setting(self):
        #print(f"floyd_warshall repeat : {self.max_number**3}")
        for i in range(1,self.max_number+1):
            for g in range(1,self.max_number+1):
                self.path[i][g]=i
        for j in range(1,self.max_number+1):
            mid_j=self.dimensional_change_up(j)
            if MAP[mid_j[1]][mid_j[0]]!=0:continue
            for i in range(1,self.max_number+1):
                mid_i=self.dimensional_change_up(i)
                if MAP[mid_i[1]][mid_i[0]]!=0:continue
                for g in range(1,self.max_number+1):
                    mid_g=self.dimensional_change_up(g)
                    #print(mid_g,g)
                    if MAP[mid_g[1]][mid_g[0]]!=0:continue
                    if self.dp[i][g]>self.dp[i][j]+self.dp[j][g] and self.dp[i][j]<inf and self.dp[j][g]<inf:
                        #if (i==326 and g==389) or (i==389 and g==326):
                            #print(i,j,g)
                            #print("@#@#@#@")
                            #print(self.dp[i][j],self.dp[j][g],self.dp[i][g])
                        self.dp[i][g]=self.dp[i][j]+self.dp[j][g]
                        self.path[i][g]=j
                    event = pygame.event.poll()
                    if event.type == pygame.QUIT:
                        #print("!!!!!!!!!!!!!!!")
                        break

            #print(j)
        print("dp")
        print(*self.dp, sep=', \n')
        print("path")
        print(*self.path, sep=', \n')
                    

    def dimensional_change_up(self,num):
        return ((num-1)%(self.x_length+1),(num-1)//(self.x_length+1))

    def find_path(self,A,B):
        prev=self.path[A][B]
        #print(A,B,prev)
        #print("pos")
        #print(f" A pos : {self.dimensional_change_up(A)}")
        #print(f" B pos : {self.dimensional_change_up(B)}")
        #print(len(self.dp[0]),len(self.dp))
        if self.dp[A][prev]>=inf or self.dp[prev][B]>=inf:
            return
        if prev==A:
            self.root.append(prev)
            return
        if prev==-1:return
        self.find_path(A,prev)
        self.find_path(prev,B)


    def shortest_path(self,start,end):
        self.root=[]
        #print("A->B number")
        #print("idx")
        #print(self.idx_pos(start),self.idx_pos(end))
        #print(self.dimensional_change(self.idx_pos(start)),self.dimensional_change(self.idx_pos(end)))
        self.find_path(self.dimensional_change(self.idx_pos(start)),self.dimensional_change(self.idx_pos(end)))
        for i in range(len(self.root)):
            self.root[i]=self.dimensional_change_up(self.root[i])

        #print(f"start : {start}, end : {end}")
        #print(self.root)

        return deque(self.root)







    def draw(self):

        for i in range(self.y_length+5):
                for g in range(self.x_length+5):
                    if MAP[i][g]!=0:
                        #pygame.draw.rect(SURFACE, color["yellow"], [g*self.tile_size,i*self.tile_size,self.tile_size,self.tile_size])
                        imsi_img=pygame.transform.rotate(self.tile_img[self.image_map[i][g][0]],-self.image_map[i][g][1]*90)
                        imsi_img_rect=imsi_img.get_rect()
                        imsi_img_rect.center=((2*g*self.tile_size+self.tile_size)/2,(2*i*self.tile_size+self.tile_size)/2)
                        SURFACE.blit(imsi_img,imsi_img_rect)

        """
        for i in range(self.y_length+5):
            if i*self.tile_size>=size[1]:
                break
            pygame.draw.line(SURFACE,color["white"],[0,i*self.tile_size],[size[0],i*self.tile_size],1)

        for i in range(self.x_length+5):
            if i*self.tile_size>=size[0]:
                break
            pygame.draw.line(SURFACE,color["white"],[i*self.tile_size,0],[i*self.tile_size,size[1]],1)
        """

    def mouse(self):
        POS=(pygame.mouse.get_pos()[0]//self.tile_size,pygame.mouse.get_pos()[1]//self.tile_size)
        MAP[POS[1]][POS[0]]=1

    def mouse_del(self):
        POS=(pygame.mouse.get_pos()[0]//self.tile_size,pygame.mouse.get_pos()[1]//self.tile_size)
        MAP[POS[1]][POS[0]]=0


    def idx_pos(self,pos):
        return [int(pos[0]//self.tile_size),int(pos[1]//self.tile_size)]
    
    def real_pos(self,pos):
        return [(2*pos[0]*self.tile_size+self.tile_size)/2,(2*pos[1]*self.tile_size+self.tile_size)/2]



class ghost(pygame.sprite.Sprite):
    global MAP
    def __init__(self,x_length,y_length,tile_size=50,ghost_img_idx=-1):
        pygame.sprite.Sprite.__init__(self)
        self.img_x_size=50#self.img_rect.size[0]/10
        self.img_y_size=50#self.img_rect.size[1]/10
        self.tile_size=tile_size
        if ghost_img_idx==-1:
            self.x=(2*x_length/2*self.tile_size+self.tile_size)/2-self.tile_size
            self.y=(2*y_length/2*self.tile_size+self.tile_size)/2+2*self.tile_size
        else:
            self.x=(2*x_length/2*self.tile_size+self.tile_size)/2
            self.y=(2*y_length/2*self.tile_size+self.tile_size)/2
        self.dy=[-1,1,0,0]
        self.dx=[0,0,-1,1]
        self.y_length=y_length
        self.x_length=x_length
        self.rotation=0
        self.ghost_img_name=["green","pink","red","yellow"]
        self.ghost_img_idx=ghost_img_idx

        self.v=1

        if ghost_img_idx==-1:
            self.last_attention=0
            self.player_item_mode=0
            self.nitem_img=[pygame.image.load("pac_man_image/pac_man_open.png").convert_alpha(),
                      pygame.image.load("pac_man_image/pac_man_close.png").convert_alpha()]
            self.nitem_img=[pygame.transform.scale(self.nitem_img[i],(self.img_x_size,self.img_y_size))for i in range(len(self.nitem_img))]
            self.yitem_img=[pygame.image.load("pac_man_image/pac_man_open_2.png").convert_alpha(),
                      pygame.image.load("pac_man_image/pac_man_close_2.png").convert_alpha()]
            self.yitem_img=[pygame.transform.scale(self.yitem_img[i],(self.img_x_size,self.img_y_size))for i in range(len(self.yitem_img))]
            
            self.img=[self.nitem_img[0],self.nitem_img[1]]
        else:
            self.img=[pygame.image.load(f"pac_man_ghost_image/{self.ghost_img_name[self.ghost_img_idx]}.png").convert_alpha()]
            self.img=[pygame.transform.scale(self.img[i],(self.img_x_size,self.img_y_size))for i in range(len(self.img))]
            self.move_stack=[]


        self.rect=self.img[0].get_rect()

        self.moving=[0,0,0,0,1] # up, down, left, right
        self.MOVE=[self.up,self.down,self.left,self.right]
        self.roatation_list=[3,1,2,0]
        self.change=0
        self.img_idx=0

        self.all_move=0


    def check(self,idx):

        X=self.x
        Y=self.y

        if idx==0:
            Y=self.y+(self.tile_size/2)-1
        elif idx==1:
            Y=self.y-(self.tile_size/2)
        if idx==2:
            X=self.x+(self.tile_size/2)-1
        elif idx==3:
            X=self.x-(self.tile_size/2)

        pos=self.idx_pos(X,Y)



        #pos=self.idx_pos(self.x,self.y)
        ny=pos[1]+self.dy[idx]
        nx=pos[0]+self.dx[idx]
        A=[nx,ny]
        B=self.real_pos(A[0],A[1])

        #if 0>A[1] or self.y_length+5<=A[1] or 0>A[0] or self.x_length<=A[0]:
        #    return 0,(B[0]-self.dx[idx],B[1]-self.dy[idx])
        
        #if 0>B[1] or size[1]<B[1] or 0>B[0] or size[0]<B[0]:
        #    return 0,(B[0]-self.dx[idx],B[1]-self.dy[idx])

        if MAP[A[1]][A[0]]!=0:
            #print(f"idx : {idx}.")
            return 0,(B[0]-self.dx[idx]*self.tile_size,B[1]-self.dy[idx]*self.tile_size)
        
        
        return 1,(-1,-1)
    

    def jump(self,attention=-1):
        if attention==-1:
            for i in range(4):
                    if self.moving[i]:
                        nx=self.x+self.dx[i]*self.tile_size*2  
                        ny=self.y+self.dy[i]*self.tile_size*2
                        pos=self.idx_pos(nx,ny)
                        if 0>pos[1] or pos[1]>=self.y_length or 0>pos[0] or pos[0]>=self.x_length:
                            return
                        if MAP[pos[1]][pos[0]]==0:
                            self.x=nx
                            self.y=ny
                            self.player_item_mode=0
                            self.img=[self.nitem_img[i]for i in range(len(self.nitem_img))]
                            self.rotation=self.roatation_list[attention]*90
                            self.moving=[0]*5
                            self.moving[attention]=1
                        return
                    
            nx=self.x+self.dx[self.last_attention]*self.tile_size*2  
            ny=self.y+self.dy[self.last_attention]*self.tile_size*2
        else:
            nx=self.x+self.dx[attention]*self.tile_size*2  
            ny=self.y+self.dy[attention]*self.tile_size*2

        pos=self.idx_pos(nx,ny)
        if 0>pos[1] or pos[1]>=self.y_length or 0>pos[0] or pos[0]>=self.x_length:
            return
        if MAP[pos[1]][pos[0]]==0:
            self.x=nx
            self.y=ny
            self.player_item_mode=0
            self.img=[self.nitem_img[i]for i in range(len(self.nitem_img))]
            self.rotation=self.roatation_list[attention]*90
            self.moving=[0]*5
            self.moving[attention]=1
        return


    def move(self,pt_idx,be_idx):
        #Ghost.moving=[0,0,0,0]
        OK=0
        #print("MOVE")
        #print(pt_idx,be_idx)

        
        if pt_idx==-1 and be_idx==-1:
            #print("moving list")
            #print(self.moving)
            for i in range(4):
                if self.moving[i]:
                    result,pos=self.check(i)
                    #print("check :",result,pos)
                    #print("RESULT,POS")
                    #print(result,pos)
                    if result:
                        self.MOVE[i](self.v)
                        self.all_move+=1
                        self.all_move%=(self.tile_size/self.v)
                        OK=1
                        #self.moving[i]=0
                    else:
                        #print("!!!!!!!!!!!!!!!!!!!!!!!",pos,(self.x,self.y))
                        self.x=pos[0]
                        self.y=pos[1]
                        self.all_move=0
                        #self.half_move(i)
                        self.last_attention=i
                        self.moving[i]=0
                        self.moving[4]=1
        else:
            
            result,pos=self.check(pt_idx)
            #print("RESULT,POS")
            #print(result,pos)
            #print("check :",result,pos)
            if result:
                #print("Before pos")
                #print(self.x,self.y)
                self.MOVE[pt_idx]()
                #print("after pos")
                #print(self.x,self.y)
                self.all_move+=1
                self.all_move%=self.tile_size
                self.moving[be_idx]=0
                self.moving[pt_idx]=1
                #print("MOVING")
                #print(self.moving)
                OK=1

                self.rotation=self.roatation_list[pt_idx]*90

        return OK

                
        #print("ghost pos:",self.x,self.y)
        #print("tile pos:",self.x//self.tile_size,self.y//self.tile_size)

    def idx_pos(self,x,y):
        return [int(x//self.tile_size),int(y//self.tile_size)]
    
    def real_pos(self,x,y):
        return [(2*x*self.tile_size+self.tile_size)/2,(2*y*self.tile_size+self.tile_size)/2]


    def left(self,r=1):
        self.x-=r
    def right(self,r=1):
        self.x+=r
    def up(self,r=1):
        self.y-=r
    def down(self,r=1):
        self.y+=r

    def draw(self):
        imsi_img=pygame.transform.rotate(self.img[self.img_idx],-self.rotation)
        imsi_img_rect=imsi_img.get_rect()
        imsi_img_rect.center=(self.x,self.y)
        SURFACE.blit(imsi_img,imsi_img_rect)#(self.rect.centerx,self.rect.centerx))
        self.change+=1
        if self.change%50==0:
            self.img_idx+=1
            self.img_idx%=len(self.img)
            self.change=0


    def end_point_check(self,X,Y,rotate,distance):
        idx=0
        if rotate==0:idx=3
        elif rotate==90:idx=1
        elif rotate==180:idx=2
        elif rotate==270:idx=0

        nx=X+self.dx[idx]*distance
        ny=Y+self.dy[idx]*distance
        #print(X,Y,nx,ny)

        if nx<0 or nx>=self.x_length or ny < 0 or ny>= self.y_length:
            return 0,(-1,-1)
        
        if MAP[ny][nx]!=0:
            return 0,(-1,-1)
        
        #print(tuple(self.real_pos(nx,ny)))
        
        return 1,tuple(self.real_pos(nx,ny))
    
    def green_end_point_check(self,X,Y,rotate,distance_x,distance_y):
        idx=0
        if rotate==0:idx=3
        elif rotate==90:idx=1
        elif rotate==180:idx=2
        elif rotate==270:idx=0

        nx=X+self.dx[idx]*distance_x
        ny=Y+self.dy[idx]*distance_y
        #print(X,Y,nx,ny)

        if nx<0 or nx>=self.x_length or ny < 0 or ny>= self.y_length:
            return 0,(-1,-1)
        
        if MAP[ny][nx]!=0:
            return 0,(-1,-1)
        
        #print(tuple(self.real_pos(nx,ny)))
        
        return 1,tuple(self.real_pos(nx,ny))
        
        
def PAC_MAN():
    global MAP,SCORE

    start_time=time.time()

    tile_size=50
    Map=map(tile_size)
    #MAP=[[0 for g in range(Map.x_length+5)]for i in range(Map.y_length+5)]
    MAP=dataset("map")

    Map.uploading_MapData(MAP)

    Player=ghost(Map.x_length,Map.y_length,tile_size)

    Ghosts=[[ghost(Map.x_length,Map.y_length,tile_size,ghost_img_idx=i),randint(1,13),0,deque([])] for i in range(4)]

    item=Item(tile_size)
    item.produce_item(MAP)
    developer=1

    SCORE=0




    while 1:
        #print("while start")
        SURFACE.fill(color["black"])
        key=0

        event = pygame.event.poll()
        if event.type == pygame.QUIT:return 1
        keys = pygame.key.get_pressed()
        ok_check=0
        if Player.all_move==0:
            #print("###@@@###")
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                #print(f"w idx : {Player.moving.index(1)}.")
                ok_check=max(ok_check,Player.move(0,Player.moving.index(1)))
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                #print(f"s idx : {Player.moving.index(1)}.")
                ok_check=max(ok_check,Player.move(1,Player.moving.index(1)))
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                #print(f"d idx : {Player.moving.index(1)}.")
                ok_check=max(ok_check,Player.move(3,Player.moving.index(1)))
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                #print(f"a idx : {Player.moving.index(1)}.")
                ok_check=max(ok_check,Player.move(2,Player.moving.index(1)))
            if Player.player_item_mode==1:
                if keys[pygame.K_SPACE]:
                    if keys[pygame.K_w] or keys[pygame.K_UP]:
                        Player.jump(0)
                    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                        Player.jump(1)
                    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        Player.jump(3)
                    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        Player.jump(2)
                    else:
                        Player.jump()

        if ok_check==0:
            #print("!!!@@@@@!!!")
            Player.move(-1,-1)


        for i in range(len(Ghosts)):
            #print("real pos")
            #print(Ghosts[i][0].x,Ghosts[i][0].y)
            POS=Ghosts[i][0].idx_pos(Ghosts[i][0].x,Ghosts[i][0].y)
            ok_check=0
            if Ghosts[i][0].all_move==0:
                if len(Ghosts[i][3])==0:
                    START_pos=(Ghosts[i][0].x,Ghosts[i][0].y)
                    END_pos=(0,0)
                    if Ghosts[i][0].ghost_img_name[Ghosts[i][0].ghost_img_idx]=="red":
                        END_pos=(Player.x,Player.y)
                    elif Ghosts[i][0].ghost_img_name[Ghosts[i][0].ghost_img_idx]=="pink":
                        Idx_pos=Player.idx_pos(Player.x,Player.y)
                        CHECK=Ghosts[i][0].end_point_check(Idx_pos[0],Idx_pos[1],Player.rotation,4)
                        if CHECK[0]:
                            END_pos=CHECK[1]
                        else:
                            END_pos=(Player.x,Player.y)

                    elif Ghosts[i][0].ghost_img_name[Ghosts[i][0].ghost_img_idx]=="yellow":
                        Idx_pos=Player.idx_pos(Player.x,Player.y)
                        CHECK=Ghosts[i][0].end_point_check(Idx_pos[0],Idx_pos[1],Player.rotation,randint(3,7))
                        if CHECK[0]:
                            END_pos=CHECK[1]
                        else:
                            END_pos=(Player.x,Player.y)

                    elif Ghosts[i][0].ghost_img_name[Ghosts[i][0].ghost_img_idx]=="green":
                        Idx_pos=Player.idx_pos(Player.x,Player.y)
                        CHECK=Ghosts[i][0].green_end_point_check(Idx_pos[0],Idx_pos[1],Player.rotation,randint(-5,5),randint(-5,5))
                        if CHECK[0]:
                            END_pos=CHECK[1]
                        else:
                            END_pos=(Player.x,Player.y)
                    #print(POS)
                    Ghosts[i][3]=Map.shortest_path(START_pos,END_pos)
                    LAST=Player.idx_pos(END_pos[0],END_pos[1])
                    Ghosts[i][3].append((LAST[0],LAST[1]))
                    #sys.exit()
                    #print(f"test : {Map.shortest_path((Ghosts[i][0].x,Ghosts[i][0].y),(Ghosts[i][0].x+Ghosts[i][0].tile_size,Ghosts[i][0].y))}")
                else:
                    #print("1!!!!!!!!!!!!!!!!1")s
                    Ghosts[i][3].popleft()
        

                if len(Ghosts[i][3])!=0:
                    while len(Ghosts[i][3])>0:
                        #print("@!!!!!@22222")
                        #print(Ghosts[i][3][0],POS)
                        if Ghosts[i][3][0][0]==POS[0] and Ghosts[i][3][0][1]==POS[1]:
                            #print("1!!!!!!!!!!!!!!!!2222")
                            Ghosts[i][3].popleft()
                        else:break
                    #print("##",Ghosts[i][3])
                    if len(Ghosts[i][3])>0:
                        Next=Ghosts[i][3][0]


                        V=0
                        #print(" select V")
                        #print(POS,Next)
                        if POS[0]<Next[0]:V=3
                        elif POS[0]>Next[0]:V=2
                        elif POS[1]<Next[1]:V=1
                        elif POS[1]>Next[1]:V=0
                        #print("NEXT1")
                        #print(Next,V)
                        Ghosts[i][0].move(V,Ghosts[i][0].moving.index(1))
        
                    ok_check=1

            if ok_check==0:
                #print("NO KEY")
                #print("##",i)
                if len(Ghosts[i][3])>0:

                    Ghosts[i][0].move(-1,-1)#(V,Ghosts[i][0].moving.index(1))



        for i in range(len(Ghosts)):
            #Ghost
            imsi_img=pygame.transform.rotate(Ghosts[i][0].img[0],-Ghosts[i][0].rotation)
            imsi_img_rect=imsi_img.get_rect()
            imsi_img_rect.center=(Ghosts[i][0].x,Ghosts[i][0].y)
            Ghosts[i][0].rect=imsi_img_rect
            Ghosts[i][0].mask=pygame.mask.from_surface(imsi_img)

            #Player
            imsi_img=pygame.transform.rotate(Player.img[Player.img_idx],-Player.rotation)
            imsi_img_rect=imsi_img.get_rect()
            imsi_img_rect.center=(Player.x,Player.y)
            Player.rect=imsi_img_rect
            Player.mask=pygame.mask.from_surface(imsi_img)

            if pygame.sprite.collide_mask(Ghosts[i][0], Player):
                print(f"Crash {Player.ghost_img_name[i]} ghost.")
                myFont = pygame.font.Font( None, 300)
                retry_font = pygame.font.Font( None, 100)
                score_font = pygame.font.Font( None, 100)
                text_Title= myFont.render("Game Over", True, color["white"])
                text_rect=text_Title.get_rect()
                text_rect.center=(size[0]/2,(size[1]+100)/2)
                for score in range(SCORE+100,SCORE-1,-1):
                    SURFACE.fill(color["black"])
                    event = pygame.event.poll()
                    if event.type == pygame.QUIT:return
                    score_text= score_font.render(f"Your score is {score}", True, color["white"])
                    score_rect=score_text.get_rect()
                    score_rect.center=(size[0]/2,(size[1]+50)/2+200)
                    SURFACE.blit(score_text, score_rect)
                    SURFACE.blit(text_Title, text_rect)
                    FPSCLOCK.tick(200)
                    pygame.display.update()

                score_text= score_font.render(f"Your score is {SCORE}", True, color["white"])
                retry= retry_font.render("Do you want retry? Presh ESC key", True, color["red"])

                retry_rect=retry.get_rect()
                retry_rect.center=(size[0]/2,(size[1]+50)/2+330)
                score_rect=score_text.get_rect()
                score_rect.center=(size[0]/2,(size[1]+50)/2+200)

                while 1:
                    SURFACE.fill(color["black"])
                    event = pygame.event.poll()
                    if event.type == pygame.QUIT:return 1

                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        #print("ASD")
                        return 0
                
                    SURFACE.blit(text_Title, text_rect)
                    SURFACE.blit(retry, retry_rect)
                    SURFACE.blit(score_text, score_rect)
                    pygame.display.update()




        if developer:
            if pygame.mouse.get_pressed()[0]==1:
                Map.mouse()
                Map.uploading_MapData(MAP)
            if pygame.mouse.get_pressed()[2]==1:
                Map.mouse_del()

            if keys[pygame.K_0]:
                print("################")
                print(*MAP, sep=', \n')
        Map.draw()
        item.draw()
        player_interaction=item.collect_item(Player.x,Player.y)
        if player_interaction==1:
            Player.player_item_mode=1
            Player.img=[Player.yitem_img[i]for i in range(len(Player.yitem_img))]
        elif player_interaction==2:
            finish_time=time.time()
            print("Game finish")
            myFont = pygame.font.Font( None, 300)
            retry_font = pygame.font.Font( None, 100)
            score_font = pygame.font.Font( None, 100)


            score_text=score_font.render(f"Your record is {datetime.timedelta(seconds=finish_time-start_time)}", True, color["white"])
            retry= retry_font.render("Do you want retry? Presh ESC key", True, color["red"])

            retry_rect=retry.get_rect()
            retry_rect.center=(size[0]/2,(size[1]+100)/2+130)
            score_rect=score_text.get_rect()
            score_rect.center=(size[0]/2,(size[1]+100)/2)

            while 1:
                SURFACE.fill(color["black"])
                event = pygame.event.poll()
                if event.type == pygame.QUIT:return 1

                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    print("ASD")
                    return 0
            
                SURFACE.blit(retry, retry_rect)
                SURFACE.blit(score_text, score_rect)
                pygame.display.update()

        Player.draw()
        for i in range(len(Ghosts)):
            Ghosts[i][0].draw()

        
        myFont = pygame.font.Font( None, 60)
        text_Title= myFont.render(f"Score : {SCORE}", True, color["white"])

        text_rect=text_Title.get_rect()
        text_rect.centery=825
        text_rect.x=10
        SURFACE.blit(text_Title, text_rect)

        


        #FPSCLOCK.tick(200)

        pygame.display.update()


while 1:
    turn_off=PAC_MAN()
    if turn_off==1:break
    event = pygame.event.poll()
    if event.type == pygame.QUIT:break