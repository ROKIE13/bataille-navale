class bateau:
    def __init__(self, x, y, orientation, taille):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.taille = taille
        self.touche = 0
        self.taille_grille = taille_grille

    def position(self):
        pos = []
        for i in range(self.taille):
            if self.orientation == H:
                x = self.x
                y = self.y + 1
            else:
                x = self.x + 1
                y = self.y
            if x < 0 or y < 0 or x >= self.taille_grille or y >= self.taille_grille:
                print ("Placement impossible : le bateau dépasse la grille")
            pos.append((x, y))
        return pos 

    def est_touche(self, x, y):
        if (x, y) in self.position():
            self.touches += 1
            return True 
        return False
    
    def est_coule(self):
        return self.touches >= self.taille
