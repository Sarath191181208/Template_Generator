import os
import pygame
from colorama import Fore, Style
from tkinter import Tk 
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
# from components.editor import text_editor

from components.main import load_template

def PYtxt(txt: str, fontSize: int = 28, font: str = pygame.font.match_font('arial', bold=False, italic=False), fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(str(txt), True, fontColour)

def load_btn_imgs():
    try:
        edit_img = pygame.image.load(os.path.join('assets','edit.png'))
        play_img = pygame.image.load(os.path.join('assets','run.png'))
        remove_img = pygame.image.load(os.path.join('assets','cancel.png'))

    except:
        print(Fore.RED,'Failed to load images !',Style.RESET_ALL)
        edit_img = 'Brush'
        play_img = 'Start'
        remove_img = 'Delete'
    
    return edit_img, play_img, remove_img

class Component():
    def __init__(self, x=25, y=0, delete_func=None) -> None:
        self.x, self.y = x, y
        self.width, self.height = 380, 50
        self.path = ''

        y_btn = self.height/2-10+self.y
        x_btn = 260
        edit_img, run_img, remove_img = load_btn_imgs()
        self.edit_btn = Button(x=x_btn, y=y_btn, text=edit_img, func= lambda: self.edit())
        self.run_btn = Button(x=x_btn+52.5, y=y_btn, text=run_img, func= lambda: self.run())
        self.trash_btn = Button(x=x_btn+100, y=y_btn, text=remove_img, func= lambda : delete_func(self.idx-1))

        self.buttons = []
        self.buttons.append(self.edit_btn)
        self.buttons.append(self.run_btn)
        self.buttons.append( self.trash_btn)

        self.idx = 1
        self.txt = 'component'

    
    def draw(self, win):
        # border line
        BLACK = (60,60,60)
        pygame.draw.rect(win, BLACK, (self.x,self.y,self.width,self.height),1)
        if len(self.txt) > 22:
            self.txt = self.txt[:21]
            self.txt += "..."
        txt = PYtxt(self.txt,15)
        # 168
        win.blit(txt, (168-txt.get_width()/2,self.y+25-txt.get_height()/2))
        # idx, text seperator line
        pygame.draw.line(win, BLACK, (self.x+60,self.y),(self.x+60, self.y+self.height-1))
        # index text
        txt = PYtxt(str(self.idx), 18)
        win.blit(txt, (self.x+30-txt.get_width()/2,self.y+25-txt.get_height()/2))

    def update(self, pos, win):
        self.draw(win)
        for btn in self.buttons:
            btn.y = self.height/2-10+self.y
            btn.update(pos, win)
    
    def run(self):
        root = Tk()
        root.withdraw()
        des_path = askdirectory()
        if des_path == "" or des_path is None:
            return
        # des_path = ""
    
        if self.path is None or self.path == '' :
            return
        if not os.path.exists(self.path):
            print(Fore.RED, 'Invalid path',Style.RESET_ALL)
        temp = os.path.split(self.path)[1]
        temp = temp.split('.')[1]

        if temp != 'bt':
            print(Fore.RED, "Invalid extension", Style.RESET_ALL)
        # choose location to dump template
        load_template(self.path, des_path)
        messagebox.showinfo("Info", "Done")
    
    def edit(self):
        if self.path is None or self.path == '':
            return
        if not os.path.exists(self.path):
            return
        window = Tk()
        window.withdraw()
        path =  askopenfilename(title="Open File", filetypes=[("BoilerPlate files","*.bt")])
        if path == '' or path is None:
            return
        self.path = path
        self.txt = os.path.split(path)[1].split('.')[0]

class Button():
    def __init__(self, x:int = 0, y:int = 0, width:int = 20, height:int = 20, text='',color = (255,255,255), func=None):

        self.color = color
        self.y_offset = 0
        self.x, self.y = x, y
        self.width, self.height = width, height

        self.text = text
        if self.text == '':
            self.text = 'Button'
        if type(self.text) != pygame.Surface:
            self.text = PYtxt(str(self.text))

        self.clicked = False
        self.func = func

    def draw(self, win):
        win.blit(self.text, (self.x + (self.width/2 - self.text.get_width()/2), self.y + (self.height/2 - self.text.get_height()/2)))


    def is_hovering(self,pos) -> bool:
        x, y = pos 
        #Pos is the mouse position or a tuple of (x,y) coordinates
        return (
            x > self.x
            and x < self.x + self.width
            and y > self.y 
            and y < self.y + self.height 
        )
    def update(self,pos, win):
        if self.is_hovering(pos):
            if pygame.mouse.get_pressed()[0]:
                # only to register click once
                if self.clicked == False and self.func is not None:
                    self.func()

                self.clicked = True
            else:
                self.clicked = False
            # self.draw(1)
            self.draw(win)
        else:
            self.draw(win)
            self.clicked = False

def main():
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((420, 600))
    pygame.display.set_caption('')
    FPS = 60

    cmp = Component(win=WIN)
    cmp2 = Component(win=WIN,x=20, y=100)
    cmp2.idx = 11
    
    run = True
    WHITE = (255,255,255)
    while run:
        WIN.fill(WHITE)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        cmp.update()
        cmp2.update()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()