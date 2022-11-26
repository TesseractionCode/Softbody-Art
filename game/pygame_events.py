import pygame
import time

class EventHandler:
    
    key_dict = {"a": pygame.K_a, "b": pygame.K_b, "c": pygame.K_c, "d": pygame.K_d, "e": pygame.K_e, "f": pygame.K_f, "g": pygame.K_g, "h": pygame.K_h, "i": pygame.K_i, 
                "j": pygame.K_j, "k": pygame.K_k, "l": pygame.K_l, "m": pygame.K_m, "n": pygame.K_n, "o": pygame.K_o, "p": pygame.K_p, "q": pygame.K_q, "r": pygame.K_r, 
                "s": pygame.K_s, "t": pygame.K_t, "u": pygame.K_u, "v": pygame.K_v, "w": pygame.K_w, "x": pygame.K_x, "y": pygame.K_y, "z": pygame.K_z, 
                
                "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN, "delete": pygame.K_DELETE, "backspace": pygame.K_BACKSPACE,
                "tab": pygame.K_TAB, "esc": pygame.K_ESCAPE, "leftshift": pygame.K_LSHIFT, "rightshift": pygame.K_RSHIFT, "enter": pygame.K_RETURN, "space": pygame.K_SPACE,
                
                "0": pygame.K_0, "1": pygame.K_1, "2": pygame.K_2, "3": pygame.K_3, "4": pygame.K_4,
                "5": pygame.K_5, "6": pygame.K_6, "7": pygame.K_7, "8": pygame.K_8, "9": pygame.K_9,
                
                "f1": pygame.K_F1, "f2": pygame.K_F2, "f3": pygame.K_F3, "f4": pygame.K_F4, "f5": pygame.K_F5,
                "f6": pygame.K_F6, "f7": pygame.K_F7, "f8": pygame.K_F8, "f9": pygame.K_F9, "f10": pygame.K_F10,
                "f11": pygame.K_F11, "f12": pygame.K_F12, "f13": pygame.K_F13, "f14": pygame.K_F14, "f15": pygame.K_F15}
    
    key_input = []
    mouse_input = [(0, 0), (False, False, False), [False, False]]
    
    is_quit = False # whether the user has pressed the red x
    key_down = False # whether a key was pushed down
    key_up = False # whether a key was released
    mouse_down = False # whether a mouse button was pushed down
    mouse_up = False # whether a mouse button was released
    
    # Process events at the time of its calling
    @staticmethod
    def handleEvents():
        # process which keys are pressed
        EventHandler.registerKeys()
        EventHandler.registerMouse()
        
        # process events
        has_keydown = False
        has_keyup = False
        has_mousedown = False
        has_mouseup = False
        events = pygame.event.get()
        for event in events:
            
            if event.type == pygame.QUIT:
                EventHandler.is_quit = True
            
            if event.type == pygame.KEYDOWN:
                EventHandler.key_down = True
                has_keydown = True
                
            if event.type == pygame.KEYUP:
                EventHandler.key_up = True
                has_keyup = True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                EventHandler.mouse_down = True
                has_mousedown = True
                
                if event.button == 4:
                    # mouse scroll up
                    EventHandler.mouse_input[2][1] = True
                if event.button == 5:
                    # mouse scroll down
                    EventHandler.mouse_input[2][0] = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                EventHandler.mouse_up = True
                has_mouseup = True
                
            
        if not has_keydown:
            EventHandler.key_down = False
        if not has_keyup:
            EventHandler.key_up = False
        if not has_mousedown:
            EventHandler.mouse_down = False
        if not has_mouseup:
            EventHandler.mouse_up = False
            
    @staticmethod
    def registerKeys():
        """ Discover which keys are down."""
        EventHandler.key_input = pygame.key.get_pressed()
        
    @staticmethod
    def registerMouse():
        """ Discover mouse pos and pressed buttons."""
        EventHandler.mouse_input = [pygame.mouse.get_pos(), pygame.mouse.get_pressed(), [False, False]]
        
    @staticmethod
    def getMouseScrollDown():
        """ Return 0 or 1 depending on whether mouse wheel has meen scrolled down."""
        if EventHandler.mouse_input[2][0]:
            return 1
        return 0
    
    @staticmethod
    def getMouseScrollUp():
        """ Return 0 or 1 depending on whether mouse wheel has meen scrolled up."""
        if EventHandler.mouse_input[2][1]:
            return 1
        return 0
        
    @staticmethod
    def getMousePos():
        """ Get the position of the mouse relative to window in a tuple."""
        return EventHandler.mouse_input[0]
        
    @staticmethod
    def getLeftMouse():
        """ Return 0 or 1 depending on whether left mouse button is down."""
        return EventHandler.mouse_input[1][0]
    
    @staticmethod
    def getMiddleMouse():
        """ Return 0 or 1 depending on whether middle mouse button is down."""
        return EventHandler.mouse_input[1][1]
    
    @staticmethod
    def getRightMouse():
        """ Return 0 or 1 depending on whether right mouse button is down."""
        return EventHandler.mouse_input[1][2]
    
    @staticmethod
    def getLeftMouseDown():
        """ Return 0 or 1 depending on whether left mouse button was pressed."""
        EventHandler.registerMouse()
        if EventHandler.mouse_down:
            return EventHandler.getLeftMouse()
        return 0
    
    @staticmethod
    def getMiddleMouseDown():
        """ Return 0 or 1 depending on whether middle mouse button was pressed."""
        EventHandler.registerMouse()
        if EventHandler.mouse_down:
            return EventHandler.getMiddleMouse()
        return 0
    
    @staticmethod
    def getRightMouseDown():
        """ Return 0 or 1 depending on whether right mouse button was pressed."""
        EventHandler.registerMouse()
        if EventHandler.mouse_down:
            return EventHandler.getRightMouse()
        return 0
    
    @staticmethod
    def getLeftMouseUp():
        """ Return 0 or 1 depending on whether left mouse button was released."""
        if EventHandler.mouse_up:
            return EventHandler.getLeftMouse()
        return 0
    
    @staticmethod
    def getMiddleMouseUp():
        """ Return 0 or 1 depending on whether middle mouse button was released."""
        if EventHandler.mouse_up:
            return EventHandler.getMiddleMouse()
        return 0
    
    @staticmethod
    def getRightMouseUp():
        """ Return 0 or 1 depending on whether right mouse button was released."""
        if EventHandler.mouse_up:
            return EventHandler.getRightMouse()
        return 0
        
    @staticmethod
    def getKey(key: str):
        """ Return 0 or 1 depending on whether specified key is down. """
        key_index = EventHandler.key_dict[key]
        return EventHandler.key_input[key_index]
    
    @staticmethod
    def getKeyDown(key: str):
        """ Return 0 or 1 depending on whether specified key was pressed. """
        EventHandler.registerKeys()
        if EventHandler.key_down:
            return EventHandler.getKey(key)
        return 0
    
    @staticmethod
    def getKeyUp(key: str):
        """ Return 0 or 1 depending on whether specified key was released. """
        if EventHandler.key_up:
            return EventHandler.getKey(key)
        return 0
    
    @staticmethod
    def isQuit():
        """ Returns whether the user has decided to quit. """
        return EventHandler.is_quit