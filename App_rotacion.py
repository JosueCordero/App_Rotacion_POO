#Interfaz desktop
from tkinter import ttk
from tkinter import *
#Graficado
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt 


class Product:
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

        ttk.Button(frame, text = 'Mostrar imagen rotada', command = self.imagen_rotar).grid(row = 9, columnspan = 2,pady = 20)

    def selec_ejex(self):
        self.ejex = True
    def selec_ejey(self):
        self.ejey = True
    def selec_ejez(self):
        self.ejez = True
    
    #Rotacion de la imagen en 3D
    def imagen_rotar(self):
        #Variables
        v_t = 40
        v_s = 10
        px = float(self.pointx.get())
        py = float(self.pointy.get())
        pz = float(self.pointz.get())

        teta = float(self.grados.get())*(np.pi/180) #Angulo en radianes

        #Crea el espacio en 3D
        fig = plt.figure()
        ax = plt.axes(projection="3d")

        #Creacion de la banda de Mobius

        t = np.linspace(0,2*np.pi,v_t)
        w = .3
        s = np.linspace(-w,w,v_s)
        T,S = np.meshgrid(t,s)

        #Radio y parametrizaciones
        R = 1
        x = px+(R+S*np.cos(T/2))*np.cos(T)
        y = py+(R+S*np.cos(T/2))*np.sin(T)
        z = (pz+S*np.sin(T/2))

        #Matrices Rotaciones
        
        rotx = np.array([[1,0,0],[0,np.cos(teta),-np.sin(teta)],[0,np.sin(teta),np.cos(teta)]])
        roty = np.array([[np.cos(teta),0,np.sin(teta)],[0,1,0],[-np.sin(teta),0,np.cos(teta)]])
        rotz = np.array([[np.cos(teta),-np.sin(teta),0],[np.sin(teta),np.cos(teta),0],[0,0,1]])


        #Rotar los puntos en X
        if(self.ejex==True):
            for i in range(v_s):
                for j in range(v_t):
                    rxyz = np.array([[x[i][j]],[y[i][j]],[z[i][j]]])
                    x[i][j], y[i][j], z[i][j] = np.dot(rotx,rxyz)
        #Rotar los puntos en y
        if(self.ejey==True):
            for i in range(v_s):
                for j in range(v_t):
                    rxyz = np.array([[x[i][j]],[y[i][j]],[z[i][j]]])
                    x[i][j], y[i][j], z[i][j] = np.dot(roty,rxyz)
        #Rotar los puntos en z
        if(self.ejez==True):
            for i in range(v_s):
                for j in range(v_t):
                    rxyz = np.array([[x[i][j]],[y[i][j]],[z[i][j]]])
                    x[i][j], y[i][j], z[i][j] = np.dot(rotz,rxyz)
                
        ax.plot_surface(x,y,z,cmap="viridis")       
                


        #ax.scatter3D(0,0,0, c = 'r')
        plt.show()
    
    
if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()