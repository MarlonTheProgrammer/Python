import socket
import threading
import sys
import pickle
import mysql.connector

#Se crea la clase servidor con los atributos cnn para hacer la conexion con la base de datos en Mysql y owner para guardar el nombre de los clientes
class Servidor:
        def __init__(self):
                super(Servidor, self).__init__()
                self.cnn = mysql.connector.connect(host="localhost", user="root", passwd = "soniteamo", database = "sistemas_distribuidos")             
                self.owner = ''
                
#Se crea una funcion para establecer el nombre y puerto del socket y se llaman las funciones 'aceptarCon' y 'procesarCon' para recibir a los clientes
        def iniciarServer(self):

                self.clientes = []
                
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind(("localhost",4000))
                self.sock.listen(10)
                self.sock.setblocking(False)
                
                aceptar = threading.Thread(target=self.aceptarCon)
                procesar = threading.Thread(target=self.procesarCon)
                
                aceptar.daemon = True
                aceptar.start()

                procesar.daemon = True
                procesar.start()

                print()
                print("****************EL SERVIDOR SE HA INICIALIZADO CORRECTAMENTE****************")

#Envia el mensaje enviado por un cliente a los demas clientes conectados
        def msg_to_all(self, msg, cliente):
                for c in self.clientes:
                        try:
                                if c != cliente:
                                        c.send(msg)
                        except:
                                self.clientes.remove(c)
                                
#Recibe la conexion y direccion del cliente y se agrega a la lista de clientes
        def aceptarCon(self):
                print("aceptarCon iniciado")
                while True:
                        try:
                                conn, addr = self.sock.accept()
                                conn.setblocking(False)
                                self.clientes.append(conn)
                        except:
                                pass
                        
#Procesa los mensajes enviados por el cliente
        def procesarCon(self):
                print("ProcesarCon iniciado")
                while True:
                        if len(self.clientes) > 0:
                                for c in self.clientes:
                                        try:
                                                data = c.recv(1024)
                                                if data:
                                                        self.msg_to_all(data,c)
                                        except:
                                                pass
                                        
#Crea una sala con el nombre que el cliente le ha enviado y se modifica el atributo Sala de la base de datos
        def crearSala(self,nombreSala):
                usuario = ("'"+self.owner+"'")
                cur = self.cnn.cursor()
                cur.execute("UPDATE clientes SET Sala = '"+nombreSala+"' WHERE User = "+usuario)
                self.cnn.commit()    
                cur.close()
                print("Sala creada Correctamente")
                print()
                print("****************Bienvenido a "+nombreSala+"****************")
                print()
                
#Cambia la Sala en la que el cliente se encuentre por la predeterminada osea la Sala Global
        def salirSala(self):
                usuario = ("'"+self.owner+"'")
                cur = self.cnn.cursor()
                cur.execute("UPDATE clientes SET Sala = 'Global' WHERE User = "+usuario)
                self.cnn.commit()    
                cur.close()
                print("*******************Bienvenido a la sala Global*******************")
                print()

#Pide los datos al Cliente para registrarlo como usuario
        def registroCliente(self):
                print()
                print("**************BIENVENIDO AL REGISTRO***************")
                print()
                nombre = input("Nombres: ")
                apellido = input("Apellidos: ")
                usuario = input ("login : ")
                password = input ("Password : ")
                edad = input ("Edad : ")
                genero = input ("genero(M or F) : ")
                estado = 'Offline'
                sala = 'Ninguna'
                s = Servidor()
                s.insertar_cliente(nombre, apellido, usuario, password, edad, genero, estado, sala)

#Valida las credenciales de los clientes para entrar a la Sala Global
        def inicioSesion(self):
                print()
                print("**************BIENVENIDO AL INICIO DE SESION***************")
                print()
                bandera=False
                usuarioNormal = input ("User : ")
                usuarioNormal2 = ("'"+usuarioNormal+"'")
                usuarioVerificacion = (usuarioNormal,)
                password = (input ("Password : "),)
                cur = self.cnn.cursor()
                cur.execute("SELECT User FROM clientes")
                datosos = cur.fetchall()
                cur.execute("SELECT Password FROM clientes")
                datososcontra = cur.fetchall()
                for i in range(0,len(datosos)):
                        if usuarioVerificacion == datosos[i] and password == datososcontra[i]:
                                bandera=True
                                cur.execute("UPDATE clientes SET Estado = 'Online', Sala = 'Global' WHERE User = "+usuarioNormal2)
                                self.cnn.commit()    
                                cur.close()
                                self.owner = str(usuarioNormal)
                                print("BIENVENIDO " + self.owner )
                                return True
                              
                        else:
                                if i == (len(datosos)-1) and bandera==False:
                                        print("DATOS INCORRECTOS")
                               
                                
#Se establecen y se ingresan los datos del cliente en la base de datos
        def insertar_cliente(self,Nombres, Apellidos, User, Password, Edad, Genero, Estado, Sala):
                cur = self.cnn.cursor()
                sql='''INSERT INTO clientes (Nombres, Apellidos, User, Password, Edad, Genero, Estado, Sala) 
                VALUES('{}', '{}', '{}', '{}','{}','{}','{}','{}')'''.format(Nombres, Apellidos, User, Password, Edad, Genero, Estado, Sala)
                cur.execute(sql)
                self.cnn.commit()    
                cur.close()
                print("El registro fue exitoso")

#Cambia el Estado del cliente a Offline y Sala a Ninguna
        def cerrarSesion(self):
                usuario = ("'"+self.owner+"'")
                cur = self.cnn.cursor()
                cur.execute("UPDATE clientes SET Estado = 'Offline', Sala = 'Ninguna' WHERE User = "+usuario)
                self.cnn.commit()    
                cur.close()
                print("Sesion Cerrada Correctamente")
                print()
                
  
#Se ejecuta el Servidor
if __name__ == "__main__":
        s = Servidor()
        s.iniciarServer()
