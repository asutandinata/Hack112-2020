from cmu_112_graphics import *
import random
from PIL import Image

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
    resetAxolotlStats(app)
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
    app.coins = 0
    #egg
    app.eggCounter = 0
    app.eggScreenVisible = False
    app.eggX, app.eggY = app.width/2, app.height/2
    Worms, Snails, Seaweed, Moss, Rez, Ball = 0,0,0,0,0,0
    inventory = [Worms, Snails, Seaweed, Moss, Rez, Ball]
    Amount_of_Worms = 0
    Amount_of_Snails = 0
    #play info
    app.timeSincePlay=0
    app.timeBored=1000
    

def resetAxolotlStats(app):
    app.hunger=6
    app.size=0
    app.happiness=3
    app.time=0
    app.growThreshold=1000

def mousePressed(app, event):
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
    if app.market:
        mgn = 75
        grid = 300
        bigmgn = 175
        bigmgn2 = 125
        if (event.x>mgn + bigmgn and event.x<mgn + bigmgn + grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            print("Purchased worm")
        elif (event.x>mgn + bigmgn + grid and event.x<mgn + bigmgn + 2*grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            print("Purchased snail")
        elif (event.x>mgn + bigmgn + 2*grid and event.x<mgn + bigmgn + 3*grid and 
        event.y>mgn*2 + bigmgn2 and event.y<mgn*2 + bigmgn2 + grid):
            print("Purchased seaweed")
        elif (event.x>mgn + bigmgn and event.x<mgn + bigmgn + grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            print("Purchased mossball")
        elif (event.x>mgn + bigmgn + grid and event.x<mgn + bigmgn + 2*grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            print("purchased rez")
        elif (event.x>mgn + bigmgn + 2*grid and event.x<mgn + bigmgn + 3*grid and 
        event.y>bigmgn2 + grid and event.y<mgn*2 + bigmgn2 + grid*2):
            print("purchased ball")            

def keyPressed(app, event):
    if event.key == "Space":
        app.eggScreenVisible = True
    
def hatchEgg(app):
    if app.eggCounter > 10:
        app.gameStarted = True
        app.eggScreenVisible = False
    

def timerFired(app):
    #seaweed sprite animation
    if(app.time%500==0 and app.hunger>0):app.hunger-=1
    app.time+=app.timerDelay
    app.timeSincePlay+=app.timerDelay
    if(app.time==app.growThreshold):
        app.size+=1
        app.time-=app.growThreshold
        if(app.size>2):
            app.size=2

    if app.timeSincePlay==app.timeBored:
        if(app.happiness>0):app.happiness-=2
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
        if(app.happiness<app.maxHappiness):app.happiness+=1
    
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
    canvas.create_rectangle(bigmgn, bigmgn2, 
                            app.width-bigmgn, app.height-bigmgn2, fill="pink")
    #Worm 
    canvas.create_rectangle(mgn + bigmgn, mgn*2 + bigmgn2, 
                            mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid, fill="white")
    worm=PhotoImage(file="wormBig.png")
    canvas.create_image(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid/2, image=worm)
    #Snail
    canvas.create_rectangle(mgn + bigmgn + grid, mgn*2 + bigmgn2, 
                            mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid, fill="white")
    snail=PhotoImage(file="snailBig.png")
    canvas.create_image(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid/2, image=snail)
    #Seaweed
    canvas.create_rectangle(mgn + bigmgn + 2*grid, mgn*2 + bigmgn2, 
                            mgn + bigmgn + 3*grid, mgn*2 + bigmgn2 + grid, fill="white")
    seaweed=PhotoImage(file="seaweedBig.png")
    canvas.create_image(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid/2, image=seaweed)
    #Moss Ball
    canvas.create_rectangle(mgn + bigmgn, mgn*2 + bigmgn2 + grid, 
                            mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid*2, fill="white")
    mossball=PhotoImage(file="mossball.png")
    canvas.create_image(mgn + bigmgn + grid/2, mgn*2 + bigmgn2 + grid*1.5, image=mossball)
    #Rez
    canvas.create_rectangle(mgn + bigmgn + grid, mgn*2 + bigmgn2 + grid, 
                              mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid*2, fill="white")
    rez=PhotoImage(file="rezBig.png")
    canvas.create_image(mgn + bigmgn + grid*1.5, mgn*2 + bigmgn2 + grid*1.5, image=rez)
    #Ball
    canvas.create_rectangle(mgn + bigmgn + 2*grid, mgn*2 + bigmgn2 + grid, 
                              mgn + bigmgn + 3*grid, mgn*2 + bigmgn2 + grid*2, fill="white")
    ball=PhotoImage(file="ballBig.png")
    canvas.create_image(mgn + bigmgn + grid*2.5, mgn*2 + bigmgn2 + grid*1.5, image=ball)

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
    
# def drawKimcheeSmall(app, canvas):
#     kimcheeSmall=PhotoImage(file=f"axolotlSmall.png") 
#     canvas.create_image(app.width/2, app.height/2, image=kimcheeSmall)

# def drawKimcheeMedium(app, canvas):
#     kimcheeMedium=PhotoImage(file="axolotlMedium.png") 
#     canvas.create_image(app.width/2 + 200, app.height/2, image=kimcheeMedium)

# def drawKimcheeLarge(app, canvas):
#     kimcheeLarge=PhotoImage(file="axolotlLarge.png") 
#     canvas.create_image(app.width/2 + 400, app.height/2, image=kimcheeLarge)

def drawSplashScreen(app, canvas):
    splashScreen=PhotoImage(file='splashscreen.png')
    canvas.create_image(app.width/2, app.height/2, image=splashScreen)  

def drawEggScreen(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill="white")
    canvas.create_text(app.width/2, app.height*(3/4),font='arial 24 bold',
                         text="Click on the egg to hatch your axolotl!")
    
    egg=PhotoImage(file='egg1.png')
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
    canvas.create_text(x0-30, y0+(width*3),text=f'Coins: {app.coins}', font='arial 16 bold', anchor='e')

def drawButtons(app, canvas):
    if app.market:
        marketButton=PhotoImage(file='exit.png')
    else:
        marketButton=PhotoImage(file='market.png')
    canvas.create_image(app.marketX, app.marketY, image=marketButton)

def drawFood(app, canvas):
    if app.market:
        WormPicture=PhotoImage(file="Worm.png")
        canvas.create_image(app.wormX-50, app.wormY, image=WormPicture)
    if app.market:
        SnailPicture=PhotoImage(file="Snail.png")
        canvas.create_image(app.snailX+50, app.snailY, image=SnailPicture)
    
    
def redrawAll(app, canvas):
    
    drawBackground(app, canvas)
    drawDynamicAquarium(app, canvas)
    # drawKimchee(app, canvas)  
    if not app.moving:
        drawKimchee(app, canvas)
    else:
        drawSwimmingKimchee(app, canvas)
    if app.market:
        drawMarketScreen(app, canvas)
    

    # drawKimcheeSmall(app, canvas)  
    # drawKimcheeMedium(app, canvas) 
    # drawKimcheeLarge(app, canvas) 

    drawStats(app, canvas)
    drawButtons(app, canvas)
    drawFood(app,canvas)
    
    if not app.gameStarted:
        drawSplashScreen(app, canvas)
        if app.eggScreenVisible:
            drawEggScreen(app, canvas)
    
runApp(width=1400, height=1000)