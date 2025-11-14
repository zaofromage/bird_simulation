import random
import math
from utils import normalize, add, norme


class Bird:
    def __init__(self, label):
        # random starting position and angle
        self.x = random.randrange(0, 1000)
        self.y = random.randrange(0, 750)
        # random starting velocity
        self.vx=random.uniform(-1, 1)
        self.vy=random.uniform(-1, 1)
        
        self.size=12
        self.angle = math.atan2(self.vy,self.vx) 
        # label for the bird
        self.label = label
        
        self.collide_radius = 50
        self.vision_radius = 100
        self.coeff_align = 0.1
        self.coeff_sep = 0.1
        max_speed = 5


    def draw_bird(self, canvas):
        
        x1 = self.x + self.size * math.cos(self.angle)
        x2 = self.y + self.size * math.sin(self.angle)
        canvas.create_line(self.x, self.y, x1, x2, fill='black', arrow='last', arrowshape=(12.8,16,4.8), width=2, tags=self.label)
        canvas.create_oval(self.x - self.collide_radius, self.y - self.collide_radius,
                           self.x + self.collide_radius, self.y + self.collide_radius,
                            outline='blue', dash=(2, 4), tags=self.label)
        canvas.create_oval(self.x - self.vision_radius, self.y - self.vision_radius,
                           self.x + self.vision_radius, self.y + self.vision_radius,
                            outline='green', dash=(2, 4), tags=self.label)

    def update_position(self, canvas, screen_size, birds):
        # calculate the vector of separation
        sep_vect = self.detect_sep(birds)
        # canvas.create_line(self.x, self.y, self.x + sep_vect[0], self.y + sep_vect[1], fill='red', width=1)
        coh_vect = self.detect_coh(birds)
        # canvas.create_line(self.x, self.y, self.x + coh_vect[0], self.y + coh_vect[1], fill='green', width=1)
        # if self.label == "oiseau":
        #    print(sep_vect)
        # calculate next the bird moves to
        self.vx += sep_vect[0] * self.coeff_sep
        self.vy += sep_vect[1] * self.coeff_sep
        self.vx += coh_vect[0] * self.coeff_align
        self.vy += coh_vect[1] * self.coeff_align
        self.x += self.vx
        self.y += self.vy
        self.angle = math.atan2(self.vy,self.vx)
        # when bird goes off screen, will come back from other side of screen
        self.x = self.x % screen_size[0]
        self.y = self.y % screen_size[1]
        
        canvas.delete(self.label)
        self.draw_bird(canvas)
        
    def detect_coh(self, birds) -> tuple[int, int]:
        moy_x = 0
        moy_y = 0
        cpt = 0
        moy_speed = 0
        for b in birds:
            if b.x == self.x and b.y == self.y:
                continue
            dist = math.sqrt((self.x - b.x)**2 + (self.y - b.y)**2)
            if dist < self.vision_radius and dist > self.collide_radius:
                cpt += 1
                moy_x += b.x
                moy_y += b.y
                moy_speed += norme((b.vx, b.vy))
        moy_x /= max(cpt, 1)
        moy_y /= max(cpt, 1)
        moy_speed /= max(cpt, 1)
        if cpt == 0:
            return (0, 0)
        vec_x = moy_x - self.x
        vec_y = moy_y - self.y
        # armoniser
        
        return normalize((vec_x, vec_y))
    
    def detect_sep(self, birds) -> tuple[int, int]:
        final_vect = (0, 0)
        for b in birds:
            if b.x == self.x and b.y == self.y:
                continue
            dist = math.sqrt((self.x - b.x)**2 + (self.y - b.y)**2)
            if dist < self.collide_radius and dist > 0:
                final_vect = add(final_vect, (self.x - b.x, self.y - b.y))
        return normalize(final_vect) if final_vect != (0, 0) else final_vect
        

