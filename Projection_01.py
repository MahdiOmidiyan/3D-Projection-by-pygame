

from math import *
import pygame, random, sys

window = pygame.display.set_mode((700,700))
window.fill((0,0,0))
pygame.display.set_caption("projection")
center = [350, 350]
expansion_factor = 4

colors = [( random.randint(1,255) ,random.randint(1,255) ,random.randint(1,255) ) for i in range(12)]
cc = 0
# defining variable axis x , y, z based on fix axis xx, yy, zz
x = [1, 0, 0]
y = [0, 1, 0]
z = [0, 0, 1]

coordinate = [x,y,z]

def rotate(delta,axis): # delta in degrees , axis of rev : 1--> x , 2-->y , 3-->z
    arg1 = axis % 3
    arg2 = (axis + 1) % 3
    
    for i in coordinate:     # rotating every x , y , z vectors around xx or yy or zz
        r = sqrt( pow(i[arg1],2) + pow(i[arg2],2) )
        theta = (pi /2) if i[arg1] == 0 else atan(i[arg2] /i[arg1])

        if (theta == (pi / 2)) and (i[arg2] < 0) : theta = - pi / 2
        
            
        theta += pi if i[arg1] < 0 else 0
        
        theta += delta * pi / 180 

        i[arg1] = r * cos(theta)
        i[arg2] = r * sin(theta)
        

def translate(dot): #converting from x,y,z cordinate to xx,yy,zz cordinate plus expansion and offset
    xx = dot[0] * x[0] + dot[1] * y[0] + dot[2] * z[0]

    yy = dot[0] * x[1] + dot[1] * y[1] + dot[2] * z[1]

    new_point = list(map(lambda x,offset: (x * expansion_factor)+ offset ,[xx,yy] ,center ))
    
    return new_point


def drawline(dots):
    tr_dot1 = translate(dots[0])
    tr_dot2 = translate(dots[1])
    global cc
    color = colors[cc % 12]
    cc += 1
    pygame.draw.line(window,color,tr_dot1,tr_dot2,3)

def drawpoly(points):
    corresponding = [1,2,-2,-1]
    
    for i in range(len(points)):
        #j = ( i + 1 ) % len(points)
        j = corresponding[i] + i
        drawline([points[i],points[j]])
        
 
def drawcube(point): # point is one of eight cube vertices
    edge = 20 # size of cube edge
    vertices = []
    
    for i in range(8): #0 to 8 in base 2 --> dr 
        dx = i%2 * edge
        dy = i//2 %2 * edge
        dz = i//4 %2 * edge
        dr = [dx,dy,dz]
        
        vertix = list(map( lambda x,y: x+y, point, dr ))
        vertices.append(vertix)

    drawpoly(vertices[:4])
    drawpoly(vertices[4:])
    for i in range(4):
        drawline( [ vertices[i + j * 4] for j in [0,1] ] ) # draw line between vertices (0 , 4) & (1 , 5) & ... 
        
    #print(vertices)
        

def drawguide():
     a0 = translate([-50, -50, 0])
     a1 = translate([-30, -50, 0])
     a2 = translate([-50, -70, 0])
     a3 = translate([-50, -50, 20])
     
     a1 = list(map( lambda x,y : (x - y)/expansion_factor * 3 + 70, a1, a0 )) # to translate the guide to the right up corner and with constant scale

     a2 = list(map( lambda x,y : (x - y)/expansion_factor * 3 + 70, a2, a0 ))

     a3 = list(map( lambda x,y : (x - y)/expansion_factor * 3 + 70, a3, a0 ))

     a0 = list(map( lambda x,y : (x - y)/expansion_factor * 3 + 70, a0, a0 )) # or a0 = [70,70]

     pygame.draw.line(window,(255,0,0),a0,a1,3)
     pygame.draw.line(window,(0,255,0),a0,a2,3)
     pygame.draw.line(window,(0,0,255),a0,a3,3)
 
     
    
dot1 = [00 , 00 , 0]

def refresh():
    #print(coordinate)
    window.fill((0,0,0))
    drawguide()
    drawcube(dot1)

refresh()
move = False
move_count = 0

while True:
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP:
                rotate(5,1)
                
                
            if event.key == pygame.K_DOWN:
                rotate(-5,1)

            if event.key == pygame.K_LEFT:
                rotate(-5,2)

            if event.key == pygame.K_RIGHT:
                rotate(5,2)

            refresh()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                expansion_factor += 0.3
            elif event.button == 5:
                expansion_factor -= 0.3
            elif event.button == 1:
                move = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                move = False
                move_count = 0
        if event.type == pygame.MOUSEMOTION:
            if move:
                ds = pygame.mouse.get_rel()
                move_count += 1
                
            if move_count > 2 :
                center = [ds[i] + center[i] for i in range(len(center))]
                
               
                
        refresh()
    
