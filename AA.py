#contient le système pyxel d'affichage et de MaJ des variables du jeu
import pyxel as px
import random as rd
import time as time
import math as math
import scriptrunner as sc
import importlib as imp
import pygame


px.init(5*128, 3*128, "algorythmic adventure")
px.load("textures.pyxres")

pygame.mixer.init()
pygame.mixer.music.load("igm\\main.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)
pygame.mixer.set_num_channels(100)

played=-1 # used to prevent some musics from resetting on level reset

#ne pas toucher
mainframe=0
uiframe=0

beaten=False
#vfx for ????
glitchframe=0
glitches=[]

switchtoremix=False #used to switch to remix mode when the player reaches the alternate path

insequence=False #wether the player is in an algorithmic sequence
step=0 #the step in the algorythm
delay=0 #the delay (in frames) elapsed
maxdelay=10 #the max delay before starting the next instruction (in frames)

#used for the switch effect animation
switcheffectanimx=0
switcheffectanimy=0
switchboost=30 #boosts the scrolling speed on switch

#conveyers : move the player one tile in the targetted direction if the target tile is valid
conveyor_up=[]
conveyor_down=[]
conveyor_left=[]
conveyor_right=[]

#redconveyers only work in red state, blue conveyers only work in blue state
red_conveyor_up=[]
red_conveyor_down=[]
red_conveyor_left=[]
red_conveyor_right=[]

blue_conveyor_up=[]
blue_conveyor_down=[]
blue_conveyor_left=[]
blue_conveyor_right=[]


# sounds :
# 0 : movement
# 1 : rotation
# 2 : switches
# 3 : box move
# 4 : box settling
# 5 : forbidden movement

#variables globales du jeu
position_x = 0
position_y = 0
doppleposition_x = 0
doppleposition_y = 0
animate=False
doline=0
linelist=[]
#list of sublists : [y,width,dither,movespeed]

# wether controls are enabled of not
play = True
# used for the level animation
playframe = 999


#wether to use doppleganger mechanics
doppleon=False

#this is for the alternate path
remix=False

baseposition_x = 0
baseposition_y = 0

dopplebaseposition_x = 0
dopplebaseposition_y = 0

heading = 1 # 0 : up, 1 : right, 2 : down, 3 : left
doppleheading = 3 # 0 : up, 1 : right, 2 : down, 3 : left
level=-3
#level=int(input("select level"))-1
finished=True
zoom=3

# final tile
endtile=[0,0]
doppleendtile=[0,0]

#list of valid tiles for movement
validtiles=[]

#tiles that chip away when stepped on
breakable3=[]
breakable2=[]
breakable1=[]
broken=[]

#tiles that only exist when switches have the corresponding colour state
bluetiles=[]
redtiles=[]

#rotators that only trigger when switches have the corresponding colour state
#red and blue refer to the state in which they are active, left and right to their direction

rightrotators_blue=[]
leftrotators_blue=[]
rightrotators_red=[]
leftrotators_red=[]

#rotators that change direction when switches are toggled
#left and right refer to their initial direction (in a red state)
rightrotators_switch=[]
leftrotators_switch=[]

#starting tile for the doppleganger
dopple_start=[]


speed=0.5

#state of switches and switch tiles
switches=[]
switchstate=False
# for remix mode
altstate=False
# true : green state, false : yellow state

#two states : red (False) and blue (True)

#zones that instantly reset the level when stepped on
killzones=[]

#spikes that are active when the switch is off/on and vice versa, kills the player on contact if active
spikelist=[]
reversespikelist=[]

#rotators that always trigger
leftrotators=[]
rightrotators=[]

#state of the level exit (locked/unlocked) and list of trigger tiles
unlocked=True
#3 values : x and y position, boolean for wether the tile has been triggered
#if all tiles are triggered, the level exit is enabled
triggertiles=[]

# variable to set mode to manual (cheat code, used for debugging)
manual=False

# partial walls : cannot go on a partial wall from a certain direction : partial_left : can't go to it from the left
partial_left=[]
partial_right=[]
partial_up=[]
partial_down=[]

# boxes : pushable blocks, if a box lands on a boxhole, it fills the hole and the tile becomes walkable (move the box coordinates to settledboxes with the boxhole coordinates, remove the boxhole from boxholes and the box from boxes), boxes can trigger switches
boxes=[]
boxholes=[]
settledboxes=[]
halfboxes=[]#pushable boxes that cannot fill boxholes, made specifically for that one elite ball knowledge level
#box rules : cannot push a box into another box, if trying to, revert the player to the previous tile, cannot push a box off the valid tiles, if trying to, revert the player to the previous tile.

# movable killtiles : have no collisions with boxes, the player, or the dopple, behaves like a killtile except it can be moved by conveyors
movablekilltiles=[]
vanitykilltiles=[]
#these have no collision its to display the shitty collision of the other killtiles

#switch conveyors : conveyors that move in the opposite direction in blue state : leftswitchconveyor moves left on red state and right on blue state

leftswitchconveyor=[]
rightswitchconveyor=[]
upswitchconveyor=[]
downswitchconveyor=[]

#switch module : its just a switch with a different texture behaves the same

switchmodules=[]

# stuff for altstate :
altleftrotators=[]
altrightrotators=[]
altkillzones=[]
yellow_conveyor_up=[]
yellow_conveyor_down=[]
yellow_conveyor_left=[]
yellow_conveyor_right=[]
green_conveyor_up=[]
green_conveyor_down=[]
green_conveyor_left=[]
green_conveyor_right=[]
altconveyorswitch_up=[]
altconveyorswitch_down=[]
altconveyorswitch_left=[]
altconveyorswitch_right=[]
altswitchmodules=[]
altswitches=[]
greentiles=[]
yellowtiles=[]
left_altrotatorswitch=[]
right_altrotatorswitch=[]
altswitchboost=30
altswitcheffectanimx=0
altswitcheffectanimy=0


# [x,y,rotation]
#for rotations : 0 = up, 1 = right, 2 = down, 3 = left
redlaser=[]
bluelaser=[]
yellowlaser=[]
greenlaser=[]

# [x,y,rotation]
#for rotations : 0 = horizontal, 1 = vertical
redbeam=[]
bluebeam=[]
yellowbeam=[]
greenbeam=[]

# [x,y,rotation]
#for rotations : 0 = up, 1 = right, 2 = down, 3 = left
redbeamend=[]
bluebeamend=[]
yellowbeamend=[]
greenbeamend=[]

# [x,y,rotation]
#for rotations : 0 = up/right , 1 = right/down , 2 = down/left , 3 = left/up
redcornerbeam=[]
bluecornerbeam=[]
greencornerbeam=[]
yellowcornerbeam=[]


#------ Block behaviours functions to be used in runsequence.py -------
def speedchangecheck():
    global speed
    if px.btnr(px.KEY_LSHIFT):
        speed=0.1
    if px.btnr(px.KEY_LCTRL):
        speed=0.5
def singleforward():
    global position_x, position_y, heading,validtiles,doppleposition_x,doppleposition_y,doppleon,doppleheading,play
    if play==True:
        if heading == 0:
            if [position_x, position_y-1] in validtiles:
                position_y -= 1
                px.play(0,0)
            else:
                px.play(1,5)
        elif heading == 1:
            if [position_x+1, position_y] in validtiles:
                position_x += 1
                px.play(0,0)
            else:
                px.play(1,5)
        elif heading == 2:
            if [position_x, position_y+1] in validtiles:
                position_y += 1
                px.play(0,0)
            else:
                px.play(1,5)
        elif heading == 3:
            if [position_x-1, position_y] in validtiles:
                position_x -= 1
                px.play(0,0)
            else:
                px.play(1,5)
        if doppleon==True:
            if doppleheading == 0:
                if [doppleposition_x, doppleposition_y-1] in validtiles:
                    doppleposition_y -= 1
                    px.play(0,0)
                else:
                    px.play(1,5)
            elif doppleheading == 1:
                if [doppleposition_x+1, doppleposition_y] in validtiles:
                    doppleposition_x += 1
                    px.play(0,0)
                else:
                    px.play(1,5)
            elif doppleheading == 2:
                if [doppleposition_x, doppleposition_y+1] in validtiles:
                    doppleposition_y += 1
                    px.play(0,0)
                else:
                    px.play(1,5)
            elif doppleheading == 3:
                if [doppleposition_x-1, doppleposition_y] in validtiles:
                    doppleposition_x -= 1
                    px.play(0,0)
                else:
                    px.play(1,5)
        blockeffects()
        conveyoreffects()
        killtiles()
        unlockedexit()
        
def forward(steps):
    global play,level,speed
    if play==True:
        for _ in range(steps):
            singleforward()
            draw()
            px.flip()
            unlockedexit()
            

def wait():
    blockeffects()
    conveyoreffects()
    killtiles()
    unlockedexit()

def turnright():
    global heading,doppleheading,doppleon,play
    if play==True :
        heading = (heading + 1) % 4
        if doppleon==True:
            doppleheading = (doppleheading + 1) % 4
        px.play(2,1)

        unlockedexit()

def turnleft():
    global heading,doppleheading,doppleon,play
    if play==True:
        heading = (heading - 1) % 4
        if doppleon==True:
            doppleheading = (doppleheading - 1) % 4
        px.play(2,1)

        unlockedexit()

#manual switch for debugging
def manualswitch():
    global manual
    if px.btnp(px.KEY_M):
        manual= not manual


#------ reset functions -------
def resetlevel():
    global halfboxes,yellowtiles,greentiles,position_x,vanitykilltiles, position_y, heading,switchstate,broken,leftswitchconveyor,rightswitchconveyor,upswitchconveyor,downswitchconveyor,doppleposition_x,doppleposition_y,triggertiles,unlocked,dopplebaseposition_x,dopplebaseposition_y,conveyor_up,conveyor_down,conveyor_left,conveyor_right,red_conveyor_up,red_conveyor_down,red_conveyor_left,red_conveyor_right,blue_conveyor_up,blue_conveyor_down,blue_conveyor_left,blue_conveyor_right,altstate,upswitchconveyor,downswitchconveyor,leftswitchconveyor,rightswitchconveyor,switchmodules,movablekilltiles,vanitykilltiles,halfboxes,altleftrotators,altrightrotators,altkillzones,yellow_conveyor_up,yellow_conveyor_down,yellow_conveyor_left,yellow_conveyor_right,green_conveyor_up,green_conveyor_down,green_conveyor_left,green_conveyor_right,altconveyorswitch_up,altconveyorswitch_down,altconveyorswitch_left,altconveyorswitch_right,altswitchmodules,altswitches,yellowlaser,greenlaser,bluelaser,redlaser,yellowbeam,greenbeam,bluebeam,redbeam,yellowbeamend,greenbeamend,bluebeamend,redbeamend,yellowcornerbeam,greencornerbeam,bluecornerbeam,redcornerbeam
    conveyor_up.clear()
    conveyor_down.clear()
    conveyor_left.clear()
    conveyor_right.clear()
    red_conveyor_up.clear()
    red_conveyor_down.clear()
    red_conveyor_left.clear()
    red_conveyor_right.clear()
    blue_conveyor_up.clear()
    blue_conveyor_down.clear()
    blue_conveyor_left.clear()
    blue_conveyor_right.clear()
    triggertiles = []
    breakable3.clear()
    breakable2.clear()
    breakable1.clear()
    switches.clear()
    spikelist.clear()
    reversespikelist.clear()
    leftrotators.clear()
    rightrotators.clear()
    killzones.clear()
    redtiles.clear()
    bluetiles.clear()
    leftrotators_blue.clear()
    rightrotators_blue.clear()
    leftrotators_red.clear()
    rightrotators_red.clear()
    leftrotators_switch.clear()
    rightrotators_switch.clear()
    partial_down.clear()
    partial_up.clear()
    partial_left.clear()
    partial_right.clear()
    boxes.clear()
    boxholes.clear()
    settledboxes.clear()
    switchstate=False
    altstate=False
    upswitchconveyor.clear()
    downswitchconveyor.clear()
    leftswitchconveyor.clear()
    rightswitchconveyor.clear()
    switchmodules.clear()
    movablekilltiles.clear()
    vanitykilltiles.clear()
    halfboxes.clear()
    altleftrotators.clear()
    altrightrotators.clear()
    altkillzones.clear()
    yellow_conveyor_up.clear()
    yellow_conveyor_down.clear()
    yellow_conveyor_left.clear()
    yellow_conveyor_right.clear()
    green_conveyor_up.clear()
    green_conveyor_down.clear()
    green_conveyor_left.clear()
    green_conveyor_right.clear()
    altconveyorswitch_up.clear()
    altconveyorswitch_down.clear()
    altconveyorswitch_left.clear()
    altconveyorswitch_right.clear()
    altswitchmodules.clear()
    altswitches.clear()
    yellowtiles.clear()
    greentiles.clear()
    yellowlaser.clear()
    greenlaser.clear()
    bluelaser.clear()
    redlaser.clear()
    yellowbeam.clear()
    greenbeam.clear()
    bluebeam.clear()
    redbeam.clear()
    yellowbeamend.clear()
    greenbeamend.clear()
    bluebeamend.clear()
    redbeamend.clear()
    yellowcornerbeam.clear()
    greencornerbeam.clear()
    bluecornerbeam.clear()
    redcornerbeam.clear()

    
    lvproperties()
    position_x = 0
    position_y = 0
    doppleposition_x = dopplebaseposition_x
    doppleposition_y = dopplebaseposition_y
    heading = 1
    broken=[]
    unlockedexit()

def fullreset():
    global level
    level = 0
    resetlevel()
if px.btnp(px.KEY_R):
    if px.btn(px.KEY_LSHIFT):
        fullreset()
    else:
        resetlevel()


#------ level settings -------
def lvproperties():
    global yellowlaser,greenlaser,bluelaser,redlaser,yellowbeam,greenbeam,bluebeam,redbeam,yellowbeamend,greenbeamend,bluebeamend,redbeamend,yellowcornerbeam,greencornerbeam,bluecornerbeam,redcornerbeam,greentiles,yellowtiles,halfboxes,baseposition_x,manual,played,vanitykilltiles, baseposition_y, position_x, position_y, heading,zoom,level,validtiles,endtile,leftrotators,rightrotators,breakable1,breakable2,breakable3,broken,switches,switchstate,spikelist,reversespikelist,triggertiles,unlocked,killzones,redtiles,bluetiles,leftrotators_blue,rightrotators_blue,leftrotators_red,rightrotators_red,leftrotators_switch,rightrotators_switch,dopplebaseposition_x,dopplebaseposition_y,doppleon,doppleheading,doppleposition_x,doppleposition_y,doppleendtile,partial_right,partial_left,partial_down,partial_up,boxes,boxholes,settledboxes,conveyor_up,conveyor_down,conveyor_left,conveyor_right,red_conveyor_up,red_conveyor_down,red_conveyor_left,red_conveyor_right,blue_conveyor_up,blue_conveyor_down,blue_conveyor_left,blue_conveyor_right,leftswitchconveyor,rightswitchconveyor,upswitchconveyor,downswitchconveyor,movablekilltiles,switchmodules,altstate,upswitchconveyor,downswitchconveyor,leftswitchconveyor,rightswitchconveyor,switchmodules,movablekilltiles,vanitykilltiles,halfboxes,altleftrotators,altrightrotators,altkillzones,yellow_conveyor_up,yellow_conveyor_down,yellow_conveyor_left,yellow_conveyor_right,green_conveyor_up,green_conveyor_down,green_conveyor_left,green_conveyor_right,altconveyorswitch_up,altconveyorswitch_down,altconveyorswitch_left,altconveyorswitch_right,altswitchmodules,altswitches
    if level==-2:
        zoom=3
        baseposition_x=0
        baseposition_y=0
        endtile= [1,0]
        validtiles=[[1,0]]
        manual=True
    if not remix:
        if level == 0:
            manual=False
            zoom=3
            baseposition_x = 1
            baseposition_y = 3.5
            position_x = baseposition_x
            position_y = baseposition_y
            heading = 1
            validtiles = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0]]
            endtile = [5,0]

        if level == 1:
            zoom=3
            baseposition_x = 1
            baseposition_y = 1
            position_x = baseposition_x
            position_y = baseposition_y
            heading = 1
            validtiles = [[0,0],[1,0],[2,0],[3,0],[4,0],[4,1],[4,2],[4,3],[4,4],[3,4],[2,4],[2,3],[2,2],[1,2],[0,2]]
            endtile = [0,2]

        if level == 2:
            zoom=3
            baseposition_x = 2
            baseposition_y = 1.5
            position_x = baseposition_x
            position_y = baseposition_y
            heading = 1
            validtiles = [[0,0],[1,0],[2,0],[3,0],[1,1],[3,1],[1,2],[2,2],[3,2],[3,3],[3,4]]
            endtile = [3,4]
            global triggertiles
            triggertiles = [[3,0,False]]
        
        if level == 3:
            zoom=3
            baseposition_x = 1
            baseposition_y = 1
            position_x = baseposition_x
            position_y = baseposition_y
            heading = 1
            validtiles = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[1,2],[2,2],[3,2],[4,2],[5,2],[0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[5,1],[5,3],[1,1],[1,3]]
            endtile = [0,4]
            triggertiles = [[3,0,False],[3,2,False],[3,4,False]]

        if level == 4 :
            zoom=3
            baseposition_x = 1
            baseposition_y = 3.5
            position_x = baseposition_x
            position_y = baseposition_y
            heading = 1

            # valid tiles : 0,0 to 6,0 /// 6,-1 to 6,-3 /// 4,-3 and 5,-3 /// 4,-2 to 4,3 /// 3,-1 to 3,1
            # end tile on 4,3
            #breakable 3 on 2,0, breakable 2 on 3,0, breakable 1 on 4,0
            # triggertile on 6,0

            validtiles = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[6,-1],[6,-2],[6,-3],[5,-3],[4,-3],[4,-2],[4,-1],[4,1],[4,2],[4,3],[3,-1],[3,1]]
            endtile = [4,3]
            breakable3=[[2,0]]
            breakable2=[[3,0]]
            breakable1=[[4,0]]
            triggertiles = [[6,0,False]]

        if level == 5 :
            zoom=3
            baseposition_x = 0.5
            baseposition_y = 1.5
            position_x = baseposition_x
            position_y = baseposition_y
            heading = 1

            # valid tiles : from 0,0 to 6,0 /// from 2,0 to 4,5 (3x5 rectangle)
            # regular tiles : 1,0 and 5,0
            #start tile at 0,0
            # end tile on 6,0
            #trigger tiles on 3,1 , 2,2 ,3,3 and 4,4

            validtiles = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[2,1],[3,1],[4,1],[2,2],[3,2],[4,2],[2,3],[3,3],[4,3],[2,4],[3,4],[4,4]]
            endtile = [6,0]
            triggertiles = [[3,1,False],[2,2,False],[3,3,False],[4,4,False]]
            breakable1 = [[2,0],[3,0],[4,0],[2,1],[4,1],[3,2],[4,2],[2,3],[4,3],[2,4],[3,4]]
            

        if level == 6 :
            zoom=3
            baseposition_x = 1
            baseposition_y = 4.5
            position_x = baseposition_x
            position_y = baseposition_y
            heading = 1


            validtiles = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[0,-1],[1,-1],[2,-1],[3,-1],[4,-1],[5,-1],[0,-2],[1,-2],[2,-2],[3,-2],[4,-2],[5,-2]]
            endtile = [5,0]
            killzones = [[0,-2],[1,-2],[2,-2],[3,-2],[4,-2],[5,-2],[0,-1],[5,-1],[2,0],[3,0]]

        if level == 7 :
            zoom=3
            baseposition_x =1
            baseposition_y =5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1

            validtiles = [[0,0],[1,0],[2,0],[3,0],[3,-1],[3,-2],[4,-2],[5,-2]]
            leftrotators = [[3,0]]
            rightrotators = [[3,-2]]
            endtile = [5,-2]
        
        if level == 8 :
            zoom=3
            baseposition_x =0.5
            baseposition_y =3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1

            validtiles = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[2,-1],[4,1]]
            killzones = [[2,-1],[4,1]]
            leftrotators = [[2,0]]
            rightrotators = [[4,0]]
            endtile = [6,0]
        
        if level ==9 :
            zoom=3
            baseposition_x =0.5
            baseposition_y =0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=True
            dopple_start=[6,6]
            dopplebaseposition_x=dopple_start[0]
            dopplebaseposition_y=dopple_start[1]
            doppleheading=3

            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[6,1],[6,2],[6,3],[6,4],[5,4],[4,4],[3,4],[3,3],[3,2],[2,2],[1,2],[0,2],[0,3],[0,4],[0,5],[0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6]]
            endtile=[3,3]
            doppleendtile=[3,3]
            triggertiles=[[6,3,False],[3,6,False]]

        if level ==10 :
            zoom=3
            baseposition_x =0.5
            baseposition_y =0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=True
            dopple_start=[6,6]
            dopplebaseposition_x=dopple_start[0]
            dopplebaseposition_y=dopple_start[1]
            doppleheading=3

            triggertiles=[[3,2,False],[5,2,False]]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[1,1],[2,1],[3,1],[4,1],[5,1],[1,2],[2,2],[3,2],[4,2],[5,2],[1,4],[2,4],[3,4],[4,4],[5,4],[1,5],[2,5],[3,5],[4,5],[5,5],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6]]
            killzones=[[2,4],[4,4],[5,4],[1,6],[4,6]]
            endtile=[4,0]
            doppleendtile=[2,6]

        if level == 11:
            zoom=3
            baseposition_x =0.5
            baseposition_y =0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=True
            dopple_start=[6,6]
            dopplebaseposition_x=dopple_start[0]
            dopplebaseposition_y=dopple_start[1]
            doppleheading=3

            leftrotators=[[4,0],[6,4]]
            rightrotators=[[5,0],[4,6]]
            endtile=[5,2]
            doppleendtile=[6,3]
            validtiles=[[1,0],[2,0],[3,0],[4,0],[5,0],[5,1],[5,2],[6,6],[5,6],[4,6],[4,5],[4,4],[5,4],[6,4],[6,3]]

        if level == 12:
            zoom=3
            baseposition_x =0.5
            baseposition_y =4.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False

            endtile=[6,0]
            switches=[[2,-2]]
            bluetiles=[[4,0],[5,0]]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[6,0],[2,-1],[2,-2]]
        
        if level == 13:
            zoom=3
            baseposition_x =0.5
            baseposition_y =6.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False

            endtile=[6,0]
            switches=[[5,-6]]
            redtiles=[[1,-1],[1,-2]]
            bluetiles=[[5,-1]]
            spikelist=[[5,0],[5,-2],[5,-3],[4,-3],[3,-3],[2,-3],[2,-4],[2,-5],[3,-5],[4,-5],[5,-5]]
            reversespikelist=[[1,-3],[1,-4],[1,-5],[1,-6],[2,-6],[3,-6],[4,-6],[5,-4],[4,-4],[3,-4]]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[1,-1],[1,-2],[5,-2],[1,-3],[2,-3],[3,-3],[4,-3],[5,-3],[1,-4],[2,-4],[3,-4],[4,-4],[5,-4],[1,-5],[2,-5],[3,-5],[4,-5],[5,-5],[1,-6],[2,-6],[3,-6],[4,-6],[5,-6]]

        if level == 14:
            zoom=3
            baseposition_x =0.5
            baseposition_y =3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False

            endtile=[6,2]
            switches=[[6,0],[3,2]]
            triggertiles=[[6,-2,False]]
            bluetiles=[[1,1],[1,-1]]
            redtiles=[[5,2]]
            rightrotators_red=[[5,-2],[3,0]]
            rightrotators_blue=[[3,-2],[2,0]]
            leftrotators_red=[[2,-2],[4,0]]
            leftrotators_blue=[[5,0],[4,-2]]
            leftrotators_switch=[[2,2]]
            rightrotators_switch=[[4,2]]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[1,2],[2,2],[3,2],[4,2],[5,2],[1,-2],[2,-2],[3,-2],[4,-2],[5,-2],[6,2],[6,-2]]

        if level == 15:
            zoom=3
            baseposition_x =0.5
            baseposition_y =3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False

            endtile=[6,0]
            partial_left=[[2,0]]
            partial_right=[[4,0]]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[1,-1],[2,-1]]
        
        if level == 16:
            zoom=3
            baseposition_x =0.5
            baseposition_y =3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False

            endtile=[6,0]
            partial_up=[[2,0],[1,1],[3,1],[6,1]]
            partial_down=[[0,-1],[1,-1],[4,-1],[5,-1],[6,-1],[4,0],[5,0]]
            partial_left=[[1,0],[3,0],[2,-1],[3,-1],[2,1],[4,1]]
            partial_right=[[0,1],[5,-1]]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[0,-1],[1,-1],[2,-1],[3,-1],[4,-1],[5,-1],[6,-1]]
        
        if level == 17:
            zoom=3
            baseposition_x =0.5
            baseposition_y =3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[6,0]
            boxes=[[2,0]]
            boxholes=[[5,0]]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[6,0]]

        if level == 18:
            zoom=3
            baseposition_x =0.5
            baseposition_y =3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[5,-3]
            boxes=[[1,0],[3,1],[5,0],[5,-1]]
            boxholes=[[2,0],[5,3],[5,-2],[4,-1]]
            validtiles=[[0,0],[1,0],[3,0],[3,1],[3,2],[3,3],[2,2],[2,3],[4,3],[5,2],[5,1],[5,0],[5,-1],[6,1],[6,0],[6,-1],[5,-3]]

        if level == 19:
            zoom=2
            baseposition_x =.5
            baseposition_y =.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[7,10]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[7,0],[2,1],[3,1],[4,1],[6,1],[7,1],[8,1],[2,2],[5,2],[6,2],[2,3],[4,3],[6,3],[7,3],[1,4],[2,4],[4,4],[3,4],[6,4],[6,5],[2,5],[4,7],[5,7],[6,7],[7,7],[8,7],[9,7],[4,8],[5,8],[6,8],[7,8],[8,8],[9,8],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9],[4,10],[5,10],[6,10],[7,10],[8,10],[9,10],[4,6],[5,6],[6,6],[7,6],[8,6],[9,6]]
            switches=[[4,0],[4,3],[1,4]]
            redtiles=[[3,4]]
            bluetiles=[[5,4]]
            killzones=[[3,0],[5,2],[7,3],[2,5],[4,6],[4,7],[4,8],[4,9],[4,10],[5,10],[6,10],[6,9],[7,9],[7,6],[7,7],[6,7],[9,6],[9,7],[9,8],[9,9],[9,10]]
            spikelist=[[2,2]]
            rightrotators=[[2,4],[6,3]]
            leftrotators=[[6,2]]
            partial_down=[[6,5]]
            triggertiles=[[8,1,False],[8,6,False],[5,9,False]]

        if level == 20:
            zoom=2
            baseposition_x=0.5
            baseposition_y=1
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[10,2]
            validtiles=[[1,-1],[3,-1],[4,-1],[5,-1],[6,-1],[1,0],[3,0],[6,0],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[1,2],[3,2],[10,2],[1,3],[10,3],[3,4],[10,4],[3,5],[10,5],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6],[10,6],[4,7],[5,7],[10,7],[0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[9,8],[10,8]]
            killzones=[[1,3],[1,6],[6,6],[4,7]]
            boxholes=[[3,3]]
            boxes=[[6,0]]
            switches=[[0,8]]
            conveyor_left=[[4,1],[5,1],[6,1]]
            bluetiles=[[0,9],[1,9],[2,9],[3,9],[4,9]]
            conveyor_down=[[1,-1],[1,0],[1,1],[1,2]]
            conveyor_right=[[2,6],[3,6],[4,6],[5,6]]
            conveyor_up=[[10,6],[10,5],[10,4],[10,3],[10,7]]
            blue_conveyor_left=[[1,8],[2,8],[3,8]]
            red_conveyor_left=[[6,8],[7,8],[8,8],[9,8]]


        if level == 21:
            zoom=2
            baseposition_x=0.5
            baseposition_y=.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[10,3]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[5,1],[5,2],[5,3],[5,4],[4,4],[3,4],[2,4],[2,3],[2,2],[3,2],[0,2],[0,3],[0,4],[0,5],[0,6],[2,5],[2,6],[2,7],[3,7],[4,7],[4,6],[4,8],[5,8],[6,8],[6,9],[6,7],[7,7],[8,7],[8,8],[8,9],[8,10],[9,10],[10,10],[8,6],[8,5],[9,5],[10,4],[10,3],[10,9],[10,8],[10,7],[10,6]]
            boxes=[[0,5],[9,10]]
            killzones=[[4,6],[6,9]]
            switchmodules=[[0,2],[0,6]]
            upswitchconveyor=[[0,2],[0,3],[0,4],[0,5],[0,6],[4,7]]
            downswitchconveyor=[[6,8]]
            red_conveyor_up=[[10,10],[10,9]]
            blue_conveyor_up=[[10,8],[10,6],[10,7]]
            triggertiles=[[3,2,False]]
            boxholes=[[10,5]]
            spikelist=[[3,0]]
            redtiles=[[3,4],[4,4]]
            reversespikelist=[[5,0],[5,1],[5,2],[2,2],[2,3]]


        if level == 22:
            zoom=3
            baseposition_x=0.5
            baseposition_y=3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[6,0]
            validtiles=[[6,0],[0,0],[1,-3],[2,-3],[3,-3],[4,-3],[5,-3],[1,-2],[2,-2],[3,-2],[4,-2],[5,-2],[1,-1],[2,-1],[3,-1],[4,-1],[5,-1],[1,0],[2,0],[3,0],[4,0],[5,0],[1,1],[2,1],[3,1],[4,1],[5,1],[1,2],[2,2],[3,2],[4,2],[5,2],[1,3],[2,3],[3,3],[4,3],[5,3],]
            killzones=[[1,-3],[1,-2],[1,-1],[1,1],[1,2],[1,3],[5,-1],[5,-2],[5,-3],[5,1],[5,2],[5,3],[3,-2],[3,-1],[3,0],[3,-2]]
            conveyor_down=[[2,-3],[2,-2],[2,-1],[2,0],[2,1],[2,2]]
            conveyor_up=[[4,3],[4,2],[4,1],[4,0],[4,-1],[4,-2]]
            conveyor_left=[[4,-3],[3,-3]]
            conveyor_right=[[2,3],[3,3]]
            movablekilltiles=[[2,-1],[4,1]]
        
        if level == 40:
            zoom=2
            baseposition_x=0.5
            baseposition_y=.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[10,8]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],
                        [2,1],[3,1],[5,1],
                        [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],
                        [1,3],[2,3],[4,3],[5,3],[6,3],[7,3],[3,3],
                        [0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[8,4],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[8,5],[9,5],[10,5],
                        [0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6],[8,6],[9,6],[10,6],[7,6],
                        [0,7],[1,7],[5,7],[6,7],[7,7],[8,7],[9,7],[10,7],
                        [0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[10,8],
                        [0,9],[1,9],[2,9],[3,9],[4,9],[10,9],
                        [0,10],[1,10],[2,10],[3,10],[4,10],[5,10],[6,10],[8,10],[9,10],[10,10],[7,10]]
            switches=[[2,0],[4,2],[4,4],[5,10]]
            breakable1=[[6,9]]
            triggertiles=[[0,2,False],[5,7,False],[7,7,False]]
            redtiles=[[4,3],[8,6],[9,6]]
            bluetiles=[[1,1],[4,1],[7,5],[6,9],[7,9],[8,9],[9,9],[9,8]]
            switchmodules=[[2,5],[0,8]]
            killzones=[[0,4],[3,0],[1,4],[2,4],[1,6],[2,6],[3,6],[4,6],[5,6],[1,7],[1,8],[2,8],[3,8],[4,8],[0,10],[1,10],[2,10],[3,10],[6,7],[8,7],[6,8],[7,8],[8,8],[10,7]]
            conveyor_down=[[6,4],[0,5],[0,6],[0,7],[0,8]]
            conveyor_left=[[1,5],[2,5],[3,5],[4,5],[5,5],[6,5]]
            conveyor_right=[[0,9],[1,9],[2,9],[3,9],[4,9]]
            boxes=[[5,4]]
            boxholes=[[5,9]]
            spikelist=[[2,1],[3,1],[1,3],[2,3],[3,3],[5,3],[8,4],[8,5],[9,5],[10,5],[10,6],[5,8],[4,10]]
            reversespikelist=[[1,0],[4,0],[5,0],[1,2],[2,2],[3,2],[5,1],[5,2],[6,3],[7,3],[7,4],[3,4],[6,6],[7,6],[6,10],[7,10],[8,10],[9,10],[10,10],[10,9]]

        if level==41:
            zoom=2
            baseposition_x=0.5
            baseposition_y=0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[0,6]
            validtiles=[[2,0],[3,0],[4,0],
                        [0,1],
                        [0,2],[1,2],[2,2],[3,2],[4,2],[6,2],[7,2],[8,2],[9,2],[10,2],
                        [0,3],[1,3],[2,3],[4,3],[6,3],[7,3],[8,3],[9,3],[10,3],
                        [0,4],[1,4],[2,4],[4,4],[5,4],[6,4],[7,4],[8,4],[9,4],[10,4],
                        [6,5],[7,5],[8,5],[9,5],[10,5],
                        [0,6],[2,6],[3,6],[4,6],[5,6],[6,6],[7,6],[8,6],[9,6],[10,6],
                        [1,7],[2,7],[3,7],[4,7],[5,7],[6,7],[7,7],[8,7],[9,7],[10,7],
                        [1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[9,8],[10,8],
                        [1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9],[10,9],
                        [1,10],[2,10],[3,10],[4,10],[5,10],[6,10],[7,10],[8,10],[9,10],[10,10],]
            leftswitchconveyor=[[2,0],[3,0],[4,0]]
            switchmodules=[[2,0],[4,0]]
            boxes=[[3,0]]
            breakable1=[[0,1],[0,4],[6,3]]
            partial_down=[[10,5]]
            leftrotators=[[0,2],[0,3]]
            killzones=[[1,2],[6,2],[7,2],[8,2],[9,2],[10,2],
                    [1,3],[6,3],
                    [6,5],[7,5],[8,5],[9,5],
                    [1,7],[2,7],[3,7],[5,7],[6,7],[8,7],[9,7],[10,7],
                    [1,9],[2,9],[3,9],[5,9],[6,9],[8,9],[9,9],[10,9],
                    [1,8],[5,8],[6,8],[10,8],
                    [1,10],[10,10]]
            upswitchconveyor=[[7,4],[8,3],[10,3]]
            downswitchconveyor=[[9,4]]
            redtiles=[[5,4],[2,6]]
            bluetiles=[[1,6]]
            triggertiles=[[2,8,False],[2,10,False],[9,8,False],[9,10,False]]
            spikelist=[[1,4],[2,4],[3,2],[4,3],[8,8],[3,10]]
            reversespikelist=[[2,2],[4,2],[2,3],[4,4],[3,8],[8,10]]
            conveyor_down=[[7,6],[7,7],[7,8],[7,9]]
            conveyor_up=[[4,10],[4,9],[4,8],[4,7]]
            conveyor_left=[[5,10],[6,10],[7,10]]
            conveyor_right=[[4,6],[5,6],[6,6]]
        
        if level==  42:
            zoom=2
            baseposition_x=0
            baseposition_y=0
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[11,9]
            validtiles=[[0,0],[1,0],[2,0],[4,0],[5,0],[6,0],[7,0],[9,0],[10,0],[11,0],
                        [0,1],[1,1],[2,1],[4,1],[5,1],[6,1],[7,1],[9,1],[10,1],[11,1],[3,1],
                        [0,2],[1,2],[2,2],[4,2],[5,2],[6,2],[7,2],[9,2],[10,2],[11,2],
                        [0,4],[1,4],[2,4],[4,4],[5,4],[6,4],[7,4],[9,4],[10,4],[11,4],[3,4],
                        [0,5],[1,5],[2,5],[4,5],[5,5],[6,5],[7,5],[3,5],
                        [0,6],[1,6],[2,6],[4,6],[5,6],[6,6],[7,6],[9,6],[10,6],[11,6],[3,6],[8,6],
                        [0,7],[1,7],[2,7],[4,7],[5,7],[6,7],[7,7],[9,7],[10,7],[11,7],
                        [0,9],[1,9],[2,9],[4,9],[5,9],[6,9],[7,9],[9,9],[10,9],[11,9],[8,9],
                        [0,10],[1,10],[2,10],[4,10],[5,10],[6,10],[7,10],[9,10],[10,10],[11,10],
                        [0,11],[1,11],[2,11],[4,11],[5,11],[6,11],[7,11],[9,11],[10,11],[11,11],[3,11],
                        [6,3],[10,3],[4,8],[10,8]]
            breakable1=[[3,1],[6,3],[8,6],[10,8],[8,9],[3,5],[3,6]]
            breakable2=[[3,4],[10,3],[4,8],[3,11]]
            triggertiles=[[11,0,False],[7,0,False],[2,9,False]]
            killzones=[[1,0],[1,1],[4,2],[5,1],[6,1],[5,7],[6,7],[7,7],[1,10],[2,10]]
            boxholes=[[9,5],[10,5],[11,5]]
            boxes=[[10,6]]
            switches=[[0,7]]
            leftrotators=[[1,9],[5,11]]
            rightrotators=[[5,9],[1,11]]
            red_conveyor_down=[[9,2],[10,2],[11,2]]
            spikelist=[[1,4],[5,4],[7,4],
                    [1,5],[7,5],
                    [0,6],[1,6],[5,6],[6,6],[7,6],
                    [4,10],[5,10],[6,10]]
            reversespikelist=[[0,4],[4,4],[0,5],[2,5],[4,5],[5,5],[6,5],[2,6],[1,7],[2,7],[4,7]]

        if level == 43:
            zoom=2
            baseposition_x=0.5
            baseposition_y=.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=True
            endtile=[5,5]
            doppleendtile=[5,5]
            dopple_start=[10,10]
            dopplebaseposition_x=dopple_start[0]
            dopplebaseposition_y=dopple_start[1]
            doppleheading=3
            validtiles=[[x,y] for x in range(11) for y in range(11) if y!=5 or x==5]
            killzones=[[7,0],[8,0],[9,0],
                    [1,1],[2,1],[3,1],
                    [1,2],[8,2],
                    [1,3],[4,3],[6,3],
                    [6,4],
                    [1,6],[2,6],[3,6],
                    [2,7],[9,7],
                    [4,8],
                    [0,9],[8,9],
                    [0,10],[5,10],[6,10]
                    ]
            triggertiles=[[2,2,False],[8,1,False],[7,3,False],[0,6,False],[3,7,False],[7,8,False],[1,9,False]]

        if level==44:
            zoom=2
            baseposition_x=0.5
            baseposition_y=0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[8,5]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],
                        [3,1],[4,1],[5,1],[6,1],
                        [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],[7,2],[8,2],[9,2],
                        [0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],[8,3],[9,3],
                        [0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[8,4],[9,4],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],
                        [0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6],[8,6],
                        [0,7],[1,7],[2,7],[3,7],[4,7],[5,7],[6,7],[7,7],[8,7],
                        [0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],
                        [0,9],[1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9]
                        ]
            partial_down=[[3,0]]
            partial_up=[[3,1],[7,7]]
            partial_right=[[3,4]]
            switches=[[4,4]]
            boxholes=[[7,6]]
            triggertiles=[[0,2,False],[8,3,False],[0,8,False]]
            killzones=[[1,2],[4,2],[7,2],[8,2],[9,2],
                    [1,3],[3,3],[4,3],[9,3],
                    [7,4],[8,4],[9,4],
                    [1,5],[3,5],[4,5],[5,5],[6,5],
                    [1,6],[8,6],
                    [1,7],[2,7],[3,7],[4,7],[5,7],[6,7],[8,7],
                    [9,8],
                    [0,9],[1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9]]
            spikelist=[[4,0],[5,0],[6,0],
                    [6,1],[6,2],
                    [1,4],[5,4],[6,4]]
            reversespikelist=[[4,1],[5,1],[5,2],[5,3],[7,3],[0,5],[0,6]]
            leftrotators=[[1,8],[3,8],[5,8]]
            rightrotators=[[2,8],[4,8],[6,8]]
            boxes=[[2,5]]
            switchmodules=[[6,6]]
            conveyor_right=[[2,6],[3,6],[4,6],[5,6],[6,6]]

        if level==45:
            zoom=2
            baseposition_x=0.5
            baseposition_y=0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[10,6]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],
                        [2,1],[3,1],[4,1],[5,1],[6,1],
                        [2,2],[3,2],[4,2],[5,2],[6,2],
                        [1,3],[2,3],[3,3],[4,3],[5,3],[6,3],
                        [1,4],[2,4],[3,4],[4,4],[5,4],[6,4],
                        [1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],
                        [0,6],[1,6],[2,6],[4,6],[5,6],[6,6],[7,6],[8,6],[9,6],[10,6],
                        [2,7],[4,7],[5,7],[6,7],[7,7],[8,7],
                        [1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],
                        [1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],
                        [1,10],[2,10],[4,10]]
            killzones=[[5,0],
                    [2,1],[5,1],[6,1],
                    [2,2],[6,2],
                    [1,3],[2,3],[3,3],[4,3],[6,3],
                    [1,4],[6,4],
                    [1,5],[3,5],[4,5],[5,5],
                    [5,7],
                    [5,8]]
            conveyor_down=[[5,3],[5,4]]
            conveyor_left=[[3,1],[4,1],
                        [2,4],[3,4],[4,4]]
            partial_left=[[2,6]]
            partial_right=[[1,6]]
            triggertiles=[[0,6,False],[1,8,False],[3,8,False],[2,9,False],[1,10,False],[4,10,False]]
            breakable1=[[7,5],[8,5],[8,7],[2,8],[2,10],[1,9],[3,9]]
            rightrotators_switch=[[5,6]]
            spikelist=[[6,5],[4,9],[5,9],[6,9],[7,9],[8,9],[8,8]]
            reversespikelist=[[7,6],[9,6],[7,7],[7,8],[6,8]]
            conveyor_right=[[3,2],[4,2],[5,2]]
            switches=[[8,6]]
            

        if level==47:
            zoom=1
            baseposition_x=0.5
            baseposition_y=0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[10,6]
            validtiles=[]
        
        if level==23:
            zoom=3
            baseposition_x=0.5
            baseposition_y=0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[6,6]
            validtiles=[[0,0],[1,0],[5,0],
                        [1,1],[2,1],[3,1],[4,1],[5,1],
                        [1,2],[5,2],
                        [1,3],[2,3],[3,3],[4,3],[5,3],
                        [1,4],[5,4],
                        [1,5],[2,5],[3,5],[4,5],[5,5],
                        [1,6],[5,6],[6,6]]
            switches=[[4,1],[4,5],[2,3]]
            triggertiles=[[2,1,False],[4,3,False],[2,5,False]]
            spikelist=[[3,1],[3,5]]
            reversespikelist=[[3,3]]
        
        if level==24 :
            zoom=3
            baseposition_x=1
            baseposition_y=6
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[5,-5]
            validtiles=[[-1,-6],[0,-6],[1,-6],[2,-6],[3,-6],[4,-6],[5,-6],[6,-6],
                        [-1,-5],[0,-5],[1,-5],[2,-5],[3,-5],[5,-5],[6,-5],
                        [-1,-4],[0,-4],[3,-4],[5,-4],[6,-4],
                        [-1,-3],[0,-3],[3,-3],[5,-3],[6,-3],
                        [-1,-2],[0,-2],[1,-2],[2,-2],[3,-2],[4,-2],[5,-2],[6,-2],
                        [-1,-1],[3,-1],[4,-1],[5,-1],[6,-1],
                        [-1,0],[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],
                        [-1,1],[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],]
            
            killzones=[[-1,-6],[0,-6],[1,-6],[2,-6],[3,-6],[4,-6],[5,-6],[6,-6],
                    [-1,1],[0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],
                    [-1,-5],[-1,-4],[-1,-3],[-1,-2],[-1,-1],[-1,0],
                    [6,-5],[6,-4],[6,-3],[6,-2],[6,-1],[6,0],[4,-1]]
            breakable1=[[0,-2],[3,-5],[5,-4],[5,-1],[4,0],[1,0]]
            breakable2=[[3,-1],[4,-2]]
            triggertiles=[[0,-5,False],[3,-2,False],[5,0,False]]

        if level==31 :
            zoom=3
            baseposition_x =0
            baseposition_y =0
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[0,4]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[7,0],[6,0],
                        [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],
                        [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],[7,2],
                        [2,3],[3,3],[4,3],[7,3],
                        [0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],
                        [0,6],[1,6],[3,6],[4,6],[5,6],[6,6],[7,6],
                        [0,7],[2,7],[4,7],[5,7],[6,7],[7,7]]
            boxes=[[1,1],[6,6]]
            boxholes=[[7,1],[2,6]]
            killzones=[[1,0],[3,1],[6,2],[2,4],[5,4],[6,4]]
            triggertiles=[[5,2,False],[4,4,False],[2,7,False],[7,3,False]]
            switches=[[0,2],[7,2]]
            partial_down=[[2,3],[3,3],[4,3]]
            red_conveyor_down=[[2,5]]
            blue_conveyor_down=[[7,0]]

        if level==25:
            zoom=3
            baseposition_x =2.5
            baseposition_y =2.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[2,2]
            validtiles=[[0,-2],[1,-2],[2,-2],
                        [-1,-1],[0,-1],[1,-1],[2,-1],[3,-1],
                        [-2,0],[-1,0],[0,0],[1,0],[2,0],[3,0],[4,0],
                        [-2,1],[-1,1],[0,1],[1,1],[2,1],[3,1],[4,1],
                        [-2,2],[-1,2],[0,2],[1,2],[2,2],[3,2],[4,2],
                        [-1,3],[0,3],[1,3],[2,3],[3,3],
                        [0,4],[1,4],[2,4]]
            killzones=[[-1,-1],[3,-1],[-1,3],[3,3],[1,1]]
            triggertiles=[[2,0,False],[0,2,False],[1,-2,False],[1,4,False],[-2,1,False],[4,1,False]]
            conveyor_down=[[1,2],[1,3]]
            conveyor_up=[[1,-1],[1,0]]
            conveyor_left=[[-1,1],[0,1]]
            conveyor_right=[[2,1],[3,1]]
            breakable1=[[0,-2],[2,-2],[0,-1],[2,-1],[-2,0],[-1,0],[3,0],[4,0],[-2,2],[-1,2],[3,2],[4,2],[0,3],[0,4],[2,3],[2,4]]

        if level == 26:
            zoom=3
            baseposition_x=0.5
            baseposition_y=.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=True
            endtile=[3,4]
            doppleendtile=[4,1]
            dopple_start=[6,6]
            dopplebaseposition_x=dopple_start[0]
            dopplebaseposition_y=dopple_start[1]
            doppleheading=3
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],
                        [1,1],[2,1],[3,1],[4,1],
                        [3,2],[4,2],
                        [1,3],[2,3],[3,3],[4,3],[5,3],[6,3],
                        [3,4],[4,4],
                        [3,5],[4,5],[5,5],[6,5],
                        [4,6],[5,6],[6,6]]
            killzones=[[2,0]]
            partial_right=[[3,1],[3,2],[3,3],[1,3],[4,5],[5,6]]
            partial_left=[[4,0],[4,3],[4,4]]
            partial_up=[[3,5]]
            triggertiles=[[6,3,False]]

        if level==27:
            zoom=3
            baseposition_x =0.5
            baseposition_y =.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[6,6]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],
                        [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],
                        [0,2],[1,2],[2,2],[3,2],[5,2],[6,2],
                        [0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],
                        [4,4],[5,4],[6,4],
                        [0,5],[1,5],[4,5],[5,5],[6,5],
                        [0,6],[1,6],[4,6],[5,6],[6,6],
                        ]
            boxes=[[0,6]]
            switchmodules=[[1,5]]
            conveyor_down=[[1,5]]
            conveyor_up=[[0,6]]
            conveyor_left=[[1,6]]
            conveyor_right=[[0,5]]
            partial_up=[[4,6],[5,6]]
            redtiles=[[0,2],[5,2]]
            bluetiles=[[4,2],[3,5],[3,6]]
            spikelist=[[1,1]]
            reversespikelist=[[1,2]]
            leftrotators_switch=[[4,3],[4,5]]
            rightrotators_switch=[[3,3],[5,5]]
            breakable1=[[2,1],[2,2],[2,3],[4,1]]
            blue_conveyor_up=[[5,4]]
            partial_left=[[5,3]]
            triggertiles=[[0,3,False],[5,1,False]]
            killzones=[[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[3,1],[3,2],[1,3],[3,4],[4,4]]

        if level==28:
            zoom=3
            baseposition_x =0.5
            baseposition_y =.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[0,6]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],
                        [0,1],[2,1],
                        [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],
                        [0,3],[1,3],[2,3],[3,3],[5,3],[6,3],
                        [0,4],[3,4],[4,4],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],
                        [0,6],[3,6],[4,6],[5,6],[6,6]]
            redtiles=[[1,0],[2,0],[1,2],[2,2],[5,2],[6,2],[1,5],[3,5],[4,5],[5,5],[6,5]]
            bluetiles=[[1,1],[3,1],[4,1],[5,1],[6,1],[1,4],[2,4],[5,4],[6,4],[1,6],[2,6]]
            breakable1=[[3,2],[3,4]]
            spikelist=[[0,1],[4,4],[2,5]]
            reversespikelist=[[2,1],[4,2],[0,5]]
            triggertiles=[[0,2,False],[0,4,False]]
            switches=[[6,3]]
            killzones=[[3,0],[4,0],[5,0],[6,0],[0,3],[1,3],[2,3],[3,3],[5,3],[3,6],[4,6],[5,6],[6,6]]
        
        if level==29 :
            zoom=3
            baseposition_x =0
            baseposition_y =0
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[7,7]
            validtiles=[[0,0],[7,0],
                        [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],
                        [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],[7,2],
                        [0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],[7,3],
                        [0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],
                        [3,5],
                        [3,6],
                        [0,7],[3,7],[6,7],[7,7]]
            triggertiles=[[0,7,False],[3,7,False],[6,7,False]]
            bluetiles=[[0,5],[0,6],[6,6],[6,5]]
            redtiles=[[3,5],[3,6]]
            killzones=[[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3]]
            partial_left=[[7,2]]
            partial_right=[[0,2]]
            rightswitchconveyor=[[1,2],[2,2],[3,2],[4,2],[5,2],[6,2]]
            switchmodules=[[1,2],[6,2]]
            boxes=[[2,2]]
            breakable3=[[0,1]]
            breakable2=[[7,0]]
        
        if level == 30 : 
            zoom=2
            baseposition_x =0.5
            baseposition_y =0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[2,8]
            validtiles=[[0,0],[5,0],[6,0],[7,0],[9,0],
                        [0,1],[5,1],[6,1],[7,1],[9,1],
                        [0,2],[3,2],[4,2],[5,2],[6,2],[7,2],[8,2],[9,2],[10,2],
                        [0,3],[9,3],
                        [0,4],[2,4],[3,4],[4,4],[7,4],[8,4],[9,4],
                        [2,5],[4,5],[9,5],
                        [2,6],[4,6],
                        [2,7],[4,7],[5,7],[6,7],[7,7],[8,7],[9,7],
                        [2,8],[4,8],
                        [4,9],[5,9],[6,9],[7,9],[8,9],[9,9]]
            boxholes=[[9,6],[4,10]]
            boxes=[[9,4],[9,5],[4,9]]
            switchmodules=[[9,9]]
            bluetiles=[[1,2],[2,2]]
            switches=[[0,4],[6,1],[10,2],[9,7],[4,6]]
            triggertiles=[[9,0,False]]
            spikelist=[[9,1],[5,7],[6,7],[7,7],[8,7],[2,4],[3,4],[4,4],[2,5],[4,5],[2,6],[2,7]]
            reversespikelist=[[4,2]]
            leftswitchconveyor=[[7,0],[7,1],[7,2],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9]]
            rightswitchconveyor=[[5,0],[5,1],[5,2],[8,4]]
            upswitchconveyor=[[6,2]]
            downswitchconveyor=[[6,0]]
            red_conveyor_right=[[7,4]]
            blue_conveyor_left=[[9,4]]
        if level==35:
            zoom=2
            baseposition_x =5.5
            baseposition_y =0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[0,10]
            validtiles=[[-5,0],[-4,0],[-3,0],[-2,0],[0,0],[4,0],
                        [0,1],[1,1],[5,1],
                        [-5,2],[-4,2],[-1,2],[0,2],[1,2],[2,2],[3,2],[5,2],
                        [-5,3],[-4,3],[-3,3],[-2,3],[-1,3],[2,3],
                        [-1,4],[0,4],[2,4],[3,4],[4,4],[5,4],
                        [-5,5],[-4,5],[-3,5],[-2,5],[0,5],[1,5],[2,5],[4,5],[5,5],
                        [-5,6],[-4,6],[-3,6],[-2,6],[0,6],[1,6],[2,6],[4,6],[5,6],
                        [-5,7],[-4,7],[-3,7],[-2,7],[0,7],[1,7],[2,7],[5,7],
                        [-5,8],[-3,8],[-2,8],[1,8],[2,8],[3,8],[4,8],[5,8],
                        [-4,9],[-3,9],[-2,9],[0,9],[1,9],[3,9],[4,9],[5,9],
                        [-5,10],[-3,10],[-2,10],[0,10],[3,10],[4,10],[5,10]
                        ]
            boxholes=[[-1,1],[4,1],[4,2],[-5,4],[-2,4],[4,7],[-4,8],[-1,9],[-4,10]]
            boxes=[[0,1],[-3,0],[-1,2],[-4,3],[-1,4],[-3,6],[1,8],[0,9],[-3,9],[-3,10],[5,9]]
            triggertiles=[[4,0,False],[-5,10,False],[0,4,False]]
            leftswitchconveyor=[[-5,0],[-4,0],[-3,0],[-2,0],[4,6],[5,6],[5,7]]
            switchmodules=[[-5,0],[-2,0]]
            killzones=[[-3,2],[1,6],[1,5],[4,8],[4,9]]
            upswitchconveyor=[[-2,8]]
            breakable2=[[3,10],[4,10],[5,10]]
            conveyor_down=[[-4,6],[-2,6],[-5,7],[-3,7]]
            conveyor_up=[[5,2]]
            conveyor_left=[[-4,7],[-2,7],[3,4],[4,4],[5,4],[5,1]]
            conveyor_right=[[-5,6],[-5,8],[-2,9]]
            partial_up=[[-2,5],[0,5]]

        if level == 32 :
            zoom=2
            baseposition_x =5.5
            baseposition_y =0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[0,10]
            validtiles=[
                [-5,0],[-4,0],[-3,0],[-2,0],[-1,0],[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],
                [-5,1],[-4,1],[-3,1],[0,1],[3,1],[4,1],[5,1],
                [-5,2],[-4,2],[-3,2],[-1,2],[0,2],[1,2],[2,2],[3,2],[4,2],[5,2],
                [-5,3],[-4,3],[-3,3],[-2,3],[-1,3],[0,3],[1,3],[3,3],[4,3],[5,3],
                [-5,4],[-4,4],[-3,4],[3,4],[4,4],[5,4],
                [-5,5],[-4,5],[-3,5],[-2,5],[-1,5],[0,5],[1,5],[2,5],
                [-5,6],[-4,6],[-3,6],[0,6],[3,6],[5,6],
                [-5,7],[-4,7],[-3,7],[-2,7],[-1,7],[0,7],[1,7],[3,7],[4,7],[5,7],
                [-5,8],[-4,8],[-3,8],[-1,8],[0,8],[1,8],[2,8],[4,8],[5,8],
                [-5,9],[-4,9],[-3,9],[3,9],[4,9],
                [-5,10],[-4,10],[-3,10],[-2,10],[-1,10],[0,10],[1,10],[2,10],[3,10],[4,10]]
            halfboxes=[[0,2],[0,3],[0,7],[0,8]]
            boxes=[[0,1],[0,6],[-4,9],[-4,6]]
            boxholes=[[0,4],[0,9]]
            bluetiles=[[3,5],[4,5],[5,5],[4,6],[3,8],[5,9],[5,10]]
            redtiles=[[3,6],[5,6],[5,7],[3,10]]
            switches=[[-3,2],[4,7],[5,8],[3,9],[4,10]]
            spikelist=[[-2,3],[1,5],[2,5]]
            reversespikelist=[[5,2],[4,3],[5,3]]
            conveyor_down=[[-4,7]]
            conveyor_up=[[-3,7]]
            leftrotators=[[3,0]]
            rightrotators=[[4,0]]
            killzones=[[-4,1],[-3,1],[3,1],[4,1],
                    [-4,2],[-1,2],[4,2],
                    [1,3],
                    [-5,4],[-4,4],[-3,4],[3,4],[4,4],[5,4],
                    [1,7],[3,7],
                    [-3,8],[-1,8],[4,8],
                    [4,9],
                    [-2,10],[-1,10],[1,10],[2,10]
                    ]
        if level == 33 :
            zoom=2
            baseposition_x =0.5
            baseposition_y =0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[10,10]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[10,0],[11,0],[12,0],[13,0],
                        [0,1],[1,1],[2,1],[4,1],[5,1],[6,1],[7,1],[8,1],[10,1],[13,1],
                        [0,2],[1,2],[2,2],[4,2],[5,2],[6,2],[7,2],[8,2],[10,2],[13,2],
                        [4,3],[10,3],[11,3],[12,3],[13,3],
                        [0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[12,4],[13,4],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[10,5],[11,5],[12,5],[13,5],
                        [0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6],[10,6],[13,6],[9,6],
                        [0,7],[4,7],[5,7],[6,7],[10,7],[11,7],[12,7],[13,7],
                        [-3,8],[-2,8],[-1,8],[0,8],[1,8],[2,8],[4,8],[5,8],[6,8],
                        [-3,9],[-2,9],[-1,9],[0,9],[1,9],[2,9],[4,9],[5,9],[6,9],
                        [-3,10],[-2,10],[1,10],[2,10],[3,10],[4,10],[5,10],[6,10],[10,10],
                        [-3,11],[-2,11],[1,11],[2,11],
                        [-3,12],[-2,12],[-1,12],[0,12],[1,12],[2,12],
                        [-3,13],[-2,13],[-1,13],[0,13],[1,13],[2,13]]
            killzones=[[2,0],[7,0],
                    [2,4],
                    [2,5],[5,5],
                    [5,7]]
            boxes=[[1,1],[4,0],[1,5],[5,6],[5,10]]
            boxholes=[[3,1],[9,1],[7,10],[8,10],[9,10]]
            conveyor_down=[[10,0],[10,1],[10,2],[12,3],[12,4],[10,5],[10,6],[2,8],[2,9],[2,10],[2,11],[2,12],[-2,9],[-2,10],[-2,11]]
            conveyor_up=[[13,1],[13,2],[13,3],[13,4],[13,5],[13,6],[13,7],[-3,8],[-3,9],[-3,10],[-3,11],[-3,12],[-3,13],[1,10],[1,11],[1,12],[8,2]]
            conveyor_left=[[11,0],[12,0],[13,0],[11,5],[12,5],[-2,13],[-1,13],[0,13],[1,13],[2,13],[-1,9],[0,9],[1,9]]
            conveyor_right=[[10,3],[11,3],[10,7],[11,7],[12,7],[-3,8],[-2,8],[-1,8],[0,8],[1,8],[-2,12],[-1,12],[0,12],[6,2]]
            switchmodules=[[-2,12]]
            red_conveyor_down=[[5,1]]
            blue_conveyor_down=[[5,0]]
            blue_conveyor_up=[[7,1],[7,2]]
            breakable2=[[0,7],[3,10]]
            movablekilltiles=[[-3,8],[2,8],[-3,13],[2,13],[10,0],[13,0],[13,2],[13,7],[10,5],[12,4]]

        if level == 39 :
            zoom=2
            baseposition_x=0
            baseposition_y=0
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=True
            endtile=[11,9]
            doppleendtile=[0,2]
            dopple_start=[11,11]
            dopplebaseposition_x=dopple_start[0]
            dopplebaseposition_y=dopple_start[1]
            doppleheading=3 
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],[11,0],
                [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[11,1],
                [0,2],[1,2],[2,2],[5,2],[6,2],[7,2],[8,2],[9,2],[10,2],[11,2],
                [0,3],[1,3],[2,3],[9,3],[10,3],[11,3],
                [0,4],[1,4],[2,4],[4,4],[5,4],[6,4],[7,4],[10,4],[11,4],
                [0,5],[1,5],[4,5],[5,5],[6,5],[7,5],[10,5],[11,5],
                [0,6],[1,6],[4,6],[5,6],[6,6],[7,6],[10,6],[11,6],
                [0,7],[1,7],[4,7],[5,7],[6,7],[7,7],[9,7],[10,7],[11,7],
                [0,8],[1,8],[2,8],[9,8],[10,8],[11,8],
                [0,9],[1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[9,9],[10,9],[11,9],
                [0,10],[1,10],[2,10],[3,10],[4,10],[5,10],[6,10],[7,10],[8,10],[9,10],[10,10],[11,10],
                [0,11],[1,11],[2,11],[3,11],[4,11],[5,11],[6,11],[7,11],[8,11],[9,11],[10,11],[11,11]]
            killzones=[[7,0],
                    [0,1],[1,1],[5,1],[7,1],
                    [1,2],[2,2],[5,2],
                    [1,3],[2,3],[9,3],[10,3],
                    [1,4],[2,4],
                    [10,5],[11,5],
                    [0,6],[1,6],
                    [9,7],[10,7],
                    [1,8],[2,8],[9,8],[10,8],
                    [6,9],[9,9],[10,9],
                    [4,10],[6,10],[10,10],[11,10],
                    [4,11]]
            redtiles=[[11,3],[11,4],[0,7],[0,8]]
            bluetiles=[[2,5],[2,6],[2,7],[9,4],[9,5],[9,6]]
            leftrotators_switch=[[6,0],[6,2],[5,9],[5,11]]
            rightrotators_switch=[[6,1],[5,10]]
            blue_conveyor_down=[[0,5]]
            blue_conveyor_up=[[11,6]]
            upswitchconveyor=[[3,0],[4,0],[3,1],[4,1]]
            downswitchconveyor=[[7,10],[8,10],[7,11],[8,11]]
            red_conveyor_right=[[0,3],[8,2],[9,2],[1,11],[2,11]]
            red_conveyor_left=[[11,8],[9,0],[10,0],[2,9],[3,9]]
            red_conveyor_up=[[10,1],[10,2],[3,10],[3,11]]
            red_conveyor_down=[[1,9],[1,10],[8,0],[8,1]]
            conveyor_right=[[4,4],[5,4],[6,4]]
            conveyor_left=[[5,7],[6,7],[7,7]]
            conveyor_up=[[4,5],[4,6],[4,7]]
            conveyor_down=[[7,4],[7,5],[7,6]]
            boxes=[[4,4],[7,5]]
            switchmodules=[[7,7]]
            partial_left=[[11,1],[11,2]]
            partial_right=[[0,10],[0,9]]
            movablekilltiles=[[10,0],[8,0],[1,11],[3,11]]
        
        if level==36 :
            zoom=2
            baseposition_x =1.5
            baseposition_y =1.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[8,8]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],
                        [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],
                        [0,2],[1,2],[2,2],[3,3],[4,2],[5,2],[6,2],[7,2],[8,2],
                        [0,3],[1,3],[2,3],[3,4],[4,3],[5,3],[6,3],[7,3],[8,3],
                        [0,4],[1,4],[2,4],[3,2],[4,4],[5,4],[6,4],[7,4],[8,4],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],
                        [0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,7],[7,6],[8,6],
                        [0,7],[1,7],[2,7],[3,7],[4,7],[5,7],[6,8],[7,7],[8,7],
                        [0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[6,6],[7,8],[8,8]]
            switches=[[0,4]]
            killzones=[[0,2],[6,1],[4,7],[7,6],[2,3]]
            triggertiles=[[8,0,False],[4,4,False],[0,8,False]]
            blue_conveyor_up=[[8,7]]
            boxes=[[0,7],[1,0],[1,1],[1,2],[1,3],[1,5],[1,6],[1,7],[2,0],[3,4],[3,5],[3,6],[3,8],[4,1],[4,3],[4,6],[5,4],[5,5],[5,6],[6,2],[7,0],[7,3],[7,7],[7,8],[8,2],[8,3],[8,5]]

        if level==37 :
            zoom=2
            baseposition_x =1.5
            baseposition_y =1.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[2,0]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],
                        [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],
                        [0,2],[1,2],[2,2],[3,3],[4,2],[5,2],[6,2],[7,2],[8,2],
                        [0,3],[1,3],[2,3],[3,4],[4,3],[5,3],[6,3],[7,3],[8,3],
                        [0,4],[1,4],[2,4],[3,2],[4,4],[5,4],[6,4],[7,4],[8,4],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],[7,5],[8,5],
                        [0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,7],[7,6],[8,6],
                        [0,7],[1,7],[2,7],[3,7],[4,7],[5,7],[6,8],[7,7],[8,7],
                        [0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[6,6],[7,8],[8,8]]
            triggertiles=[[4,0,False],[6,0,False],[8,0,False]]
            killzones=[[5,0],[7,0],[3,0],[3,1],[5,1],[7,1],[0,1],[1,1],[0,3],[1,3],[1,4],[1,5],[0,8],[2,3],[3,3],[6,7],[7,3],[7,4],[7,5],[7,7],[8,7]]
            spikelist=[[4,1],[4,3],[4,4],[3,5],[2,5],[6,1],[6,3],[5,6],[5,7],[7,2]]
            reversespikelist=[[2,4],[2,6],[3,8],[4,5],[4,7],[4,8],[5,2],[5,3],[5,4],[5,5],[8,1],[8,3]]
            switches=[[8,8]]
            boxes=[[1,7]]
            conveyor_up=[[0,5],[0,6],[0,7]]
            conveyor_right=[[0,4]]
            conveyor_left=[[3,4]]
            breakable2=[[7,8]]

        if level==38 :
            zoom=2
            baseposition_x =.5
            baseposition_y =.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[10,10]
            validtiles=[[0,0],[1,0],[7,0],[8,0],[9,0],[10,0],
                        [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],
                        [1,2],[2,2],[3,2],[4,2],[5,2],[6,2],[7,2],[8,2],[9,2],[10,2],
                        [1,3],[2,3],[3,3],[4,3],[6,3],[7,3],[8,3],[9,3],[10,3],
                        [1,4],[2,4],[3,4],[4,4],[5,4],[6,4],[7,4],[8,4],[9,4],
                        [1,5],[2,5],[4,5],[5,5],[6,5],[7,5],[8,5],[9,5],
                        [1,6],[2,6],[3,6],[4,6],[5,6],[6,6],[8,6],[9,6],
                        [0,7],[1,7],[2,7],[3,7],[4,7],[5,7],[7,7],[8,7],[9,7],
                        [0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[9,8],
                        [0,9],[1,9],[2,9],[3,9],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9],
                        [0,10],[1,10],[2,10],[3,10],[10,10]]
            redtiles=[[1,0],[0,1],[4,3],[3,4],[7,5],[5,7]]
            bluetiles=[[5,3],[3,5],[6,7],[7,6],[10,9],[9,10]]
            spikelist=[[10,2],[2,10],[5,4],[4,5],[8,6],[6,8]]
            reversespikelist=[[8,0],[0,8],[2,4],[4,2],[6,5],[5,6]]
            triggertiles=[[3,3,False],[7,7,False]]
            breakable1=[[5,5]]
            boxes=[[8,2],[2,8]]
            switchmodules=[[7,3],[3,7]]
            conveyor_down=[[7,1],[7,2],[9,3],[9,4],[9,5],[9,6],[9,7],[9,8]]
            conveyor_up=[[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[3,8],[3,9]]
            conveyor_left=[[2,7],[3,7],[4,9],[5,9],[6,9],[7,9],[8,9],[9,9]]
            conveyor_right=[[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,3],[8,3]]

        if level==34 :
            zoom=3
            baseposition_x =0.5
            baseposition_y =0.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[6,6]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],
                        [0,1],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],
                        [0,2],[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],
                        [0,3],[1,3],[2,3],[3,3],[4,3],[5,3],[6,3],
                        [0,4],[1,4],[2,4],[3,4],[4,4],[5,4],[6,4],
                        [0,5],[1,5],[2,5],[3,5],[4,5],[5,5],[6,5],
                        [0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[6,6]]
            triggertiles=[[0,6,False],[6,0,False]]
            killzones=[[1,1],[1,3],[1,5],
                    [3,1],[3,3],[3,5],
                    [5,1],[5,3],[5,5]]
            partial_up=[[4,1],[6,1],[6,3],[6,5],[0,5]]
            partial_down=[[0,3],[0,1],[2,1],[2,3],[2,5],[4,3],[4,5]]
            partial_left=[[3,0],[5,0],[1,2],[3,2],[5,2],[3,4],[5,4],[1,6]]

        if level==46 :
            manual=True
            zoom=3
            baseposition_x =3.5
            baseposition_y =3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            endtile=[36,14]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],
                        [6,1],[29,1],[30,1],[31,1],
                        [6,2],[22,2],[29,2],[30,2],[31,2],
                        [6,3],[13,3],[14,3],[15,3],[22,3],[27,3],[28,3],[29,3],[30,3],[31,3],[32,3],
                        [6,4],[7,4],[8,4],[9,4],[10,4],[12,4],[13,4],[15,4],[16,4],[17,4],[18,4],[22,4],[26,4],[27,4],[28,4],[29,4],[30,4],[31,4],[32,4],
                        [5,5],[6,5],[7,5],[8,5],[9,5],[10,5],[11,5],[12,5],[13,5],[15,5],[16,5],[17,5],[18,5],[19,5],[20,5],[21,5],[22,5],[26,5],[27,5],[28,5],[29,5],[30,5],[31,5],[32,5],
                        [5,6],[6,6],[7,6],[8,6],[9,6],[10,6],[12,6],[13,6],[15,6],[16,6],[17,6],[18,6],[26,6],[27,6],[28,6],[29,6],[30,6],[31,6],
                        [5,7],[6,7],[7,7],[13,7],[14,7],[15,7],[27,7],[28,7],[29,7],[30,7],[31,7],
                        [35,3],[36,3],[37,3],
                        [33,4],[34,4],[35,4],[36,4],[37,4],
                        [35,5],[36,5],[37,5],
                        [36,6],
                        [35,7],[36,7],[37,7],[38,7],
                        [34,8],[35,8],[36,8],[37,8],[38,8],[39,8],
                        [32,9],[33,9],[34,9],[35,9],[36,9],[37,9],[38,9],[39,9],[40,9],[41,9],[42,9],[43,9],[44,9],[45,9],[46,9],[47,9],[48,9],
                        [30,10],[31,10],[32,10],[33,10],[34,10],[35,10],[36,10],[37,10],[38,10],[39,10],[40,10],[48,10],
                        [29,11],[30,11],[31,11],[32,11],[33,11],[34,11],[35,11],[36,11],[37,11],[38,11],[39,11],[40,11],[48,11],
                        [28,12],[29,12],[30,12],[31,12],[32,12],[33,12],[34,12],[35,12],[36,12],[37,12],[38,12],[39,12],[40,12],[41,12],[48,12],
                        [28,13],[29,13],[30,13],[31,13],[32,13],[33,13],[34,13],[35,13],[36,13],[37,13],[38,13],[39,13],[40,13],[41,13],[48,13],[49,13],[50,13],[51,13],
                        [28,14],[29,14],[30,14],[31,14],[32,14],[33,14],[34,14],[35,14],[36,14],[37,14],[38,14],[39,14],[40,14],[41,14],[42,14],[51,14],[52,14],[53,14],[54,14],[55,14],[56,14],[57,14],[58,14],[59,14],[60,14],[61,14],[62,14],[63,14],[64,14],[65,14],[66,14],[67,14],[68,14],[69,14],[70,14],[71,14],[72,14],[73,14],[74,14],[75,14],[76,14],[77,14],[78,14],
                        [28,15],[29,15],[30,15],[31,15],[32,15],[33,15],[34,15],[35,15],[36,15],[37,15],[38,15],[39,15],[40,15],[41,15],[42,15],[51,15],
                        [28,16],[29,16],[30,16],[31,16],[32,16],[33,16],[34,16],[35,16],[36,16],[37,16],[38,16],[39,16],[40,16],[41,16],[42,16],[51,16],
                        [29,17],[30,17],[31,17],[32,17],[33,17],[34,17],[35,17],[36,17],[37,17],[38,17],[39,17],[40,17],[41,17],[42,17],[47,17],[48,17],[49,17],[50,17],[51,17],
                        [31,18],[32,18],[33,18],[34,18],[35,18],[36,18],[37,18],[38,18],[39,18],[40,18],[41,18],[47,18],
                        [31,19],[33,19],[34,19],[35,19],[36,19],[37,19],[38,19],[39,19],[47,19],
                        [31,20],[35,20],[36,20],[37,20],[47,20],
                        [31,21],[47,21],
                        [31,22],[47,22],
                        [31,23],[47,23],
                        [31,24],[40,24],[41,24],[42,24],[43,24],[44,24],[45,24],[46,24],[47,24],
                        [31,25],[40,25],
                        [31,26],[32,26],[33,26],[34,26],[35,26],[40,26],
                        [35,27],[40,27],
                        [35,28],[36,28],[37,28],[38,28],[39,28],[40,28]]
            switches=[[22,2]]
            bluetiles=[[23,5],[24,5],[25,5]]
            redtiles=[[21,5],[20,5],[19,5]]
            conveyor_down=[[13,3],[13,4],[13,5],[13,6],
                            [40,24],[40,25],[40,26],[40,27],[40,28],
                            [47,17],[47,18],[47,19],[47,20],[47,21],[47,22],[47,23],
                            [51,13],[51,14],[51,15],[51,16],
                            [48,9],[48,10],[48,11],[48,12]
                        ]
            conveyor_up=[[15,4],[15,5],[15,6],[15,7],
                            [31,17],[31,18],[31,19],[31,20],[31,21],[31,22],[31,23],[31,24],[31,25],[31,26],
                            [34,10],[34,11],[34,12],[34,13],[34,14],[34,15],[34,16],
                            [35,27],[35,28]
                        ]
            conveyor_left=[[15,3],[14,3],
                        [48,17],[49,17],[50,17],[51,17],
                        [41,24],[42,24],[43,24],[44,24],[45,24],[46,24],[47,24],
                        [36,28],[37,28],[38,28],[39,28],[40,28],
                        [32,26],[33,26],[34,26],[35,26]]
            conveyor_right=[[13,7],[14,7],[34,9],[35,9],[36,9],[37,9],[38,9],[39,9],[40,9],[41,9],[42,9],[43,9],[44,9],[45,9],[46,9],[47,9],
                        [48,13],[49,13],[50,13],
                        [31,16],[32,16],[33,16]]
            movablekilltiles=[[13,3],[15,3],[13,7],[15,7]]
            spikelist=[[17,4],[18,4],[17,6],[18,6]]
            reversespikelist=[[28,5],[29,5]]
            killzones=[[35,3],[36,3],[37,3],[37,4],[35,5],[37,5],[35,10],[35,11],[35,12],[35,13],[35,14]]
            boxes=[
                    [40,24],[40,28],
                    [47,18],[47,22],
                    [51,14],[51,16],
                    [48,10],[48,12],

                    [31,18],[31,23],[31,26],
                    [34,11],[34,15],

                    [49,17],[51,17],
                    [42,24],[46,24],
                    [37,28],[40,28],
                    [33,26],[35,26],

                    [36,9],[41,9],[46,9],
                    [49,13],
                    [32,16]]
            
    if remix:
        if level==0:
            zoom=3
            baseposition_x =.5
            baseposition_y =3.5
            position_x =baseposition_x
            position_y =baseposition_y
            heading = 1
            doppleon=False
            manual=False
            endtile=[6,0]
            validtiles=[[0,0],[1,0],[2,0],[3,0],[6,0],[1,-1],[1,-2],[2,-2],[3,-2],[3,-1],[1,1],[1,2],[2,2],[3,2],[3,1]]
            altswitches=[[2,-2]]
            killzones=[[1,-1]]
            altkillzones=[[3,-1]]
            switches=[[2,2]]
            spikelist=[[1,1]]
            reversespikelist=[[3,1]]
            greentiles=[[5,0]]
            yellowtiles=[[3,-2]]
            redtiles=[[3,2]]
            bluetiles=[[4,0]]

