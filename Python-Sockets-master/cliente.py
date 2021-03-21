import socket
import threading
import sys
import pickle
import re
from servidor import Servidor

s = Servidor()


class Cliente():
        def __init__(self):
                super(Cliente, self).__init__()
                

#Se definen los comandos al servidor con sus respectivas funciones
        def comandos(self,data):

                if data=='#cR':
                        nombreSala = input("Ingrese el nombre de la sala que desea crear: ")
                        s.crearSala(nombreSala)
                        return False

                elif data=='#gR':
                        print("entró a la sala")
                        return False

                elif data=='#eR':
                        s.salirSala()
                        return False

                elif data=='#exit':
                        print("Cliente desconectado")
                        s.cerrarSesion()
                        self.sock.close()
                        self.menu()
                        
                elif data=='#lR':
                        print("se veria el listado de la sala y numero de personas conectadas en ellas")
                        return False

                elif data=='#dR':
                        print("sala eliminada si es el dueño")
                        return False

                elif data=='#show users':
                        print("se verian todas las personas conectadas en el sistema")
                        return False

                elif data=='#private':
                        print("mensaje privado para _______: ")
                        return False

#Establece la conexion del cliente con el servidor y lo deja en el chat Global
        def iniciarCliente(self):

                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect(("localhost", 4000))

                msg_recv = threading.Thread(target=self.msg_recv)

                msg_recv.daemon = True
                msg_recv.start()

                print("********************BIENVENIDO AL CHAT GLOBAL******************")

                self.wait_message()

#Se queda a la espera de los mensajes del cliente y se envian al servidor
        def wait_message(self):
                while True:
                        msg = input('->')
                        msgFinal = (s.owner+" : "+msg)
                        if self.comandos(msg) != False:
                                self.send_msg(msgFinal)
                        

                        
                                
#Recibe mensajes del servidor
        def msg_recv(self):
                while True:
                        try:
                                data = self.sock.recv(1024)
                                if data:
                                        print(pickle.loads(data))
                        except:
                                pass
#Envia mensajes al servidor
        def send_msg(self, msg):
                self.sock.send(pickle.dumps(msg))

#Menu para hacer el registro e inicio de sesion
        def menu(self):
                        
                salir = False
                opcion = 0
                
                
                while not salir:

                        print ("*********************************MENU PRINCIPAL*********************************") 
                        print ("1. Registrarse")
                        print ("2. Iniciar Sesion")
                        print ("3. Salir")
                             
                        opcion = input("Elige una opcion: ")
                         
                        if opcion == '1':
                            print()
                            s.registroCliente()
                            print()
                        if opcion == '2':
                            print()
                            if s.inicioSesion()==True:
                                self.iniciarCliente()
                            else:
                                    print()
                                    self.menu()
                                    print()
                        if opcion == '3':
                            salir = True
                        else:
                            print ("Introduce un numero entre 1 y 3")
                print()         
                print ("Fin")
                sys.exit()


if __name__ == "__main__":
        c = Cliente()
        c.menu()  
