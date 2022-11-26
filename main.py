from game import *
from particle import Particle
from spring import Spring

import pygame
from pygame import Vector2
import math

class MyGame(Game):
    
    # runs when the game first starts
    def onStart(self):
        self.canvas = pygame.Surface(self.res, pygame.SRCALPHA)
        self.draw_color = (180, 180, 180)
        
        self.particle_spacing = 20
        self.stiffness = 10000
        self.damping = 1
        
        self.draw_radius = 5
        self.erase_radius = 20
        self.is_erasing = False
        
        self.physics_strength = 20
        self.physics_mode = False
        
        Particle.draw_radius = 3
        Spring.draw_width = 1
        
        
    # runs when game closes
    def onStop(self):
        pass
    
    # runs every frame (limited by framerate)
    def onTick(self, screen):

        if self.physics_mode:
            pygame.draw.circle(screen, (20,220,20), EventHandler.getMousePos(), self.physics_strength, 1)
        else:
            screen.blit(self.canvas, (0,0))
            if self.is_erasing:
                pygame.draw.circle(screen, (220,20,20), EventHandler.getMousePos(), self.erase_radius, 1)
            else:
                pygame.draw.circle(screen, (20,20,220), EventHandler.getMousePos(), self.draw_radius, 1)
            
        Spring.renderAll(screen)
        Particle.renderAll(screen)
        
    # runs every gameloop iteration (as fast as the computer can handle)
    def onUpdate(self, deltaTime):
        mouse_pos = EventHandler.getMousePos()
        
        # Switch between erasing and not erasing
        if EventHandler.getKeyUp("e"):
            self.is_erasing = not self.is_erasing
        
        # Draw Selections
        if self.physics_mode:
            # Radial force when in physics mode instead of draw
            if EventHandler.getLeftMouse():
                for particle in Particle.particles:
                    squared_dist = Vector2(mouse_pos).distance_squared_to(particle.pos)
                    direction = (particle.pos - Vector2(mouse_pos)).normalize()
                    if squared_dist == 0:
                        continue
                    force = (100000 / squared_dist) * direction
                    
                    particle.applyForce(force)
            if EventHandler.getRightMouse():
                for particle in Particle.particles:
                    squared_dist = Vector2(mouse_pos).distance_squared_to(particle.pos)
                    direction = (particle.pos - Vector2(mouse_pos)).normalize()
                    if squared_dist == 0:
                        continue
                    force = (100000 / squared_dist) * direction
                    
                    particle.applyForce(-force)
        else:
            if EventHandler.getLeftMouse():
                # Draw between last position and new position
                if self.last_draw_pos and (self.last_draw_pos != mouse_pos):
                    if self.is_erasing:
                        pygame.draw.line(self.canvas, (0,0,0,0), self.last_draw_pos, mouse_pos, 2 * self.erase_radius)
                        pygame.draw.circle(self.canvas, (0,0,0,0), self.last_draw_pos, self.erase_radius)
                        pygame.draw.circle(self.canvas, (0,0,0,0), mouse_pos, self.erase_radius)
                    else:
                        pygame.draw.line(self.canvas, self.draw_color, self.last_draw_pos, mouse_pos, 2 * self.draw_radius)
                        pygame.draw.circle(self.canvas, self.draw_color, self.last_draw_pos, self.draw_radius)
                        pygame.draw.circle(self.canvas, self.draw_color, mouse_pos, self.draw_radius)
                    
                self.last_draw_pos = mouse_pos
            else:
                self.last_draw_pos = None
            
        # Increase and decrease erase radius
        if self.physics_mode:
            if EventHandler.getMouseScrollUp():
                self.physics_strength += 3
            elif EventHandler.getMouseScrollDown():
                self.physics_strength -= 3
        else:
            if self.is_erasing:
                if EventHandler.getMouseScrollUp():
                    self.erase_radius += 3
                elif EventHandler.getMouseScrollDown():
                    self.erase_radius -= 3
            else:
                if EventHandler.getMouseScrollUp():
                    self.draw_radius += 3
                elif EventHandler.getMouseScrollDown():
                    self.draw_radius -= 3
        
            
        # Fill selections if press F
        if EventHandler.getKeyUp("f") and not self.physics_mode:
            self.floodFill(self.canvas, mouse_pos, self.draw_color)
            
        # Come up with the points to fill drawn shapes
        if EventHandler.getKeyUp("enter"):
            particle_matrix = self.createSpringLattice(self.particle_spacing, self.stiffness, self.damping)
            
        # Clear canvas if press Backspace
        if EventHandler.getKeyUp("backspace"):
            self.canvas.fill((0,0,0,0))
            
        # Switch to physics mode if press space
        if EventHandler.getKeyUp("space"):
            self.physics_mode = not self.physics_mode
            
        if self.physics_mode: 
            Spring.updateAll(deltaTime)
            Particle.updateAll(deltaTime)
    
    # runs when screen resizes
    def onResize(self, last_resolution):
        pass
    
    
    # Non-recursive flood fill (Not created by me)
    def floodFill(self, surface, position, fill_color):
        fill_color = surface.map_rgb(fill_color)  # Convert the color to mapped integer value.
        surf_array = pygame.surfarray.pixels2d(surface)  # Create an array from the surface.
        
        frontier = [position]
        while len(frontier) > 0:
            x, y = frontier.pop()
            try:  # Add a try-except block in case the position is outside the surface.
                if surf_array[x, y] != 0:
                    continue
            except IndexError:
                continue
            surf_array[x, y] = fill_color
            # Then we append the neighbours of the pixel in the current position to our 'frontier' list.
            frontier.append((x + 1, y))  # Right.
            frontier.append((x - 1, y))  # Left.
            frontier.append((x, y + 1))  # Down.
            frontier.append((x, y - 1))  # Up.

        pygame.surfarray.blit_array(surface, surf_array)
        
    def createSpringLattice(self, particle_spacing, stiffness, damping):           
        # Delete all existing springs and particles
        Spring.deleteAll()
        Particle.deleteAll()
           
        # Find all points in the shapes given
        particle_matrix = [] 
        for y in range(0, self.screen.get_height(), particle_spacing):
            row = []
            for x in range(0, self.screen.get_width(), particle_spacing):
                if self.canvas.get_at((x, y)) == self.draw_color:
                    row.append(Particle(Vector2(x, y)))
                else:
                    row.append(None)
            particle_matrix.append(row)
            
        matrix_width = len(particle_matrix[0])
        matrix_height = len(particle_matrix)
                
        ''' Calculate the spring connections between the points '''
        
        # Create horizontal connections
        for row in particle_matrix:
            for column_i in range(matrix_width - 1):
                particle1 = row[column_i]
                particle2 = row[column_i + 1]
                
                if particle1 and particle2:
                    Spring(particle1, particle2, stiffness, damping)
                    
        # Create vertical connections
        for column_i in range(matrix_width):
            for row_i in range(matrix_height - 1):
                particle1 = particle_matrix[row_i][column_i]
                particle2 = particle_matrix[row_i + 1][column_i]
                
                if particle1 and particle2:
                    Spring(particle1, particle2, stiffness, damping)
                    
        # Create diagonal connections
        for column_i in range(matrix_width - 1):
            for row_i in range(matrix_height - 1):
                particle_topL = particle_matrix[row_i][column_i]
                particle_topR = particle_matrix[row_i][column_i + 1]
                particle_bottomL = particle_matrix[row_i + 1][column_i]
                particle_bottomR = particle_matrix[row_i + 1][column_i + 1]
                
                if particle_topL and particle_bottomR:
                    Spring(particle_topL, particle_bottomR, stiffness, damping)
                    
                if particle_topR and particle_bottomL:
                    Spring(particle_topR, particle_bottomL, stiffness, damping)
                    
        return particle_matrix
    
    
    
    
''' Setup the display for your game. '''

game = MyGame(
    
    window_title = "Stretchiness", 
    icon_dir = None, 
    resolution = (800, 600), 
    background_color = (25, 25, 29), 
    resizable = False
    
    )

game.start()


