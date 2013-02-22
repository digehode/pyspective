#!/usr/bin/python
import sys, pygame
from pygame.locals import *
import math
from math import sin, cos
from euclid import Vector2
#from random import uniform
import random
uniform=random.uniform
#random.seed(100)
white=(255,255,255)
black=(0,0,0)

background=black
fg=white

#TODO: Polygons instead of circles?

subpix=3 #Number of subpixels per "real" pixel

width,height=size=(800,600)

screenPos=0.5 #Half way across
eyePos=0.0 #left hand side
nPixels=15 #How many pixels in the screen
pixelWidth=10


#World full of circles (x,y,r,col)
objects=[(100,100,10,(255,55,255))]
nPixels=1.0*nPixels #Saves rounding errors later
for i in range(int(nPixels)):
    r=uniform(5,height/nPixels)
    y=uniform(i*height/nPixels,(i+1)*height/nPixels)
    objects.append((uniform(r+pixelWidth,width*screenPos),y,r,(uniform(0,255),uniform(0,255),uniform(0,255))))

#Sort objects by x (equivalent of z ordering in 3D) Subtract radius so
#larger circles do show in front of smaller ones that are closer to
#the screen, but withinthe radius of the larger one.  This makes
#sense, I promise.
objects.sort(lambda x,y: int((x[0]-x[2])-(y[0]-y[2])))

pygame.init()
ticker=pygame.time.Clock()
screen = pygame.display.set_mode(size)

def coladd(p1,p2):
    #TODO: Just return this.  Was for debugging
    o=[p1[x]+p2[x] for x in range(3)]
    #print "!\t\t",p1,p2,o
    return o

def coldiv(p, d):
    return [p[x]/d for x in range(3)]

#Returns true if line and circle intersect
def intersect(c, #Center of circle
              r, #Radius
              p1,#Point 1 of line             
              p2 #point 2 of line
              ):
    c=Vector2(c[0],c[1])
    p1=Vector2(p1[0],p1[1])
    p2=Vector2(p2[0],p2[1])
    d=p2-p1
    f=p2-c
    a=d.dot(d)
    b=2*f.dot(d)
    c=f.dot(f)-r*r
    discriminant = b*b-4*a*c
    if discriminant<0: return False
    return True


mStep=0.01

while 1:
    screen.fill(background)
    #Events.  Move eye, screen, check for close
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type is KEYDOWN:

            if event.key==pygame.K_RIGHT: 
                screenPos+=mStep
                if screenPos > 0.5:
                    screenPos-=mStep

            if event.key==pygame.K_LEFT: 
                screenPos-=mStep
                if screenPos <= eyePos:
                    screenPos+=mStep
            if event.key==pygame.K_PAGEUP:
                nPixels+=5
            if event.key==pygame.K_PAGEDOWN:
                nPixels-=5
                if nPixels<=2:
                    nPixels=2




    #draw eye
    pygame.draw.circle(screen,fg,(int(width*eyePos),int(height/2)),10,1)
    pygame.draw.circle(screen,(0,0,255),(int(width*eyePos),int(height/2)),5)


    #draw screen/pixels and rays
    #screen
    pygame.draw.line(screen,fg,(width*screenPos-1,0),(width*screenPos-1,height))
    pygame.draw.line(screen,fg,(width*screenPos+pixelWidth,0),(width*screenPos+pixelWidth,height))
    #Draw world objects
    for i in objects:
        pygame.draw.circle(screen, i[3],(int(i[0]+width/2),int(i[1])),int(i[2]))

    for i in range(int(nPixels)):

        #pygame.draw.rect(screen,black,(x,y,pixelWidth,m),1)
        col=(0,0,0) #accumulator
        hitcount=0
        m=height/(1.0*nPixels*subpix) #multiplier
        x=width*screenPos
        #Eye position...
        x0=width*eyePos
        y0=height/2.0

        for k in range(subpix):

            y=(i*subpix+k)*m

            #Now find CENTRE of sub pixel
            yc=y+height/(nPixels*subpix)/2.0


            #Gradient
            g=(yc-y0)/(x-x0)
            #Ray end point
            x2=width*1.0
            y2=y0+width*g



            #If collision, add to col accumulator

            for j in objects:
                if intersect((j[0]+width/2,j[1]),j[2],(x0,y0),(x2,y2)):

                    col=coladd(col,j[3])
                
                    #For debugging, show collisions
                    pygame.draw.circle(screen, (255,0,0),(int(j[0]+width/2),int(j[1])),int(j[2]/4.0))
                    pygame.draw.aaline(screen,j[3],(x0,y0),(x2,y2))
                    break
            else:
                col=coladd(col,background)
                #TODO: use a background colour var  and do this properly
        col=coldiv(col,float(subpix))
        
        #calc actual pixel size
        m=height/(1.0*nPixels) #multiplier
        x=width*screenPos
        y=(i)*m

        yc=y+height/(nPixels)/2.0

        #Gradient
        g=(yc-y0)/(x-x0)
        #Ray end point
        x2=width*1.0
        y2=y0+width*g

        pygame.draw.aaline(screen,coldiv(coladd(col,background),2),(x0,y0),(x2,y2))
        #pygame.draw.aaline(screen,col,(x0,y0),(x2,y2+1))
        #pygame.draw.aaline(screen,col,(x0,y0),(x2,y2-1))


        #print "\t\t",col
        pygame.draw.rect(screen,col,(x,y,pixelWidth+1,m+1))



    
    ticker.tick(30)
    pygame.display.flip()    

    print "FPS: %d"%(ticker.get_fps())
