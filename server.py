#!/usr/bin/python3

from grid import *
import random
import socket
import select
import time

#Fonction d'envoie de toute la grille à un joueur ou spectateur
#
def send_info(grid, connect):
    J1 = "1"
    J1 = J1.encode("ascii")
    J2 = "2"
    J2 = J2.encode("ascii")
    free = "0"
    free = free.encode("ascii")
    
    for i in range(9):
        if grid.cells[i] == 1:
            connect.send(J1)
        elif grid.cells[i] == 2:
            connect.send(J2)
        else:
            connect.send(free)
        connect.recv(1024)


def main():
    
    #On ouvre la connexion
    #
    connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect.bind(('', 6666))
    connect.listen(5)
    clients_connectes = []


    #On attend qu'au moins deux joueurs se connectent
    #
    print("En attente de joueurs ...")
    while len(clients_connectes) < 2:
        connexions_demandees, wlist, xlist = select.select([connect], [], [])
        for connexion in connexions_demandees:
            connexion_avec_client, infos_connexion = connexion.accept()
            clients_connectes.append(connexion_avec_client)
    print("Les deux joueurs sont connectes !")

    
    #On initialise le protocole
    #
    spec = "0"
    J1 = "1"
    J2 = "2"
    spec = spec.encode("ascii")
    J1 = J1.encode("ascii")
    J2 = J2.encode("ascii")
    
    caseMessage = "c"
    caseMessage = caseMessage.encode("ascii")
    displayMessage = "d"
    displayMessage = displayMessage.encode("ascii")
    
    winMessage = "w"
    winMessage = winMessage.encode("ascii")
    loseMessage = "l"
    loseMessage = loseMessage.encode("ascii")
    endMessage = "e"
    endMessage = endMessage.encode("ascii")
    
    freeMessage = "f"
    freeMessage = freeMessage.encode("ascii")
    usedMessage = "u"
    usedMessage = usedMessage.encode("ascii")


    #On crée la grille et on l'affiche
    #
    gridG = grid()
    current_player = J1
    gridG.display()

    
    #Initialisation des variables
    #
    currentJ1 = 0
    currentJ2 = 1
    end = False
    
    while end == False:
        #On envoie à tous les clients leur statut, s'ils sont joueurs ou spectateurs
        #
        for i in range (len(clients_connectes)) :
            if i == currentJ1:
                clients_connectes[i].send(J1)
            elif i == currentJ2:
                clients_connectes[i].send(J2)
            else:
                clients_connectes[i].send(spec)
        
        #Tant que la partie n'est pas finie :
        #
        while gridG.gameOver() == -1:
            if current_player == J1:
                shot = -1
                while shot <0 or shot >=NB_CELLS:
                    clients_connectes[currentJ1].send(caseMessage)
                    shot = clients_connectes[currentJ1].recv(1024)
                    shot = shot.decode("ascii")
                    shot = int(shot)
            else:
                shot = -1
                while shot <0 or shot >=NB_CELLS:
                    clients_connectes[currentJ2].send(caseMessage)
                    shot = clients_connectes[currentJ2].recv(1024)
                    shot = shot.decode("ascii")
                    shot = int(shot)
            if (gridG.cells[shot] != EMPTY):
                if current_player == J1:
                    clients_connectes[currentJ1].send(usedMessage)
                else :
                    clients_connectes[currentJ2].send(usedMessage)
            else:
                if current_player == J1:
                    clients_connectes[currentJ1].send(freeMessage)
                    gridG.play(1, shot)
                    current_player = J2
                else:
                    clients_connectes[currentJ2].send(freeMessage)
                    gridG.play(2, shot)
                    current_player = J1
                gridG.display()
                
            #On vérifie si d'autre clients se connectent et on leur indique qu'ils sont spec
            #
            connexions_demandees, wlist, xlist = select.select([connect],[],[], 0.05)
            for connexion in connexions_demandees:
                connexion_avec_client, infos_connexion = connexion.accept()
                connexion_avec_client.send(spec)
                clients_connectes.append(connexion_avec_client)

            time.sleep(0.1)

            #On envoie le statut de la partie à tous les spectateurs
            #
            for i in range (len(clients_connectes)) :
                if i != currentJ1 and i != currentJ2:
                    clients_connectes[i].send(displayMessage)
                    tpo = clients_connectes[i].recv(1024)
                    shot = str(shot)
                    shot = shot.encode("ascii")
                    clients_connectes[i].send(shot)
                    tpo = clients_connectes[i].recv(1024)
                    if current_player == J1:
                        clients_connectes[i].send(J2)
                    else :
                        clients_connectes[i].send(J1)
                    
            
            

        #On dit aux joueurs s'ils ont gagné ou perdu
        #
        print("Le jeu est fini")
        if gridG.gameOver() == 1:
            clients_connectes[currentJ1].send(winMessage)
            clients_connectes[currentJ2].send(loseMessage)
        else:
            clients_connectes[currentJ2].send(winMessage)
            clients_connectes[currentJ1].send(loseMessage)
        for i in range (len(clients_connectes)):
            if i != currentJ1 and i != currentJ2:
                clients_connectes[i].send(endMessage)
            
        time.sleep(0.1)

        #On envoie toute la grille aux deux joueurs
        #
        send_info(gridG, clients_connectes[currentJ1])
        send_info(gridG, clients_connectes[currentJ2])

        #On demande aux clients s'ils veulent jouer
        #
        currentJ1 = -1
        currentJ2 = -1
        while currentJ1 == -1 or currentJ2 == -1:
            clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [])
            for client in clients_a_lire :
                msg_recu = client.recv(1024)
                msg_recu = msg_recu.decode("ascii")
                for i in range (len(clients_connectes)) :
                    if client == clients_connectes[i] :
                        tmp = i
                if msg_recu == "o":
                    if currentJ1 == -1:
                        currentJ1 = tmp
                    elif currentJ2 == -1:
                        currentJ2 = tmp
                elif msg_recu == "n":
                    del clients_connectes[tmp]
        
        gridG = grid()
        current_player = J1
        gridG.display()


    connect.close()
main()
