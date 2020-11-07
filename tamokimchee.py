from cmu_112_graphics import *
import random
from PIL import Image
from playsound import playsound
# from dataclasses import make_dataclass

def appStarted(app):
    app.gameStarted = False
  
    app.aquariumL=120
    app.aquariumR=app.width-120
    app.aquariumBot=app.height-350
    app.kimcheeX = app.width/2
    app.kimcheeY = app.height/2
    app.size = 0
    app.seaweed=[(app.aquariumL+100, app.aquariumBot-40,1,'l'), 
                 (app.aquariumR-50, app.aquariumBot,2,'s')]
    app.bubbles=[]
    app.barWidth=50
    app.maxHunger=10
    app.maxHappiness=10
    app.shiftMarginPositive = [10 + 5*i for i in range(9)]
    app.shiftMarginNegative = [-10 - 5*i for i in range(9)]
    app.marketWidth=150
    app.marketHeight=75
    app.marketX, app.marketY=app.width-100, 80
    #moving
    app.newX, app.newY = app.kimcheeX, app.kimcheeY
    app.swimAnimations = [1,2,3,2]
    app.kimcheeSizes = ["s", "m", "l"]
    app.kimcheei = 0
    app.moving = False
    app.movingDirection = None
    app.timerDelay=10
    app.market = False
    app.wormX, app.wormY = app.width/2, app.height/2
    app.snailX, app.snailY = app.width/2, app.height/2
    app.kimcheeToggle = True
    app.Coins = 999
    #egg
    app.eggCounter = 0
    app.eggScreenVisible = False
    app.eggX, app.eggY = app.width/2, app.height/2
    app.inventory=dict()
    app.inventory['worms']=1
    app.inventory['snails']=1
    app.inventory['seaweed']=1
    app.inventory['moss']=1
    app.inventory['rez']=1
    app.inventory['ball']=1
    app.inventory['log']=1
    app.inventory['flag']=1
    app.inventory['beer']=1
    app.inventory['dragon']=1
    app.inventory['taylor']=1
    app.inventory['kosbie']=1
    #play info
    app.timeSincePlay=0
    app.timeBored=1000
    app.marketPageOne = True
    app.marketPageTwo = False 

    #help
    app.helpx, app.helpy = app.width - 50, app.height - 50
    app.helpVisible = False
    #coin
    app.coinX=random.randint(app.aquariumL, app.aquariumR)
    app.coinY=random.randint(app.aquariumBot-400,app.aquariumBot)
    app.coinTime=0
    app.CoinsearchTime=750
    resetAxolotlStats(app)

    #drag
    app.drawnItems = []
    app.currentx, app.currenty = 0,0
    app.draggedItemX, app.draggedItemY = 0,0
    app.currentImage = None
    app.dragging = False
    app.drawDraggedItem = False

def resetAxolotlStats(app):
    app.hunger=8
    app.size=0
    app.happiness=5
    app.time=0
    app.growThreshold=1000
    app.gameOver=False

