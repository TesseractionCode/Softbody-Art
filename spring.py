from pygame import Vector2, draw
from particle import Particle

class Spring:
    
    springs = []
    visible = True
    draw_width = 2
    
    def __init__(self, particle1: Particle, particle2: Particle, stiffness, damping):
        self.particle1 = particle1
        self.particle2 = particle2
        self.stiffness = stiffness
        self.damping = damping
        
        self.rest_length = (particle2.pos - particle1.pos).length()
        
        Spring.springs.append(self)
        
    @staticmethod
    def updateAll(dT):
        for spring in Spring.springs:
            spring.update(dT)
            
    @staticmethod
    def renderAll(screen):
        if Spring.visible:
            for spring in Spring.springs:
                spring.render(screen)
                
    def update(self, dT):
        length = (self.particle2.pos - self.particle1.pos).magnitude()
        damp_force = (self.particle2.vel - self.particle1.vel) * self.damping
        spring_force = self.stiffness * (length - self.rest_length) * (self.particle2.pos - self.particle1.pos).normalize()
        
        total_force = spring_force + damp_force
        
        self.particle1.applyForce(total_force)
        self.particle2.applyForce(-total_force)
    
    def render(self, screen):
        draw.line(screen, (255, 250, 45), self.particle1.pos, self.particle2.pos, self.draw_width)
        
    @staticmethod
    def deleteAll():
        Spring.springs = []
        
    def delete(self):
        Spring.springs.remove(self)