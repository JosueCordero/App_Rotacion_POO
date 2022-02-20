#Interfaz desktop
from tkinter import ttk
from tkinter import *
#Graficado
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt 


class Aplicacion:
    """Aplicacion la cual consite en rotar una figura, en este caso elegi la banda de Moebius
    como figura a rotar a travez de los ejes xyz 
    
    La logica principal de la aplicacion ya la tenia hecha y lo que ahora implemente fue 
    modularizarla en 3 clases diferentes para tener una buena aplicacion del paradigma de POO 
    
    """
    #Constructor
    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Rotacion en XYZ')

        self.ejex =False
        self.ejey =False
        self.ejez =False

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Ingrese el punto incial, angulo y eje de rotacion')
        frame.grid(row = 0, column = 0, pady = 20)

        # Puntos iniciales
        Label(frame, text = 'Punto en X: ').grid(row = 1, column = 0)
        self.pointx = Entry(frame)
        self.pointx.focus()
        self.pointx.grid(row = 1, column = 1)

        Label(frame, text = 'Punto en Y: ').grid(row = 2, column = 0)
        self.pointy = Entry(frame)
        self.pointy.grid(row = 2, column = 1)

        Label(frame, text = 'Punto en Z: ').grid(row = 3, column = 0)
        self.pointz = Entry(frame)
        self.pointz.grid(row = 3, column = 1)
        
        # Angulo 

        Label(frame, text = 'Angulo (Grados): ').grid(row = 4, column = 0)
        self.grados = Entry(frame)
        self.grados.grid(row = 4, column = 1)

        # Botones seleccionar Ejes
        Label(frame, text = 'Seleccione los ejes a rotar:').grid(row = 5, column = 0, pady = 10)

        ttk.Button(frame, text = 'Eje X', command = self.selec_ejex).grid(row = 6, columnspan = 2)
        ttk.Button(frame, text = 'Eje Y', command = self.selec_ejey).grid(row = 7, columnspan = 2)
        ttk.Button(frame, text = 'Eje Z', command = self.selec_ejez).grid(row = 8, columnspan = 2)

        #Boton mostrar imagen rotada

        ttk.Button(frame, text = 'Mostrar imagen rotada', command = self.mostrarImagen).grid(row = 9, columnspan = 2,pady = 20)

    def selec_ejex(self):
        self.ejex = True
    def selec_ejey(self):
        self.ejey = True
    def selec_ejez(self):
        self.ejez = True
    
    #Rotacion de la imagen en 3D
    def mostrarImagen(self):
        imagen = BandaMoebius(self)
        accion = RotacionEnElMismoEJE(self,imagen)
        accion.rotar_figura()
        

class RotacionEnElMismoEJE:
    def __init__(self,App,fig) -> None:
        self.app = App
        self.fig = fig

        
    def rotar_figura(self):
        #Variables (Punto inicial y angulo(radianes))
        

        teta = float(self.app.grados.get())*(np.pi/180)

        figura = self.fig #Figura a rotar

        #Crea el espacio en 3D
        fig = plt.figure()
        ax = plt.axes(projection="3d")

        #Matrices Rotacionales
        
        rotx = np.array([[1,0,0],[0,np.cos(teta),-np.sin(teta)],[0,np.sin(teta),np.cos(teta)]])
        roty = np.array([[np.cos(teta),0,np.sin(teta)],[0,1,0],[-np.sin(teta),0,np.cos(teta)]])
        rotz = np.array([[np.cos(teta),-np.sin(teta),0],[np.sin(teta),np.cos(teta),0],[0,0,1]])

        #Rotar los puntos en X
        if(self.app.ejex==True):
            for i in range(figura.v_s):
                for j in range(figura.v_t):
                    rxyz = np.array([[figura.x[i][j]],[figura.y[i][j]],[figura.z[i][j]]])
                    figura.x[i][j], figura.y[i][j], figura.z[i][j] = np.dot(rotx,rxyz)
        #Rotar los puntos en y
        if(self.app.ejey==True):
            for i in range(figura.v_s):
                for j in range(figura.v_t):
                    rxyz = np.array([[figura.x[i][j]],[figura.y[i][j]],[figura.z[i][j]]])
                    figura.x[i][j], figura.y[i][j], figura.z[i][j] = np.dot(roty,rxyz)
        #Rotar los puntos en z
        if(self.app.ejez==True):
            for i in range(figura.v_s):
                for j in range(figura.v_t):
                    rxyz = np.array([[figura.x[i][j]],[figura.y[i][j]],[figura.z[i][j]]])
                    figura.x[i][j], figura.y[i][j], figura.z[i][j] = np.dot(rotz,rxyz)
                
        ax.plot_surface(figura.x,figura.y,figura.z,cmap="viridis")       
                
        #ax.scatter3D(0,0,0, c = 'r')
        plt.show()


class BandaMoebius:
    def __init__(self,App) -> None:
        self.app = App

        px = float(self.app.pointx.get())
        py = float(self.app.pointy.get())
        pz = float(self.app.pointz.get())
        
        #Variables
        self.v_t = 40
        self.v_s = 10
        
        #Creacion de la banda de Mobius

        t = np.linspace(0,2*np.pi,self.v_t)
        w = .3
        s = np.linspace(-w,w,self.v_s)
        T,S = np.meshgrid(t,s)

        #Radio y parametrizaciones
        R = 1
        self.x = px+(R+S*np.cos(T/2))*np.cos(T)
        self.y = py+(R+S*np.cos(T/2))*np.sin(T)
        self.z = (pz+S*np.sin(T/2))

  
if __name__ == '__main__':
    window = Tk()
    application = Aplicacion(window)
    window.mainloop()