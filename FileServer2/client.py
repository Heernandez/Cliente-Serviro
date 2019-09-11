import zmq 
import json
import easygui as eg
import os
import hashlib


cant = 1024*1024*10

def verify():
   
   Archivo = eg.fileopenbox(msg="Abrir archivo",title="Control: fileopenbox",default='',filetypes= ["*All Files"] )
   NombreArchivo = bytes(os.path.basename(Archivo),'utf-8') #nombre y extension del archivo
   
   #recorrer el archivo para calcularle el sha
   with open(Archivo ,'rb') as f:
      sha256 = hashlib.sha256()
      while True:
         file = f.read(cant)
         if not file:
            break
         else:
            sha256.update(file)
   
   NuevoNombre = sha256.hexdigest().encode() #hash sha256 del archivo
   s.send_multipart( [b'1',NombreArchivo,NuevoNombre ])
   confirmacion = int(s.recv_string())
   return confirmacion,Archivo,NuevoNombre

def upload(s):
   #el servidor comprueba si el archivo se puede cargar
   flag,Archivo,NuevoNombre = verify()
   
   if flag == 1: 
      with open(Archivo,'rb') as f:
         while True:
            file = f.read(cant)
            if not file:
               break
            else:
               s.send_multipart([ b'2' ,file,NuevoNombre])        
               a = s.recv()
      
      s.send_multipart( [ b'3' ,NombreArchivo,NuevoNombre]  )
      m = s.recv()
      print("{}".format(m))
   else: 
      print("el archivo ya existe en el servidor")
      
def download(s):
   s.send_multipart([b'4'])
   lista = s.recv()
   print(lista)

def connection():

   ctx = zmq.Context()
   s   = ctx.socket(zmq.REQ)
   s.connect("tcp://localhost:5555") #Ip del servidor

   return s

if __name__ == '__main__':

   s = connection()
   
   while(True):
      os.system("clear")
      print("\n-----------------------\n")
      print("Sistema de Archivos \n")
      print("1.Cargar Archivos al Servidor\n")
      print("2.Descargar Archivos del Servidor\n")
      print("3.Desconectar\n")
      
      op = int(input("Ingrese opcion: "))

      print('\n')

      if op == 1:
         upload(s)
         x = input("presione una tecla ---")
      elif op == 2:
         #download(s)
         pass
      elif op == 3:
         break



