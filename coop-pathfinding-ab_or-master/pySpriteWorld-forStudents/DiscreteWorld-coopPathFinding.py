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
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer1'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 20  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
    
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
                        
                while a[3]:   
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
    
def collisionOp(init,goal,wallStates, i,coup,boolean,j,adv,chemin):
  wS= wallStates.copy()
  if boolean:
    print("Collision réelle")
    wS.append(coup)
    
  #if j<adv:  
  ast=astar(init,goal,wS)
  res=[]
  print(i)
  for j in range(i):
    res.append((0,0))
  for k in ast:
    res.append(k)
#  else:
#    res=[]
#    for l in range(len(chemin)):
#      if l==i-1:
#        res.append(chemin[l])
#        res.append(chemin[l])
#      else:
#        res.append(chemin[l])
  print("new",res)
  return res
    
  
  
def main():

    #for arg in sys.argv:
    iterations = 50 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    
    
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
    # Placement aleatoire des fioles 
    #-------------------------------
    
    
    # on donne a chaque joueur une fiole a ramasser
    # en essayant de faire correspondre les couleurs pour que ce soit plus simple à suivre
    
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
        
    # bon ici on fait juste plusieurs random walker pour exemple...
    while(True):
      posPlayers = initStates
      listeAstar = []
      listecollision=[]
      estarrive=[]
      print("reset")
      wallS = wallStates.copy()
      for i in range(nbPlayers):
        listeAstar.append(astar([players[i].get_rowcol()],[goalStates[i]],wallS))
        listecollision.append(False)
        estarrive.append(False)
      #maxLen = longueur du plus long parcours
      #iteration sur maxlen avec un while (ne pas oublier d'iterer i)
      
      for i in range(iterations):
          print(len(wallS))
          for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
              if i >= len(listeAstar[j]): # ce if sert a gerer le cas ou un ou deux
                #personne ont trouvé leur fiole pour permettre d'attendre que tout le monde 
                #ai la sienne
                continue
                
              
              next_row,next_col=listeAstar[j][i]
              #collision
              if (next_row, next_col) in posPlayers:
                if (next_row, next_col)==posPlayers[j]:
                  print("Début de la recherche joueur ",j)
                else:
                  listecollision[j]=True
                  for k in range(len(posPlayers)):
                    if posPlayers[k]==(next_row, next_col):
                      print('Collsion entre ',j, 'et', k)
                      adv=k
                  print("old",listeAstar[j])
                  listeAstar[j]=collisionOp([posPlayers[j]],[goalStates[j]],wallS,i,(next_row,next_col),True,j,adv,listeAstar[j])
              #else:
               # if listecollision[j]==True:
               #   listeAstar[j]=collision([players[j].get_rowcol()],[goalStates[j]],wallStates,i,(next_row,next_col),False)
                #  listecollision[j]==False
              next_row,next_col=listeAstar[j][i]
              players[j].set_rowcol(next_row,next_col)
              print ("pos :", j, next_row,next_col)
              game.mainiteration()
  
              col=next_col
              row=next_row
              posPlayers[j]=(row,col)
              
        
          
              
              # si on a  trouvé un objet on le ramasse
              if (row,col) in goalStates:
                  o = players[j].ramasse(game.layers)
                  game.mainiteration()
                  print ("Objet trouvé par le joueur ", j)
                  goalStates.remove((row,col)) # on enlève ce goalState de la liste
                  score[j]+=1
                  
          
                  # et on remet un même objet à un autre endroit
                  x = random.randint(1,5)
                  y = random.randint(1,5)
                  while (x,y) in wallStates or (x,y) in goalStates or (x,y) in posPlayers:
                      x = random.randint(1,5)
                      y = random.randint(1,5)
                  o.set_rowcol(x,y)
                  goalStates.append((x,y)) # on ajoute ce nouveau goalState
                  game.layers['ramassable'].add(o)
                  game.mainiteration()                
                  
            
    
    print ("scores:", score)
    pygame.quit()
    
        
    
   

if __name__ == '__main__':
    main()
    



  
  
  