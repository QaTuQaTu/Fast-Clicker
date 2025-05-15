import pygame
import time
from random import randint

pygame.init()

# Creating the program window
back = (200, 255, 255)  # Background color
mw = pygame.display.set_mode((500, 500))  # Main window
mw.fill(back)
clock = pygame.time.Clock()

# Rectangle class
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)  # Rectangle
        self.fill_color = color
    
    def color(self, new_color):
        self.fill_color = new_color
    
    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)
    
    def outline(self, frame_color, thickness):
        pygame.draw.rect(mw, frame_color, self.rect, thickness)
    
    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

# Label class
class Label(Area):
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        super().__init__(x, y, width, height, color)
        self.image = None
    
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        font = pygame.font.SysFont('verdana', fsize)
        self.image = font.render(text, True, text_color)
    
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        if self.image:
            mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 51)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 100)
BLUE = (80, 80, 255)
LIGHT_GREEN = (200, 255, 200)
LIGHT_RED = (250, 128, 114)

cards = []
num_cards = 4
x = 70

# Game Interface
time_text = Label(0, 0, 500, 50, back)
time_text.set_text('Time:', 40, DARK_BLUE)
time_text.draw(20, 20)

timer = Label(50, 55, 100, 40, back)
timer.set_text('0', 40, DARK_BLUE)
timer.draw(0, 0)

score_text = Label(380, 0, 120, 50, back)
score_text.set_text('Count:', 45, DARK_BLUE)
score_text.draw(20, 20)

score = Label(430, 55, 100, 40, back)
score.set_text('0', 40, DARK_BLUE)
score.draw(0, 0)

for i in range(num_cards):
    new_card = Label(x, 170, 70, 100, YELLOW)
    new_card.outline(BLUE, 10)
    new_card.set_text('CLICK', 26)
    cards.append(new_card)
    x += 100

wait = 0
points = 0
start_time = time.time()
cur_time = start_time

while True:
    # Drawing cards and displaying clicks
    if wait == 0:
        wait = 20  # How many ticks of the label will be in one place
        click = randint(1, num_cards)
        for i in range(num_cards):
            cards[i].color(YELLOW)
            if (i + 1) == click:
                cards[i].draw(10, 40)
            else:
                cards[i].fill()
    else:
        wait -= 1
    
    # Handling clicks on cards
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos
            for i in range(num_cards):
                # Looking for the card that the click hit
                if cards[i].collidepoint(x, y):
                    if i + 1 == click:
                        # If there is a label on the card, color it green, add a point
                        cards[i].color(GREEN)
                        points += 1
                    else:
                        # Otherwise color it red, minus a point
                        cards[i].color(RED)
                        points -= 1
                    cards[i].fill()
                    score.set_text(str(points), 40, DARK_BLUE)
                    score.draw(0, 0)
    
    # Winning and losing conditions
    new_time = time.time()
    
    if new_time - start_time >= 11:
        win = Label(0, 0, 500, 500, LIGHT_RED)
        win.set_text("Time's up!!!", 60, DARK_BLUE)
        win.draw(110, 180)
        break
    
    if int(new_time) - int(cur_time) == 1:
        # Check if there is a difference of 1 second between the old and new time
        timer.set_text(str(int(new_time - start_time)), 40, DARK_BLUE)
        timer.draw(0, 0)
        cur_time = new_time
    
    if points >= 5:
        win = Label(0, 0, 500, 500, LIGHT_GREEN)
        win.set_text("You won!!!", 60, DARK_BLUE)
        win.draw(140, 180)
        result_time = Label(90, 230, 250, 250, LIGHT_GREEN)
        result_time.set_text("Completion time: " + str(int(new_time - start_time)) + " sec", 40, DARK_BLUE)
        result_time.draw(0, 0)
        break
    
    pygame.display.update()
    clock.tick(40)

pygame.quit()