#------ Other functions to get game state -------

def getvalues():
    global position_x, position_y, heading
    return position_x, position_y, heading

def unlockedexit():
    global position_x, position_y, triggertiles, unlocked
    valid = True
    for tile in triggertiles:
        if [tile[0], tile[1]] == [position_x, position_y]:
            if tile[2] == False:  # Only play sound when transitioning from False to True
                beacon_sound = pygame.mixer.Sound("sfx\\beacon.ogg")
                beacon_sound.set_volume(0.25)
                channel = pygame.mixer.Channel(3)
                channel.play(beacon_sound)
            tile[2] = True
        if doppleon == True:
            if [tile[0], tile[1]] == [doppleposition_x, doppleposition_y]:
                if tile[2] == False:  # Only play sound when transitioning from False to True
                    beacon_sound = pygame.mixer.Sound("sfx\\beacon.ogg")
                    beacon_sound.set_volume(0.25)
                    channel = pygame.mixer.Channel(3)
                    channel.play(beacon_sound)
                tile[2] = True
        if tile[2] == True:
            pass
        else:
            valid = False
    
    previous_unlocked = unlocked
    if valid == True:
        unlocked = True
    else:
        unlocked = False
    
    # Play unlock sound only when transitioning from False to True
    if unlocked == True and previous_unlocked == False:
        unlock_sound = pygame.mixer.Sound("sfx\\unlock.ogg")
        unlock_sound.set_volume(0.25)
        channel = pygame.mixer.Channel(3)
        channel.play(unlock_sound)

