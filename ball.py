import pygame,random,sys,time,math
from pygame.locals import *

#定义窗口变量
WORLDWIDTH = 1500  #世界宽度
WORLDHEIGHT = 1500  #世界高度
HALFWWIDTH = int(WORLDWIDTH//2)
HALFWHEIGHT = int(WORLDHEIGHT//2)
WIDTH = 1000  #窗口宽度
HEIGHT = 700  #窗口高度
CENTERWIDTH = int(WIDTH//2)
CENTERHEIGHT = int(HEIGHT//2)
FPS = 60  #帧率
SPLITBASE = 1.01 #分裂基数
pi = math.pi
INITIALWEIGHT = 20  #初始重量

#定义颜色变量
LIGHTBLACK = (10,51,71)
LIGHTBLUE = (51,102,205)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

#定义方向变量
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


#定义球球类
class Ball():
    def __init__(self,xpos,ypos,weight,color): #定义球的x，y，重量，颜色
        self.xpos = xpos
        self.ypos = ypos
        self.radius = weightToRadius(weight)
        self.weight = weight
        self.speed = weightToSpeed(weight)
        self.color = color

    def move(self,direction):  #小球移动
        rec = pygame.Rect(-HALFWWIDTH, -HALFWHEIGHT, WORLDWIDTH, WORLDHEIGHT)
        if direction == UP:
            if rec.top < self.ypos - self.radius: #限制在上边界以下
                self.ypos -= int(self.speed//20)
        elif direction == DOWN:
            if rec.bottom > self.ypos +self.radius:
                self.ypos += int(self.speed//20)
        elif direction == RIGHT:
            if rec.right > self.xpos + self.radius:
                self.xpos += int(self.speed//20)
        elif direction == LEFT:
            if rec.left < self.xpos - self.radius:
                self.xpos -= int(self.speed//20)

    def split(self,direction): #分裂小球函数
        newweight = math.floor((self.weight // 2) * SPLITBASE)
        newball = Ball(self.xpos, self.ypos, newweight, self.color)
        if direction == UP:
            #分裂流畅动画
            for i in range(10):
                newball.ypos -= round(0.2*self.radius)
                drawBall(newball)
                pygame.display.update()
        elif direction == DOWN:
            for i in range(10):
                newball.ypos += round(0.2*self.radius)
                drawBall(newball)
                pygame.display.update()
        elif direction == LEFT:
            for i in range(10):
                newball.xpos -= round(0.2*self.radius)
                drawBall(newball)
                pygame.display.update()
        elif direction == RIGHT:
            for i in range(10):
                newball.xpos += round(0.2*self.radius)
                drawBall(newball)
                pygame.display.update()
        self.setWeight(newweight) #分裂完后设置球的重量
        selfBalls.append(newball)

    def setWeight(self,newweight):
        self.weight = newweight
        self.speed = weightToSpeed(newweight)
        self.radius = weightToRadius(newweight)

    def eatFood(self): #吃食物
        global foodlist
        selfworldx = self.xpos
        selfworldy = self.ypos
        for food in foodlist:
            distance = math.sqrt((selfworldx-food.xpos)*(selfworldx-food.xpos)+(selfworldy-food.ypos)*(selfworldy-food.ypos))
            if distance < self.radius:
                self.setWeight(self.weight+food.weight)
                foodlist.remove(food)

#食物类
class Food():
    def __init__(self,xpos,ypos,weight,color,radius):
        self.xpos = xpos
        self.ypos = ypos
        self.weight = weight
        self.color = color
        self.radius = radius

#其他球类
class OtherBall():
    def __init__(self,xpos,ypos,weight,color):
        self.xpos = xpos
        self.ypos = ypos
        self.weight = weight
        self.radius = weightToRadius(weight)
        self.speed = weightToSpeed(weight)
        self.color = color
        self.direction = random.uniform(0,2*pi) #方向角度

    def eatFood(self):
        global foodlist
        for food in foodlist:
            distance = math.sqrt((self.xpos-food.xpos)**2+(self.ypos-food.ypos)**2)
            if distance < self.radius:
                self.setWeight(self.weight+food.weight)
                foodlist.remove(food)

    def setWeight(self,newweight):
        self.weight = newweight
        self.speed = weightToSpeed(newweight)
        self.radius = weightToRadius(newweight)

    def move(self):#使小球能在方框内移动
        rec = pygame.Rect(-HALFWWIDTH,-HALFWHEIGHT,WORLDWIDTH,WORLDHEIGHT)
        if rec.left>self.xpos:
            self.direction = pi - self.direction
            self.xpos += self.speed//10 #之前没有这句，小球在碰撞几次墙壁之后就会跳动着出界
        if rec.right<self.xpos:
            self.direction = pi - self.direction
            self.xpos -= self.speed//10
        if rec.top >self.ypos:
            self.direction = 2*pi-self.direction
            self.ypos += self.speed//10
        if rec.bottom < self.ypos:
            self.direction = 2*pi-self.direction
            self.ypos -= self.speed//10
        self.xpos += math.floor(math.cos(self.direction)*self.speed//40)
        self.ypos -= math.floor(math.sin(self.direction)*self.speed//40)

def main():
    global FPSCLOCK,DISPLAYSURF,cameray,camerax,selfBalls,otherBalls,foodlist,rec #设置全局变量
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WIDTH,HEIGHT))

    camerax = -CENTERWIDTH
    cameray = -CENTERHEIGHT
    dirction = ''

    #定义小球列表
    selfBalls = []
    otherBalls = []
    foodlist = []

    for i in range(500): #创建其他小球
        xpos = random.randint(-HALFWWIDTH, HALFWWIDTH)
        ypos = random.randint(-HALFWHEIGHT, HALFWHEIGHT)
        otherb = OtherBall(xpos,ypos,INITIALWEIGHT,randomColor())
        otherBalls.append(otherb)

    for i in range(1000): #初始化创建1000个食物
        createFood(foodlist)

    ball = Ball(0, 0, INITIALWEIGHT, randomColor()) #建立第一个小球
    selfBalls.append(ball)

    fontObj = pygame.font.Font('C:/Windows/Fonts/simkai.ttf',20)  #字体对象，我用的是系统字体
    winfont = pygame.font.Font('C:/Windows/Fonts/simkai.ttf',36)

    allweight = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                time.sleep(3)
                exit()
            if event.type == KEYUP: #响应键盘
                if event.key == K_UP:
                    dirction = UP
                elif event.key == K_DOWN:
                    dirction = DOWN
                elif event.key == K_RIGHT:
                    dirction = RIGHT
                elif event.key == K_LEFT:
                    dirction = LEFT
                elif event.key == K_f:  #分裂
                    count = len(selfBalls)
                    if count < 16:
                        for i in range(count):
                            if selfBalls[i].weight > 20:
                                selfBalls[i].split(dirction)

        DISPLAYSURF.fill(LIGHTBLACK) #背景填充
        rec = pygame.Rect(-(camerax + HALFWHEIGHT), -(cameray + HALFWHEIGHT), WORLDWIDTH, WORLDHEIGHT) #边界矩形
        drawBorder(rec)

        text = '重量为：'+str(allweight)+'   敌人还剩：'+str(len(otherBalls))
        displayText(text,fontObj,WHITE,200,20)
        if len(foodlist)<500:  #当食物数量小于500时，增加食物
            createFood(foodlist)
        drawFoods(foodlist)

        if len(otherBalls)>0: #当其他球还有的时候进行吃球的操作
            balleatBall()
        if len(otherBalls)==0:  #胜利条件
            displayText('恭喜你！最终你胖到了'+str(allweight)+'斤',winfont,RED,CENTERWIDTH,CENTERHEIGHT)
            pygame.display.update()
            time.sleep(3)
            pygame.quit()
        if len(selfBalls)==0:
            displayText('你被吃了~继续努力吧~',winfont,RED,CENTERWIDTH,CENTERHEIGHT)
            pygame.display.update()
            time.sleep(3)
            pygame.quit()
        
        allweight = 0
        for b in selfBalls:  #得到所有重量和移动所有球
            allweight += b.weight
            b.move(dirction)

        for b in otherBalls: #移动其他的球
            b.move()
            b.eatFood()

        drawBalls(selfBalls)

        camerax = selfBalls[0].xpos - CENTERWIDTH
        cameray = selfBalls[0].ypos - CENTERHEIGHT

        for ball in selfBalls:
            ball.eatFood()

        drawBalls(otherBalls)

        if len(selfBalls)>=2:
            unite()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def displayText(text,fontObj,textcolor,xpos,ypos):  #显示字函数
    textsurf = fontObj.render(text, True, textcolor)
    textRect = textsurf.get_rect()
    textRect.center = (xpos, ypos)
    DISPLAYSURF.blit(textsurf, textRect)

def balleatBall(): #我方球吃其他球，本游戏不设置其他球互吃
    global selfBalls,otherBalls
    for ball1 in selfBalls:
        for ball2 in otherBalls:
            distance = math.sqrt((ball1.xpos - ball2.xpos) ** 2 + (ball1.ypos - ball2.ypos) ** 2)
            if distance < (ball1.radius + ball2.radius) / 2:
                if ball1.radius > ball2.radius + 3:
                    ball1.setWeight(ball1.weight + ball2.weight)
                    otherBalls.remove(ball2)
                elif ball1.radius+3 < ball2.radius :
                    ball2.setWeight(ball1.weight + ball2.weight)
                    selfBalls.remove(ball1)


def unite(): #联合两个小球
    global selfBalls
    for ball1 in selfBalls:
        for ball2 in selfBalls:
            if ball1!=ball2:
                distance = math.sqrt((ball1.xpos-ball2.xpos)**2+(ball1.ypos-ball2.ypos)**2)
                if distance<(ball1.radius+ball2.radius)/2:
                    ball1.setWeight(ball1.weight+ball2.weight)
                    selfBalls.remove(ball2)


def createFood(foodlist):
    xpos = random.randint(-HALFWWIDTH,HALFWWIDTH)
    ypos = random.randint(-HALFWHEIGHT,HALFWHEIGHT)
    weight = 5  #每个食物的重量
    radius = 3  #每个食物的半径
    newfood = Food(xpos,ypos,weight,randomColor(),radius)
    foodlist.append(newfood)

def drawFoods(foodlist):
    global camerax,cameray
    for food in foodlist:
        pygame.draw.circle(DISPLAYSURF, food.color, ((food.xpos - camerax), (food.ypos - cameray)), food.radius)

def drawBalls(balls): #画所有球
    global camerax,cameray
    for ball in balls:
        pos = (ball.xpos-camerax,ball.ypos-cameray)
        radius = ball.radius
        color = ball.color
        pygame.draw.circle(DISPLAYSURF,color,pos,radius)

def weightToSpeed(weight):#重量转换为速度
    if weight < 8000:
        return math.floor(-0.02*weight+200)
    elif weight >=8000:
        return 40  #最低速度为40

def weightToRadius(weight):  #将小球的重量转化为半径
    if weight < 100:
        return math.floor(0.1*weight + 10)
    elif weight>=100:
        return math.floor(2*math.sqrt(weight))

def drawBorder(rec): #画边界
    borderthick = 5
    pygame.draw.rect(DISPLAYSURF,WHITE,rec,borderthick)
    recleft = (rec[0]-CENTERWIDTH,rec[1]-CENTERHEIGHT,CENTERWIDTH,WORLDHEIGHT+HEIGHT)
    recright = (rec[0]+WORLDWIDTH,rec[1]-CENTERHEIGHT,CENTERWIDTH,WORLDHEIGHT+HEIGHT)
    rectop = (rec[0],rec[1]-CENTERHEIGHT,WORLDWIDTH,CENTERHEIGHT)
    recbottom = (rec[0],rec[1]+WORLDHEIGHT,WORLDWIDTH,CENTERHEIGHT)
    pygame.draw.rect(DISPLAYSURF,BLACK,recleft,0)
    pygame.draw.rect(DISPLAYSURF, BLACK, rectop, 0)
    pygame.draw.rect(DISPLAYSURF, BLACK, recright, 0)
    pygame.draw.rect(DISPLAYSURF, BLACK, recbottom, 0)

def drawBall(Obj):
    pygame.draw.circle(DISPLAYSURF,Obj.color,(Obj.xpos,Obj.ypos),Obj.radius)

def randomColor(): #随机获取颜色
    return (random.randint(1,255),random.randint(1,255),random.randint(1,255))


if __name__ =="__main__":
    main()
