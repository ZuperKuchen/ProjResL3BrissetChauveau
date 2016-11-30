#!/usr/bin/python3

from grid import *
import  random
import  socket


def main():
    
    #On ouvre la connexion et on attend que les deux joueurs se connectent
    
    connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect.bind(('', 6666))
    connect.listen(5)
    
    J1connect, J1infos = connect.accept()
    print (J1infos, "J1 vient de se connecter.")
    J2connect, J2infos = connect.accept()
    print (J2infos, "J2 vient de se connecter.")

    globalMessage = "Les deux joueurs sont connectes, le jeu commence."
    globalMessage = globalMessage.encode("ascii")
    J1connect.send(globalMessage)
    J2connect.send(globalMessage)

    #Le jeu commence

    caseMessage = "c"
    caseMessage = caseMessage.encode("ascii")
    winMessage = "w"
    winMessage = winMessage.encode("ascii")
    loseMessage = "l"
    loseMessage = loseMessage.encode("ascii")

    grids = [grid(), grid(), grid()]
    current_player = J1
    grids[0].display()
    
    while grids[0].gameOver() == -1:
        if current_player == J1:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                J1connect.send(caseMessage)
                shot = J1connect.recv(1024)
                shot = shot.decode("ascii")
                shot = int(shot)
        else:
            shot = -1
            while shot <0 or shot >=NB_CELLS:
                J2connect.send(caseMessage)
                shot = J2connect.recv(1024)
                shot = shot.decode("ascii")
                shot = int(shot)
        if (grids[0].cells[shot] != EMPTY):
            grids[current_player].cells[shot] = grids[0].cells[shot]
        else:
            grids[current_player].cells[shot] = current_player
            grids[0].play(current_player, shot)
            current_player = current_player%2+1
        
        grids[0].display()
        
    print("Le jeu est fini")
    
    if grids[0].gameOver() == J1:
        J1connect.send(winMessage)
        J2connect.send(loseMessage)
    else:
        J1connect.send(winMessage)
        J2connect.send(loseMessage)





    connect.close()
main()