def raycast(x,y,dir):
    global yellowlaser,greenlaser,bluelaser,redlaser,yellowbeam,greenbeam,bluebeam,redbeam,yellowbeamend,greenbeamend,bluebeamend,redbeamend,yellowcornerbeam,greencornerbeam,bluecornerbeam,redcornerbeam


def blockeffects():
    global halfboxes,position_x, position_y, heading, yellowtiles,greentiles,switches, altswitchboost,switchboost,switchstate, spikelist, reversespikelist, leftrotators, rightrotators, breakable1, breakable2, breakable3, broken, validtiles, killzones, redtiles, bluetiles, leftrotators_blue, rightrotators_blue, leftrotators_red, rightrotators_red, leftrotators_switch, rightrotators_switch, doppleheading, doppleposition_x, doppleposition_y, conveyor_up, conveyor_down, conveyor_left, conveyor_right, red_conveyor_up, red_conveyor_down, red_conveyor_left, red_conveyor_right, blue_conveyor_up, blue_conveyor_down, blue_conveyor_left, blue_conveyor_right, partial_left, partial_right, partial_up, partial_down, boxes, boxholes, settledboxes,altleftrotators,altrightrotators,altkillzones,yellow_conveyor_up,yellow_conveyor_down,yellow_conveyor_left,yellow_conveyor_right,green_conveyor_up,green_conveyor_down,green_conveyor_left,green_conveyor_right,altconveyorswitch_up,altconveyorswitch_down,altconveyorswitch_left,altconveyorswitch_right,altswitchmodules,altswitches,altstate
    if not altstate:
        # rotators
        if [position_x,position_y] in leftrotators:
            heading= (heading - 1) % 4
            px.play(2,1)
        if [position_x,position_y] in rightrotators:
            heading= (heading + 1) % 4
            px.play(2,1)
        if doppleon==True:
            if [doppleposition_x,doppleposition_y] in leftrotators:
                doppleheading= (doppleheading - 1) % 4
                px.play(2,1)
            if [doppleposition_x,doppleposition_y] in rightrotators:
                doppleheading= (doppleheading + 1) % 4
                px.play(2,1)

    #breakable blocks
    if [position_x,position_y] in breakable1:
        broken.append([position_x,position_y])
        validtiles.remove([position_x,position_y])
        breakable1.remove([position_x,position_y])


    if [position_x,position_y] in breakable2:
        breakable1.append([position_x,position_y])
        breakable2.remove([position_x,position_y])
    
    if [position_x,position_y] in breakable3:
        breakable2.append([position_x,position_y])
        breakable3.remove([position_x,position_y])
    
    if doppleon==True:
        if [doppleposition_x,doppleposition_y] in breakable1:
            broken.append([doppleposition_x,doppleposition_y])
            validtiles.remove([doppleposition_x,doppleposition_y])
            breakable1.remove([doppleposition_x,doppleposition_y])

        if [doppleposition_x,doppleposition_y] in breakable2:
            breakable1.append([doppleposition_x,doppleposition_y])
            breakable2.remove([doppleposition_x,doppleposition_y])
        
        if [doppleposition_x,doppleposition_y] in breakable3:
            breakable2.append([doppleposition_x,doppleposition_y])
            breakable3.remove([doppleposition_x,doppleposition_y])

    #switches
    if [position_x,position_y] in switches or [position_x,position_y] in switchmodules:
        switchstate= not switchstate
        switchboost=0
        px.play(3,2)
        if spikelist!=[] and switchstate==False:
            spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
            spikesound.set_volume(0.3)
            channel = pygame.mixer.Channel(3)
            channel.play(spikesound)
        if reversespikelist!=[] and switchstate==True:
            spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
            spikesound.set_volume(0.3)
            channel = pygame.mixer.Channel(3)
            channel.play(spikesound)
            
        
        for tile in bluetiles:
            if switchstate==True:
                if tile not in validtiles:
                    validtiles.append(tile)
            else:
                if tile in validtiles:
                    validtiles.remove(tile)
        for tile in redtiles:
            if switchstate==False:
                if tile not in validtiles:
                    validtiles.append(tile)
            else:
                if tile in validtiles:
                    validtiles.remove(tile)
    
    #switches triggered by boxes
    for box in boxes:
        if box in switches or box in switchmodules:
            switchstate= not switchstate
            switchboost=0
            px.play(3,2)
            if spikelist!=[] and switchstate==False:
                spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                spikesound.set_volume(0.3)
                channel = pygame.mixer.Channel(3)
                channel.play(spikesound)
            if reversespikelist!=[] and switchstate==True:
                spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                spikesound.set_volume(0.3)
                channel = pygame.mixer.Channel(3)
                channel.play(spikesound)

        #colour-dependent tiles (only change validity and appearance during a colour state change)
        for tile in bluetiles:
            if switchstate==True:
                if tile not in validtiles:
                    validtiles.append(tile)
            else:
                if tile in validtiles:
                    validtiles.remove(tile)
        for tile in redtiles:
            if switchstate==False:
                if tile not in validtiles:
                    validtiles.append(tile)
            else:
                if tile in validtiles:
                    validtiles.remove(tile)
    if doppleon==True:
        if [doppleposition_x,doppleposition_y] in switches:
            switchstate= not switchstate
            switchboost=0
            for tile in bluetiles:
                if switchstate==True:
                    if tile not in validtiles:
                        validtiles.append(tile)
                else:
                    if tile in validtiles:
                        validtiles.remove(tile)
            for tile in redtiles:
                if switchstate==False:
                    if tile not in validtiles:
                        validtiles.append(tile)
                else:
                    if tile in validtiles:
                        validtiles.remove(tile)

    

    
    #rotators that depend on switch state
    if switchstate==False:
        for rotator in leftrotators_red:
            if [position_x,position_y]==rotator:
                heading= (heading - 1) % 4
                px.play(2,1)
        for rotator in rightrotators_red:
            if [position_x,position_y]==rotator:
                heading= (heading + 1) % 4
                px.play(2,1)
    else:
        for rotator in leftrotators_blue:
            if [position_x,position_y]==rotator:
                heading= (heading - 1) % 4
                px.play(2,1)
        for rotator in rightrotators_blue:
            if [position_x,position_y]==rotator:
                heading= (heading + 1) % 4
                px.play(2,1)
    if doppleon==True:
        if switchstate==False:
            for rotator in leftrotators_red:
                if [doppleposition_x,doppleposition_y]==rotator:
                    doppleheading= (doppleheading - 1) % 4
                    px.play(2,1)
            for rotator in rightrotators_red:
                if [doppleposition_x,doppleposition_y]==rotator:
                    doppleheading= (doppleheading + 1) % 4
                    px.play(2,1)
        else:
            for rotator in leftrotators_blue:
                if [doppleposition_x,doppleposition_y]==rotator:
                    doppleheading= (doppleheading - 1) % 4
                    px.play(2,1)
            for rotator in rightrotators_blue:
                if [doppleposition_x,doppleposition_y]==rotator:
                    doppleheading= (doppleheading + 1) % 4
                    px.play(2,1)
    
    #rotators that change direction when switches are toggled
    for rotator in leftrotators_switch:
        if [position_x,position_y]==rotator:
            if switchstate==False:
                heading= (heading - 1) % 4
                px.play(2,1)
            else:
                heading= (heading + 1) % 4
                px.play(2,1)
    for rotator in rightrotators_switch:
        if [position_x,position_y]==rotator:
            if switchstate==False:
                heading= (heading + 1) % 4
                px.play(2,1)
            else:
                heading= (heading - 1) % 4
                px.play(2,1)
    if doppleon==True:
        for rotator in leftrotators_switch:
            if [doppleposition_x,doppleposition_y]==rotator:
                if switchstate==False:
                    doppleheading= (doppleheading - 1) % 4
                    px.play(2,1)
                else:
                    doppleheading= (doppleheading + 1) % 4
                    px.play(2,1)
        for rotator in rightrotators_switch:
            if [doppleposition_x,doppleposition_y]==rotator:
                if switchstate==False:
                    doppleheading= (doppleheading + 1) % 4
                    px.play(2,1)
                else:
                    doppleheading= (doppleheading - 1) % 4
                    px.play(2,1)
    
    # partial walls : if the player moved to a partial wall from a forbidden direction, move the player back to the previous tile
    if [position_x,position_y] in partial_left:
        if heading==1:
            position_x-=1
            px.play(3,5)
    if [position_x,position_y] in partial_right:
        if heading==3:
            position_x+=1
            px.play(3,5)
    if [position_x,position_y] in partial_up:
        if heading==2:
            position_y-=1
            px.play(3,5)
    if [position_x,position_y] in partial_down:
        if heading==0:
            position_y+=1
            px.play(3,5)
    if doppleon==True:
        if [doppleposition_x,doppleposition_y] in partial_left:
            if doppleheading==1:
                doppleposition_x-=1
                px.play(3,5)
        if [doppleposition_x,doppleposition_y] in partial_right:
            if doppleheading==3:
                doppleposition_x+=1
                px.play(3,5)
        if [doppleposition_x,doppleposition_y] in partial_up:
            if doppleheading==2:
                doppleposition_y-=1
                px.play(3,5)
        if [doppleposition_x,doppleposition_y] in partial_down:
            if doppleheading==0:
                doppleposition_y+=1
                px.play(3,5)    

    for box in boxes:
        if [position_x,position_y]==box:
            if heading==0:
                if ([box[0],box[1]-1] in validtiles or [box[0],box[1]-1] in boxholes) and [box[0],box[1]-1] not in boxes and [box[0],box[1]-1] not in halfboxes:
                    box[1]-=1
                    px.play(3,3)
                else:
                    position_y+=1
                    px.play(3,5)
            if heading==1:
                if ([box[0]+1,box[1]] in validtiles or [box[0]+1,box[1]] in boxholes) and [box[0]+1,box[1]] not in boxes and [box[0]+1,box[1]] not in halfboxes:
                    box[0]+=1
                    px.play(3,3)
                else:
                    position_x-=1
                    px.play(3,5)
            if heading==2:
                if ([box[0],box[1]+1] in validtiles or [box[0],box[1]+1] in boxholes) and [box[0],box[1]+1] not in boxes and [box[0],box[1]+1] not in halfboxes:
                    box[1]+=1
                    px.play(3,3)
                else:
                    position_y-=1
                    px.play(3,5)
            if heading==3:
                if ([box[0]-1,box[1]] in validtiles or [box[0]-1,box[1]] in boxholes) and [box[0]-1,box[1]] not in boxes and [box[0]-1,box[1]] not in halfboxes:
                    box[0]-=1
                    px.play(3,3)
                else:
                    position_x+=1
                    px.play(3,5)
            #check for boxholes
            if box in boxholes:
                px.play(3,4)
                settledboxes.append(box)
                validtiles.append(box)
                boxholes.remove(box)
                boxes.remove(box)

        if [doppleposition_x,doppleposition_y]==box and doppleon:
            if doppleheading==0:
                if ([box[0],box[1]-1] in validtiles or [box[0],box[1]-1] in boxholes) and [box[0],box[1]-1] not in boxes and [box[0],box[1]-1] not in halfboxes:
                    box[1]-=1
                    px.play(3,3)
                else:
                    doppleposition_y+=1
                    px.play(3,5)
            if doppleheading==1:
                if ([box[0]+1,box[1]] in validtiles or [box[0]+1,box[1]] in boxholes) and [box[0]+1,box[1]] not in boxes and [box[0]+1,box[1]] not in halfboxes:
                    box[0]+=1
                    px.play(3,3)
                else:
                    doppleposition_x-=1
                    px.play(3,5)
            if doppleheading==2:
                if ([box[0],box[1]+1] in validtiles or [box[0],box[1]+1] in boxholes) and [box[0],box[1]+1] not in boxes and [box[0],box[1]+1] not in halfboxes:
                    box[1]+=1
                    px.play(3,3)
                else:
                    doppleposition_y-=1
                    px.play(3,5)
            if doppleheading==3:
                if ([box[0]-1,box[1]] in validtiles or [box[0]-1,box[1]] in boxholes) and [box[0]-1,box[1]] not in boxes and [box[0]-1,box[1]] not in halfboxes:
                    box[0]-=1
                    px.play(3,3)
                else:
                    doppleposition_x+=1
                    px.play(3,5)
            #check for boxholes
            if box in boxholes:
                px.play(3,4)
                settledboxes.append(box)
                validtiles.append(box)
                boxholes.remove(box)
                boxes.remove(box)

    for box in halfboxes:
        if [position_x,position_y]==box:
            if heading==0:
                if [box[0],box[1]-1] in validtiles and [box[0],box[1]-1] not in boxes and [box[0],box[1]-1] not in halfboxes:
                    box[1]-=1
                    px.play(3,3)
                else:
                    position_y+=1
                    px.play(3,5)
            if heading==1:
                if [box[0]+1,box[1]] in validtiles and [box[0]+1,box[1]] not in boxes and [box[0]+1,box[1]] not in halfboxes:
                    box[0]+=1
                    px.play(3,3)
                else:
                    position_x-=1
                    px.play(3,5)
            if heading==2:
                if [box[0],box[1]+1] in validtiles and [box[0],box[1]+1] not in boxes and [box[0],box[1]+1] not in halfboxes:
                    box[1]+=1
                    px.play(3,3)
                else:
                    position_y-=1
                    px.play(3,5)
            if heading==3:
                if [box[0]-1,box[1]] in validtiles and [box[0]-1,box[1]] not in boxes and [box[0]-1,box[1]] not in halfboxes:
                    box[0]-=1
                    px.play(3,3)
                else:
                    position_x+=1
                    px.play(3,5)


        if [doppleposition_x,doppleposition_y]==box and doppleon:
            if doppleheading==0:
                if [box[0],box[1]-1] in validtiles and [box[0],box[1]-1] not in boxes and [box[0],box[1]-1] not in halfboxes:
                    box[1]-=1
                    px.play(3,3)
                else:
                    doppleposition_y+=1
                    px.play(3,5)
            if doppleheading==1:
                if [box[0]+1,box[1]] in validtiles and [box[0]+1,box[1]] not in boxes and [box[0]+1,box[1]] not in halfboxes:
                    box[0]+=1
                    px.play(3,3)
                else:
                    doppleposition_x-=1
                    px.play(3,5)
            if doppleheading==2:
                if [box[0],box[1]+1] in validtiles and [box[0],box[1]+1] not in boxes and [box[0],box[1]+1] not in halfboxes:
                    box[1]+=1
                    px.play(3,3)
                else:
                    doppleposition_y-=1
                    px.play(3,5)
            if doppleheading==3:
                if [box[0]-1,box[1]] in validtiles and [box[0]-1,box[1]] not in boxes and [box[0]-1,box[1]] not in halfboxes:
                    box[0]-=1
                    px.play(3,3)
                else:
                    doppleposition_x+=1
                    px.play(3,5)
    for altswitch in altswitches :
        if [position_x,position_y] == altswitch:
            altstate = not altstate
            altswitchboost=0
            px.play(3,2)
            if altkillzones!=[] and altstate==True:
                spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                spikesound.set_volume(0.3)
                channel = pygame.mixer.Channel(3)
                channel.play(spikesound)
            if killzones!=[] and altstate==False:
                spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                spikesound.set_volume(0.3)
                channel = pygame.mixer.Channel(3)
                channel.play(spikesound)
        if doppleon==True:
            if [doppleposition_x,doppleposition_y] == altswitch:
                altstate = not altstate
                px.play(3,2)
                if altkillzones!=[] and altstate==True:
                    spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                    spikesound.set_volume(0.3)
                    channel = pygame.mixer.Channel(3)
                    channel.play(spikesound)
                if killzones!=[] and altstate==False:
                    spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                    spikesound.set_volume(0.3)
                    channel = pygame.mixer.Channel(3)
                    channel.play(spikesound)

    for altswitch in altswitchmodules :
        if [position_x,position_y] == altswitch:
            altstate = not altstate
            altswitchboost=0
            px.play(3,2)
            if altkillzones!=[] and altstate==True:
                spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                spikesound.set_volume(0.3)
                channel = pygame.mixer.Channel(3)
                channel.play(spikesound)
            if killzones!=[] and altstate==False:
                spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                spikesound.set_volume(0.3)
                channel = pygame.mixer.Channel(3)
                channel.play(spikesound)
        if doppleon==True:
            if [doppleposition_x,doppleposition_y] == altswitch:
                altstate = not altstate
                px.play(3,2)
                if altkillzones!=[] and altstate==True:
                    spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                    spikesound.set_volume(0.3)
                    channel = pygame.mixer.Channel(3)
                    channel.play(spikesound)
                if killzones!=[] and altstate==False:
                    spikesound = pygame.mixer.Sound("sfx\\spikeswitch.ogg")
                    spikesound.set_volume(0.3)
                    channel = pygame.mixer.Channel(3)
                    channel.play(spikesound)
        
