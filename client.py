#!/usr/bin/python3

from grid import *
import socket
import os, sys

def recep_info(grid, connect):
    ok = "k"
    ok = ok.encode("ascii")
    for i in range(9):
        recept = connect.recv(1024)
        recept = recept.decode("ascii")
        if recept == "1" and grid.cells[i] == EMPTY:
            grid.play(1, i)
        elif recept == "2" and grid.cells[i] == EMPTY:
            grid.play(2, i)
        connect.send(ok)
        

    

def main():
    #On se connecte au serveur
    #
    serv = sys.argv[1]
    print("En attente d'une réponse du serveur...")
    connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect.connect((serv, 6666))

    #On attend de recevoir le statut du client (J1, J2, spec)
    #
    player = connect.recv(1024)
    player = player.decode("ascii")

    if player == "1":
        player = 1
        print("Vous êtes joueur 1.")
    elif player == "2":
        player = 2
        print("Vous êtes joueur 2.")
    else :
        print("Vous êtes spectateur.")
        

    
    #Initialisation
    #
    playerGrid = grid()
    end = False
    
    while not end:
        #On attend l'instruction du serveur
        #
        whatToDo = connect.recv(1024)
        whatToDo = whatToDo.decode("ascii")

        #Le server demande la case à jouer (joueur)
        #
        if whatToDo == "c":
            shot = int(input ("Quelle case voulez-vous jouer ? "))
            shot = str(shot)
            shot = shot.encode("ascii")
            connect.send(shot)

            shot = int(shot)
            answer = connect.recv(1024)
            answer = answer.decode("ascii")
            if answer == "f":
                playerGrid.play(player, shot)
            else :
                if playerGrid.cells[shot] == EMPTY :
                    if player == 1:
                        playerGrid.play(2, shot)
                    else:
                        playerGrid.play(1, shot)
            playerGrid.display()
            print("En attente de l'autre joueur ...")

        #Le server envoie la grille à afficher (spectateur)
        #
        if whatToDo == "d":
            recep_info(playerGrid, connect)
            playerGrid.display()

        #Le client a gagné (joueur)
        #
        if whatToDo == "w":
            print("Vous avez gagne !")
            recep_info(playerGrid, connect)
            playerGrid.display()

        #Le client a perdu (joueur)
        #
        if whatToDo == "l":
            print("Vous avez perdu.")
            recep_info(playerGrid, connect)
            playerGrid.display()

        #La partie est finie (spectateur)
        #
        if whatToDo == "e":
            print("La partie est finie.")
            
        if whatToDo == "w" or whatToDo == "l" or whatToDo == "e":
            replay = "a"
            while replay != "o" and replay != "n":
                replay = input ("Voulez-vous rejouer ? <o> pour oui <n> pour non, et attendre pour être spectateur.")
            replay = replay.encode("ascii")
            connect.send(replay)

            if replay == "n":
                end = True
            else:
                playerGrid = grid()
                player = connect.recv(1024)
                player = player.decode("ascii")
                print(player)
                if player == "1":
                    player = 1
                    print("Vous êtes joueur 1.")
                elif player == "2":
                    player = 2
                    print("Vous êtes joueur 2.")
                else :
                    print("Vous êtes spectateur.")
    


    connect.close()
main()
