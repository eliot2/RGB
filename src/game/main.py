#===============================================================================
# File:   RGB - beta
# Author: Eliot Carney-Seim
# Date:   1/20/2013
# Email:  eliot2@umbc.edu
# Description:
#        A rhythm game based around the monitor's use of RGB pixels to create
# images to be displayed to the screen.
#===============================================================================

import pygame, sys, os, datetime, platform  # @UnusedImport
import pgext, pygame.gfxdraw, pygame.surface  # @UnusedImport @UnresolvedImport
from pygame.locals import *  # @UnusedWildImport
from pygame.compat import geterror  # @UnusedImport
import math as m  # @UnusedImport
from constants import Constants  # @UnusedImport
from debug import debug  # @UnusedImport
from log import log as logger # @UnusedImport @Reimport
from loader import load_image, load_song  # @UnusedImport
from menu import menu  # @UnusedWildImport
from time import sleep  # @UnusedImport @Reimport
from campaign import campaign
from stock import Stock
from creative import creative
from store import Store
from errorbox import errorbox as errorbox




def main(debugSet):
    # A holding object for transferring major variables and constants.
    c = Constants()
    
    # if debug is set manually, we need to change it, though this is non-in-game
    if debugSet:
        c.DEBUG = True
        
    # holds and loads all game's images.
    stock = Stock(c)
    #holds and loads all the game's music/sounds.
    store = Store(c)

    if c.DEBUG:
        logFile = logger(c)
    # since constants doesn't know about 'debug', and it is where the boolean is
    # made, we'll print the 'whichDisplay' here for debugging.
    debug(c.DEBUG, (c.whichDisplay, c.screenError))
    debug(c.DEBUG, c.displayInfo)
    
    # SCREEN IS LOADED HERE, environment is instantiated within constants.py
    # for convenience purposes.

    debug(c.DEBUG, "ENTERING: main")
    # display the version ID
    font_renderObj = c.FONT_SMALL.render(c.VERSION, False, c.BLACK, c.WHITE)
    versionID_SurfaceObj = font_renderObj
    versionID_RectObj = versionID_SurfaceObj.get_rect()
    versionID_RectObj.topleft = (0, 0)


    

    PygLogo = load_image(c, 'pygame_logo.png')
    PygLogo = pygame.transform.smoothscale(PygLogo, (600, 350))
    PygLogo_rect = PygLogo.get_rect()
    PygLogo_rect.center = c.CENTER
    # fade logo in and out
    fade = 0
    pgext.color.setAlpha(PygLogo, fade, 1)
    pygame.event.clear()
    # fade in LOGO
    for fade in range(255):
        c.DISPLAYSURFACE.fill((0, 0, 0))
        c.DISPLAYSURFACE.blit(PygLogo, PygLogo_rect)
        pgext.color.setAlpha(PygLogo, fade, 1)
        c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        pygame.display.flip()
        sleep(0.01)
        if pygame.event.poll().type != NOEVENT:
            break
    fade = 255
    pgext.color.setAlpha(PygLogo, fade, 1)
    c.DISPLAYSURFACE.fill((0, 0, 0))


    mult = 1.7
    background = load_image(c, 'starBG.png')#.convert_alpha()
    #cut the background into a smaller, more manageable size.
    background = background.subsurface((0,0),(800*mult, 600*mult) ).copy()
    background_rect = background.get_rect()
    background_rect.center = c.CENTER

    fade = 0
    background_rect = background.get_rect()
    background_rect.center = c.CENTER
    pgext.color.setAlpha(background, fade, 1)
    pygame.event.clear()
    # fade in BACKGROUND
    store.music["menu2"].play()
    for fade in range(0, 200, 3):
        c.DISPLAYSURFACE.fill((0, 0, 0))
        c.DISPLAYSURFACE.blit(background, background_rect)
        pgext.color.setAlpha(background, fade, 1)
        c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
        pygame.display.flip()
        sleep(0.01)
        if pygame.event.poll().type != NOEVENT:
            break
    fade = 255
    pgext.color.setAlpha(background, fade, 1)


    playing = True
    while playing:
        selected = menu(c, background, stock, store) 
        store.music['menu2'].stop()
        # menu will return a list, [gamemode,option,quit]. if it's gamemode
        # we have to look at the second number in the list.
        if selected == 'campaign':
            campaign(c, background, stock, store)
            None
        elif selected == 'creative':
            creative(c, background, stock, store)
            None
        elif selected == 'options':
            None
        elif selected == "QUIT":
            playing = False
    # parent loop, for the whole game. Keep looping till proper option given
        # call the menu function, an option is what it will return.
        # if option is not quit, do one of the following:
            # run game mode 1: campaign
            # run game mode 2: creative
            # run game mode 3: alpha
            # run credits
            # run options
            
    Credits = load_image(c, 'credits/Credits.png')
#     credits = pygame.transform.smoothscale(credits, (c.DISPLAY_W, c.DISPLAY_H))
    pygame.event.clear()
    Credits = pygame.transform.smoothscale(Credits, (500,500))
    credits_rect = Credits.get_rect()
    credits_rect.center = c.CENTER
    c.DISPLAYSURFACE.blit(Credits, credits_rect)
    c.DISPLAYSURFACE.blit(versionID_SurfaceObj, versionID_RectObj)
    pygame.display.flip()
    for time in range(100):
        sleep(0.1)
        if pygame.event.poll().type != NOEVENT:
            break
            
            
    try:
        logger(c)
        logFile.close()
    except Exception:
        debug(c.DEBUG, "File never opened")

        
    pygame.quit()
    sys.exit()
def debugMain():
    print "HEY THERE WE'RE DOING SPECIAL DEBUGGING"
    import logging
    DATE = datetime.date.timetuple(datetime.date.today())[0] , \
           datetime.date.timetuple(datetime.date.today())[1] , \
           datetime.date.timetuple(datetime.date.today())[2]
    MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
    MAIN_DIR = os.path.split(MAIN_DIR)[0]
    DATA_DIR = os.path.join(MAIN_DIR, 'data')
    saveDir = os.path.join(DATA_DIR, 'logs','crash-log-{0}.txt'.format(DATE))
    logFile = open(saveDir, 'w')
    logFile.close()
    logging.basicConfig(level=logging.DEBUG, filename = saveDir)
    try:
        main(1)
    except Exception as exception:
        logging.exception("Oops: ")
        errorbox('Main Error', repr(exception))
