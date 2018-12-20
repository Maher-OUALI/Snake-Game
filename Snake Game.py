import pygame,sys
from pygame.locals import *
from asset.annex import *
from random import randint,choice

pygame.init() #initialize pygame library

#get the stored HIGHSCORE
file=open('asset/highscore.txt','r')
HIGHSCORE = int(file.read())
file.close()
#constants
width,height,constFPS = 594,500,3
fontStyle = 'freesansbold.ttf'
imgWidth,imgHeight,GAP = 20,20,2
nbrColomn = width // (imgWidth + GAP )
nbrLine = int(0.748*height) // (imgHeight + GAP )

#Set up default values
UP = 'e'
DOWN = 'd'
RIGHT = 'f'  #put it this way in order to solve the problem of multiple things at the same time the first is var and the second isn't
LEFT = 's'
snakeSpeed,volume,score,timePassed = 4,1,0,0  #time in seconds 
intro,play,control,pause,death,appleGone= True,False,False,False,False,False
direction = 'd'
assert volume<11 and volume>0
assert snakeSpeed<11 and snakeSpeed>0
assert score>=0
assert timePassed>=0
 
#Set up Colors
White =(255,255,255)
Green = ( 0, 128, 0)
Blue = ( 0, 0, 255)
Red = (255, 0, 0)
Grey = (211,211,211)
Pink = (255,20,147)
Black = (0,0,0)
Orange = (255, 128, 0)

#Set up extra variables
counter = 0

#Set up the window
DISPLAYSURF = pygame.display.set_mode((width,height))#create the display window
pygame.display.set_caption('Snake Game') #set the window name
icon = pygame.image.load('asset/snakegame.png')
pygame.display.set_icon(icon) #set the window icon (replace the default icon )
def set_bg():
    global DISPLAYSURF
    bgimage = pygame.image.load('asset/bgimage.jpg')
    DISPLAYSURF.blit(bgimage,(0,0))
    showText(DISPLAYSURF,'© OM',fontStyle,10,(580,10),Black)

#Set background music
def load_bg_music(musicSrc,vol = 10):
    pygame.mixer.music.load(musicSrc)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(vol/100)

load_bg_music('asset/snakegame.wav',volume)

#Clock ,FPS rate and timer
clock = pygame.time.Clock()
FPS =constFPS+snakeSpeed
pygame.time.set_timer(pygame.USEREVENT , 1000)

