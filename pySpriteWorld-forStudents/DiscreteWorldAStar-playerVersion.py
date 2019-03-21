# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo

import random 
import numpy as np
import sys


# ---- ---- ---- ---- ---- ----
# ---- Misc                ----
# ---- ---- ---- ---- ---- ----




# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'pathfindingWorld3'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def astar(initState, goalState, wallStates):
    
    positionDepart = { "pos" : initState[0], "score": 0}
    
    coupexplore = [[positionDepart.get("pos"), 0, abs(initState[0][0] - goalState[0][0]) + abs(initState[0][1] - goalState[0][1]), None]]
    reserve = []
    while(True):
        for i in [(0,1),(0,-1),(1,0),(-1,0)]: #on prend les nouveau coup      
            newlig = positionDepart.get("pos")[0]+i[0]
            newcol = positionDepart.get("pos")[1]+i[1]
            newPos = (newlig,newcol)
            if (newPos not in wallStates) and (newPos not in [coupexplore[i][0] for i in range(len(coupexplore))]) and newlig>=0 and newlig<20 and newcol>=0 and newcol<20 : 
#tout ce if permet de faire ce que notre couppossible d'avant
              
              
              #si on arrive a la pose final
              if newPos in goalState:
                listeCoups = []
                listeCoups.append(newPos)   #on fait une nouvelle liste avec les nouveau coup qui respectent les critere
                
                
                for c in coupexplore:#{
                    if c[0] == positionDepart.get("pos"):
                        a = c
                        break #}
                #
                        
                while a[3]!= None:   #a[3] c'est les peres  
                  #{
                    listeCoups.append(a[0])
                    newPos = a[3] 
                    
                    for c in coupexplore:
                        if c[0] == newPos:
                            a = c
                            break 
                  #}
                  
                  
                  
                #return de la fonction est la 
                listeCoups.append(initState[0])
                ltmp = []
                for k in range(len(listeCoups),0,-1):
                    ltmp.append(listeCoups[k-1])
                return ltmp
              if not (newlig,newcol) in reserve:#{
                    score = positionDepart.get("score") + abs(newlig - goalState[0][0]) + abs(newcol - goalState[0][1])
                    tmp = [newPos,positionDepart.get("score")+1,score,positionDepart.get("pos")]
                    coupexplore.append(tmp)
                    reserve.append(tmp)
                    #}
            
            
                    
        #boucle dans la reserve et prise de choix
        minR = 100000000
        choix = None
        for i in reserve:
            if i[2] < minR:
                minR = i[2]
                positionDepart = { "pos" : i[0], "score" : i[1] }
                choix = i
        reserve.remove(choix)
        #on oublie pas d'enlever le choix pour pas faire plusieurs fois le meme choix
    
    
    
    
      
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Building the matrix
    #-------------------------------
       
           
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
        
    
    #-------------------------------
    # Building the best path with A*
    #-------------------------------    
        
    #-------------------------------
    # Moving along the path
    #-------------------------------
        
    # bon ici on fait juste un random walker pour exemple...
    

    row,col = initStates[0]
    #row2,col2 = (5,5)

    path = astar(initStates, goalStates, wallStates)
    for i in range(len(path)):
      
        next_row,next_col = path[i]       
        player.set_rowcol(next_row,next_col)
        print ("pos 1:",next_row,next_col)
        game.mainiteration()

        # si on a  trouvé l'objet on le ramasse
        if (row,col)==goalStates[0]:
            o = game.player.ramasse(game.layers)
            game.mainiteration()
            print ("Objet trouvé!", o)
            break
        '''
        #x,y = game.player.get_pos()
    
        '''

    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    


