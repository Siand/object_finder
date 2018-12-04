
# mult = 0.9
# .87 .75  .75  .75  .75
# .78 .675 .675 .675 .675  
# .7  .608 .608 .608 .608 
# .63 .547 .547 .547 .547 
#



class PosFromGrid(object):
    def __init__(self):
        self.lengths = [0.315,0.98,1.72,2.55]
        self.widths = [0.75,0.68,0.61,0.58]
    def get_rel_pos(self,cell):
        r = int(cell / 4)
        c = (cell % 4)
        xSize = self.widths[r]
        xPos = 0
        if c == 0:     
            xPos = -1.5 * xSize
        elif c == 1:     
            xPos = -0.5 * xSize
        elif c == 2:     
            xPos = 0.5 * xSize
        elif c == 3:     
            xPos = 1.5 * xSize
        return xPos, self.lengths[3-r]
