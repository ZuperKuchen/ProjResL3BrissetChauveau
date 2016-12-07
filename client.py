#!/usr/bin/python3

from grid import *
import socket
import os, sys

def recep_info(grid, connect):
    for i in range 9:
        recept = connect.recv(1024)
        if recept == 1:
            grid.cells[i] = 1
        elif recept == 2:
            grid.cells[i] = 2
        else:
            grid.cells[i] = EMPTY

    

def main():
    serv = sys.argv[1]
    print(serv)
    connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect.connect((serv, 6666))

    player = connect.recv(1024)
    player = player.decode("ascii")
    print(player)
    if player == "1":
        player = 1
    else :
        player = 2
    
    print("Les deux joueurs sont connectes, le jeu commence.")

    playerGrid = grid()
    end = False
    
    while not end:
        whatToDo = connect.recv(1024)
        whatToDo = whatToDo.decode("ascii")
        print(whatToDo)
        if whatToDo == "c":
            shot = int(input ("Quelle case voulez-vous jouer ? "))
            shot = str(shot)
            shot = shot.encode("ascii")
            connect.send(shot)

            shot = int(shot)
            answer = connect.recv(1024)
            answer.decode("ascii")
            print(answer)
            if answer == b'f':
                playerGrid.play(player, shot)
            else :
                if playerGrid.cells[shot] == EMPTY :
                    if player == 1:
                        playerGrid.play(2, shot)
                    else:
                        playerGrid.play(1, shot)
            
            playerGrid.display()
            
        if whatToDo == "w":
            print("Vous avez gagne !")
            end = True
        if whatToDo == "l":
            print("Vous avez perdu.")
            end = True
            

    
    







    connect.close()
main()
