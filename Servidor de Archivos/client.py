import zmq 
import easygui as eg
import os


def search_file():
   # read a path file to upload on server and return absolute path and basename
   Archivo = eg.fileopenbox(msg="Abrir archivo",title="Control: fileopenbox",default='',filetypes= ["*All Files"] )
   nombreArchivo = os.path.basename(Archivo) #nombre y extension del archivo
   return Archivo,nombreArchivo

def upload(s):
   
   rutaArchivo,nombreArchivo = search_file()

   with open(rutaArchivo,'rb') as f:
      content = f.read()
      f.close()
   s.send_pyobj({
      "request": "upload",
      "fileName": nombreArchivo,
      "data": content
   })
   try:
      reply = s.recv_pyobj()
      print(reply["message"])
   except:
      print("El tiempo de espera ha superado el límite, verifica tu conexión al servidor...")

def download(s):
  
   fileName = str(input("Ingrese el nombre y extensión del archivo que desea descargar..."))
   s.send_pyobj({
      "request" : "download",
      "fileName" : fileName
   })
   try:
      reply = s.recv_pyobj()
   except:
      print("El tiempo de espera ha superado el límite, verifica tu conexión al servidor...")
      return
   
   print(reply["message"])
   if reply["status"] == 0:
      with open(os.getcwd()+'/'+ fileName, 'wb') as f:
         f.write(reply["data"])
         f.close() 
   
def delete(s):
   fileName = str(input("Ingrese el nombre y extensión del archivo que desea eliminar..."))
   s.send_pyobj({
      "request" : "delete",
      "fileName" : fileName
   })
   try:
      reply = s.recv_pyobj()
      print(reply["message"])
   except:
      print("El tiempo de espera ha superado el límite, verifica tu conexión al servidor...")

def file_list(s):
   s.send_pyobj({
      "request" : "list"
   })
   
   try:
      reply = s.recv_pyobj()
      print(reply["message"])
      if reply["status"] == 0:
         print(reply["data"])
    
   except:
      print("El tiempo de espera ha superado el límite, verifica tu conexión al servidor...")
   
if __name__ == '__main__':
   
   ctx = zmq.Context()
   s   = ctx.socket(zmq.REQ)
   s.setsockopt( zmq.RCVTIMEO, 1000 ) # 10 seconds
   #s.connect("tcp://localhost:5555") 
   
   while(True):
      s.connect("tcp://localhost:5555") 
      os.system("cls..") # On Windows O.S
      # os.system("clear") #On Linux O.S
      print("\n-----------------------\n")
      print("Sistema de Archivos \n")
      print("1.Cargar Archivos al Servidor\n")
      print("2.Descargar Archivos del Servidor\n")
      print("3.Listar Archivos del Servidor\n")
      print("4.Eliminar Archivo del Servidor\n")
      print("5.Desconectar\n")
      
      op = int(input("Ingrese opcion: "))

      print('\n')
   
      if op == 1:
         upload(s)
         x = input("presione una tecla para continuar....")
      
      elif op == 2:
         download(s)
         x = input("presione una tecla para continuar....")
   
      elif op == 3:
         file_list(s)
         x = input("presione una tecla para continuar....")
      
      elif op == 4:
         delete(s)
         x = input("presione una tecla para continuar....")

      elif op == 5:
         break
      
      else: 
         print(" Opcion no válida..")
      
      s.close()
      s   = ctx.socket(zmq.REQ)
      s.setsockopt( zmq.RCVTIMEO, 10000 ) 