def killtiles():
    # killzones
    if ([position_x, position_y] in killzones and altstate==False) or [position_x, position_y] in movablekilltiles:
        resetlevel()
        kill_sound = pygame.mixer.Sound("sfx\\killtile.ogg")
        kill_sound.set_volume(0.25)
        channel = pygame.mixer.Channel(2)
        channel.play(kill_sound)
    if doppleon == True:
        if ([doppleposition_x, doppleposition_y] in killzones and altstate==False)  or [doppleposition_x, doppleposition_y] in movablekilltiles:
            resetlevel()
            kill_sound = pygame.mixer.Sound("sfx\\killtile.ogg")
            kill_sound.set_volume(0.25)
            channel = pygame.mixer.Channel(2)
            channel.play(kill_sound)
        #spikes
    if [position_x,position_y] in spikelist and switchstate==False:
        resetlevel()
        kill_sound = pygame.mixer.Sound("sfx\\killtile.ogg")
        kill_sound.set_volume(0.25)
        channel = pygame.mixer.Channel(2)
        channel.play(kill_sound)
    if [position_x,position_y] in reversespikelist and switchstate==True:
        resetlevel()
        kill_sound = pygame.mixer.Sound("sfx\\killtile.ogg")
        kill_sound.set_volume(0.25)
        channel = pygame.mixer.Channel(2)
        channel.play(kill_sound)
    if doppleon==True:
        if [doppleposition_x,doppleposition_y] in spikelist and switchstate==False:
            resetlevel()
            kill_sound = pygame.mixer.Sound("sfx\\killtile.ogg")
            kill_sound.set_volume(0.25)
            channel = pygame.mixer.Channel(2)
            channel.play(kill_sound)
        if [doppleposition_x,doppleposition_y] in reversespikelist and switchstate==True:
            resetlevel()
            kill_sound = pygame.mixer.Sound("sfx\\killtile.ogg")
            kill_sound.set_volume(0.25)
            channel = pygame.mixer.Channel(2)
            channel.play(kill_sound)
    if ([position_x, position_y] in altkillzones and altstate==True) or [position_x, position_y] in movablekilltiles:
        resetlevel()
        kill_sound = pygame.mixer.Sound("sfx\\killtile.ogg")
        kill_sound.set_volume(0.25)
        channel = pygame.mixer.Channel(2)
        channel.play(kill_sound)    
    if doppleon == True:
        if ([doppleposition_x, doppleposition_y] in altkillzones and altstate==True)  or [doppleposition_x, doppleposition_y] in movablekilltiles:
            resetlevel()
            kill_sound = pygame.mixer.Sound("sfx\\killtile.ogg")
            kill_sound.set_volume(0.25)
            channel = pygame.mixer.Channel(2)
            channel.play(kill_sound)

    for tile in greentiles:
            if altstate==True:
                if tile not in validtiles:
                    validtiles.append(tile)
            else:
                if tile in validtiles:
                    validtiles.remove(tile)
    for tile in yellowtiles:
        if altstate==False:
            if tile not in validtiles:
                validtiles.append(tile)
        else:
            if tile in validtiles:
                validtiles.remove(tile)

