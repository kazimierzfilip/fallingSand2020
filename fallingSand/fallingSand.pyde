EMPTY = 0
SAND = 1
OBSTACKLE = -1
i = 1
start = False

rows, cols = (100, 100)
canvas = [[EMPTY]*rows for i in range(cols)]
width = 8

sandRows, sandCols = (12, 64)


def setup():
    size(800,600)
    frameRate(120)
    
def mouseClicked():
    if mouseButton == LEFT:
        insertObstackle(mouseX, mouseY)
    elif mouseButton == RIGHT:
        generateSand()
        global start
        start = True    
        
def insertObstackle(x, y):
    canvas[y/width][x/width] = OBSTACKLE
        
def generateSand():
    colOffset = (cols-sandCols)/2
    for row in range(0, sandRows):
        for column in range(0, sandCols):
            if int(random(2))==1:
                canvas[row][column+colOffset] = SAND
            else:
                canvas[row][column+colOffset] = EMPTY
    
def mouseDragged():
    insertObstackle(mouseX, mouseY)
    
def keyPressed():
    img = None
    if key == 'k':
        img = loadImage('klepsydra.png')
    elif key == 'm':
        img = loadImage('miska.png')
    elif key == 'o':
        img = loadImage('okrag.png')
    elif key == 's':
        img = loadImage('skosy.png')
    elif key == 'r':
        global start
        start = False
        clearCanvas()
        
    if img:
        pixels = parseImg(img)
        applyPixels(pixels)
        
def clearCanvas():
    global canvas
    canvas = [[EMPTY]*rows for i in range(cols)]
        
def parseImg(img):
    img.loadPixels()
    list = []
    list = [pixel for pixel in img.pixels]
    pixels = [list[i*img.width:i*img.width+img.width] for i in range(0, img.height)]
    return pixels

def applyPixels(pixels):
    rowOffset = (rows-len(pixels))/2
    colOffset = (cols-len(pixels[0]))/2
    for row in range(0, len(pixels)):
        for column in range(0, len(pixels[row])):
            if pixels[row][column] != -1:
                canvas[row+rowOffset][column+colOffset] = OBSTACKLE

def draw():
    global canvas
    drawCanvas(canvas)
    global i
    global start
    if start:
        sandFall(i, canvas)
        i+=1
                
def drawCanvas(canvas):
    x = 0
    y = 0
    for row in range(0, len(canvas)):
        for column in range(0, len(canvas[row])):
            hideBorder()
            colorCell(canvas[row][column])
            addCell(x, y, width)
            x += width
        y += width
        x = 0
 
def colorCell(cell):
    if cell == SAND:
        fill(255, 224, 102)
    elif cell == OBSTACKLE:
        fill(0, 0, 0)
    elif cell == EMPTY:
        fill(255, 255, 255)
        
def hideBorder():
    noStroke()
    
def addCell(x, y, width):
    rect(x, y, width, width)
    
def sandFall(i, canvas):
    if i%2==0:
        for row in range(1, len(canvas)-1, 2):
            for column in range(1, len(canvas[row])-1, 2):
                changePlaces(canvas, column, column+1, row, row+1)
    else:
        for row in range(0, len(canvas), 2):
            for column in range(0, len(canvas[row]), 2):
                changePlaces(canvas, column, column+1, row, row+1)
                
def changePlaces(canvas, c1, c2, r1, r2):
    if s_eo_e_eos(c1,c2,r1,r2) or s_s_e_os(c1,c2,r1,r2):
        canvas[r1][c1]=EMPTY
        canvas[r2][c1]=SAND
    elif s_s_e_e(c1,c2,r1,r2):
        canvas[r1][c1]=EMPTY
        canvas[r1][c2]=EMPTY
        canvas[r2][c1]=SAND
        canvas[r2][c2]=SAND
    elif eo_s_eos_e(c1,c2,r1,r2) or s_s_os_e(c1,c2,r1,r2):
        canvas[r1][c2]=EMPTY
        canvas[r2][c2]=SAND
    elif s_e_os_e(c1,c2,r1,r2):
        canvas[r1][c1]=EMPTY
        canvas[r2][c2]=SAND
    elif e_s_e_os(c1,c2,r1,r2):
        canvas[r1][c2]=EMPTY
        canvas[r2][c1]=SAND
        
def s_eo_e_eos(c1,c2,r1,r2):
    return (canvas[r1][c1]==SAND and (canvas[r1][c2]==EMPTY or canvas[r1][c2]==OBSTACKLE) 
            and canvas[r2][c1]==EMPTY and (canvas[r2][c2]==EMPTY or canvas[r2][c2]==OBSTACKLE or canvas[r2][c2]==SAND))
    
def s_s_e_os(c1,c2,r1,r2):
    return (canvas[r1][c1]==SAND and canvas[r1][c2]==SAND 
        and canvas[r2][c1]==EMPTY and (canvas[r2][c2]==OBSTACKLE or canvas[r2][c2]==SAND))
    
def s_s_e_e(c1,c2,r1,r2):    
    return (canvas[r1][c1]==SAND and canvas[r1][c2]==SAND and canvas[r2][c1]==EMPTY and canvas[r2][c2]==EMPTY)

def eo_s_eos_e(c1,c2,r1,r2):
    return ((canvas[r1][c1]==EMPTY or canvas[r1][c1]==OBSTACKLE) and canvas[r1][c2]==SAND 
        and (canvas[r2][c1]==EMPTY or canvas[r2][c1]==OBSTACKLE or canvas[r2][c1]==SAND) and canvas[r2][c2]==EMPTY)
    
def s_s_os_e(c1,c2,r1,r2):
    return (canvas[r1][c1]==SAND and canvas[r1][c2]==SAND 
        and (canvas[r2][c1]==OBSTACKLE or canvas[r2][c1]==SAND) and canvas[r2][c2]==EMPTY)

def s_e_os_e(c1,c2,r1,r2):
    return (canvas[r1][c1]==SAND and canvas[r1][c2]==EMPTY 
        and (canvas[r2][c1]==OBSTACKLE or canvas[r2][c1]==SAND) and canvas[r2][c2]==EMPTY)

def e_s_e_os(c1,c2,r1,r2):
    return (canvas[r1][c1]==EMPTY and canvas[r1][c2]==SAND 
        and canvas[r2][c1]==EMPTY and (canvas[r2][c2]==OBSTACKLE or canvas[r2][c2]==SAND))
