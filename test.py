from Bird import Bird

bird = Bird("prout")
bird.x = 3
bird.y = 1
bird.vx = 1
bird.vy = 0

other = Bird("22")
other.x = 2
other.y = 2

birds = [bird, other]

print(bird.detect_sep(birds))