def conveyoreffects():
    # conveyor belts
    global position_x,position_y,doppleposition_y,doppleposition_x
    hasmoved = []

    def box_can_move_to(x, y):
        target = [x, y]
        return (target in validtiles or target in boxholes) and target not in boxes and target != [position_x, position_y] and (not doppleon or target != [doppleposition_x, doppleposition_y])
    
    # Process regular conveyors (always active)
    for conveyor in conveyor_up:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
            if [position_x, position_y - 1] in validtiles and [position_x, position_y - 1] not in boxes and [position_x, position_y - 1] not in partial_up:
                position_y -= 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
            if [doppleposition_x, doppleposition_y - 1] in validtiles and [doppleposition_x, doppleposition_y - 1] not in boxes and [doppleposition_x, doppleposition_y - 1] not in partial_up:
                doppleposition_y -= 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved:
                if box_can_move_to(box[0], box[1] - 1):
                    box[1] -= 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
        for kill in movablekilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0], kill[1] - 1] in validtiles:
                    kill[1] -= 1
                    hasmoved.append(kill)
        for kill in vanitykilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0], kill[1] - 1] in validtiles:
                    kill[1] -= 1
                    hasmoved.append(kill)
    
    for conveyor in conveyor_down:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
            if [position_x, position_y + 1] in validtiles and [position_x, position_y + 1] not in boxes and [position_x, position_y + 1] not in partial_down:
                position_y += 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
            if [doppleposition_x, doppleposition_y + 1] in validtiles and [doppleposition_x, doppleposition_y + 1] not in boxes and [doppleposition_x, doppleposition_y + 1] not in partial_down:
                doppleposition_y += 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved:
                if box_can_move_to(box[0], box[1] + 1):
                    box[1] += 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
        for kill in movablekilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0], kill[1] + 1] in validtiles:
                    kill[1] += 1
                    hasmoved.append(kill)
        for kill in vanitykilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0], kill[1] + 1] in validtiles:
                    kill[1] += 1
                    hasmoved.append(kill)
    
    for conveyor in conveyor_left:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
            if [position_x - 1, position_y] in validtiles and [position_x - 1, position_y] not in boxes and [position_x - 1, position_y] not in partial_left:
                position_x -= 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
            if [doppleposition_x - 1, doppleposition_y] in validtiles and [doppleposition_x - 1, doppleposition_y] not in boxes and [doppleposition_x - 1, doppleposition_y] not in partial_left:
                doppleposition_x -= 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved:
                if box_can_move_to(box[0] - 1, box[1]):
                    box[0] -= 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
        for kill in movablekilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0] - 1, kill[1]] in validtiles:
                    kill[0] -= 1
                    hasmoved.append(kill)
        for kill in vanitykilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0] - 1, kill[1]] in validtiles:
                    kill[0] -= 1
                    hasmoved.append(kill)
    
    for conveyor in conveyor_right:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
            if [position_x + 1, position_y] in validtiles and [position_x + 1, position_y] not in boxes and [position_x + 1, position_y] not in partial_right:
                position_x += 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
            if [doppleposition_x + 1, doppleposition_y] in validtiles and [doppleposition_x + 1, doppleposition_y] not in boxes and [doppleposition_x + 1, doppleposition_y] not in partial_right:
                doppleposition_x += 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved:
                if box_can_move_to(box[0] + 1, box[1]):
                    box[0] += 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
        for kill in movablekilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0] + 1, kill[1]] in validtiles:
                    kill[0] += 1
                    hasmoved.append(kill)
        for kill in vanitykilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0] + 1, kill[1]] in validtiles:
                    kill[0] += 1
                    hasmoved.append(kill)
    
    # Process red conveyors
    if switchstate == False:
        for conveyor in red_conveyor_up:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x, position_y - 1] in validtiles and [position_x, position_y - 1] not in boxes and [position_x, position_y - 1] not in partial_up:
                    position_y -= 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x, doppleposition_y - 1] in validtiles and [doppleposition_x, doppleposition_y - 1] not in boxes and [doppleposition_x, doppleposition_y - 1] not in partial_up:
                    doppleposition_y -= 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0], box[1] - 1):
                        box[1] -= 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
        
        for conveyor in red_conveyor_down:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x, position_y + 1] in validtiles and [position_x, position_y + 1] not in boxes and [position_x, position_y + 1] not in partial_down:
                    position_y += 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x, doppleposition_y + 1] in validtiles and [doppleposition_x, doppleposition_y + 1] not in boxes and [doppleposition_x, doppleposition_y + 1] not in partial_down:
                    doppleposition_y += 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0], box[1] + 1):
                        box[1] += 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
        
        for conveyor in red_conveyor_left:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x - 1, position_y] in validtiles and [position_x - 1, position_y] not in boxes and [position_x - 1, position_y] not in partial_left:
                    position_x -= 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x - 1, doppleposition_y] in validtiles and [doppleposition_x - 1, doppleposition_y] not in boxes and [doppleposition_x - 1, doppleposition_y] not in partial_left:
                    doppleposition_x -= 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0] - 1, box[1]):
                        box[0] -= 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
        
        for conveyor in red_conveyor_right:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x + 1, position_y] in validtiles and [position_x + 1, position_y] not in boxes and [position_x + 1, position_y] not in partial_right:
                    position_x += 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x + 1, doppleposition_y] in validtiles and [doppleposition_x + 1, doppleposition_y] not in boxes and [doppleposition_x + 1, doppleposition_y] not in partial_right:
                    doppleposition_x += 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0] + 1, box[1]):
                        box[0] += 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
    
    # Process blue conveyors
    if switchstate == True:
        for conveyor in blue_conveyor_up:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x, position_y - 1] in validtiles and [position_x, position_y - 1] not in boxes and [position_x, position_y - 1] not in partial_up:
                    position_y -= 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x, doppleposition_y - 1] in validtiles and [doppleposition_x, doppleposition_y - 1] not in boxes and [doppleposition_x, doppleposition_y - 1] not in partial_up:
                    doppleposition_y -= 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0], box[1] - 1):
                        box[1] -= 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
        
        for conveyor in blue_conveyor_down:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x, position_y + 1] in validtiles and [position_x, position_y + 1] not in boxes and [position_x, position_y + 1] not in partial_down:
                    position_y += 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x, doppleposition_y + 1] in validtiles and [doppleposition_x, doppleposition_y + 1] not in boxes and [doppleposition_x, doppleposition_y + 1] not in partial_down:
                    doppleposition_y += 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0], box[1] + 1):
                        box[1] += 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
        
        for conveyor in blue_conveyor_left:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x - 1, position_y] in validtiles and [position_x - 1, position_y] not in boxes and [position_x - 1, position_y] not in partial_left:
                    position_x -= 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x - 1, doppleposition_y] in validtiles and [doppleposition_x - 1, doppleposition_y] not in boxes and [doppleposition_x - 1, doppleposition_y] not in partial_left:
                    doppleposition_x -= 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0] - 1, box[1]):
                        box[0] -= 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
        
        for conveyor in blue_conveyor_right:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x + 1, position_y] in validtiles and [position_x + 1, position_y] not in boxes and [position_x + 1, position_y] not in partial_right:
                    position_x += 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x + 1, doppleposition_y] in validtiles and [doppleposition_x + 1, doppleposition_y] not in boxes and [doppleposition_x + 1, doppleposition_y] not in partial_right:
                    doppleposition_x += 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0] + 1, box[1]):
                        box[0] += 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
    
    # Process switch conveyors (leftswitchconveyor)
    for conveyor in leftswitchconveyor:
        direction = -1 if switchstate == False else 1
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
            if [position_x + direction, position_y] in validtiles and [position_x + direction, position_y] not in boxes and [position_x + direction, position_y] not in (partial_left if direction == -1 else partial_right):
                position_x += direction
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
            if [doppleposition_x + direction, doppleposition_y] in validtiles and [doppleposition_x + direction, doppleposition_y] not in boxes and [doppleposition_x + direction, doppleposition_y] not in (partial_left if direction == -1 else partial_right):
                doppleposition_x += direction
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved:
                if box_can_move_to(box[0] + direction, box[1]):
                    box[0] += direction
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
        for kill in movablekilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0] + direction, kill[1]] in validtiles:
                    kill[0] += direction
                    hasmoved.append(kill)
        for kill in vanitykilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0] + direction, kill[1]] in validtiles:
                    kill[0] += direction
                    hasmoved.append(kill)
    
    # Process switch conveyors (rightswitchconveyor)
    for conveyor in rightswitchconveyor:
        direction = 1 if switchstate == False else -1
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
            if [position_x + direction, position_y] in validtiles and [position_x + direction, position_y] not in boxes and [position_x + direction, position_y] not in (partial_right if direction == 1 else partial_left):
                position_x += direction
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
            if [doppleposition_x + direction, doppleposition_y] in validtiles and [doppleposition_x + direction, doppleposition_y] not in boxes and [doppleposition_x + direction, doppleposition_y] not in (partial_right if direction == 1 else partial_left):
                doppleposition_x += direction
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved:
                if box_can_move_to(box[0] + direction, box[1]):
                    box[0] += direction
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
        for kill in movablekilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0] + direction, kill[1]] in validtiles:
                    kill[0] += direction
                    hasmoved.append(kill)
        for kill in vanitykilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0] + direction, kill[1]] in validtiles:
                    kill[0] += direction
                    hasmoved.append(kill)
    
    # Process switch conveyors (upswitchconveyor)
    for conveyor in upswitchconveyor:
        direction = -1 if switchstate == False else 1
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
            if [position_x, position_y + direction] in validtiles and [position_x, position_y + direction] not in boxes and [position_x, position_y + direction] not in (partial_up if direction == -1 else partial_down):
                position_y += direction
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
            if [doppleposition_x, doppleposition_y + direction] in validtiles and [doppleposition_x, doppleposition_y + direction] not in boxes and [doppleposition_x, doppleposition_y + direction] not in (partial_up if direction == -1 else partial_down):
                doppleposition_y += direction
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved:
                if box_can_move_to(box[0], box[1] + direction):
                    box[1] += direction
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
        for kill in movablekilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0], kill[1] + direction] in validtiles:
                    kill[1] += direction
                    hasmoved.append(kill)
        for kill in vanitykilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0], kill[1] + direction] in validtiles:
                    kill[1] += direction
                    hasmoved.append(kill)
    
    # Process switch conveyors (downswitchconveyor)
    for conveyor in downswitchconveyor:
        direction = 1 if switchstate == False else -1
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
            if [position_x, position_y + direction] in validtiles and [position_x, position_y + direction] not in boxes and [position_x, position_y + direction] not in (partial_down if direction == 1 else partial_up):
                position_y += direction
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
            if [doppleposition_x, doppleposition_y + direction] in validtiles and [doppleposition_x, doppleposition_y + direction] not in boxes and [doppleposition_x, doppleposition_y + direction] not in (partial_down if direction == 1 else partial_up):
                doppleposition_y += direction
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved:
                if box_can_move_to(box[0], box[1] + direction):
                    box[1] += direction
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
        for kill in movablekilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0], kill[1] + direction] in validtiles:
                    kill[1] += direction
                    hasmoved.append(kill)
        for kill in vanitykilltiles:
            if kill == conveyor and kill not in hasmoved:
                if [kill[0], kill[1] + direction] in validtiles:
                    kill[1] += direction
                    hasmoved.append(kill)

    # yellow conveyors
    for conveyor in yellow_conveyor_up:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved and altstate == False:
            if [position_x, position_y - 1] in validtiles and [position_x, position_y - 1] not in boxes and [position_x, position_y - 1] not in partial_up:
                position_y -= 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved and altstate == False:
            if [doppleposition_x, doppleposition_y - 1] in validtiles and [doppleposition_x, doppleposition_y - 1] not in boxes and [doppleposition_x, doppleposition_y - 1] not in partial_up:
                doppleposition_y -= 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved and altstate == False:
                if box_can_move_to(box[0], box[1] - 1):
                    box[1] -= 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == False:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == False:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
    for conveyor in yellow_conveyor_down:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved and altstate == False:
            if [position_x, position_y + 1] in validtiles and [position_x, position_y + 1] not in boxes and [position_x, position_y + 1] not in partial_down:
                position_y += 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved and altstate == False:
            if [doppleposition_x, doppleposition_y + 1] in validtiles and [doppleposition_x, doppleposition_y + 1] not in boxes and [doppleposition_x, doppleposition_y + 1] not in partial_down:
                doppleposition_y += 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved and altstate == False:
                if box_can_move_to(box[0], box[1] + 1):
                    box[1] += 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == False:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == False:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
    for conveyor in yellow_conveyor_left:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved and altstate == False:
            if [position_x - 1, position_y] in validtiles and [position_x - 1, position_y] not in boxes and [position_x - 1, position_y] not in partial_left:
                position_x -= 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved and altstate == False:
            if [doppleposition_x - 1, doppleposition_y] in validtiles and [doppleposition_x - 1, doppleposition_y] not in boxes and [doppleposition_x - 1, doppleposition_y] not in partial_left:
                doppleposition_x -= 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved and altstate == False:
                if box_can_move_to(box[0] - 1, box[1]):
                    box[0] -= 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == False:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == False:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
    for conveyor in yellow_conveyor_right:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved and altstate == False:
            if [position_x + 1, position_y] in validtiles and [position_x + 1, position_y] not in boxes and [position_x + 1, position_y] not in partial_right:
                position_x += 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved and altstate == False:
            if [doppleposition_x + 1, doppleposition_y] in validtiles and [doppleposition_x + 1, doppleposition_y] not in boxes and [doppleposition_x + 1, doppleposition_y] not in partial_right:
                doppleposition_x += 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved and altstate == False:
                if box_can_move_to(box[0] + 1, box[1]):
                    box[0] += 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == False:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == False:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
    for conveyor in green_conveyor_up:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved and altstate == True:
            if [position_x, position_y - 1] in validtiles and [position_x, position_y - 1] not in boxes and [position_x, position_y - 1] not in partial_up:
                position_y -= 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved and altstate == True:
            if [doppleposition_x, doppleposition_y - 1] in validtiles and [doppleposition_x, doppleposition_y - 1] not in boxes and [doppleposition_x, doppleposition_y - 1] not in partial_up:
                doppleposition_y -= 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved and altstate == True:
                if box_can_move_to(box[0], box[1] - 1):
                    box[1] -= 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == True:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == True:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
    for conveyor in green_conveyor_down:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved and altstate == True:
            if [position_x, position_y + 1] in validtiles and [position_x, position_y + 1] not in boxes and [position_x, position_y + 1] not in partial_down:
                position_y += 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved and altstate == True:
            if [doppleposition_x, doppleposition_y + 1] in validtiles and [doppleposition_x, doppleposition_y + 1] not in boxes and [doppleposition_x, doppleposition_y + 1] not in partial_down:
                doppleposition_y += 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved and altstate == True:
                if box_can_move_to(box[0], box[1] + 1):
                    box[1] += 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == True:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == True:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
    for conveyor in green_conveyor_left:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved and altstate == True:
            if [position_x - 1, position_y] in validtiles and [position_x - 1, position_y] not in boxes and [position_x - 1, position_y] not in partial_left:
                position_x -= 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved and altstate == True:
            if [doppleposition_x - 1, doppleposition_y] in validtiles and [doppleposition_x - 1, doppleposition_y] not in boxes and [doppleposition_x - 1, doppleposition_y] not in partial_left:
                doppleposition_x -= 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved and altstate == True:
                if box_can_move_to(box[0] - 1, box[1]):
                    box[0] -= 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == True:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == True:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
    for conveyor in green_conveyor_right:
        if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved and altstate == True:
            if [position_x + 1, position_y] in validtiles and [position_x + 1, position_y] not in boxes and [position_x + 1, position_y] not in partial_right:
                position_x += 1
                px.play(0, 0)
                hasmoved.append([position_x, position_y])
        if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved and altstate == True:
            if [doppleposition_x + 1, doppleposition_y] in validtiles and [doppleposition_x + 1, doppleposition_y] not in boxes and [doppleposition_x + 1, doppleposition_y] not in partial_right:
                doppleposition_x += 1
                px.play(0, 0)
                hasmoved.append([doppleposition_x, doppleposition_y])
        for box in boxes:
            if box == conveyor and box not in hasmoved and altstate == True:
                if box_can_move_to(box[0] + 1, box[1]):
                    box[0] += 1
                    px.play(0, 0)
                    hasmoved.append(box)
                    if box in boxholes:
                        px.play(3, 4)
                        settledboxes.append(box)
                        validtiles.append(box)
                        boxholes.remove(box)
                        boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == True:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved and altstate == True:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
    for conveyor in altconveyorswitch_up:
        if altstate == False:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x, position_y - 1] in validtiles and [position_x, position_y - 1] not in boxes and [position_x, position_y - 1] not in partial_up:
                    position_y -= 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x, doppleposition_y - 1] in validtiles and [doppleposition_x, doppleposition_y - 1] not in boxes and [doppleposition_x, doppleposition_y - 1] not in partial_up:
                    doppleposition_y -= 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0], box[1] - 1):
                        box[1] -= 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
        if altstate == True:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x, position_y + 1] in validtiles and [position_x, position_y + 1] not in boxes and [position_x, position_y + 1] not in partial_down:
                    position_y += 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x, doppleposition_y + 1] in validtiles and [doppleposition_x, doppleposition_y + 1] not in boxes and [doppleposition_x, doppleposition_y + 1] not in partial_down:
                    doppleposition_y += 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0], box[1] + 1):
                        box[1] += 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
    for conveyor in altconveyorswitch_down:
        if altstate == False:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x, position_y + 1] in validtiles and [position_x, position_y + 1] not in boxes and [position_x, position_y + 1] not in partial_down:
                    position_y += 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x, doppleposition_y + 1] in validtiles and [doppleposition_x, doppleposition_y + 1] not in boxes and [doppleposition_x, doppleposition_y + 1] not in partial_down:
                    doppleposition_y += 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0], box[1] + 1):
                        box[1] += 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] + 1] in validtiles:
                        kill[1] += 1
                        hasmoved.append(kill)
        if altstate == True:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x, position_y - 1] in validtiles and [position_x, position_y - 1] not in boxes and [position_x, position_y - 1] not in partial_up:
                    position_y -= 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x, doppleposition_y - 1] in validtiles and [doppleposition_x, doppleposition_y - 1] not in boxes and [doppleposition_x, doppleposition_y - 1] not in partial_up:
                    doppleposition_y -= 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0], box[1] - 1):
                        box[1] -= 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0], kill[1] - 1] in validtiles:
                        kill[1] -= 1
                        hasmoved.append(kill)
    for conveyor in altconveyorswitch_left:
        if altstate == False:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x - 1, position_y] in validtiles and [position_x - 1, position_y] not in boxes and [position_x - 1, position_y] not in partial_left:
                    position_x -= 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x - 1, doppleposition_y] in validtiles and [doppleposition_x - 1, doppleposition_y] not in boxes and [doppleposition_x - 1, doppleposition_y] not in partial_left:
                    doppleposition_x -= 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0] - 1, box[1]):
                        box[0] -= 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
        if altstate == True:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x + 1, position_y] in validtiles and [position_x + 1, position_y] not in boxes and [position_x + 1, position_y] not in partial_right:
                    position_x += 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x + 1, doppleposition_y] in validtiles and [doppleposition_x + 1, doppleposition_y] not in boxes and [doppleposition_x + 1, doppleposition_y] not in partial_right:
                    doppleposition_x += 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0] + 1, box[1]):
                        box[0] += 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
    for conveyor in altconveyorswitch_right:
        if altstate == False:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x + 1, position_y] in validtiles and [position_x + 1, position_y] not in boxes and [position_x + 1, position_y] not in partial_right:
                    position_x += 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x + 1, doppleposition_y] in validtiles and [doppleposition_x + 1, doppleposition_y] not in boxes and [doppleposition_x + 1, doppleposition_y] not in partial_right:
                    doppleposition_x += 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0] + 1, box[1]):
                        box[0] += 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] + 1, kill[1]] in validtiles:
                        kill[0] += 1
                        hasmoved.append(kill)
        if altstate == True:
            if [position_x, position_y] == conveyor and [position_x, position_y] not in hasmoved:
                if [position_x - 1, position_y] in validtiles and [position_x - 1, position_y] not in boxes and [position_x - 1, position_y] not in partial_left:
                    position_x -= 1
                    px.play(0, 0)
                    hasmoved.append([position_x, position_y])
            if doppleon == True and [doppleposition_x, doppleposition_y] == conveyor and [doppleposition_x, doppleposition_y] not in hasmoved:
                if [doppleposition_x - 1, doppleposition_y] in validtiles and [doppleposition_x - 1, doppleposition_y] not in boxes and [doppleposition_x - 1, doppleposition_y] not in partial_left:
                    doppleposition_x -= 1
                    px.play(0, 0)
                    hasmoved.append([doppleposition_x, doppleposition_y])
            for box in boxes:
                if box == conveyor and box not in hasmoved:
                    if box_can_move_to(box[0] - 1, box[1]):
                        box[0] -= 1
                        px.play(0, 0)
                        hasmoved.append(box)
                        if box in boxholes:
                            px.play(3, 4)
                            settledboxes.append(box)
                            validtiles.append(box)
                            boxholes.remove(box)
                            boxes.remove(box)
            for kill in movablekilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)
            for kill in vanitykilltiles:
                if kill == conveyor and kill not in hasmoved:
                    if [kill[0] - 1, kill[1]] in validtiles:
                        kill[0] -= 1
                        hasmoved.append(kill)

    hasmoved.clear()

