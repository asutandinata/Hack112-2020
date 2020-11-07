from cmu_112_graphics import *

# from dataclasses import make_dataclass

def appStarted(app):
    app.bubbles=[]
    app.aquariumL=28
    app.aquariumR=app.width-28
    app.aquariumBot=app.height-80-700
    app.kimcheeX = app.width/2
    app.kimcheeY = app.height/2

###############################################################################
#VIEW

def drawBackground(app, canvas):
    table = PhotoImage(file="table.png") 
    canvas.create_image(app.width/2, app.height-80, image=table)
    aquarium=PhotoImage(file='aquarium.png')
    canvas.create_image(app.width/2, app.height/2, image=aquarium)  

def drawDynamicAquarium(app, canvas):
    seaweed1=PhotoImage(file="seaweed-1.png")
    canvas.create_image(app.aquariumL+20, app.aquariumBot-50,image=seaweed1)
    
def drawKimchee(app, canvas):
    kimchee = PhotoImage(file="axolotl.png") 
    canvas.create_image(app.kimcheeX, app.kimcheeY, image=kimchee)
    
def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawDynamicAquarium(app, canvas)
    drawKimchee(app, canvas)    
    
runApp(width=1400, height=1000)