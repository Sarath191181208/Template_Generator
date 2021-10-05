import os
import pygame
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from components.colors import *
from components.component import Button, Component
from components.scrollbar import ScrollBar

pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 440, 600
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('must add a caption')
FPS = 60

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

def grab(win, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    sub = win.subsurface(rect)
    surfce = pygame.Surface((width, height))
    surfce.blit(sub, (0,0))
    # return surfce
    return surfce

class MainWindow():
    def __init__(self, win, x=0, y =0) -> None:
        self.x, self.y = x, y 
        self.win = win
        self.y_offset = 20
        self.width, self.height = 420, 500

        self.surface = pygame.Surface((self.width, 2000))

        self.children = []
        self.draw()
    
    def draw(self):
        self.surface.fill(WHITE)
        for idx, child in enumerate(self.children):
            child.y = (idx*(50+10))
            child.idx = idx+1
            if self.y_offset < child.y+child.height < self.height+self.y_offset:
                child.draw()
    
    def update(self):
        self.surface.fill(WHITE)
        x, y = pygame.mouse.get_pos()
        y += max(0,self.y_offset) - 20
        for child in self.children:
            if self.y_offset < child.y+child.height < self.height+self.y_offset:
                child.update(pos=(x, y))
        blit_surface = grab(win=self.surface, x=0, y=max(0,min(self.y_offset,2000-self.width)), width=self.width, height=self.height)
        self.win.blit(blit_surface, (0, 20))
        pygame.draw.line(self.win,BLACK, (10,10), (10,self.height))
        pygame.draw.line(self.win,BLACK, (10,10), (self.width,10))
        pygame.draw.line(self.win,BLACK, (10,self.height), (self.width,self.height))
        pygame.draw.line(self.win,BLACK, (self.width,10), (self.width,self.height))
    
    def insert(self):
        window = Tk()
        window.withdraw()
        path =  askopenfilename(title="Open File", filetypes=[("BoilerPlate files","*.bt")])
        if path == '' or path is None:
            return
            
        self.children.append(Component(self.surface,y=len(self.children*(50+10)) ,delete_func= lambda idx :self.delete(idx)))
        self.children[-1].txt = os.path.split(path)[1].split('.')[0]
        self.children[-1].path = path
        self.draw()
    
    def delete(self, idx):
        self.children.pop(idx)
        time.sleep(0.1)
        self.draw()

main_win = MainWindow(win=WIN)
scroll_bar = ScrollBar(win=WIN, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT, min_=1, max_=1450)
add_btn = pygame.image.load(os.path.join('assets','add_button.png'))
add_btn = Button(win=WIN, x=200, y=540, width=40, height=40, text=add_btn,func=lambda:main_win.insert())


run = True
while run:
    clock.tick(FPS)
    WIN.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    main_win.y_offset = scroll_bar.get_val()-40
    # print(scroll_bar.get_val()-50)

    add_btn.update(pygame.mouse.get_pos())
    scroll_bar.update()
    main_win.update()

    pygame.display.update()
pygame.quit()