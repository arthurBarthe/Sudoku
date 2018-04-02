# -*- coding: utf-8 -*-
"""Solveur de Sudoku par Arthur Guillaumin.
Créé le 08/08/2014.
"""

import copy

class Sudoku:
    """Classe représentant un sudoku et ses 81 cases."""
    def __init__(self):
        """Constructeur."""
        #Tableau contenant les valeurs entre 1 et 9.
        #Un 0 correspond à une valeur inconnue.
        self.values = [[0]*9 for _ in range(9)]

    def setBoxValue(self, value, i, j):
        """Définit la valeur à la ligne i et la colonne j.
        **params:
        v           int - Nouvelle valeur de la case
        i           int - Ligne de la case à définir
        j           int - Colonne de la case à définir

        **Returns:
        r           bool - True si une ancienne valeur a été écrasée.
        """
        if value > 9 or value <= 0 or type(value) is not int:
            raise ValueError("La valeur de la case doit être un entier entre 1 et 9.")
        else:
            r = self.values[i][j] != 0
            self.values[i][j] = value

    def getBoxValue(self, i, j):
        return self.values[i][j]

    def boxIsDefined(self, i, j):
        return self.values[i][j] != 0

    def getSquare9(i, j):
        """Renvoie les cases du carré de taille 9 dans lequel se trouve la case (i,j)."""
        topI = i/3 *3
        topJ = j/3 * 3
        return [(a,b) for a in range(topI, topI+3) for b in range(topJ, topJ+3)]

    getSquare9 = staticmethod(getSquare9)

class SolveurSudoku:
    """Classe permettant la résolution d'un sudoku."""
    def __init__(self, possibilities = None):
        """Constructeur.
        **params:
        sudoku      Sudoku - Le sudoku à résoudre
        """
        #Ensemble des possibilités.
        if possibilities is None:
            self.possibilities = [[[k for k in range(1,10)] for i in range(9)] for j in range(9)]
        else:
            self.possibilities = copy.deepcopy(possibilities)

    def makeHypothesis(self, i, j, value):
        self.possibilities[i][j] = [value,]

    def setPossibilitiesUsingGivenSudoku(self, sudoku):
        for i in range(9):
            for j in range(9):
                if sudoku.boxIsDefined(i,j):
                    self.possibilities[i][j] = [sudoku.getBoxValue(i,j),]

    def get_sudo(self):
        sudo = Sudoku()
        for i in range(9):
            for j in range(9):
                sudo.setBoxValue(self.possibilities[i][j][0], i, j)
        return sudo

    def solve(self):
        solved = False
        changed = True
        while changed is True:
            #On élimine les possibilités non cohérentes
            changed = False
            solved = True
            for i in range(9):
                for j in range(9):
                    if len(self.possibilities[i][j]) > 1:
                        solved = False
                    else:
                        valueIJ = self.possibilities[i][j][0]
                        #Traitement de la ligne
                        for l in range(9):
                            if l != j and valueIJ in self.possibilities[i][l]:
                                self.possibilities[i][l].remove(valueIJ)
                                if len(self.possibilities[i][l]) == 1:
                                    changed = True
                                elif len(self.possibilities[i][l]) < 1:
                                    return (False, [])
                        #Traitement de la colonne
                        for k in range(9):
                            if k != i and valueIJ in self.possibilities[k][j]:
                                self.possibilities[k][j].remove(valueIJ)
                                if len(self.possibilities[k][j]) == 1:
                                    changed = True
                                elif len(self.possibilities[k][j]) < 1:
                                    return (False, [])
                        #Traitement du carré de taille 9
                        for (k,l) in Sudoku.getSquare9(i,j):
                            if (k,l) != (i,j) and valueIJ in self.possibilities[k][l]:
                                self.possibilities[k][l].remove(valueIJ)
                                if len(self.possibilities[k][l]) == 1:
                                    changed = True
                                elif len(self.possibilities[k][l]) < 1:
                                    return (False, [])
            if solved == True:
                return (True, self.get_sudo())
        #Si on est bloqué il faut faire une hypothèse
        for i in range(9):
            for j in range(9):
                if len(self.possibilities[i][j]) > 1:
                    for k in range(len(self.possibilities[i][j])):
                        solveur = SolveurSudoku(self.possibilities)
                        solveur.makeHypothesis(i, j, self.possibilities[i][j][k])
                        (solved, solution) = solveur.solve()
                        if solved == True:
                            return (True, solution)
                    return (False, [])
                        
                        
    
