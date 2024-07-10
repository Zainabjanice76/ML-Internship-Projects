import pygame
import sys
from pygame.locals import *
import numpy as np 
from keras.models import load_model
import cv2

WINDOWSIZEX = 600
WINDOWSIZEY = 400

# Initialiser pygame
pygame.init()

BOUNDRYINC= 5
ALMOND=(240,220,202)
BLACK = (0,0,0)
LIVER = (115, 87, 81)
FONT= pygame.font.Font("FreeSansBold.ttf", 18)

IMAGESAVE = False

MODEL = load_model("handwrittendigit.h5")

LABELS = {0:"Zero", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine"}

pygame.display.set_caption("Digit Board")

# Window setting
screen = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))

# Set pen color
pen_color = (240, 220, 202)  # Almond color
pen_radius = 4.5

#Variabl to control the drawing
drawing = False


iswriting=False
number_xcord=[]
number_ycord=[]
image_cnt=1
PREDICT=True

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            drawing = True
        elif event.type == MOUSEBUTTONUP:
            drawing = False
        elif event.type == MOUSEMOTION and drawing:
            mouse_x, mouse_y = event.pos
            pygame.draw.circle(screen, pen_color, (mouse_x, mouse_y), pen_radius)
        if event.type ==  MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(screen, ALMOND, (xcord, ycord), 4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)
            
            
        if event.type == MOUSEBUTTONDOWN:
            iswriting=True    
            
            
            
        if event.type == MOUSEBUTTONUP:
            iswriting=False
            number_xcord=sorted(number_xcord)
            number_ycord=sorted(number_ycord)
            
            rect_min_x , rect_max_x = max(number_xcord[0]-BOUNDRYINC,0 ), min(WINDOWSIZEX, number_xcord[-1]+BOUNDRYINC)
            rect_min_y , rect_max_y = max(number_ycord[0]-BOUNDRYINC,0 ), min(WINDOWSIZEY, number_ycord[-1]+BOUNDRYINC, WINDOWSIZEX)

            number_xcord = []
            number_ycord = []
            
            img_array=np.array(pygame.PixelArray(screen))[rect_min_x:rect_max_x, rect_min_y:rect_max_y].T.astype(np.float32)
            
            if IMAGESAVE:
                cv2.imwrite("image.png")
                image_cnt +=1
            
            if PREDICT:
                image= cv2.resize(img_array,(28,28))    
                image = np.pad(image, (10,10), 'constant', constant_values=0)
                image = cv2.resize(image, (28,28))/255
                label=str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])
                
                textSurface =FONT.render(label, True, LIVER, ALMOND)
                textRecObj= textSurface.get_rect()
                textRecObj.left , textRecObj.bottom = rect_min_x , rect_max_y 
                
                screen.blit(textSurface, textRecObj)
                
            if event.type == KEYDOWN:
                    if event.unicode =="n":
                        screen.fill(BLACK)
    pygame.display.update()
