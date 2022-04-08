import pygame

difficulty = input ('Easy, Medium, Hard, Very Hard')
if difficulty == 'Easy':
    vel = 1
elif difficulty == 'Medium':
    vel = 2.5
elif difficulty == 'Hard':
    vel = 3.5
elif difficulty == 'Very Hard':
    vel = 5

pygame.init()

icon = pygame.image.load('ping-pong.png')
scrheight = 500
scrwidth = 700
screen = pygame.display.set_mode((scrwidth,scrheight))
pygame.display.set_caption('Pong')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
WHITE = (255,255,255)
LIME = (81, 255, 46)

paddle1 = pygame.image.load('001-ping-pong.png')

class paddle(object):
    COLOR = WHITE
    VELOCITY = vel
    def __init__ (self, x, y, height, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw (self, screen):
        pygame.draw.rect(screen, self.COLOR, (self.x, self.y, self.width, self.height))

    def move (self, up=True):
        if up == True:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

class ball ():
    MAXVEL = 5.5
    COLOR = WHITE
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.xvel = 5.5
        self.yvel = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.xvel
        self.y += self.yvel

def draw (paddles, ball):
    for paddle in paddles:
        paddle.draw(screen)

    for i in range (2, scrheight, scrheight//15):
        if i % 2 == 1:
            continue
        else:
            pygame.draw.rect(screen, LIME, (scrwidth//2 - paddlewidth//2, i, 5, 25))

    ball.draw(screen)

def handle_paddle_movement(keys, left, right):
    if keys[pygame.K_w] and left.y - left.VELOCITY >= 0:
        left.move(up=True)
    if keys[pygame.K_s] and left.y + left.height + left.VELOCITY <= scrheight:
        left.move(up=False)
    if keys[pygame.K_UP] and right.y - right.VELOCITY >= 0:
        right.move(up=True)
    if keys[pygame.K_DOWN] and right.y + right.height + right.VELOCITY <= scrheight:
        right.move(up=False)

#def collisions():

    
paddleheight, paddlewidth = 100, 20

left_paddle = paddle (10, scrheight//2 - paddleheight//2, paddleheight, paddlewidth)
right_paddle = paddle (scrwidth - 10 - paddlewidth, scrheight//2 - paddleheight//2, paddleheight, paddlewidth)
ball = ball(scrwidth//2 - 7 , scrheight//2 - 7 , 7)



running = True
while running:
    clock.tick(120)
    clock.tick_busy_loop(5)
    screen.fill((22, 77, 158))
    draw([left_paddle, right_paddle], ball)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    handle_paddle_movement(keys, left_paddle, right_paddle)
    ball.move()
    pygame.display.update()

    