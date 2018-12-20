import pygame
""" showText and renderText are similar but one returns the box coordinates in
order to be used later and the other just shows the text without retuning
anything"""
def renderText(surface,text,fontStyle,fontSize,pos,textColor=(0,0,0),bgColor=None):
    fontObject = pygame.font.Font(fontStyle, fontSize)
    textSurfaceObject = fontObject.render(text, True, textColor ,bgColor)
    textRectObject = textSurfaceObject.get_rect()
    textRectObject.center = pos
    surface.blit(textSurfaceObject, textRectObject)
    return([textRectObject.topleft,textRectObject.bottomright])

def showText(surface,text,fontStyle,fontSize,pos,textColor=(0,0,0),bgColor=None):
    fontObject = pygame.font.Font(fontStyle, fontSize)
    textSurfaceObject = fontObject.render(text, True, textColor,bgColor)
    textRectObject = textSurfaceObject.get_rect()
    textRectObject.center = pos
    surface.blit(textSurfaceObject, textRectObject)

""" showImage and renderImage are similar but one returns the box coordinates in
order to be used later and the other just shows the Image without retuning
anything""" 
def renderImage(surface,imgSrc,pos,angle = 0):
    image = pygame.image.load(imgSrc)
    image = pygame.transform.rotate(image,angle)
    imageRect = image.get_rect()
    imageRect.center = pos
    surface.blit(image, imageRect)
    return([imageRect.topleft,imageRect.bottomright])

def showImage(surface,imgSrc,pos,angle = 0):
    image = pygame.image.load(imgSrc)
    image = pygame.transform.rotate(image,angle)
    imageRect = image.get_rect()
    imageRect.center = pos
    surface.blit(image, imageRect)

""" values_in_rect checks whether mousex and mousey are in a rectangle """ 
def values_in_rect(x,y,rect):
    if (x > rect[0][0])and(x < rect[1][0])and(y > rect[0][1])and(y < rect[1][1]):
        return (True)
    else :
        return(False)

""" Create the Grid lists so that we make it easier to blit pictures """
def createGrid(startingPos,width,height,nbrLine,nbrColomn,gap=0):
    listRect = [[(startingPos[0]+j*(width+gap),startingPos[1]+i*(gap+height)),(startingPos[0]+(j+1)*(width+gap),startingPos[1]+(i+1)*(height+gap))] for i in range(nbrLine) for j in range(nbrColomn)]
    listPosCenter = [((listRect[j+i*nbrColomn][1][0]+listRect[j+i*nbrColomn][0][0])//2,(listRect[j+i*nbrColomn][1][1]+listRect[j+i*nbrColomn][0][1])//2) for i in range(nbrLine) for j in range(nbrColomn)]
    return(listRect , listPosCenter)
                     
""" The snake class that controlls everything from memorizing location to moving rendering and checking collisions """
class Snake(object):
    def __init__(self,startingPos,width = 10,height = 10,gap = 1,nbr = 4):
        self.listRect = [[(startingPos[0]+i*(width+gap),startingPos[1]),(startingPos[0]+(i+1)*(width+gap),startingPos[1]+(height+gap))] for i in range(nbr)]
        self.listPosCenter = [((self.listRect[i][1][0]+self.listRect[i][0][0])//2,(self.listRect[i][1][1]+self.listRect[i][0][1])//2) for i in range(nbr)]
        self.particularLengths = [width,height,gap]
        self.len = nbr
        
    def addtoTale(self,Rect,Center):
        self.len +=1
        self.listRect.insert(0,Rect)
        self.listPosCenter.insert(0,Center)
    def isColide(self,posTarget):
        if self.listPosCenter[self.len -1 ] == posTarget:
            return(True)
        else :
            return(False)
    def futureHeadPos(self,direction,border = None):
        head = self.listPosCenter[self.len -1]
        newHead = (direction == 'z')*(head[0],head[1]-(self.particularLengths[1]+self.particularLengths[2]))
        newHead +=(direction == 's')*(head[0],head[1]+(self.particularLengths[1]+self.particularLengths[2]))
        newHead +=(direction == 'q')*(head[0]-(self.particularLengths[0]+self.particularLengths[2]),head[1])
        newHead +=(direction == 'd')*(head[0]+(self.particularLengths[0]+self.particularLengths[2]),head[1])
        if border == None:
            return(newHead)
        else :
            return(border[1])
    def updateList(self,direction,border = None): #only use z,q,s,d for directions whatever are controls
        head = self.listRect[self.len -1]
        self.listRect = [self.listRect[i+1] for i in range(self.len -1)]
        newHead = (direction == 'z')*[(head[0][0],head[0][1]-(self.particularLengths[1]+self.particularLengths[2])),(head[1][0],head[1][1]-(self.particularLengths[1]+self.particularLengths[2]))]
        newHead +=(direction == 's')*[(head[0][0],head[0][1]+(self.particularLengths[1]+self.particularLengths[2])),(head[1][0],head[1][1]+(self.particularLengths[1]+self.particularLengths[2]))] 
        newHead +=(direction == 'q')*[(head[0][0]-(self.particularLengths[0]+self.particularLengths[2]),head[0][1]),(head[1][0]-(self.particularLengths[0]+self.particularLengths[2]),head[1][1])]
        newHead +=(direction == 'd')*[(head[0][0]+(self.particularLengths[0]+self.particularLengths[2]),head[0][1]),(head[1][0]+(self.particularLengths[0]+self.particularLengths[2]),head[1][1])]
        if border ==None:
            self.listRect.append(newHead)
        else :
            self.listRect.append(border[0])
        
        
        head = self.listPosCenter[self.len -1]
        self.listPosCenter = [self.listPosCenter[i+1] for i in range(self.len -1)]
        newHead = (direction == 'z')*(head[0],head[1]-(self.particularLengths[1]+self.particularLengths[2]))
        newHead +=(direction == 's')*(head[0],head[1]+(self.particularLengths[1]+self.particularLengths[2]))
        newHead +=(direction == 'q')*(head[0]-(self.particularLengths[0]+self.particularLengths[2]),head[1])
        newHead +=(direction == 'd')*(head[0]+(self.particularLengths[0]+self.particularLengths[2]),head[1])
        if border == None:
            self.listPosCenter.append(newHead)
        else :
            self.listPosCenter.append(border[1])
    def isDead(self,direction): #for the moment the only way to die is by hiting himself
        if self.listPosCenter[self.len -1 ] in self.listPosCenter[0:self.len -2 ]:
            return(True)
        else:
            return(False)
    def show(self,surface,imageSrcHead,imageSrcBody,angle = 0):
        for i in range(0,self.len - 1):
            showImage(surface,imageSrcBody,self.listPosCenter[i])
        showImage(surface,imageSrcHead,self.listPosCenter[self.len - 1],angle)
    
        
        
                                   
        
