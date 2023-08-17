import pygame,sys,random,pickle
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()
cycletick = 0
FPS = 30
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
font1 = pygame.font.SysFont('comicsans',45,1,0)
font2 = pygame.font.SysFont('comicsans',30,0,0)

screen = (620,675)
win = pygame.display.set_mode(screen)
pygame.display.set_caption('Snake')
bgcolor = black

griddraw = (600,600)
CELLSIZE = 20
BODYOFFSET = 6
gridsize = 600
field = pygame.Surface((gridsize,gridsize))
tab = pygame.Surface((600,50))
field.fill(bgcolor)
tab.fill(bgcolor)
titlesnake = []
buttonsize = (200,50)

with open('Data.dat','rb') as file:
    highscore = pickle.load(file)
    stats = pickle.load(file)
    playername = pickle.load(file)

def savestatus():
    with open('Data.dat','wb') as file:
        pickle.dump(highscore,file)
        pickle.dump(stats,file)
        pickle.dump(playername,file)

def checkbutton(coord,size=buttonsize):
    if mpos[0] >= coord[0] and mpos[0] <= coord[0]+size[0]:
        if mpos[1] >= coord[1] and mpos[1] <= coord[1]+size[1]:
            return True

def buttondraw(surface,text,coord,color=white,size=buttonsize):
    Text = font1.render(text,0,color)
    pygame.draw.rect(surface,color,(coord,size))
    pygame.draw.rect(surface,bgcolor,(coord[0]+5,coord[1]+5,size[0]-10,size[1]-10))
    surface.blit(Text,(coord[0]+10,coord[1]+10))

def tiledraw(surface,text,coord,size,color=white):
    Text = font2.render(text,0,color)
    pygame.draw.rect(surface,bgcolor,(coord,size))
    surface.blit(Text,(coord[0]+5,coord[1]+10))

def drawsnake(body,surface,color=green):
    l = len(body)
    for i in range(l-1):
        start = body[i]
        end = body[i+1]
        x = min(start[0],end[0])*CELLSIZE + BODYOFFSET
        y = min(start[1],end[1])*CELLSIZE + BODYOFFSET
        w = (abs(end[0]-start[0])+1)*CELLSIZE - 2*BODYOFFSET
        h = (abs(end[1]-start[1])+1)*CELLSIZE - 2*BODYOFFSET
        pygame.draw.rect(surface,color,(x,y,w,h))  

def updatescore(score):
    # num = 0
    # onboard = 0
    scored = False
    for n in range(15):
    #     if highscore[n][0] == playername:
    #         onboard = n+1
    #     if highscore[n][1] < score:
    #         num = n+1
    # if num and onboard:
        if not scored:
            if score > highscore[n][1]:
                highscore.insert(n,(playername,score))
                scored = True
            elif playername == highscore[n][0]:
                scored = True
                break
        else:
            if playername == highscore[n][0]:
                highscore.pop(n)
                break
    if len(highscore) > 15:
        highscore.pop()
        
                

def mainmenudraw():    
    #background
    win.fill(bgcolor)
    pname = playername
    if namechange:
        pname += '|'
    buttondraw(win,pname,(50,20),size=(520,50))
    for button in mainmenu:
        buttondraw(win,button,mainmenu[button])        

    pygame.display.update()

def gameplaydraw():
    #background
    field.fill(bgcolor)
    tab.fill(bgcolor)
    pygame.draw.rect(win,white,(5,5,screen[0]-10,screen[1]-10))    
    pygame.draw.rect(field,red,(food[0]*CELLSIZE+BODYOFFSET,food[1]*CELLSIZE+BODYOFFSET,CELLSIZE-2*BODYOFFSET,CELLSIZE-2*BODYOFFSET))
    drawsnake(snakebody,field)
    tab.blit(font1.render('Score: '+str(score),0,white),(10,10))
    tab.blit(font1.render('Level: '+str(level),0,white),(450,10))
    if End:
        if Win:
            buttondraw(field,'You Won',(200,275))
        else:
            drawsnake([head,snakebody[0]],field,color=blue)
            buttondraw(field,str(score),(200,220))
            buttondraw(field,'Lost',(200,275))
            buttondraw(field,'Retry',(200,330))   
        
    elif Paused:
        buttondraw(field,'Paused',(200,275))
    
    win.blit(field,(10,10))
    win.blit(tab,(10,griddraw[0]+5+10))

    pygame.display.update()