def mousePressed(app, event):
    if distance(event.x, event.y, app.helpx, app.helpy) < 15:
        app.helpVisible = not app.helpVisible
    if app.eggScreenVisible:
        if distance(event.x, event.y, app.eggX, app.eggY) < 300:
            app.eggCounter += 1
            hatchEgg(app)
            
    if (event.x>app.marketX-(app.marketWidth/2) and event.x<(app.marketX+app.marketWidth/2)
    and event.y>(app.marketY-app.marketHeight/2) and event.y<(app.marketY+app.marketHeight/2)):
        app.market= not app.market
    
    if (app.aquariumL<event.x<app.aquariumR and 100<event.y<app.aquariumBot) and not app.moving:
            app.newX, app.newY = event.x, event.y
            app.timeSincePlayed=0
            app.moving = not app.moving
            if app.newX > app.kimcheeX: 
                app.movingDirection = "r"
            else: 
                app.movingDirection = "l"
    if app.market and app.marketPageOne:
        mgn = 75
        grid = 300
        bigmgn = 175
        bigmgn2 = 125
        if (event.x>mgn + bigmgn and event.x<mgn + bigmgn + grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            if app.Coins >= 5:
                app.Coins -= 5
                app.inventory['worms']+=1
            else:
                print("No Money")
            
        elif (event.x>mgn + bigmgn + grid and event.x<mgn + bigmgn + 2*grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            if app.Coins >= 10:
                app.Coins -= 10
                app.inventory['snails']+=1
            else:
                print("No Money")
            
        elif (event.x>mgn + bigmgn + 2*grid and event.x<mgn + bigmgn + 3*grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            if app.Coins >= 25:
                app.Coins -= 25
                app.inventory['seaweed']+=1
                
            else:
                print("No Money")
            
            
        elif (event.x>mgn + bigmgn and event.x<mgn + bigmgn + grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            if app.Coins >= 25:
                app.Coins -= 25              
                app.inventory['moss']+=1
            else:
                print("No Money")
                
        elif (event.x>mgn + bigmgn + grid and event.x<mgn + bigmgn + 2*grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            if app.Coins >= 25:
                app.Coins -= 25
                app.inventory['rez']+=1
                
            else:
                print("No Money")
                
        elif (event.x>mgn + bigmgn + 2*grid and event.x<mgn + bigmgn + 3*grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            if app.Coins >= 25:
                app.inventory['ball']+=1
                app.Coins -= 25
            else:
                print("No Money")  
    elif app.market and app.marketPageTwo:
        mgn = 75
        grid = 300
        bigmgn = 175
        bigmgn2 = 125
        if (event.x>mgn + bigmgn and event.x<mgn + bigmgn + grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            if app.Coins >= 25:
                app.Coins -= 25
                app.inventory['log']+=1
            else:
                print("No Money")
            
        elif (event.x>mgn + bigmgn + grid and event.x<mgn + bigmgn + 2*grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            if app.Coins >= 25:
                app.Coins -= 25
                app.inventory['flag']+=1
            else:
                print("No Money")
            
        elif (event.x>mgn + bigmgn + 2*grid and event.x<mgn + bigmgn + 3*grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            if app.Coins >= 25:
                app.Coins -= 25
                app.inventory['beer']+=1
                
            else:
                print("No Money")
            
            
        elif (event.x>mgn + bigmgn and event.x<mgn + bigmgn + grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            if app.Coins >= 25:
                app.Coins -= 25              
                app.inventory['dragon']+=1
            else:
                print("No Money")
                
        elif (event.x>mgn + bigmgn + grid and event.x<mgn + bigmgn + 2*grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            if app.Coins >= 25:
                app.Coins -= 25
                app.inventory['taylor']+=1
                
            else:
                print("No Money")
                
        elif (event.x>mgn + bigmgn + 2*grid and event.x<mgn + bigmgn + 3*grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            if app.Coins >= 25:
                app.inventory['kosbie']+=1
                app.Coins -= 25
            else:
                print("No Money")  

    if not app.dragging and not app.market and ((app.aquariumL+100< event.x < app.aquariumR -100) and 
                app.aquariumBot + 250 < event.y < app.height):
        app.dragging = True  
        app.currentx, app.currenty = event.x, event.y      

def mouseDragged(app, event):
    if app.dragging:
        currentList = []
        for key in app.inventory:
            if app.inventory[key] > 0:
                currentList.append(key)
        # if (app.aquariumL+100<app.currentx<app.aquariumR-100) and (app.aquariumBot+250<app.currenty<app.height):

        if getItem(app, app.currentx, app.currenty, currentList) != False:
            app.currentImage = getItem(app, app.currentx, app.currenty, currentList)
            app.drawDraggedItem = True
        app.draggedItemX, app.draggedItemY = event.x, event.y

def mouseReleased(app, event):
    if app.dragging == True:
        app.dragging = False
        placeImage(app)

def placeImage(app):
    app.drawnItems += [(app.draggedItemX, app.draggedItemY, app.currentImage)]
    app.drawDraggedItem = False

def getItem(app, x, y, currentList):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    x0=app.aquariumL+100
    y0=app.aquariumBot+250

    cellWidth  = 80
    cellHeight = 100

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    if (x<x0) or (x>app.aquariumR - 100) or (y<y0):
        return

    
    row = int((x - x0) / cellWidth)
    if row < len(currentList):
        return currentList[row]
    else: 
        return False


def keyPressed(app, event):
    if event.key == "Space":
        app.eggScreenVisible = True
    if app.market:
        if event.key == "1":
            app.marketPageOne = True
            app.marketPageTwo = False
        elif event.key == "2":
            app.marketPageOne = False
            app.marketPageTwo = True
    
def hatchEgg(app):
    if app.eggCounter > 11:
        app.gameStarted = True
        app.eggScreenVisible = False
        resetAxolotlStats(app)

def placeCoin(app):
    app.coinX=random.randint(app.aquariumL, app.aquariumR)
    app.coinY=random.randint(app.aquariumBot-400,app.aquariumBot)
    
def timerFired(app):
    #seaweed sprite animation
    if not app.market:
        if(app.time%1000==0 and app.hunger>0):app.hunger-=1
        app.time+=app.timerDelay
        app.timeSincePlay+=app.timerDelay
        app.coinTime+=app.timerDelay
        if(app.coinTime==app.CoinsearchTime):
            placeCoin(app)
        if(distance(app.kimcheeX, app.kimcheeY, app.coinX, app.coinY)<50): 
            app.Coins+=5
            app.coinTime=0
            placeCoin(app)
        if(app.time==app.growThreshold):
            app.size+=1
            app.time-=app.growThreshold
            if(app.size>2):
                app.size=2

        if app.timeSincePlay==app.timeBored:
            if(app.happiness>0):app.happiness-=1
            app.newX, app.newY = random.randint(app.aquariumL, app.aquariumR), random.randint(app.aquariumBot-500,app.aquariumBot)
            app.timeSincePlay=0
            app.moving = not app.moving
            if app.newX > app.kimcheeX: 
                app.movingDirection = "r"
            else: 
                app.movingDirection = "l"
        updateBubbles(app)
        for n in range(len(app.seaweed)):
            x,y,i,s = app.seaweed[n]
            i+=1
            if i>3:
                i=1
            app.seaweed[n]=(x,y,i,s)
        if app.hunger==0 or app.happiness==0:
            app.gameOver=True

        #bouncing up and down
        if not app.moving:
            if app.kimcheeToggle:
                app.kimcheeY += 5
                app.kimcheeToggle = not app.kimcheeToggle
            else:
                app.kimcheeY -= 5
                app.kimcheeToggle = not app.kimcheeToggle

        #moving kimchee
        if app.moving and distance(app.kimcheeX, app.kimcheeY, app.newX, app.newY) > 25:
            app.kimcheei += 1
            app.kimcheei %= len(app.swimAnimations)
            moveKimchee(app)
        else:
            app.moving = False

def moveKimchee(app):
    if app.newX > app.kimcheeX: 
        dx = 1
    else: 
        dx = -1
    if app.newY > app.kimcheeY: dy = 1
    else: dy = -1
    app.kimcheeX += dx*10 
    app.kimcheeY += dy*10 
    if distance(app.kimcheeX, app.kimcheeY, app.newX, app.newY) < 20:
        app.kimcheeX = app.newX 
        app.kimcheeY = app.newY
        app.happiness+=1
        app.timeSincePlay=0
    
def distance(x0, y0, x1, y1):
    return ((x1-x0)**2+(y1-y0)**2)**(0.5)
    
def updateBubbles(app):
    while len(app.bubbles) < 5:
        bubbleX = random.randint(100, 1300)
        bubbleY = random.randint(600, 750)
        app.bubbles.append([bubbleX, bubbleY, 1])
    index =  0
    while index < len(app.bubbles):
        bubble = app.bubbles[index]
        if bubble[1] <= 400 or bubble[0] < 75 or bubble[0] >= 1325:
            app.bubbles.pop(index)
        else:
            bubble[0] += random.randint(-50,50)
            bubble[1] -= random.randint(10,30)
        index+=1

###############################################################################
#VIEW

def drawBackground(app, canvas):
    table = PhotoImage(file="table.png") 
    canvas.create_image(app.width/2, app.height-80, image=table)
    aquarium=PhotoImage(file='aquarium.png')
    canvas.create_image(app.width/2, app.height/2, image=aquarium)  

def drawMarketScreen(app, canvas):
    mgn = 75
    grid = 300
    bigmgn = 175
    bigmgn2 = 125
    if app.market and app.marketPageOne:
        canvas.create_rectangle(bigmgn, bigmgn2, 
                                app.width-bigmgn, app.height-bigmgn2, fill="pink")
        canvas.create_text(app.width/2, bigmgn2 + 50, text="Market", font="arial 50 bold")
        canvas.create_text(app.width/2, bigmgn2 + 100,
                            text="Press 1,2, to switch between pages", font="arial 20 bold")
        #Worm 
        canvas.create_rectangle(mgn + bigmgn, mgn*2 + bigmgn2, 
                                mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid, fill="white")
        canvas.create_text(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + 20,
                            text="Worms", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid - 20,
                            text="5", font="arial 20 bold")
        worm=PhotoImage(file="wormBig.png")
        canvas.create_image(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid/2, image=worm)
        #Snail
        canvas.create_rectangle(mgn + bigmgn + grid, mgn*2 + bigmgn2, 
                                mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid, fill="white")
        canvas.create_text(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + 20,
                            text="Snails", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid - 20,
                            text="10", font="arial 20 bold")
        snail=PhotoImage(file="snailBig.png")
        canvas.create_image(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid/2, image=snail)
        #Seaweed
        canvas.create_rectangle(mgn + bigmgn + 2*grid, mgn*2 + bigmgn2, 
                                mgn + bigmgn + 3*grid, mgn*2 + bigmgn2 + grid, fill="white")
        canvas.create_text(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + 20,
                            text="Seaweed", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid - 20,
                            text="20", font="arial 20 bold")
        seaweed=PhotoImage(file="seaweedBig.png")
        canvas.create_image(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid/2, image=seaweed)
        #Moss Ball
        canvas.create_rectangle(mgn + bigmgn, mgn*2 + bigmgn2 + grid, 
                                mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid*2, fill="white")
        canvas.create_text(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid + 20,
                            text="Moss Balls", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid*2 - 20,
                            text="20", font="arial 20 bold")
        mossball=PhotoImage(file="mossball.png")
        canvas.create_image(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid*1.5, image=mossball)
        #Rez
        canvas.create_rectangle(mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid, 
                                mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid*2, fill="white")
        canvas.create_text(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid + 20,
                            text="Rez on Fifth", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid*2 - 20,
                            text="20", font="arial 20 bold")
        rez=PhotoImage(file="rezBig.png")
        canvas.create_image(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid*1.5, image=rez)
        #Ball
        canvas.create_rectangle(mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid, 
                                mgn + bigmgn + 3*grid, mgn*2 + bigmgn2 + grid*2, fill="white")
        canvas.create_text(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid + 20,
                            text="Mystery Ball", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid*2 - 20,
                            text="20", font="arial 20 bold")
        ball=PhotoImage(file="ballBig.png")
        canvas.create_image(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid*1.5, image=ball)
    elif app.market and app.marketPageTwo:
        canvas.create_rectangle(bigmgn, bigmgn2, 
                                app.width-bigmgn, app.height-bigmgn2, fill="pink")
        canvas.create_text(app.width/2, bigmgn2 + 50, text="Market", font="arial 50 bold")
        canvas.create_text(app.width/2, bigmgn2 + 100,
                            text="Press 1,2, to switch between pages", font="arial 20 bold")
        #Log 
        canvas.create_rectangle(mgn + bigmgn, mgn*2 + bigmgn2, 
                                mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid, fill="white")
        canvas.create_text(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + 20,
                            text="Log", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid - 20,
                            text="5", font="arial 20 bold")
        log=PhotoImage(file="logBig.png")
        canvas.create_image(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid/2, image=log)
        #Flag
        canvas.create_rectangle(mgn + bigmgn + grid, mgn*2 + bigmgn2, 
                                mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid, fill="white")
        canvas.create_text(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + 20,
                            text="Flag", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid - 20,
                            text="10", font="arial 20 bold")
        flag=PhotoImage(file="flagBig.png")
        canvas.create_image(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid/2, image=flag)
        #Beer
        canvas.create_rectangle(mgn + bigmgn + 2*grid, mgn*2 + bigmgn2, 
                                mgn + bigmgn + 3*grid, mgn*2 + bigmgn2 + grid, fill="white")
        canvas.create_text(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + 20,
                            text="Beer", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid - 20,
                            text="20", font="arial 20 bold")
        beer=PhotoImage(file="beerBig.png")
        canvas.create_image(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid/2, image=beer)
        #Dragon
        canvas.create_rectangle(mgn + bigmgn, mgn*2 + bigmgn2 + grid, 
                                mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid*2, fill="white")
        canvas.create_text(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid + 20,
                            text="Dragon", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid*2 - 20,
                            text="20", font="arial 20 bold")
        dragon=PhotoImage(file="dragonBig.png")
        canvas.create_image(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid*1.5, image=dragon)
        #Taylor
        canvas.create_rectangle(mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid, 
                                mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid*2, fill="white")
        canvas.create_text(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid + 20,
                            text="Taylor", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid*2 - 20,
                            text="20", font="arial 20 bold")
        taylor=PhotoImage(file="taylorBig.png")
        canvas.create_image(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid*1.5, image=taylor)
        #Kosbie
        canvas.create_rectangle(mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid, 
                                mgn + bigmgn + 3*grid, mgn*2 + bigmgn2 + grid*2, fill="white")
        canvas.create_text(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid + 20,
                            text="Kosbie", font="arial 20 bold")
        canvas.create_text(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid*2 - 20,
                            text="20", font="arial 20 bold")
        kosbie=PhotoImage(file="kosbieBig.png")
        canvas.create_image(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid*1.5, image=kosbie)

def drawDynamicAquarium(app, canvas):
    for x,y,i,l in app.seaweed:
            seaweed=PhotoImage(file=f"seaweed{i}{l}.png")
            canvas.create_image(x,y,image=seaweed)
    for index in range(len(app.bubbles)):
        bubble = app.bubbles[index]
        x, y = bubble[0], bubble[1]
        if y <= 400 or x < 75 or x >= 1325:
            pass
        elif y <= 500 and y > 400:
            bubbleImage=PhotoImage(file='BubbleLarge.png')
            canvas.create_image(x,y,image=bubbleImage)
        elif y <= 600 and y > 500:
            bubbleImage=PhotoImage(file="BubbleMedium.png")
            canvas.create_image(x,y,image=bubbleImage)
        else:
            bubbleImage=PhotoImage(file="BubbleSmall.png")
            canvas.create_image(x,y,image=bubbleImage)

def drawSwimmingKimchee(app, canvas):
    i = app.swimAnimations[app.kimcheei]
    d = app.movingDirection
    size = app.kimcheeSizes[app.size]
    swimchee=PhotoImage(file=f"{size}swim{i}{d}.png") 
    canvas.create_image(app.kimcheeX, app.kimcheeY, image=swimchee)

def drawKimchee(app, canvas):
    size = app.kimcheeSizes[app.size]
    kimchee=PhotoImage(file=f"{size}front.png") 
    canvas.create_image(app.kimcheeX, app.kimcheeY, image=kimchee)

def drawSplashScreen(app, canvas):
    splashScreen=PhotoImage(file='splashscreen.png')
    canvas.create_image(app.width/2, app.height/2, image=splashScreen)
    canvas.create_text(app.width-400,app.height/2+50, text='Press space to begin!',font='arial 30 bold')  

def drawEggScreen(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill="white")
    canvas.create_text(app.width/2, app.height*(3/4),font='arial 24 bold',
                         text="Click on the egg to hatch your axolotl!")
    i = int(app.eggCounter/3) + 1
    egg=PhotoImage(file=f'egg{i}.png')
    canvas.create_image(app.eggX, app.eggY,image=egg)  

def drawStats(app, canvas):
    x0,y0=150,10
    width=app.barWidth
    canvas.create_text(x0-30, y0+(width/2), text='Hunger: ',font='arial 16 bold',anchor='e')
    for i in range(app.hunger):
        hunger=PhotoImage(file="hunger.png")
        canvas.create_image(x0+i*width, y0+width/2, image=hunger)
    for i in range(app.maxHunger-app.hunger):
        x1=width*app.hunger+x0*1
        empty=PhotoImage(file="emptyHunger.png")
        canvas.create_image(x1+i*width, y0+width/2, image=empty)
    
    y1=y0+width
    canvas.create_text(x0-30, y1+width/2, text='Happiness: ',font='arial 16 bold',anchor='e')
    for i in range(app.happiness):
        happy=PhotoImage(file="happy.png")
        canvas.create_image(x0+(i*width), y1+width/2, image=happy)
    for i in range(app.maxHappiness-app.happiness):
        x1=width*app.happiness+x0*1
        empty=PhotoImage(file="sad.png")
        canvas.create_image(x1+(i*width), y1+width/2, image=empty) 
    coin=PhotoImage(file='coin.png')
    canvas.create_image(x0, y0+(width*3), image=coin)
    canvas.create_text(x0-30, y0+(width*3),text=f'Coins: {app.Coins}', font='arial 16 bold', anchor='e')

def drawButtons(app, canvas):
    if app.market:
        marketButton=PhotoImage(file='exit.png')
    else:
        marketButton=PhotoImage(file='market.png')
    canvas.create_image(app.marketX, app.marketY, image=marketButton)

# def drawFood(app, canvas):
#     if app.market:
#         WormPicture=PhotoImage(file="Worm.png")
#         canvas.create_image(app.wormX-50, app.wormY, image=WormPicture)
#     if app.market:
#         SnailPicture=PhotoImage(file="Snail.png")
#         canvas.create_image(app.snailX+50, app.snailY, image=SnailPicture)
    
def drawHelpButton(app, canvas):
    cx, cy = app.width - 50, app.height - 50
    canvas.create_oval(cx-15, cy-15, cx+15,cy+15, fill="red")   
    canvas.create_text(cx,cy, text="?",font='arial 24 bold', fill="white")
    canvas.create_text(cx-30,cy,anchor="e", text="click for help") 
    
def drawHelp(app, canvas):
    help=PhotoImage(file="help.png")
    canvas.create_image(app.width/2, app.height/2, image=help)

def drawCoin(app, canvas):
    coin=PhotoImage(file='coin.png')
    canvas.create_image(app.coinX, app.coinY, image=coin)

def drawInventory(app, canvas):
    x0=app.aquariumL+100
    y0=app.aquariumBot+250
    canvas.create_text(app.width/2, y0-40, text='Inventory', font='arial 18 bold' )
    index=0
    for item in app.inventory:
        if(app.inventory[item]>0):
            icon=PhotoImage(file=f'{item}Inventory.png')
            canvas.create_image(x0+80*index, y0, image=icon)
            number=app.inventory[item]
            canvas.create_text(x0+80*index, y0+40, text=str(number), font='arial 12 bold')
            index+=1

def drawDraggedItem(app, canvas):
    if app.currentImage=='worms' or 'snail':
        icon=PhotoImage(file=f'{app.currentImage}Inventory.png')
        canvas.create_image(app.draggedItemX, app.draggedItemY, image=icon)
    elif app.currentImage=='seaweed':
        icon=PhotoImage(file=f'seaweed1l.png')
        canvas.create_image(app.draggedItemX, app.draggedItemY, image=icon)
    else:
        icon=PhotoImage(file=f'{app.currentImage}.png')
        canvas.create_image(app.draggedItemX, app.draggedItemY, image=icon)

def drawDrawnItems(app, canvas):
    for x,y,item in app.drawnItems:
        icon=PhotoImage(file=f'{item}.png')
        canvas.create_image(x,y, image=icon)
    
def redrawAll(app, canvas):
    if app.gameStarted:
        drawBackground(app, canvas)
        drawDynamicAquarium(app, canvas)
        drawCoin(app, canvas)
        drawInventory(app, canvas)
        # drawKimchee(app, canvas) 
        if not app.moving:
            drawKimchee(app, canvas)
        else:
            drawSwimmingKimchee(app, canvas)
        if app.market:
            drawMarketScreen(app, canvas)

        
        drawStats(app, canvas)
        drawButtons(app, canvas)
        if app.drawDraggedItem:
             drawDraggedItem(app,canvas)
        drawDrawnItems(app,canvas)

    if not app.gameStarted:
        drawSplashScreen(app, canvas)
        if app.eggScreenVisible:
            drawEggScreen(app, canvas)
    #help
    drawHelpButton(app, canvas)
    if app.helpVisible:
        drawHelp(app,canvas)
    

#
runApp(width=1400, height=1000)