#------ draw function -------
def draw():
    global playframe,switcheffectanimx,switcheffectanimy,switches,switchmodules,uiframe,switchboost,baseposition_y,baseposition_x,glitchframe,altswitcheffectanimx,altswitcheffectanimy,altswitchboost
    px.cls(0)
    if not remix:
        
            #game texturing
            # display of the level (no end so far)
        uiframe+=0.025
        if level == 0:
            px.bltm(128,128,0,0,0,8*16,8*16,0,0,zoom)
        if level == 1:
            px.bltm(128,128,0,8*16,0,8*16,8*16,0,0,zoom)
        if level == 2:
            px.bltm(128,128,0,16*16,0,8*16,8*16,0,0,zoom)
        if level == 3:
            px.bltm(128,128,0,24*16,0,8*16,8*16,0,0,zoom)
        if level == 4:
            px.bltm(128,128,0,32*16,0,8*16,8*16,0,0,zoom)
        if level == 5:
            px.bltm(128,128,0,0*16,8*16,8*16,8*16,0,0,zoom)
        if level == 6:
            px.bltm(128,128,0,8*16,8*16,8*16,8*16,0,0,zoom)
        if level == 7:
            px.bltm(128,128,0,16*16,8*16,8*16,8*16,0,0,zoom)
        if level == 8:
            px.bltm(128,128,0,24*16,8*16,8*16,8*16,0,0,zoom)
        if level == 9:
            px.bltm(128,128,0,32*16,8*16,8*16,8*16,0,0,zoom)
        if level == 10:
            px.bltm(128,128,0,0*16,16*16,8*16,8*16,0,0,zoom)
        if level == 11:
            px.bltm(128,128,0,8*16,16*16,8*16,8*16,0,0,zoom)
        if level == 12:
            px.bltm(128,128,0,16*16,16*16,8*16,8*16,0,0,zoom)
        if level == 13:
            px.bltm(128,128,0,24*16,16*16,8*16,8*16,0,0,zoom)
        if level == 14:
            px.bltm(128,128,0,32*16,16*16,8*16,8*16,0,0,zoom)
        if level == 15:
            px.bltm(128,128,0,0*16,24*16,8*16,8*16,0,0,zoom)
        if level == 16:
            px.bltm(128,128,0,8*16,24*16,8*16,8*16,0,0,zoom)
        if level == 17:
            px.bltm(128,128,0,16*16,24*16,8*16,8*16,0,0,zoom)
        if level == 18:
            px.bltm(128,128,0,24*16,24*16,8*16,8*16,0,0,zoom)
        if level == 19:
            px.bltm(64+32,64+32,0,80*8,0,12*16,12*16,0,0,zoom)
        if level == 20:
            px.bltm(64+32,64+32,0,104*8,0,12*16,12*16,0,0,zoom)
        if level == 21:
            px.bltm(64+32,64+32,0,128*8,0,12*16,12*16,0,0,zoom)
        if level == 22:
            px.bltm(128,128,0,80*8,24*8,8*16,8*16,0,0,zoom)
        if level == 23:
            px.bltm(128,128,2,0*16,0*16,8*16,8*16,0,0,zoom)
        if level == 24:
            px.bltm(128,128,2,8*16,0*16,8*16,8*16,0,0,zoom)
        if level == 25:
            px.bltm(128,128,2,16*16,0*16,8*16,8*16,0,0,zoom)
        if level == 26:
            px.bltm(128,128,2,24*16,0*16,8*16,8*16,0,0,zoom)
        if level == 27:
            px.bltm(128,128,2,32*16,0*16,8*16,8*16,0,0,zoom)
        if level == 28:
            px.bltm(128,128,2,40*16,0*16,8*16,8*16,0,0,zoom)
        if level==29:
            px.bltm(128,128,2,56*16,0*16,8*16,8*16,0,0,zoom)
        if level==30:
            px.bltm(64+32,64+32,2,12*16,8*16,12*16,12*16,0,0,zoom)
        if level == 31:
            px.bltm(128,128,2,48*16,0*16,8*16,8*16,0,0,zoom)
        if level == 32:
            px.bltm(64+32,64+32,2,24*16,8*16,12*16,12*16,0,0,zoom)
        if level == 33:
            px.bltm(64+32,64+32,2,48*16,8*16,12*16,12*16,0,0,zoom)
        if level == 34:
            px.bltm(128,128,2,64*16,0*16,8*16,8*16,0,0,zoom)
        if level == 35 :
            px.bltm(64+32,64+32,2,0*16,8*16,12*16,12*16,0,0,zoom)
        if level == 36:
            px.bltm(64+32,64+32,2,60*16,8*16,12*16,12*16,0,0,zoom)
        if level == 37:
            px.bltm(64+32,64+32,2,72*16,8*16,12*16,12*16,0,0,zoom)
        if level == 38:
            px.bltm(64+32,64+32,2,84*16,8*16,12*16,12*16,0,0,zoom)
        if level == 39:
            px.bltm(64+32,64+32,2,36*16,8*16,12*16,12*16,0,0,zoom)
        if level == 40:
            px.bltm(64+32,64+32,0,152*8,0,12*16,12*16,0,0,zoom)
        if level == 41:
            px.bltm(64+32,64+32,0,176*8,0,12*16,12*16,0,0,zoom)
        if level == 42:
            px.bltm(64+32,64+32,0,200*8,0,12*16,12*16,0,0,zoom)
        if level == 43:
            px.bltm(64+32,64+32,0,224*8,0,12*16,12*16,0,0,zoom)
        if level == 44:
            px.bltm(64+32,64+32,0,112*8,24*8,12*16,12*16,0,0,zoom)
        if level == 45:
            px.bltm(64+32,64+32,0,136*8,24*8,12*16,12*16,0,0,zoom)
        if level == 46:
            reqx=3.5-position_x
            reqy=3.5-position_y
            baseposition_x=((5*baseposition_x+3.5-position_x)/6)*16//1/16
            baseposition_y=((5*baseposition_y+3.5-position_y)/6)*16//1/16
            px.bltm(128,128,3,(3.5-baseposition_x)*16,(3.5-baseposition_y)*16,8*16,8*16,0,0,zoom)
    if remix:
        if level==0:
            px.bltm(128,128,4,0,0,8*16,8*16,0,0,zoom)


    if not altstate:
        for tile in killzones:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,48,32,16,16,None,0,zoom)
        for tile in altkillzones:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,48,16,16,None,0,zoom)
        for tile in altswitches:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,48,16,16,None,0,zoom)
        for tile in yellowtiles:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,224,48,16,16,None,0,zoom)
        for tile in greentiles:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,240,48,16,16,None,0,zoom)


    else:
        for tile in killzones:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,32,16,16,None,0,zoom)
        for tile in altkillzones:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,32,16,16,None,0,zoom)
        for tile in altswitches:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,48,16,16,None,0,zoom)
        for tile in yellowtiles:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,224,64,16,16,None,0,zoom)
        for tile in greentiles:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,240,64,16,16,None,0,zoom)


    for tile in triggertiles:
        if tile[2]==True:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,0,32,16,16,0,0,zoom)

    if unlocked==True:
        px.blt(endtile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), endtile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,48,16,16,16,0,0,zoom)
        if doppleon==True:
            px.blt(doppleendtile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), doppleendtile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,48,16,16,16,0,0,zoom)

    for switch in switches:
        if switchstate==False:
            px.blt(switch[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), switch[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,96,16,16,16,None,0,zoom)
        else:
            px.blt(switch[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), switch[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,80,16,16,16,None,0,zoom)

    for block in breakable3:
        px.blt(block[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), block[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,64,0,16,16,None,0,zoom)
    
    for block in breakable2:
        px.blt(block[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), block[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,80,0,16,16,None,0,zoom)

    for block in breakable1:
        px.blt(block[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), block[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,96,0,16,16,None,0,zoom)

    for rotator in rightrotators:
        px.blt(rotator[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), rotator[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,64,16,16,16,None,0,zoom)
    
    for rotator in leftrotators:
        px.blt(rotator[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), rotator[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,64,32,16,16,None,0,zoom)

    for brokenblock in broken:
        px.blt(brokenblock[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), brokenblock[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,0,0,16,16,None,0,zoom)

    for spike in spikelist:
        if switchstate==False:
            px.blt(spike[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), spike[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,80,32,16,16,None,0,zoom)
        else:
            px.blt(spike[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), spike[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,80,48,16,16,None,0,zoom)
    for spike in reversespikelist:
        if switchstate==False:
            px.blt(spike[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), spike[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,96,32,16,16,None,0,zoom)
        else:
            px.blt(spike[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), spike[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,96,48,16,16,None,0,zoom)

   

    for redright in rightrotators_red:
        if switchstate==False:
            px.blt(redright[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), redright[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,112,0,16,16,None,0,zoom)
        else:
            px.blt(redright[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), redright[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,112,16,16,16,None,0,zoom)

    for redleft in leftrotators_red:
        if switchstate==False:
            px.blt(redleft[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), redleft[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,144,0,16,16,None,0,zoom)
        else:
            px.blt(redleft[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), redleft[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,144,16,16,16,None,0,zoom)

    for blueright in rightrotators_blue:
        if switchstate==True:
            px.blt(blueright[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), blueright[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,128,16,16,16,None,0,zoom)
        else:
            px.blt(blueright[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), blueright[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,128,0,16,16,None,0,zoom)
    
    for blueleft in leftrotators_blue:
        if switchstate==True:
            px.blt(blueleft[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), blueleft[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,160,16,16,16,None,0,zoom)
        else:
            px.blt(blueleft[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), blueleft[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,160,0,16,16,None,0,zoom)

    for switchleft in leftrotators_switch:
        if switchstate==False:
            px.blt(switchleft[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), switchleft[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,144,32,16,16,None,0,zoom)
        else:
            px.blt(switchleft[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), switchleft[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,144,48,16,16,None,0,zoom)
    
    for switchright in rightrotators_switch:
        if switchstate==False:
            px.blt(switchright[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), switchright[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,160,32,16,16,None,0,zoom)
        else:
            px.blt(switchright[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), switchright[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,160,48,16,16,None,0,zoom)
    
    for redblock in redtiles:
        if switchstate==False:
            px.blt(redblock[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), redblock[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,112,32,16,16,None,0,zoom)
        else:
            px.blt(redblock[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), redblock[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,112,48,16,16,None,0,zoom)
    
    for blueblock in bluetiles:
        if switchstate==True:
            px.blt(blueblock[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), blueblock[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,128,48,16,16,None,0,zoom)
        else:
            px.blt(blueblock[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), blueblock[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,128,32,16,16,None,0,zoom)


    
    for conveyor in conveyor_up :
        px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,0,16,16,None,0,zoom)
    for conveyor in conveyor_down :
        px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,0,16,16,None,180,zoom)
    for conveyor in conveyor_left :
        px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,0,16,16,None,270,zoom)
    for conveyor in conveyor_right :
        px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,0,16,16,None,90,zoom)
    
    if switchstate==False:
        for conveyor in red_conveyor_up :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,0,16,16,None,0,zoom)
        for conveyor in red_conveyor_down :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,0,16,16,None,180,zoom)
        for conveyor in red_conveyor_left :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,0,16,16,None,270,zoom)
        for conveyor in red_conveyor_right :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,0,16,16,None,90,zoom)

        for conveyor in blue_conveyor_up :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,224,0,16,16,None,0,zoom)
        for conveyor in blue_conveyor_down :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,224,0,16,16,None,180,zoom)
        for conveyor in blue_conveyor_left :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,224,0,16,16,None,270,zoom)
        for conveyor in blue_conveyor_right :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,224,0,16,16,None,90,zoom)
        
    else :
        for conveyor in red_conveyor_up :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,0,16,16,None,0,zoom)
        for conveyor in red_conveyor_down :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,0,16,16,None,180,zoom)
        for conveyor in red_conveyor_left :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,0,16,16,None,270,zoom)
        for conveyor in red_conveyor_right :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,0,16,16,None,90,zoom)

        for conveyor in blue_conveyor_up :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,240,0,16,16,None,0,zoom)
        for conveyor in blue_conveyor_down :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,240,0,16,16,None,180,zoom)
        for conveyor in blue_conveyor_left :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,240,0,16,16,None,270,zoom)
        for conveyor in blue_conveyor_right :
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,240,0,16,16,None,90,zoom)

    for conveyor in leftswitchconveyor :
        if switchstate==False:
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,16,16,16,None,270,zoom)
        else:
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,16,16,16,None,270,zoom)
    for conveyor in rightswitchconveyor :
        if switchstate==False:
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,16,16,16,None,90,zoom)
        else:
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,16,16,16,None,90,zoom)
    for conveyor in upswitchconveyor :
        if switchstate==False:
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,16,16,16,None,0,zoom)
        else:
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,16,16,16,None,0,zoom)
    for conveyor in downswitchconveyor :
        if switchstate==False:
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,16,16,16,None,180,zoom)
        else:
            px.blt(conveyor[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), conveyor[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,16,16,16,None,180,zoom)

    for switch in switchmodules:
        if switchstate==False:
            px.blt(switch[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), switch[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,96,16,16,1,0,zoom)
        else:
            px.blt(switch[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), switch[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,112,16,16,1,0,zoom)
    if altstate :
        for tile in altswitchmodules:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,224,94,16,16,1,0,zoom)
    else:
        for tile in altswitchmodules:
            px.blt(tile[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), tile[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,224,112,16,16,1,0,zoom)

    for kill in movablekilltiles :
        px.blt(kill[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), kill[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,64,16,16,0,0,zoom)
    for kill in vanitykilltiles :
        px.blt(kill[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), kill[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,208,64,16,16,0,0,zoom)



    for left in partial_left:
        px.blt(left[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), left[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,48,48,16,16,None,0,zoom)
    for right in partial_right:
        px.blt(right[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), right[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,32,64,16,16,None,0,zoom)
    for down in partial_down:
        px.blt(down[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), down[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,32,48,16,16,None,0,zoom)
    for up in partial_up:
        px.blt(up[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), up[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,48,64,16,16,None,0,zoom)
    for box in boxes:
        px.blt(box[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), box[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,16,48,16,16,0,0,zoom)
    for box in settledboxes:
        px.blt(box[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), box[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,16,48,16,16,0,0,zoom)
    for box in boxholes:
        px.blt(box[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), box[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,16,64,16,16,None,0,zoom)
    for box in halfboxes :
        px.blt(box[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), box[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,16,16,16,16,None,0,zoom)

    if not altstate:
        for laser in yellowlaser :
            if laser[2]==0:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,88,112,16,16,None,270,zoom)
            elif laser[2]==1:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,88,112,16,16,None,0,zoom)
            elif laser[2]==2:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,88,112,16,16,None,90,zoom)
            elif laser[2]==3:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,88,112,16,16,None,180,zoom)
        for laser in greenlaser :
            if laser[2]==0:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,72,120,16,16,None,270,zoom)
            elif laser[2]==1:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,72,120,16,16,None,0,zoom)
            elif laser[2]==2:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,72,120,16,16,None,90,zoom)
            elif laser[2]==3:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,72,120,16,16,None,180,zoom)
        
        for beam in yellowbeam :
            if beam[2]==0:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,104,112,16,16,0,0,zoom)
            if beam[2]==1:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,104,112,16,16,0,90,zoom)
        
        for beam in yellowbeamend :
            if beam[2]==0:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,128,16,16,0,270,zoom)
            if beam[2]==1:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,112,16,16,0,0,zoom)
            if beam[2]==2:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,112,16,16,0,90,zoom)
            if beam[2]==3:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,176,112,16,16,0,180,zoom)

        for beam in yellowcornerbeam :
            if beam[2]==0:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,120,112,16,16,0,270,zoom)
            if beam[2]==1:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,120,112,16,16,0,0,zoom)
            if beam[2]==2:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,120,112,16,16,0,90,zoom)
            if beam[2]==3:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,120,112,16,16,0,180,zoom)

    else :
        for laser in yellowlaser :
            if laser[2]==0:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,56,120,16,16,None,270,zoom)
            elif laser[2]==1:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,56,120,16,16,None,0,zoom)
            elif laser[2]==2:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,56,120,16,16,None,90,zoom)
            elif laser[2]==3:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,56,120,16,16,None,180,zoom)
        for laser in greenlaser :
            if laser[2]==0:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,88,128,16,16,None,270,zoom)
            elif laser[2]==1:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,88,128,16,16,None,0,zoom)
            elif laser[2]==2:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,88,128,16,16,None,90,zoom)
            elif laser[2]==3:
                px.blt(laser[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), laser[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,88,128,16,16,None,180,zoom)
        for beam in greenbeam :
            if beam[2]==0:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,104,128,16,16,0,0,zoom)
            if beam[2]==1:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,104,128,16,16,0,90,zoom)
        for beam in greenbeamend :
            if beam[2]==0:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,128,16,16,0,270,zoom)
            if beam[2]==1:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,128,16,16,0,0,zoom)
            if beam[2]==2:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,128,16,16,0,90,zoom)
            if beam[2]==3:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,192,128,16,16,0,180,zoom)
        for beam in greencornerbeam :
            if beam[2]==0:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,120,128,16,16,0,270,zoom)
            if beam[2]==1:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,120,128,16,16,0,0,zoom)
            if beam[2]==2:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,120,128,16,16,0,90,zoom)
            if beam[2]==3:
                px.blt(beam[0]*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), beam[1]*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)),0,120,128,16,16,0,180,zoom)

    #the base sprite heads right, each additional heading is a 90 degree clockwise rotation
    if heading == 1:
        px.blt(position_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), position_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)), 0, 0, 48, 16, 16, 0,0,zoom)
    elif heading == 2:
        px.blt(position_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), position_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)), 0, 0, 48, 16, 16, 0,90,zoom)
    elif heading == 3:
        px.blt(position_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), position_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)), 0, 0, 48, 16, 16, 0,180,zoom)
    elif heading == 0:
        px.blt(position_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), position_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)), 0, 0, 48, 16, 16, 0,270,zoom)
    
    if doppleon==True:
        if doppleheading == 1:
            px.blt(doppleposition_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), doppleposition_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)), 0, 0, 64, 16, 16, 0,0,zoom)
        elif doppleheading == 2:
            px.blt(doppleposition_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), doppleposition_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)), 0, 0, 64, 16, 16, 0,90,zoom)
        elif doppleheading == 3:
            px.blt(doppleposition_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), doppleposition_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)), 0, 0, 64, 16, 16, 0,180,zoom)
        elif doppleheading == 0:
            px.blt(doppleposition_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1)), doppleposition_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1)), 0, 0, 64, 16, 16, 0,270,zoom)
    

    
    # ui drawing
    
    if switches!=[] or switchmodules!=[]:

        px.dither(1)
        if switchboost<30:
            switchboost+=1
        switcheffectanimx+=1-10*math.sin(math.radians((30-switchboost)))
        switcheffectanimx%=16
        switcheffectanimy+=0.1
        switchdither=1

        playerposcheck=position_y*16*zoom+baseposition_y*16*zoom+(8*(zoom-1))
        if playerposcheck<64 or playerposcheck>304:
            px.dither(0.5)
            switchdither=0.5
        if playerposcheck<32 or playerposcheck>336:
            px.dither(0.25)
            switchdither=0.25

        if switchboost!=30:
            px.dither(1)
            if switchdither==0.5 and switchboost>=15:
                px.dither(0.5)
            if switchdither==0.25 and switchboost>=10:
                px.dither(0.5)
            if switchdither==0.25 and switchboost>=20:
                px.dither(0.25)
        if switchstate:
            px.rect(0,380+2*math.sin(switcheffectanimy),1000,100,1)
            px.rect(0,0,1000,10,1)
            for i in range(45):
                px.blt(-32+switcheffectanimx+16*i,-2*math.sin(switcheffectanimy)+3,0,48,240,16,16,1,0,1)
            for i in range(45):
                px.blt(-32-switcheffectanimx+16*i,+2*math.sin(switcheffectanimy)-2,0,32,240,16,16,1,0,1)
            for i in range(45):
                px.blt(-32-switcheffectanimx+16*i,365+2*math.sin(switcheffectanimy),0,48,240,16,16,1,180,1)
            for i in range(45):
                px.blt(-32+switcheffectanimx+16*i,-2*math.sin(switcheffectanimy)+370,0,32,240,16,16,1,180,1)
        else:
            px.rect(0,380+2*math.sin(switcheffectanimy),1000,100,15)
            px.rect(0,0,1000,10,15)
            for i in range(45):
                px.blt(-32-switcheffectanimx+16*i,-2*math.sin(switcheffectanimy)+3,0,16,240,16,16,1,180,1)
            for i in range(45):
                px.blt(-32+switcheffectanimx+16*i,+2*math.sin(switcheffectanimy)-2,0,0,240,16,16,1,180,1)
            for i in range(45):
                px.blt(-32+switcheffectanimx+16*i,365+2*math.sin(switcheffectanimy),0,16,240,16,16,1,0,1)
            for i in range(45):
                px.blt(-32-switcheffectanimx+16*i,-2*math.sin(switcheffectanimy)+370,0,0,240,16,16,1,0,1)
        px.dither(1)

    if altswitches!=[] or altswitchmodules!=[]:
        if altswitchboost<30:
            altswitchboost+=1
        altswitcheffectanimx+=1-10*math.sin(math.radians((30-altswitchboost)))
        altswitcheffectanimx%=16
        altswitcheffectanimy+=0.1
        altswitchdither=1
        playerposcheck=position_x*16*zoom+baseposition_x*16*zoom+(8*(zoom-1))
        if playerposcheck<64 or playerposcheck>304:
            px.dither(0.5)
            altswitchdither=0.5
        if playerposcheck<32 or playerposcheck>336:
            px.dither(0.25)
            altswitchdither=0.25
        if altswitchboost!=30:
            px.dither(1)
            if altswitchdither==0.5 and altswitchboost>=15:
                px.dither(0.5)
            if altswitchdither==0.25 and altswitchboost>=10:
                px.dither(0.5)
            if altswitchdither==0.25 and altswitchboost>=20:
                px.dither(0.25)
        if not altstate:
            for i in range(45):
                px.blt(-2*math.sin(altswitcheffectanimy)+3,-32-altswitcheffectanimx+16*i,0,192,240,16,16,1,0,1)
            for i in range(45):
                px.blt(+2*math.sin(altswitcheffectanimy)-2,-32+altswitcheffectanimx+16*i,0,144,240,16,16,1,0,1)
            for i in range(45):
                px.blt(365+2*math.sin(altswitcheffectanimy),-32+altswitcheffectanimx+16*i,0,192,240,16,16,1,180,1)
            for i in range(45):
                px.blt(-2*math.sin(altswitcheffectanimy)+370,-32-altswitcheffectanimx+16*i,0,144,240,16,16,1,180,1)
        else:
            for i in range(45):
                px.blt(-2*math.sin(altswitcheffectanimy)+3,-32+altswitcheffectanimx+16*i,0,224,240,16,16,1,0,1)
            for i in range(45):
                px.blt(+2*math.sin(altswitcheffectanimy)-2,-32-altswitcheffectanimx+16*i,0,208,240,16,16,1,0,1)
            for i in range(45):
                px.blt(365+2*math.sin(altswitcheffectanimy),-32-altswitcheffectanimx+16*i,0,224,240,16,16,1,180,1)
            for i in range(45):
                px.blt(-2*math.sin(altswitcheffectanimy)+370,-32+altswitcheffectanimx+16*i,0,208,240,16,16,1,180,1)
            
        px.dither(1)

    px.rect(128*3+1,0,16,128*3,7)
    px.rect(128*3+16,0,128*2,128*3,0)
    # Map displays (sorted by level)
    
    if not remix:
        # Level titles and UI animations
        if level == 0:
            px.text(405, 20, "Level 0: Basic movement", 7)
            px.bltm(128*3.5+10,128,1,0,0,8*16,4*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 1:
            px.text(405, 20, "Level 1: turning", 7)
            px.bltm(128*3.5+10,128,1,0,4*16,8*16,4*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 2:
            px.text(405, 20, "Level 2: locked in", 7)
            px.bltm(128*3.5+10,128,1,8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 3:
            px.text(405, 20, "Level 3: more locks", 7)
            px.bltm(128*3.5+10,128,1,2*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 4:
            px.text(405, 20, "Level 4: maintenance required", 7)
            px.bltm(128*3.5+10,128,1,3*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 5:
            px.text(405, 20, "Level 5: all falling apart", 7)
            px.bltm(128*3.5+10,128,1,3*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 6:
            px.text(405, 20, "Level 6: entry denied", 7)
            px.bltm(128*3.5+10,128,1,4*8*16,4*16,8*16,4*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 7:
            px.text(405, 20, "Level 7: spinning on our own", 7)
            px.bltm(128*3.5+10,128,1,4*8*16,0,8*16,4*16-16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 8:
            px.text(405, 20, "Level 8: spintrap", 7)
            px.bltm(128*3.5+10,128,1,4*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 9:
            px.text(405, 20, "Level 9: twin snakes", 7)
            px.bltm(128*3.5+10,128,1,5*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 10:
            px.text(405, 20, "Level 10: two sides of the same coin", 7)
            px.bltm(128*3.5+10,128,1,6*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 11:
            px.text(405, 20, "Level 11: offset", 7)
            px.bltm(128*3.5+10,128,1,5*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 12:
            px.text(405, 20, "Level 12: beswitched", 7)
            px.bltm(128*3.5+10,128,1,7*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 13:
            px.text(405, 20, "Level 13: spiky situation", 7)
            px.bltm(128*3.5+10,128,1,8*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 14:
            px.text(405, 20, "Level 14: spinning on our own (again)", 7)
            px.bltm(128*3.5+10,128,1,9*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 15:
            px.text(405, 20, "Level 15: which side are you on ?", 7)
            px.bltm(128*3.5+10,128,1,10*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 16:
            px.text(405, 20, "Level 16: maze", 7)
            px.bltm(128*3.5+10,128,1,10*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 17:
            px.text(405, 20, "Level 17: this side up", 7)
            px.bltm(128*3.5+10,128,1,11*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 18:
            px.text(405, 20, "Level 18: thinking outside the box", 7)
            px.bltm(128*3.5+10,128,1,12*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 19:
            px.text(405, 20, "Level 19 : further perspective", 7)
        if level == 20:
            px.text(405, 20, "Level 20 : automated", 7)
            px.bltm(128*3.5+10,128,1,13*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 21:
            px.text(405, 20, "Level 21 : clockwork", 7)
            px.bltm(128*3.5+10,128,1,14*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 22:
            px.text(405, 20, "Level 22 : a moving menace", 7)
            px.bltm(128*3.5+10,128,1,15*8*16,0,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 23:
            px.text(405, 20, "Level 23 : ladder",7)
        if level == 24:
            px.text(405, 20, "Level 24 : loops",7)
        if level == 25:
            px.text(405, 20, "Level 25 : collapsing star",7)
        if level == 26:
            px.text(405, 20, "Level 26 : step by step",7)
        if level == 27:
            px.text(405, 20, "Level 27 : quarter past pain",7)
        if level == 28:
            px.text(405, 20, "Level 28 : duality",7)
        if level == 29:
            px.text(405, 20, "Level 29 : bridges",7)
        if level == 30:
            px.text(405, 20, "Level 30 : right on time !",7) 
        if level == 31:
            px.text(405, 20, "Level 31 : if there's a hole there's a goal",7)
        if level == 32:
            px.text(405, 20, "Level 32 : carve your own path",7)
            px.bltm(128*3.5+10,100,1,0,8*16,8*16,8*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 33:
            px.text(405, 20, "Level 33 : just a pushover",7)
        if level == 34:
            px.text(405, 20, "Level 34 : a maze (ing)",7)

        if level == 35:
            px.text(405, 20, "Level 35 : can a match box ?",7)
            
        if level == 36:
            px.text(405, 20, "Level 36 : less amazing", 7)

        if level == 37:
            px.text(405, 20, "Level 37 : i hate you.", 7)
        if level == 38:
            px.text(405, 20, "Level 38 : mandala effect", 7)
        if level == 39:
            px.text(405, 20, "Level 39 : subtle foreshadowing", 7)
        if level == 40:
            px.text(405, 20, "Level 40 : Welcome to hell", 7)
        if level == 41:
            px.text(405, 20, "Level 41 : overclocked", 7)
        if level == 42:
            px.text(405, 20, "Level 42 : Konigsberg", 7)
        if level == 43:
            px.text(405, 20, "Level 43 : An old friend", 7)
        if level == 44:
            px.text(405, 20, "Level 44 : Noclip", 7)
        if level == 45:
            px.text(405, 20, "Level 45 : Conveying ideas", 7)
        if level >=23 and level <= 45 and level != 32:
            px.bltm(128*3.5+10,128,1,0,8*16,8*16,4*16,0,1*math.sin(uiframe),1.8+0.1*math.sin(uiframe*0.5))
        if level == 46:
            px.text(405, 20, "Level 46 : the shelter at the end of reality", 7)
            px.blt(128*4-10,128,2,0,32,48,32,0,1*math.sin(uiframe),4+0.2*math.sin(uiframe*0.5))
        if level == 47:
            px.text(405, 20, "Level 47 : reality breaker", 7)
            px.blt(128*3.4-10,128,1,0,96,184,112,0,1*math.sin(uiframe),1+0.1*math.sin(uiframe*0.5))
    if remix:
        if level == 0:
            px.text(405, 20, "Level 0: Back to basics", 7)
        # Display of the level progression
    if not remix :
        yoffset=0
        xoffset=-2
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #0
        if level>=0 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #1
        if level>=1 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #2
        if level>=2 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #3
        if level>=3 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #4
        if level>=4 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #5
        if level>=5 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #6
        if level>=6 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #7
        if level>=7 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #8
        if level>=8 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,0,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 9
        if level>=9 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,16,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 10
        if level>=10 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,16,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 11
        if level>=11 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,16,0,16,16,None,None)
        xoffset=-2
        yoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #12
        if level>=12 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,16,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #13
        if level>=13 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,16,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #14
        if level>=14 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,16,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #15
        if level>=15 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,16,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #16
        if level>=16 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,16,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #17
        if level>=17 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,32,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #18
        if level>=18 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,32,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #19
        if level>=19 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,32,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #20
        if level>=20 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,32,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 21
        if level>=21 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,32,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 22
        if level>=22 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,32,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 23
        if level>=23 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,48,0,16,16,None,None)
        xoffset=-2
        yoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #24
        if level>=24 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,48,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #25
        if level>=25 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,48,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #26
        if level>=26 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,48,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #27
        if level>=27 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,64,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #28
        if level>=28 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,64,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #29
        if level>=29 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,64,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #30
        if level>=30 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,64,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #31
        if level>=31 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,80,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #32
        if level>=32 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,80,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 33
        if level>=33 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,80,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 34
        if level>=34 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,80,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 35
        if level>=35 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,96,0,16,16,None,None)
        xoffset=8
        yoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #36
        if level>=36 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,96,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #37
        if level>=37 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,96,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #38
        if level>=38 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,96,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #39
        if level>=39 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,112,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #40
        if level>=40 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,112,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #41
        if level>=41 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,112,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #42
        if level>=42 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,112,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #43
        if level>=43 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,128,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) #44
        if level>=44 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,128,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 45
        if level>=45 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,128,0,16,16,None,None)
        xoffset+=20
        px.blt(128*3+20+xoffset, 300+yoffset,2,0,16,16,16,None,None) # 46
        if level>=47 :
            px.blt(128*3+20+xoffset, 300+yoffset,2,144,0,16,16,None,None)

    if level>=46 and not remix:
        glitchframe+=1
        if glitchframe>=2:
            glitchframe=rd.randint(0,1)
            for i in range(5):
                if rd.randint(0,1)==0:
                    #glitches : [xcoord,ycoord,width,height,frameduration,alpha,col]
                    xcoord=rd.randint(3*128,4*128+64)
                    ycoord=rd.randint(0,3*128)
                    width=rd.randint(10,100)
                    height=rd.randint(10,40)
                    frameduration=rd.randint(5,15)
                    alpha=rd.randint(0,100)/100
                    glitches.append([xcoord,ycoord,width,height,frameduration,alpha,8])
                else:
                    #glitches : [xcoord,ycoord,width,height,frameduration,alpha,col]
                    xcoord=rd.randint(3*128,4*128+64)
                    ycoord=rd.randint(50,3*128-50)
                    width=rd.randint(10,64)
                    height=rd.randint(10,20)
                    frameduration=rd.randint(15,30)
                    alpha=rd.randint(0,100)/100
                    glitches.append([xcoord,ycoord,width,height,frameduration,alpha,12])
        for glitch in glitches:
            px.dither(glitch[5])
            px.rect(glitch[0],glitch[1],glitch[2],glitch[3],glitch[6])
            glitch[4]-=1
            if glitch[4]<=0:
                glitches.remove(glitch)
        px.dither(1)


    #code for main menu

    global mainframe,doline
    
    if level==-2:
        px.cls(0)
        doline+=1
        if doline==10:
            doline=0
            up=rd.randint(0,1)
            if up==1:
                linelist.append([-90,rd.randint(30,60),rd.randint(1,100)*0.01,rd.randint(2,6)])
            else:
                linelist.append([650,rd.randint(30,60),rd.randint(1,100)*0.01,-rd.randint(2,6)])
        for line in linelist:
            px.dither(line[2])
            px.rect(0,line[0],1000,line[1],1)
            line[0]+=line[3]
            if line[0]<-100 or line[0]>700:
                linelist.remove(line)
            px.dither(1)
        mainframe+=1
        if beaten:
            glitchframe+=1
        if glitchframe>=2:
            glitchframe=rd.randint(0,1)
            for i in range(8):
                if rd.randint(0,1)==0:
                    #glitches : [xcoord,ycoord,width,height,frameduration,alpha,col]
                    xcoord=rd.randint(0,4*128)
                    ycoord=rd.randint(0,3*128)
                    width=rd.randint(10,160)
                    height=rd.randint(10,60)
                    frameduration=rd.randint(5,15)
                    alpha=rd.randint(0,100)/100
                    glitches.append([xcoord,ycoord,width,height,frameduration,alpha,8])
                else:
                    #glitches : [xcoord,ycoord,width,height,frameduration,alpha,col]
                    xcoord=rd.randint(0,4*128)
                    ycoord=rd.randint(0,3*128)
                    width=rd.randint(10,160)
                    height=rd.randint(10,60)
                    frameduration=rd.randint(5,15)
                    alpha=rd.randint(0,100)/100
                    glitches.append([xcoord,ycoord,width,height,frameduration,alpha,12])
        for glitch in glitches:
            px.dither(glitch[5])
            px.rect(glitch[0],glitch[1],glitch[2],glitch[3],glitch[6])
            glitch[4]-=1
            if glitch[4]<=0:
                glitches.remove(glitch)
        px.dither(1)
        px.blt(190,100,1,0,0,256,90,0,5*math.sin(2*math.pi*mainframe/300),2+0.2*math.sin(2*math.pi*mainframe/400))
        if remix:
            px.blt(400,200,2,0,64,192,72,0,5*math.sin(2*math.pi*mainframe/300),1.5+0.2*math.sin(2*math.pi*mainframe/400))
        if not beaten:
            if not remix:
                px.text(280,250,"press \"Z\" to start",7)
            if remix:
                px.text(280,250,"it's here because it's funny",7)
        else :
            px.dither(0.5)
            px.rect(270,235,110,60,7)
            px.rect(275,240,100,50,0)
            px.dither(1)
            px.text(280,250,"Thank you for playing",7)
            px.text(280,270,"press \"Z\" to (re)start",7)
            
    global animate
    #level switch animation
    if level==-2 and not animate:
        px.dither(1-((playframe-60)/60))
        px.rect(0,0,1000,1000,0)
        px.dither(1)
    if animate:
        px.dither(1)
        if playframe<=60:
            if playframe<=30:
                
                px.rect(-5*128+128*5*math.sin(0.5*math.pi*(playframe/30)),0,5*128,0.6*128,7)
            else :
                px.rect(0,0,5*128,0.6*128,7)
            if playframe<=37.5:
                px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-7.5)/30)),0.6*128,5*128,0.6*128,7)
            else :
                px.rect(0,0.6*128,5*128,0.6*128,7)
            if playframe<=45:
                px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-15)/30)),1.2*128,5*128,0.6*128,7)
            else :
                px.rect(0,1.2*128,5*128,0.6*128,7)
            if playframe<=52.5:
                px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-22.5)/30)),1.8*128,5*128,0.6*128,7)
            else :
                px.rect(0,1.8*128,5*128,0.6*128,7)
            if playframe<=60:
                px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-30)/30)),2.4*128,5*128,0.6*128,7)
            else :
                px.rect(0,2.4*128,5*128,0.6*128,7)
        if playframe >60 and playframe <=120:
            px.dither(1)
            if playframe>60:
                if playframe<=90:
                    px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-30)/30)),0,5*128,0.6*128,7)
            else:
                px.rect(0,0,5*128,0.6*128,7)
            if playframe>67.5:
                if playframe<=97.5:
                    px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-37.5)/30)),0.6*128,5*128,0.6*128,7)
            else :
                px.rect(0,0.6*128,5*128,0.6*128,7)
            if playframe>75:
                if playframe<=105:
                    px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-45)/30)),1.2*128,5*128,0.6*128,7)
            else :
                px.rect(0,1.2*128,5*128,0.6*128,7)
            if playframe>82.5:
                if playframe<=112.5:
                    px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-52.5)/30)),1.8*128,5*128,0.6*128,7)
            else:
                px.rect(0,1.8*128,5*128,0.6*128,7)
            if playframe>90:
                if playframe<=120:
                    px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-60)/30)),2.4*128,5*128,0.6*128,7)
            else :
                px.rect(0,2.4*128,5*128,0.6*128,7)
        px.dither(1)

        if playframe>=15 and playframe <=75 :
            px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-15)/30)),0,5*128,0.6*128,0)
        if playframe>=22.5 and playframe <=82.5 :
            px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-22.5)/30)),0.6*128,5*128,0.6*128,0)
        if playframe>=30 and playframe <=90 :
            px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-30)/30)),1.2*128,5*128,0.6*128,0)
        if playframe>=37.5 and playframe <=97.5 :
            px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-37.5)/30)),1.8*128,5*128,0.6*128,0)
        if playframe>=45 and playframe <=105 :
            px.rect(-5*128+128*5*math.sin(0.5*math.pi*((playframe-45)/30)),2.4*128,5*128,0.6*128,0)



