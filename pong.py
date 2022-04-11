import pygame

difficulty = input ('Select difficulty \nEasy, Medium, Hard, Very Hard')
if difficulty == 'Easy':
    vel = 2
elif difficulty == 'Medium':
    vel = 7
elif difficulty == 'Hard':
    vel = 9
elif difficulty == 'Very Hard':
    vel = 13

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
BLACK = (0,0,0)
RED = (181, 18, 18)
GREEN = (25, 87, 18)
SCORE_FONT = pygame.font.SysFont('comicsans', 58)
win_font = pygame.font.SysFont('ubuntu', 40)

paddle1 = pygame.image.load('001-ping-pong.png')

class paddle(object):
    COLOR = RED
    VELOCITY = (4/5) * (vel)
    def __init__ (self, x, y, height, width):
        self.x = self.originalx = x
        self.y = self.originaly = y
        self.width = width
        self.height = height

    def draw (self, screen):
        pygame.draw.rect(screen, self.COLOR, (self.x, self.y, self.width, self.height))

    def move (self, up=True):
        if up == True:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY
    def reset(self):
        self.x = self.originalx
        self.y = self.originaly

class ball ():
    MAXVEL = vel
    COLOR = WHITE
    def __init__(self, x, y, radius):
        self.x = self.originalx = x
        self.y = self.originaly = y
        self.radius = radius
        self.xvel = vel
        self.yvel = 0

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.radius)
    
    def move(self):
        self.x += self.xvel
        self.y += self.yvel

    def reset(self):
        self.x = self.originalx
        self.y = self.originaly
        self.yvel = 0
        self.xvel *= -1
    
def draw (paddles, ball, left_score, right_score):
    
    left_score_text = SCORE_FONT.render('{}'.format(left_score), 1, BLACK)
    right_score_text = SCORE_FONT.render('{}'.format(right_score), 1, BLACK)
    screen.blit(left_score_text, (scrwidth//4 - left_score_text.get_width()//2, 25))
    screen.blit(right_score_text, ((scrwidth//4)*3 - left_score_text.get_width()//2, 25))

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

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y+ball.radius>=scrheight:
        ball.yvel*=-1
    elif ball.y-ball.radius<=0:
        ball.yvel*=-1

    if ball.xvel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.xvel *= -1

                middle_y = left_paddle.y + left_paddle.height/2
                difference_y = middle_y-ball.y
                reduction_factor = (left_paddle.height/2)/ball.MAXVEL
                maxvel = difference_y/reduction_factor
                ball.yvel = -1 * maxvel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.xvel *= -1

                middle_y = right_paddle.y + right_paddle.height/2
                difference_y = middle_y-ball.y
                reduction_factor = (right_paddle.height/2)/ball.MAXVEL
                maxvel = difference_y/reduction_factor
                ball.yvel = -1 * maxvel
    
paddleheight, paddlewidth = 100, 20

left_paddle = paddle (10, scrheight//2 - paddleheight//2, paddleheight, paddlewidth)
right_paddle = paddle (scrwidth - 10 - paddlewidth, scrheight//2 - paddleheight//2, paddleheight, paddlewidth)
ball = ball(scrwidth//2 - 7 , scrheight//2 - 7 , 7)



running = True
left_score = 0
won = False
right_score = 0
winning_score = 10 
while running:
    clock.tick(60)
    screen.fill((22, 77, 158))
    draw([left_paddle, right_paddle], ball, left_score, right_score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    keys = pygame.key.get_pressed()
    handle_paddle_movement(keys, left_paddle, right_paddle)
    ball.move()
    handle_collision(ball, left_paddle, right_paddle)
    if ball.x < 0:
        right_score += 1
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()
        pygame.time.delay(3000)
    elif ball.x > scrwidth:
        left_score += 1
        ball.reset()
        left_paddle.reset()
        right_paddle.reset()
        pygame.time.delay(3000)
    if left_score >= winning_score:
        won = True
        winning_text = 'Left player won!'
    elif right_score >= winning_score:
        won = True
        winning_text = 'Right player won!'
    if won:
        left_paddle.reset()
        right_paddle.reset()
        ball.reset()
        left_score = 0
        right_score = 0
        running = False
    pygame.display.update()

screen.fill(BLACK)
win_text = win_font.render(winning_text, 1, WHITE)
screen.blit(win_text, (scrwidth//2 - win_text.get_width()//2, scrheight//2 - win_text.get_height()//2))
pygame.display.update()
pygame.time.delay(5000)
pygame.quit()