def highscoredraw():
    win.fill(bgcolor)
    pygame.draw.rect(win,white,(10,10,screen[0]-20,screen[1]-20))
    buttondraw(win,'RANK',(10,10),size=(125,50))
    buttondraw(win,'NAME',(130,10),size=(340,50))
    buttondraw(win,'SCORE',(465,10),size=(145,50))
    yoffset = 65
    
    for n in range(15):
        tiledraw(win,str(n+1),(15,yoffset+n*40),(115,35))
        tiledraw(win,highscore[n][0],(135,yoffset+n*40),(330,35))
        tiledraw(win,str(highscore[n][1]),(470,yoffset+n*40),(135,35))

    pygame.display.update()

def statisticsdraw():
    win.fill(bgcolor)
    pygame.draw.rect(win,white,(5,5,screen[0]-10,205))

    count = 0
    for stat in stats:
        tiledraw(win,stat,(10,10+count*40),(120,35))
        tiledraw(win,str(stats[stat]),(135,10+count*40),(475,35))
        count += 1

    pygame.display.update()

Mainmenu = True
mainbuttondis = 257
mainmenu = {'Play':(210,mainbuttondis),'Statistics':(210,mainbuttondis+55),'Highscore':(210,mainbuttondis+110),'Quit':(210,mainbuttondis+165)}
Gameplay = False
Paused = False
namechange = False
Statistics = False
Highscore = False


def reset():    
    global head,move,level,step,food,moved,End,snakebody,grid,score,Win
    snakebody = [(14,15),(15,15),(16,15)]
    head = snakebody[0]
    move = (-1,0)
    grid = []
    for i in range(gridsize//CELLSIZE):
        for j in range(gridsize//CELLSIZE):
            if (i,j) not in snakebody:
                grid.append((i,j))
    level = 1    
    step = FPS
    food = random.choice(grid)
    moved = False
    End = False
    Win = False
    score = 0

reset()
STEPLEVEL = 5
levels = {1:[3,6],2:[4,6],3:[5,10],4:[6,15],5:[7,20],6:[8,0]}

while True:

    mpos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            savestatus()
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if Gameplay and Loss:
                    if checkbutton((200,330)):
                        reset()
                        Loss = False
                if Mainmenu:
                    if checkbutton(mainmenu['Play']):
                        Mainmenu = False
                        namechange = False
                        Gameplay = True
                    elif checkbutton(mainmenu['Highscore']):
                        Mainmenu = False
                        namechange = False
                        Highscore = True
                    elif checkbutton(mainmenu['Statistics']):
                        Mainmenu = False
                        namechange = False
                        Statistics = True
                    elif checkbutton((50,20),(520,50)):
                        namechange = True
                    elif checkbutton(mainmenu['Quit']):
                        savestatus()
                        pygame.quit()
                        sys.exit()

        if event.type == KEYDOWN:
            if Gameplay:
                if moved:
                    if move[1] == 0:
                        if event.key == K_UP or event.key == K_w:
                            move = (0,-1)
                        elif event.key == K_DOWN or event.key == K_s:
                            move = (0,1)
                    elif move[0] == 0:
                        if event.key == K_LEFT or event.key == K_a:
                            move = (-1,0)
                        elif event.key == K_RIGHT or event.key == K_d:
                            move = (1,0)
                    moved = False
                    
                if event.key == K_SPACE:
                    Paused = not Paused
            elif Mainmenu:
                if namechange:
                    if event.key == K_RETURN:
                        namechange = False
                    elif event.key == K_BACKSPACE:
                        playername = playername[:-1]
                    else:
                        playername += event.unicode 

            if event.key == K_ESCAPE:
                if Gameplay:
                    Gameplay = False
                elif Statistics:
                    Statistics = False
                elif Highscore:
                    Highscore = False
                Mainmenu = True
                reset()

    if Mainmenu:
        mainmenudraw()
    if Highscore:
        highscoredraw()
    if Statistics:
        statisticsdraw()

    if Gameplay:
        if not End:
            if not Paused and not Win:
                step -= levels[level][0]            
                if step <= 0:
                    moved = True
                    step = FPS
                    head = (head[0]+move[0],head[1]+move[1])                    
                    if head in grid:
                        grid.remove(head)
                        snakebody.insert(0,head)
                        if len(grid) == 0:
                            Win = True
                            stats['Wins'] += 1
                            End = True
                        elif head == food:
                            food = random.choice(grid)
                            score += 1
                            stats['Fruit Eaten'] += 1
                            levels[level][1] -= 1
                            if levels[level][1] == 0:
                                level += 1
                        else:
                            grid.append(snakebody[-1])
                            snakebody.pop()
                    else:
                        if head in snakebody[1:]:                            
                            stats['Hit Body'] += 1
                        else:
                            stats['Hit Wall'] += 1
                        End = True
                        Loss = True
                        stats['Deaths'] += 1
        else:
            updatescore(score)                                       

        gameplaydraw()
    
    clock.tick(FPS)
    cycletick += 1