#!/usr/bin/python3

from grid import *
import socket
import os, sys

def main():
    serv = sys.argv[1]
    print serv
    connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect.connect((serv, 6666))

    player = connect.recv(1024)
    player = player.decode("ascii")
    if player == "J1":
        player = J1
    else :
        player = J2
    
    print "Les deux joueurs sont connectes, le jeu commence."

    playerGrid = grid()
    end = False
    
    while not end:
        whatToDo = connect.recv(1024)
        whatToDo = whatToDo.decode("ascii")
        if whatToDo == "c":
            shot = int(input ("Quelle case voulez-vous jouer ? "))
            shot = str(shot)
            shot = shot.encode("ascii")
            connect.send(shot)

            shot = int(shot)
            answer = connect.recv(1024)
            answer.decode("ascii")
            if answer == "f":
                playerGrid.play(player, shot)
            else :
                if playerGrid.cells[shot] == EMPTY :
                    playerGrid.play(player%2+1, shot)
            
            playerGrid.display()
            
        if whatToDo == "w":
            print "Vous avez gagne !"
            end = True
        if whatToDo == "l":
            print "Vous avez perdu."
            end = True
            

    
    







    connect.close()
main()
