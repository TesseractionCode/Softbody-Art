from game.pygame_events import EventHandler
import pygame
import time

# Saving data to hard drive source (AKA shelve module): http://inventwithpython.com/blog/2012/05/03/implement-a-save-game-feature-in-python-with-the-shelve-module/

class Game:
    
    def __init__(self, window_title, icon_dir, resolution, framerate=None, background_color=(0,0,0), resizable=True):
        self.window_title = window_title
        self.icon_dir = icon_dir
        self.res = resolution
        self.framerate = framerate
        self.background_color = background_color
        self.resizable = resizable
        
        self.frame_count = 0 # how many frames have passed
        self.loop_count = 0 # how many game loops have passed
        self.deltaTime = 0.01 # start with an approximation of deltaTime
        
        pygame.init() # initialize pygame for text and stuff
        
        # setup window
        if resizable:
            self.screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption(window_title)
        
        if icon_dir:
            icon = pygame.image.load(icon_dir)
            pygame.display.set_icon(icon)
        
        self.running = False # whether the game is running or not
       
    # start game 
    def start(self):
        self.start_time = time.time() # mark the start of the game
        self.last_res = self.res
        self.running = True
        self.onStart()
        self.loop()
        
    # stop game
    def stop(self):
        self.running = False
        self.onStop()
        
    def handleEvents(self):
        if self.resizable:
            self.res = self.screen.get_size()
            
            if self.res != self.last_res:
                self.onResize(self.last_res)
                
            self.last_res = self.res
        EventHandler.handleEvents() # update player input to game
        
    # handle game loop
    def loop(self):
        last_frame = time.time() # time of the last frame
        while self.running:
            loop_start = time.time()
            
            if EventHandler.isQuit():
                self.stop()
                
            self.handleEvents() # handle user input as well as screen resizing           
            self.onUpdate(self.deltaTime)
            if (self.framerate == None) or (time.time() - last_frame >= 1/self.framerate):
                # time since last onTick() call is >= the framerate
                self.onTick(self.screen)
                self.refreshScreen()
                self.frame_count += 1
                last_frame = time.time()
            
            self.loop_count += 1
            self.deltaTime = time.time() - loop_start # time since beginning of frame
            
    def refreshScreen(self):
        pygame.display.update()
        self.screen.fill(self.background_color)
        
    def onStart(self):
        """ runs when the game first starts"""
        pass
    
    def onStop(self):
        """ runs when game closes"""
        pass
    
    def onTick(self, screen):
        """ runs every frame (limited by framerate)"""
        pass
        
    def onUpdate(self, deltaTime):
        """ runs every gameloop iteration (as fast as the computer can handle)"""
        pass
    
    def onResize(self, last_resolution):
        """ runs when screen resizes"""
        pass