#------ sequence function to be completed-------
def sequence():
    global step,delay,maxdelay,insequence,sequencelist
    #NE PAS EDITER
    if step==0:
        resetlevel()
    try:
        imp.reload(sc)
        if step==0:
            rawlist=sc.runsequence()
            sequencelist=[]
            for rawinst in rawlist:
                if rawinst=="turnright":
                    sequencelist.append("turnright")
                if rawinst=="turnleft":
                    sequencelist.append("turnleft")
                if rawinst=="wait":
                    sequencelist.append("wait")
                if type(rawinst)==list:
                    for i in range(rawinst[1]):
                        sequencelist.append("forward")
        
        if sequencelist is None or not isinstance(sequencelist, list):
            return
        if not delay >=maxdelay:
            delay +=1
        else:
            delay=0
            instruction=sequencelist[step]
            if instruction=="forward":
                singleforward()
            elif instruction=="turnleft":
                turnleft()
            elif instruction=="turnright":
                turnright()
            elif instruction=="wait":
                    wait()
            step+=1
        if step==len(sequencelist):
            insequence=False
            step=0
    except Exception as e:
        print(f"Error in sequence: {e}")
        return
def musicplayer():
    global level, played
    if not remix:
        if level>=0 and level<=8 and played !=0:
                played=0
                pygame.mixer.music.load("igm\\Dimension.mp3")
                pygame.mixer.music.play(-1)
        if level>=9 and level<=16 and played !=1:
                played=1
                pygame.mixer.music.load("igm\\ICBM.mp3")
                pygame.mixer.music.play(-1)
        if level>=17 and level<=22 and played !=2:
                played=2
                pygame.mixer.music.load("igm\\Kenophobia.mp3")
                pygame.mixer.music.play(-1)
        if level>=23 and level<=26 and played !=3:
                played=3
                pygame.mixer.music.load("igm\\Mart.mp3")
                pygame.mixer.music.play(-1)
        if level>=27 and level<=30 and played !=4:
                played=4
                pygame.mixer.music.load("igm\\babyface.mp3")
                pygame.mixer.music.play(-1)
        if level>=31 and level<=34 and played !=5:
                played=5
                pygame.mixer.music.load("igm\\youbeatthetutorial.mp3")
                pygame.mixer.music.play(-1)
        if level>=35 and level<=38 and played !=6:
                played=6
                pygame.mixer.music.load("igm\\impenigma.mp3")
                pygame.mixer.music.play(-1)
        if level>=39 and level<=42 and played !=7:
                played=7
                pygame.mixer.music.load("igm\\temporaltenacity.mp3")
                pygame.mixer.music.play(-1)
        if level>=43 and level<=45 and played !=8:
                played=8
                pygame.mixer.music.load("igm\\decaytrue.mp3")
                pygame.mixer.music.play(-1)
        if level==46 and played !=9:
                played=9
                pygame.mixer.music.load("igm\\nil.mp3")
                pygame.mixer.music.play(-1)
        if level==47 and played !=10:
                played=10
                pygame.mixer.music.load("igm\\Aerodynamics.mp3")
                pygame.mixer.music.play(-1)
        if played !=11 and level==-2 and beaten:
                played=11
                pygame.mixer.music.load("igm\\EventHorizon.mp3")
                pygame.mixer.music.play(-1)
    else :
        if level>=0 and level<=8 and played !=12:
                played=12
                pygame.mixer.music.load("igm\\Checkmate.mp3")
                pygame.mixer.music.play(-1)
        if level==-2 and played !=13:
                played=13
                pygame.mixer.music.load("igm\\UU.mp3")
                pygame.mixer.music.play(-1)

