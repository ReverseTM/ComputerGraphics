import matplotlib.pyplot as plt
import customtkinter
import numpy as np


def function(x, y, a):
    return\
        np.sign(x) * (np.abs(x)) ** (2 / 3) + np.sign(x) * (np.abs(y)) ** (2 / 3) - np.sign(x) * (np.abs(a)) ** (2 / 3)


def draw(a):
    x_min, x_max = -3, 3
    y_min, y_max = -3, 3

    x = np.linspace(x_min, x_max, 100)
    y = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x, y)

    plt.contour(X, Y, function(X, Y, a), levels=[0], colors='black')
    plt.axis('equal')

    plt.show()


def show_interface():
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    
    window = customtkinter.CTk()
    window.geometry("320x240")
    
    frame = customtkinter.CTkFrame(master=window)
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    
    label = customtkinter.CTkLabel(master=frame, text="parameter a value")
    label.pack(pady=30, padx=10)
    
    entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter a parameter value")
    entry.pack(pady=10, padx=10)
    
    button = customtkinter.CTkButton(master=frame, text="Do it", command=lambda: draw(float(entry.get())))
    button.pack(pady=10, padx=10)
    
    window.mainloop()
    

def main():
    show_interface()
    
    
if __name__ == '__main__':
    main()
    