# block of code that changes game's keys, volume and snake speed
def gameOptions():
    global UP,DOWN,RIGHT,LEFT,intro,control,snakeSpeed,volume,FPS
    def change_key(x,y,rect,direction):
        global UP,DOWN,LEFT,RIGHT,volume,snakeSpeed
        nonlocal diamondCursor 
        if values_in_rect(x,y,rect):
            set_bg()
            diamondCursor =True 
            #Controls
            showText(DISPLAYSURF,'TAPEZ POUR CHANGER',fontStyle,24,(250,450),Pink)
            RectHome = renderImage(DISPLAYSURF,'asset/homeicon.png',(550,450))
            RectUP = renderText(DISPLAYSURF,'UP: '+int(direction == UP)*'? '+(1-int(direction == UP))*str(UP),fontStyle,35,(300,50),Red)
            RectDOWN = renderText(DISPLAYSURF,'DOWN: '+int(direction == DOWN)*'? '+(1-int(direction == DOWN))*str(DOWN),fontStyle,35,(300,100),Green)
            RectRIGHT = renderText(DISPLAYSURF,'RIGHT: '+int(direction == RIGHT)*'? '+(1-int(direction == RIGHT))*str(RIGHT),fontStyle,35,(300,150),Blue)
            RectLEFT = renderText(DISPLAYSURF,'LEFT: '+int(direction == LEFT)*'? '+(1-int(direction == LEFT))*str(LEFT),fontStyle,35,(300,200),Black)
            #Music
            showText(DISPLAYSURF,'VOLUME',fontStyle,24,(180,320),Orange)
            musicBar = set_bar(volume,(250,320))    
            #Snake Speed
            showText(DISPLAYSURF,'SNAKE SPEED',fontStyle,24,(145,370),Orange)
            speedBar = set_bar(snakeSpeed,(250,370))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    UP = int(chr(event.key)!=DOWN and chr(event.key)!=RIGHT and chr(event.key)!=LEFT and direction == UP and chr(event.key)!= ' ' )*chr(event.key)+int(not(chr(event.key)!=DOWN and chr(event.key)!=RIGHT and chr(event.key)!=LEFT and direction == UP and chr(event.key)!= ' ' ))*UP
                    DOWN = int(chr(event.key)!=UP and chr(event.key)!=RIGHT and chr(event.key)!=LEFT and direction == DOWN and chr(event.key)!= ' ' )*chr(event.key)+int(not(chr(event.key)!=UP and chr(event.key)!=RIGHT and chr(event.key)!=LEFT and direction == DOWN and chr(event.key)!= ' ' ))*DOWN
                    RIGHT = int(chr(event.key)!=DOWN and chr(event.key)!=UP and chr(event.key)!=LEFT and direction == RIGHT and chr(event.key)!= ' ' )*chr(event.key)+int(not(chr(event.key)!=DOWN and chr(event.key)!=UP and chr(event.key)!=LEFT and direction == RIGHT and chr(event.key)!= ' ' ))*RIGHT
                    LEFT = int(chr(event.key)!=DOWN and chr(event.key)!=RIGHT and chr(event.key)!=UP and direction == LEFT and chr(event.key)!= ' ' )*chr(event.key)+int(not(chr(event.key)!=DOWN and chr(event.key)!=RIGHT and chr(event.key)!=UP and direction == LEFT and chr(event.key)!= ' ' ))*LEFT
    def change_bar(x,y,listRect,val):
        nonlocal diamondCursor 
        for i in range(len(listRect)):
            if values_in_rect(x,y,listRect[i]):
                diamondCursor = True 
                showText(DISPLAYSURF,'CLIQUER POUR CHANGER',fontStyle,24,(250,450),Pink)
                if(pygame.mouse.get_pressed()[0]):
                    couple = (listRect[0][0][0]+(listRect[0][1][0]-listRect[0][0][0])//2,listRect[0][0][1]+(listRect[0][1][1]-listRect[0][0][1])//2)
                    return(set_bar(i+1,couple),i+1)
        return(listRect,val)
    def set_bar(nbr,firstCenter):
        global DISPLAYSURF
        listRect =[renderImage(DISPLAYSURF,'asset/barVert.png',(firstCenter[0]+(i-1)*25,firstCenter[1])) for i in range(1,nbr+1)]+[renderImage(DISPLAYSURF,'asset/barRed.png',(firstCenter[0]+(i-1)*25,firstCenter[1])) for i in range(nbr+1,11)]
        return(listRect)            
                    
    set_bg()
    #Controls 
    RectHome = renderImage(DISPLAYSURF,'asset/homeicon.png',(550,450))
    RectUP = renderText(DISPLAYSURF,'UP: '+UP,fontStyle,35,(300,50),Red)
    RectDOWN = renderText(DISPLAYSURF,'DOWN: '+DOWN,fontStyle,35,(300,100),Green)
    RectRIGHT = renderText(DISPLAYSURF,'RIGHT: '+RIGHT,fontStyle,35,(300,150),Blue)
    RectLEFT = renderText(DISPLAYSURF,'LEFT: '+LEFT,fontStyle,35,(300,200),Black)
    #Music
    showText(DISPLAYSURF,'VOLUME',fontStyle,24,(180,320),Orange)
    musicBar = set_bar(volume,(250,320))
        
    #Snake Speed
    showText(DISPLAYSURF,'SNAKE SPEED',fontStyle,24,(145,370),Orange)
    speedBar = set_bar(snakeSpeed,(250,370))

    diamondCursor =False 
    mousex ,mousey = pygame.mouse.get_pos()
    if values_in_rect(mousex,mousey,RectHome):
        diamondCursor =True 
        if(pygame.mouse.get_pressed()[0]):
            intro = True
            control = False
    
    change_key(mousex,mousey,RectUP,UP)
    change_key(mousex,mousey,RectDOWN,DOWN)
    change_key(mousex,mousey,RectRIGHT,RIGHT)
    change_key(mousex,mousey,RectLEFT,LEFT)

    mousex ,mousey = pygame.mouse.get_pos()
    musicBar,volume = change_bar(mousex,mousey,musicBar,volume)
    speedBar,snakeSpeed = change_bar(mousex,mousey,speedBar,snakeSpeed)
    FPS =constFPS+snakeSpeed
    if diamondCursor:
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
        

# block of code that shows the menu at the begining of the game     
def gameMenu():
    global intro,play,control
    set_bg()
    showImage(DISPLAYSURF,'asset/menupicture.png',(300,150))
    RectQuit = renderText(DISPLAYSURF,'QUIT',fontStyle,40,(500,400),Red)
    RectPlay = renderText(DISPLAYSURF,'PLAY',fontStyle,40,(100,400),Green)
    RectOptions = renderText(DISPLAYSURF,'OPTIONS',fontStyle,40,(300,400),Blue)
    mousex ,mousey = pygame.mouse.get_pos()
    if values_in_rect(mousex,mousey,RectQuit):
        set_bg()
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        showImage(DISPLAYSURF,'asset/menupicture.png',(300,150))
        RectQuit = renderText(DISPLAYSURF,'QUIT',fontStyle,40,(500,400),Red)
        RectPlay = renderText(DISPLAYSURF,'PLAY',fontStyle,40,(100,400),Green)
        RectOptions = renderText(DISPLAYSURF,'OPTIONS',fontStyle,40,(300,400),Blue)
        showImage(DISPLAYSURF,'asset/snakecircle2.png',(500,390))
        if(pygame.mouse.get_pressed()[0]):
            storeHighscore()
            pygame.quit()
            sys.exit()
    elif values_in_rect(mousex,mousey,RectPlay):
        set_bg()
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        showImage(DISPLAYSURF,'asset/menupicture.png',(300,150))
        RectQuit = renderText(DISPLAYSURF,'QUIT',fontStyle,40,(500,400),Red)
        RectPlay = renderText(DISPLAYSURF,'PLAY',fontStyle,40,(100,400),Green)
        RectOptions = renderText(DISPLAYSURF,'OPTIONS',fontStyle,40,(300,400),Blue)
        showImage(DISPLAYSURF,'asset/snakecircle2.png',(100,390))
        if(pygame.mouse.get_pressed()[0]):
            intro = False
            play = True
            control = False
    elif values_in_rect(mousex,mousey,RectOptions):
        set_bg()
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        showImage(DISPLAYSURF,'asset/menupicture.png',(300,150))
        RectQuit = renderText(DISPLAYSURF,'QUIT',fontStyle,40,(500,400),Red)
        RectPlay = renderText(DISPLAYSURF,'PLAY',fontStyle,40,(100,400),Green)
        RectOptions = renderText(DISPLAYSURF,'OPTIONS',fontStyle,40,(300,400),Blue)
        showImage(DISPLAYSURF,'asset/snakecircle.png',(300,390))
        if(pygame.mouse.get_pressed()[0]):
            intro = False
            play = False
            control = True
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

# block of code that controls game Pause
def gamePaused():
    global play,pause,counter
    set_bg()
    counter+=1
    pygame.mixer.music.pause()
    showText(DISPLAYSURF,"TAPEZ SUR LA BARRE D'ESPACE POUR CONTINUER",fontStyle,20+(counter // 8 )%3,(300,200),Pink)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if chr(event.key) == ' ':
                play = True
                pause = False
                pygame.mixer.music.unpause()
                counter = 0

#block of code that controls Snake Death
def gameDeath():
    global timePassed,intro,death,play,snake,applePosCenter,HIGHSCORE,score
    set_bg()
    if score > HIGHSCORE :
        HIGHSCORE = score
    pygame.mixer.music.pause()
    showText(DISPLAYSURF,'GAME OVER',fontStyle,54,(300,200),Pink)
    RectHome = renderImage(DISPLAYSURF,'asset/homeicon.png',(250,250))
    RectReplay = renderImage(DISPLAYSURF,'asset/replayicon.png',(350,250))
    mousex ,mousey = pygame.mouse.get_pos()
    if values_in_rect(mousex,mousey,RectHome):
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        if(pygame.mouse.get_pressed()[0]):
            intro = True
            death = False
            init_snake()
            pygame.mixer.music.unpause()
            
    elif values_in_rect(mousex,mousey,RectReplay):
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        if(pygame.mouse.get_pressed()[0]):
            play = True
            death = False
            init_snake()
            pygame.mixer.music.unpause()
            
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

def storeHighscore():
    file = open('asset/highscore.txt','w')
    file.write(str(HIGHSCORE))
    file.close()
                                
def updatePlayScreen():
    global play,intro,timePassed,counter,snake
    
    def showSprites():
        value =(counter // (2*(constFPS+snakeSpeed)))
        snake.show(DISPLAYSURF,'asset/snakehead'+(value%4 != 0)*'1'+'.png','asset/snakeskin.png',0+int(direction == 'z')*90+int(direction == 's')*(-90)+int(direction == 'q')*180 )
        showImage(DISPLAYSURF,'asset/appleImage.png',applePosCenter)

    set_bg()
    pygame.draw.line(DISPLAYSURF,Blue,(0,height//5),(width,height//5),2)
    pygame.draw.line(DISPLAYSURF,Blue,(0,0.748*height+height//5),(width,0.748*height+height//5),2)
    showImage(DISPLAYSURF,'asset/appleicon.png',(40,45))
    showText(DISPLAYSURF,'x '+str(score),fontStyle,30,(85,50),Red,White)
    showText(DISPLAYSURF,'HIGHSCORE = '+str(HIGHSCORE),fontStyle,20,(150,80),Red,White)
    showText(DISPLAYSURF,'_TIME_ '+'0'*(len(str(timePassed // 60)) == 1)+str(timePassed // 60)+':'+'0'*(len(str(timePassed % 60)) == 1)+str(timePassed % 60),fontStyle,35,(300,50),Pink
                ,White)
    RectHome = renderImage(DISPLAYSURF,'asset/homeicon.png',(550,50))
    showSprites()
    mousex ,mousey = pygame.mouse.get_pos()
    if values_in_rect(mousex,mousey,RectHome):
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        if(pygame.mouse.get_pressed()[0]):
            intro = True
            play = False
            init_snake()
            
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)


#Initialize the snake segment
gridRect , gridPosCenter = createGrid((0,height//5),imgWidth,imgHeight,nbrLine,nbrColomn,GAP)
snake,applePosCenter = None,None

def init_snake():
    global direction,applePosCenter,snake,counter,timePassed,score
    snake = Snake(gridRect[(nbrLine//2-1)*nbrColomn + nbrColomn//5+4][0],imgWidth,imgHeight,GAP,5)
    applePosCenter = choice(list(set(gridPosCenter)-set(snake.listPosCenter)))
    direction = 'd'
    counter = 0
    score = 0
    timePassed = 0
init_snake()
#main game loop

while True :
    if intro :
        gameMenu()
        clock.tick(20)
    if control :
        gameOptions()
        clock.tick(20)
    if play :
        counter +=1
        clock.tick(FPS)#
        if appleGone:
            appleGone = False
            applePosCenter = choice(list(set(gridPosCenter)-set(snake.listPosCenter)))
        updatePlayScreen()
        for event in pygame.event.get():
            if event.type == QUIT:
                storeHighscore()
                pygame.quit()
                sys.exit()
            elif event.type == USEREVENT:
                timePassed +=1
            elif event.type == KEYDOWN:
                if chr(event.key) == UP :
                    if direction != 's':
                        direction = 'z'         
                elif chr(event.key) == DOWN :
                    if direction != 'z':
                        direction = 's'
                elif chr(event.key) == LEFT :
                    if direction != 'd':
                        direction = 'q'
                elif chr(event.key) == RIGHT :
                    if direction != 'q':
                        direction = 'd'
                elif chr(event.key) == ' ':
                    pause = True
                    play = False
                    counter =0
                

        if not(snake.futureHeadPos(direction) in gridPosCenter):
            rect = snake.listRect[snake.len -1]
            posCenter = snake.listPosCenter[snake.len -1]
            border = int(direction == 'z')*[[(rect[0][0],0.748*height+(height//5)-(imgHeight+GAP)),(rect[1][0],0.748*height+height//5)],(posCenter[0],0.748*height+(height//5)-((imgHeight+GAP)//2))]
            border += int(direction == 's')*[[(rect[0][0],(height//5)),(rect[1][0],height//5+imgHeight+GAP)],(posCenter[0],(height//5)+((imgHeight+GAP)//2))]
            border += int(direction == 'q')*[[(width-(imgWidth+GAP),rect[0][1]),(width,rect[0][1])],(width-((imgWidth+GAP)//2),posCenter[1])]
            border += int(direction == 'd')*[[(0,rect[0][1]),((imgWidth+GAP),rect[0][1])],(((imgWidth+GAP)//2),posCenter[1])]
        else :
            border = None
        death = snake.isDead(direction)
        play = not(death)and play

        if snake.isColide(applePosCenter):
            appleGone =True
            score +=1
            tale = [snake.listRect[0],snake.listPosCenter[0]]
        snake.updateList(direction,border)
        if appleGone :
            snake.addtoTale(tale[0],tale[1])
    if death:
        gameDeath()
        clock.tick(20)
    if pause:
        gamePaused()
        clock.tick(20)
                
        #Simple Moves not complicated at all PLZ 
    for event in pygame.event.get():
        if event.type == QUIT:
            storeHighscore()
            pygame.quit()
            sys.exit()         
    pygame.mixer.music.set_volume(volume/100)
    pygame.display.update()


#to show the image of the head add a global var called direction that determines the tale and head image  
    
#first goal is to move in the map and add a tale without eating shit and then in a second phase add the rat pos         

# need to create the grid (BLOCKWIDTH BLOCKMARGIN + assert something )
