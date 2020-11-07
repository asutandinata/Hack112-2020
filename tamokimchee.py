from cmu_112_graphics import *
import random

# from dataclasses import make_dataclass

def appStarted(app):
    
    app.aquariumL=120
    app.aquariumR=app.width-120
    app.aquariumBot=app.height-350
    app.kimcheeX = app.width/2
    app.kimcheeY = app.height/2
    app.kimcheeSize = None
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
    app.newX, app.newY = 0, 0
    app.swimAnimations = [1,2,3,2]
    app.kimcheei = 0
    app.moving = False
    app.movingDirection = None
    app.timerDelay=10
    app.market = False
    app.wormX, app.wormY = app.width/2, app.height/2
    app.snailX, app.snailY = app.width/2, app.height/2

def resetAxolotlStats(app):
    app.hunger=10
    app.age=0
    app.happiness=8

def mousePressed(app, event):
    if (event.x>app.marketX-(app.marketWidth/2) and event.x<(app.marketX+app.marketWidth/2)
    and event.y>(app.marketY-app.marketHeight/2) and event.y<(app.marketY+app.marketHeight/2)):
        app.market= not app.market
    
    if (app.aquariumL<event.x<app.aquariumR and 100<event.y<app.aquariumBot):
        if not app.moving:
            app.newX, app.newY = event.x, event.y
            app.moving = True

# def keyPressed(app, event):
    # if event.key == "Left":
    #     app.moving = True
    #     app.kimcheeX -= 10

    # elif event.key == "Right":
    #     app.moving = True
    #     app.kimcheeX+=10


# def keyReleased(app, event):
#     app.moving = False

def timerFired(app):
    #seaweed sprite animation
    updateBubbles(app)
    for n in range(len(app.seaweed)):
        x,y,i,s = app.seaweed[n]
        i+=1
        if i>3:
            i=1
        app.seaweed[n]=(x,y,i,s)

    #moving kimchee
    if distance(app.kimcheeX, app.kimcheeY, app.newX, app.newY) > 10:
        app.kimcheei += 1
        app.kimcheei %= len(app.swimAnimations)
        moveKimchee(app)
    else:
        app.moving = False

def moveKimchee(app):
    if app.newX > app.kimcheeX: 
        dx = 1
        app.movingDirection = "l"
    else: 
        dx = -1
        app.movingDirection = "r"
    if app.newY > app.kimcheeY: dy = 1
    else: dy = -1
    app.kimcheeX += dx*10 
    app.kimcheeY += dy*10 
    if distance(app.kimcheeX, app.kimcheeY, app.newX, app.newY) < 10:
        app.kimcheeX = app.newX 
        app.kimcheeY = app.newY
    
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
    swimchee=PhotoImage(file=f"swim{i}{d}.png") 
    canvas.create_image(app.kimcheeX, app.kimcheeY, image=swimchee)
    
def drawKimcheeSmall(app, canvas):
    kimcheeSmall=PhotoImage(file="axolotlSmall.png") 
    canvas.create_image(app.width/2, app.height/2, image=kimcheeSmall)

def drawKimcheeMedium(app, canvas):
    kimcheeMedium=PhotoImage(file="axolotlMedium.png") 
    canvas.create_image(app.width/2 + 200, app.height/2, image=kimcheeMedium)

def drawKimcheeLarge(app, canvas):
    kimcheeLarge=PhotoImage(file="axolotlLarge.png") 
    canvas.create_image(app.width/2 + 400, app.height/2, image=kimcheeLarge)


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

def drawButtons(app, canvas):
    if app.market:
        marketButton=PhotoImage(file='exit.png')
    else:
        marketButton=PhotoImage(file='market.png')
    canvas.create_image(app.marketX, app.marketY, image=marketButton)

def drawFood(app, canvas):
    WormPicture=PhotoImage(file="Worm.png")
    canvas.create_image(app.wormX, app.wormY, image=WormPicture)
    SnailPicture=PhotoImage(file="Snail.png")
    canvas.create_image(app.snailX, app.snailY, image=SnailPicture)

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawDynamicAquarium(app, canvas)
    # drawKimchee(app, canvas)  
    if app.moving:
        drawSwimmingKimchee(app, canvas)
    drawKimcheeSmall(app, canvas)  
    drawKimcheeMedium(app, canvas) 
    drawKimcheeLarge(app, canvas) 
    drawStats(app, canvas)
    drawButtons(app, canvas)
    drawFood(app,canvas)
    
runApp(width=1400, height=1000)