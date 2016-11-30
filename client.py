#!/usr/bin/python3

from grid import *
import socket
import os, sys

def main():
    serv = sys.argv[1]
    print serv
    connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect.connect((serv, 6666))

    gameLaunched = connect.recv(1024)
    gameLaunched = gameLaunched.decode("ascii")
    print gameLaunched



    end = False
    
    while(not end):
        whatToDo = connect.recv(1024)
        whatToDo = whatToDo.decode("ascii")
        if whatToDo == "c":
            shot = int(input ("Quelle case voulez-vous jouer ? "))
            shot = str(shot)
            shot = shot.encode("ascii")
            connect.send(shot)
        if whatToDo == "w":
            print "Vous avez gagne !"
            end = True
        if whatToDo == "l":
            print "Vous avez perdu."
            end = True
            

    
    







    connect.close()
main()
