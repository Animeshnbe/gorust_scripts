import tkinter
import customtkinter
import tkintermapview

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")
app.title("Playground")

def button_function():
    print("button pressed")

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

map_widget = tkintermapview.TkinterMapView(app, width=800, height=400, corner_radius=0)
map_widget.set_address("Kolkata, India")  # Paris, France
map_widget.set_zoom(15)
map_widget.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

app.mainloop()