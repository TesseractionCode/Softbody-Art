from pygame import draw, Vector2

class Particle:
    
    particles = []
    visible = True
    draw_radius = 4
    
    def __init__(self, pos: Vector2):
        self.pos = pos
        self.vel = Vector2(0,0)
        self.forces = Vector2(0,0)
        
        Particle.particles.append(self)
        
    @staticmethod
    def updateAll(dT):
        for particle in Particle.particles:
            particle.update(dT)
            
    @staticmethod
    def renderAll(screen):
        if Particle.visible:
            for particle in Particle.particles:
                particle.render(screen)
            
    def update(self, dT):
        self.vel += self.forces * dT
        self.pos += self.vel * dT
        
        self.forces *= 0
    
    def render(self, screen):
        draw.circle(screen, (255, 0, 0), self.pos, self.draw_radius)
        
    def applyForce(self, force: Vector2):
        self.forces += force
        
    @staticmethod
    def deleteAll():
        Particle.particles = []
        
    def delete(self):
        Particle.particles.remove(self)