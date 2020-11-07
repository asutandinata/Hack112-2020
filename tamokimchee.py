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
    app.seaweed=[(app.aquariumL+100, app.aquariumBot-40,1,'l'), (app.aquariumR-50, app.aquariumBot,2,'s')]
    app.bubbles=[]
    app.bubbleDy=20
    resetAxolotlStats(app)
    app.barWidth=50
    app.maxHunger=10
    app.maxHappiness=10
    app.shiftMarginPositive = [10 + 5*i for i in range(9)]
    app.shiftMarginNegative = [-10 - 5*i for i in range(9)]
    
def resetAxolotlStats(app):
    app.hunger=10
    app.age=0
    app.happiness=8
    

def mousePressed(app, event):
    return

def keyPressed(app, event):
    
    return

def timerFired(app):
    #seaweed sprite animation
    for n in range(len(app.seaweed)):
        x,y,i,s=app.seaweed[n]
        i+=1
        if i>3:
            i=1
        app.seaweed[n]=(x,y,i,s)
    return

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
        if y > 0 and y < 250:
            bubble=PhotoImage(file=BubbleSmall.png)
        elif y >= 250 and y < 500:
            bubble=PhotoImage(file=BubbleMedium.png)
        elif y >= 500 and y < 750:
            bubble=PhotoImage(file=BubbleLarge.png)
        elif y >= 750:
            app.bubbles.pop(index)
        canvas.create_image(x,y,image=bubble)
    
def updateBubbles(app):
    while len(app.bubbles) < 5:
        bubbleX = random.randint(300, 1100)
        bubbleY = random.randint(700, 850)
        app.bubbles.append([bubbleX, bubbleY, 1])
    for bubble in app.bubbles:
        if len(app.shiftMarginPositive) == 0:
           app.shiftMarginPositive == [10 + 5*i for i in range(9)]
        if len(app.shiftMarginNegative) == 0:
           app.shiftMarginNegative == [-10 - 5*i for i in range(9)]
        if bubble[2] == 1:
           upperLimit = len(app.shiftMarginPositive) - 1
           index = random.randint(0, upperLimit)
           bubble[0] += app.shiftMarginPositive.pop(index)
           bubble[1] += 1
        else:
           upperLimit = len(app.shiftMarginNegative) - 1
           index = random.randint(0, upperLimit)
           bubble[0] += app.shiftMarginNegative.pop(index)
           bubble[1] += 1
        bubble[2] *= -1
    
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
    canvas.create_text(x0-30, y0+(width/2), text='Hunger: ',font='arial 18 bold',anchor='e')
    for i in range(app.hunger):
        hunger=PhotoImage(file="hunger.png")
        canvas.create_image(x0+i*width, y0+width/2, image=hunger)
    for i in range(app.maxHunger-app.hunger):
        x1=width*app.hunger+x0*1
        empty=PhotoImage(file="emptyHunger.png")
        canvas.create_image(x1+i*width, y0+width/2, image=empty)
    
    y1=y0+width
    canvas.create_text(x0-30, y1+width/2, text='Happiness: ',font='arial 18 bold',anchor='e')
    for i in range(app.happiness):
        happy=PhotoImage(file="happy.png")
        canvas.create_image(x0+(i*width), y1+width/2, image=happy)
    for i in range(app.maxHappiness-app.happiness+1):
        x1=width*app.happiness+x0*1
        empty=PhotoImage(file="sad.png")
        canvas.create_image(x1+(i*width), y1+width/2, image=empty)       

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    updateBubbles(app)
    drawDynamicAquarium(app, canvas)
    # drawKimchee(app, canvas)  
    drawKimcheeSmall(app, canvas)  
    drawKimcheeMedium(app, canvas) 
    drawKimcheeLarge(app, canvas) 
    drawStats(app, canvas)
    
runApp(width=1400, height=1000)