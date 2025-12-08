class bateau:
    def __init__(self, x, y, orientation, taille):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.taille = taille
        self.touche = 0

    def position(self):
        pos = []
        for i in range(self.taille):
            if self.orientation == H:
                pos.append(self.x, self.y + 1)
            else:
                pos.append(self.x + 1, self.y)
        return pos 

    def est_touche(self, x, y):
        if
    
