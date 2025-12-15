class Grille:
    def __init__ (self):
        self.largeur=10
        self.longueur=10
        self.tab=[[None for j in range(10)] for i in range(10)]
        for i in range (len(self.tab)):
            table = ''
            for j in range(len(self.tab[i])):
                table += " " + str(self.tab[i][j])
            print(table)

uu = Grille()


