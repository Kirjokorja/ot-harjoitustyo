from tkinter import ttk, constants

def initialize_input_field(frame, text, secure):
        label = ttk.Label(master=frame, text=text)

        if secure == True:
            entry = ttk.Entry(master=frame, show="*")
        else:
            entry = ttk.Entry(master=frame)

        label.grid(padx=5, pady=5, sticky=constants.W)
        entry.grid(padx=5, pady=5, sticky=constants.EW)

        return entry
