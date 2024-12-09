import tkinter as tk
import os
from Perros.vista import Frame

def main():
    ventana = tk.Tk()
    ventana.title('Listado de Perros')
    img_dir = r'C:\Users\WINDOWS_10\Desktop\Perritos\img'
    try:
        icon_path = os.path.join(img_dir, 'favicon.ico')
        ventana.iconbitmap(icon_path)
    except Exception as e:
        print(f"Icono no establecido: {e}")
        
 



    ventana.resizable(False, False)
    app = Frame(root=ventana)  # Instancia del Frame
    ventana.mainloop()

if __name__ == '__main__':
    main()
