from tkinter import Tk, Canvas
from Bird import Bird

class Loop:
    
    def __init__(self, root, cnv, screen_size, birds):
        self.root = root
        self.cnv = cnv
        self.screen_size = screen_size
        self.birds = birds
    
    def loop(self):
        for b in self.birds:
            b.update_position(self.cnv, self.screen_size, self.birds)
        self.root.after(50, self.loop)


if __name__ == "__main__":
    root=Tk()
    root.title("Bird Simulation")
    cnv=Canvas(root, width=1000, height=750, bg="ivory")
    cnv.pack()
    birds = [Bird(f"bird_{i}") for i in range(50)]
    loop = Loop(root, cnv, (1000, 750), birds)
    root.after(200, loop.loop)
    root.mainloop()
    
    
    