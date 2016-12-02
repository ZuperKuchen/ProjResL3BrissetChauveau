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

    J1 = "1"
    J2 = "2"
    J1 = J1.encode("ascii")
    J2 = J2.encode("ascii")
    J1connect.send(J1)
    J2connect.send(J2)

    #Le jeu commence

    caseMessage = "c"
    caseMessage = caseMessage.encode("ascii")
    
    winMessage = "w"
    winMessage = winMessage.encode("ascii")
    loseMessage = "l"
    loseMessage = loseMessage.encode("ascii")
    
    freeMessage = "f"
    freeMessage = freeMessage.encode("ascii")
    usedMessage = "u"
    usedMessage = usedMessage.encode("ascii")

    gridG = grid()
    current_player = J1
    gridG.display()
    
    while gridG.gameOver() == -1:
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
        if (gridG.cells[shot] != EMPTY):
            if current_player == J1:
                J1connect.send(usedMessage)
            else :
                J2connect.send(usedMessage)
        else:
            if current_player == J1:
                J1connect.send(freeMessage)
                gridG.play(1, shot)
                current_player = J2
            else:
                J2connect.send(freeMessage)
                gridG.play(2, shot)
                current_player = J1
        gridG.display()
        
    print("Le jeu est fini")
    
    if gridG.gameOver() == J1:
        J1connect.send(winMessage)
        J2connect.send(loseMessage)
    else:
        J1connect.send(winMessage)
        J2connect.send(loseMessage)





    connect.close()
main()
