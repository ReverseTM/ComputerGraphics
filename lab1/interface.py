import customtkinter
import function


def run():
    value = float(entry1.get())
    function.draw(value)


def main():
    window.mainloop()


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

window = customtkinter.CTk()
window.geometry("320x240")

frame = customtkinter.CTkFrame(master=window)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label1 = customtkinter.CTkLabel(master=frame, text="parameter a value")
label1.pack(pady=30, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Enter a parameter value")
entry1.pack(pady=10, padx=10)

button = customtkinter.CTkButton(master=frame, text="Do it", command=run)
button.pack(pady=10, padx=10)

if __name__ == '__main__':
    main()
