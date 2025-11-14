import math

def norme(vector: tuple[int, int]):
    return math.sqrt(vector[0]**2 + vector[1]**2)
    
def normalize(vector: tuple[int, int]):
    norm = norme(vector)
    return (vector[0]/norm, vector[1]/norm)

def add(vec1, vec2):
    return (vec1[0]+vec2[0], vec1[1]+vec2[1])