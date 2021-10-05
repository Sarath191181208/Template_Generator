import pygame


class ScrollBar():
    def __init__(self, win,SCREEN_WIDTH, SCREEN_HEIGHT, min_=1, max_=100,) -> None:
        self.win = win
        self.min, self.max = min(min_,max_), max(min_,max_)

        width, height = 20, 50
        self.x, self.y = SCREEN_WIDTH - width, 5

        self.MAX_HEIGHT = SCREEN_HEIGHT-height
        self.rect = pygame.Rect(self.x, self.y, width, height)


        self.clicked = False
    
    def draw(self):
        GREAY = pygame.Color('#868686')
        pygame.draw.rect(self.win, GREAY, self.rect)
    
    def update(self):
        if pygame.mouse.get_pressed()[0] :
            pos = pygame.mouse.get_pos()
            if self.clicked or self.rect.collidepoint(pos):
                self.clicked = True
                y = pos[1] - self.rect.width
                if y > 5 and y < self.MAX_HEIGHT:
                    self.y = y
                    self.rect = pygame.Rect(self.x, self.y, self.rect.width, self.rect.height)
        else:
            self.clicked = False
        
        self.draw()

    def get_val(self):
        stp = (self.y) / self.MAX_HEIGHT
        return step(self.max * stp)

def step(num):
    if num-int(num) > 0.5:
        return int(num)+1
    else:
        return int(num)



def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

def main():

    SCREEN_WIDTH, SCREEN_HEIGHT = 540, 600
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((540, 600))
    pygame.display.set_caption('')
    FPS = 60

    scrollbar = ScrollBar(WIN, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT, min_=1, max_=100)
    WHITE = (255,255,255)
    run = True
    while run:

        WIN.fill(WHITE)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print(scrollbar.get_val())

        scrollbar.update()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()