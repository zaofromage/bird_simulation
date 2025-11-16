import random
import math
from utils import normalize, add, norme, distance


class Bird:
    def __init__(self, label):
        # random starting position and angle
        self.x = random.randrange(0, 1000)
        self.y = random.randrange(0, 750)
        # random starting velocity
        self.vx=random.uniform(-1, 5)
        self.vy=random.uniform(-1, 1)
        
        self.size=12
        self.angle = math.atan2(self.vy,self.vx) 
        # label for the bird
        self.label = label
        
        self.collide_radius = 25
        self.vision_radius = 65
        self.coeff_align = 0.2
        self.coeff_sep = 0.8
        self.coeff_coh = 0.3  
        self.coeff_bord = 0.7

        self.max_speed = 5
    def draw_bird(self, canvas):
        
        x1 = self.x + self.size * math.cos(self.angle)
        x2 = self.y + self.size * math.sin(self.angle)
        canvas.create_line(self.x, self.y, x1, x2, fill='black', arrow='last', arrowshape=(12.8,16,4.8), width=2, tags=self.label)
        """
        canvas.create_oval(self.x - self.collide_radius, self.y - self.collide_radius,
                           self.x + self.collide_radius, self.y + self.collide_radius,
                            outline='blue', dash=(2, 4), tags=self.label)
                            
        canvas.create_oval(self.x - self.vision_radius, self.y - self.vision_radius,
                           self.x + self.vision_radius, self.y + self.vision_radius,
                            outline='green', dash=(2, 4), tags=self.label)
        """
    def update_position(self, canvas, screen_size, birds):
        # calculate the vector of separation
        sep_vect = self.detect_sep(birds)
        # canvas.create_line(self.x, self.y, self.x + sep_vect[0], self.y + sep_vect[1], fill='red', width=1)
        coh_vect = self.detect_coh(birds)
        # canvas.create_line(self.x, self.y, self.x + coh_vect[0], self.y + coh_vect[1], fill='green', width=1)
        # if self.label == "oiseau":
        #    print(sep_vect)
        # calculate next the bird moves to
        ali_vect = self.detect_ali(birds)
        bord_vect = self.detect_bor(screen_size)
        self.vx += sep_vect[0] * self.coeff_sep
        self.vy += sep_vect[1] * self.coeff_sep
        self.vx += coh_vect[0] * self.coeff_coh
        self.vy += coh_vect[1] * self.coeff_coh
        self.vx += ali_vect[0] * self.coeff_align
        self.vy += ali_vect[1] * self.coeff_align
        self.vx += bord_vect[0] * self.coeff_bord
        self.vy += bord_vect[1] * self.coeff_bord

        vitesse = norme((self.vx, self.vy))
        if vitesse > self.max_speed:
            direction = normalize((self.vx, self.vy))
            self.vx = direction[0] * self.max_speed
            self.vy = direction[1] * self.max_speed

        self.x += self.vx
        self.y += self.vy
        self.angle = math.atan2(self.vy,self.vx)
        # when bird goes off screen, will come back from other side of screen
        self.x = self.x % screen_size[0]
        self.y = self.y % screen_size[1]
        
        canvas.delete(self.label)
        self.draw_bird(canvas)
        
    """
    Cohesion
    """
    def detect_coh(self, birds) -> tuple[int, int]:
        moy_x = 0
        moy_y = 0
        cpt = 0
        moy_speed = 0
        for b in birds:
            if b.x == self.x and b.y == self.y:
                continue
            dist = distance((self.x, self.y),(b.x, b.y))
            if  self.collide_radius < dist < self.vision_radius:
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
        return normalize((vec_x, vec_y))

    """
    Alignment
    """
    def detect_ali(self, birds) -> tuple[int, int]:
        lst_vx = []
        lst_vy = []
        
        for b in birds:
            if b.x == self.x and b.y == self.y:
                continue
            
            dist = distance((self.x, self.y), (b.x, b.y))
            
            # si un oiseau est entre notre zone de vision et notre zone protégée
            if self.collide_radius < dist < self.vision_radius:
                lst_vx.append(b.vx)
                lst_vy.append(b.vy)
        
        if not lst_vx:
            return (0, 0)
        avg_vx = sum(lst_vx) / len(lst_vx)
        avg_vy = sum(lst_vy) / len(lst_vy)
        
        return normalize((avg_vx, avg_vy))
        
    """
    Separation
    """
    def detect_sep(self, birds) -> tuple[int, int]:
        final_vect = (0, 0)
        for b in birds:
            if b.x == self.x and b.y == self.y:
                continue
            dist = distance((self.x, self.y), (b.x, b.y))
            if dist < self.collide_radius and dist > 0:
                final_vect = add(final_vect, (self.x - b.x, self.y - b.y))
        return normalize(final_vect) if final_vect != (0, 0) else final_vect

    """
    Border
    """
    def detect_bor(self, screen_size: tuple([int, int])) -> tuple[int, int]:
        final_vect = (0, 0)

        val_x1 = self.x + self.vision_radius
        val_x2 = self.x - self.vision_radius
        val_y1 = self.y + self.vision_radius
        val_y2 = self.y - self.vision_radius

        if val_x1 > screen_size[0] - 25:
            return normalize((-1, 0))
        if val_x2 < 25:
            return normalize((1,0))
        if val_y1 > screen_size[1] - 50:
            return normalize((0,-1))
        if val_y2 < 25:
            return normalize((0,1))
        return (0,0)