def validfinishcheck():
    global position_x, position_y, endtile,finished,unlocked,doppleendtile,doppleposition_x,doppleposition_y,level,remix,switchtoremix
    if doppleon==False:
        if [position_x, position_y] == endtile and unlocked==True:
            global finished
            finished = True
    else :
        if [position_x, position_y] == endtile and unlocked==True and [doppleposition_x,doppleposition_y] == doppleendtile :
            finished = True
    if level==33 and [position_x, position_y] == [9, 6]:
        finished = True
        switchtoremix=True
def update():
    global position_x, position_y, heading,level,finished,animate,speed,insequence,beaten,remix,switchtoremix
    if [position_x,position_y]==[6,4] and level==40:
        position_y+=1
    # vérifie si une touche de modification de la vitesse est pressée
    speedchangecheck()
    manualswitch()
    #lance la séquence si la touche espace est pressée
    if manual==False:
        if px.btnp(px.KEY_SPACE):
            insequence=True
    else: 
        if px.btnp(px.KEY_Z):
            animate=True
            forward(1)
        if px.btnp(px.KEY_D):
            turnright()
        if px.btnp(px.KEY_Q):
            turnleft()
        if px.btnp(px.KEY_R):
            resetlevel()
        if px.btnp(px.KEY_S):
            wait()
    if insequence:
        sequence()
    else:
        validfinishcheck()
    global play, playframe
    if finished==True:
        play=False
        if playframe>122:
            if level==-3:
                playframe=58
            else:
                playframe=0
        if playframe==122:
            finished=False
            play=True
        if playframe<=122:
            playframe+=2
        if playframe==60:
            if level==-2:
                level+=1
            level+=1
            if switchtoremix==True:
                level=-2
                remix=True
                switchtoremix=False
                
            resetlevel()
            unlockedexit()
    if level==48 :
        level=-2
        beaten=True
        resetlevel()
    musicplayer()

px.run(draw, update)