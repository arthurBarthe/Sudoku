# -*- coding: utf-8 -*-
###############################################
#Application graphique de résolution de sudoku#
#Arthur Guillaumin                            #
###############################################
import pygame, sys
from sudoku import *

class ApplicationSolveur:
    """Classe gérant la partie graphique de résolution."""
    def __init__(self):
        #Initialisation de pygame et de la fenêtre
        pygame.init()
        self.mainSurface = pygame.display.set_mode((800, 700))
        pygame.display.set_caption('Solveur de sudoku - par Arthur Guillaumin.')
        #Couleurs utilisées
        self.colors = {'red': pygame.Color(255, 0, 0),
                       'green': pygame.Color(0, 255, 0),
                       'blue': pygame.Color(0, 0, 255),
                       'white': pygame.Color(255, 255, 255),
                       'black': pygame.Color(0,0,0),
                       }
        #Création d'une font
        self.fontObj = pygame.font.Font('freesansbold.ttf', 32)
        #Création d'un objet sudoku
        self.sudo = Sudoku()
        #Variable contenant la case survolée
        self.over_box = [0,0]
        
        while True:
            self.mainSurface.fill(self.colors['black'])
            self.__draw_grid()
            self.__draw_sudoku()

            #Gestion des évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.__update_over_box(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.__update_selected_box(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__solve()
                    elif event.key > pygame.K_KP0 and event.key <= pygame.K_KP9:
                        self.__update_box_value(event.key-256)
                    elif event.key == pygame.K_SPACE:
                        self.__solve()
                    elif event.key >= pygame.K_UP and event.key <= pygame.K_LEFT:
                        self.__handle_move(event.key)

            #Mise à jour de la fenêtre principale
            pygame.display.update()


    def __update_over_box(self, mouse_pos):
        #On récupère le Rect de la fenêtre principale
        main_surface_rect = self.mainSurface.get_rect()
        width = main_surface_rect.width
        height = main_surface_rect.height
        #...
        x = mouse_pos[0]
        y = mouse_pos[1]
        if x >= width/2-4*50 and x <= width/2+5*50:
            if y >= height/2-4*50 and y <= height/2+5*50:
                self.over_box = ((x-(width/2-4*50))//50, (y-(height/2-4*50))//50)
    
    def __update_selected_box(self, click_pos):
        #On récupère le Rect de la fenêtre principale
        main_surface_rect = self.mainSurface.get_rect()
        width = main_surface_rect.width
        height = main_surface_rect.height
        #...
        x = click_pos[0]
        y = click_pos[1]
        if x >= width/2-4*50 and x <= width/2+5*50:
            if y >= height/2-4*50 and y <= height/2+5*50:
                self.selected_box = ((x-(width/2-4*50))/50, (y-(height/2-4*50))/50)

    def __handle_move(self, key):
        """Méthode qui gère les déplacements par flèches."""
        if key == pygame.K_UP and self.over_box[1] > 0:
            self.over_box = (self.over_box[0], self.over_box[1]-1)
        elif key == pygame.K_DOWN and self.over_box[1] < 8:
            self.over_box = (self.over_box[0], self.over_box[1]+1)
        elif key == pygame.K_LEFT and self.over_box[0] > 0:
            self.over_box = (self.over_box[0]-1, self.over_box[1])
        elif key == pygame.K_RIGHT and self.over_box[0] < 8:
            self.over_box = (self.over_box[0]+1, self.over_box[1])

    def __update_box_value(self, value):
        if self.over_box != None:
            self.sudo.setBoxValue(value, self.over_box[0], self.over_box[1])

    def __solve(self):
        """Méthode privée appelée pour la résolution."""
        solveur = SolveurSudoku()
        solveur.setPossibilitiesUsingGivenSudoku(self.sudo)
        s = solveur.solve()
        if s[0]:
            self.sudo = s[1]

    def __draw_grid(self):
        """Méthode privée qui gère le dessin de la grille du Sudoku."""
        #On récupère le Rect de la fenêtre principale
        main_surface_rect = self.mainSurface.get_rect()
        width = main_surface_rect.width
        height = main_surface_rect.height
        #On dessine à proprement parler les lignes de la grille, une à une
        for i in range(-4,6):
            if (i+4)%3 == 0:
                lineWidth = 3
            else:
                lineWidth = 1
            #ligne horizontale
            pygame.draw.line(self.mainSurface, self.colors['white'], \
                             (width/2-4*50, height/2+i*50), \
                             (width/2+5*50, height/2+i*50),
                             lineWidth)
            #ligne verticale
            pygame.draw.line(self.mainSurface, self.colors['white'], \
                             (width/2+i*50, height/2-4*50), \
                             (width/2+i*50, height/2+5*50),
                             lineWidth)
        #On colorie la case survolée
        if self.over_box != None:
            rect_over_box = pygame.Rect(width/2+(self.over_box[0]-4)*50+1, \
                                        height/2+(self.over_box[1]-4)*50+1, \
                                        49, 49)
            pygame.draw.rect(self.mainSurface, self.colors['red'], \
                             rect_over_box)

    def __draw_sudoku(self):
        #On récupère le Rect de la fenêtre principale
        main_surface_rect = self.mainSurface.get_rect()
        width = main_surface_rect.width
        height = main_surface_rect.height
        #...
        for i in range(9):
            for j in range(9):
                if self.sudo.boxIsDefined(i,j):
                    s = self.fontObj.render(str(self.sudo.getBoxValue(i,j)), \
                                            False,
                                            self.colors['blue'])
                    rect_pos = s.get_rect()
                    rect_pos.topleft = (width/2+25-rect_pos.width/2+(i-4)*50, height/2+25-rect_pos.height/2+(j-4)*50)
                    self.mainSurface.blit(s, rect_pos)

app = ApplicationSolveur()
            
